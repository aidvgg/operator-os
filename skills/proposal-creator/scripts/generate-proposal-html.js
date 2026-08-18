#!/usr/bin/env node
/**
 * generate-proposal-html.js - Northwind Labs proposal generator, 2026-08-02 design standard.
 *
 * Renders a proposal data JSON (same schema as the legacy docx generator, see
 * ../references/data-schema.md) into a self-contained print HTML file in the
 * house design language (source of record:
 * ../references/design-standard-2026-08-02.dc.html), then prints it to PDF
 * through headless Chrome.
 *
 * Usage:
 *   node skills/proposal-creator/scripts/generate-proposal-html.js \
 *     <data.json> <out.html> [<out.pdf>] [--paper letter|a4] [--html-only]
 *
 * The PDF path defaults to the HTML path with a .pdf extension. After
 * generating, run the canonical validator: scripts/pdf-check <out.pdf>
 *
 * Assets resolve via ../assets/ relative to this script (fonts + doc-page.js),
 * so run it in place. Everything is embedded: the output HTML needs no network
 * and no sibling files.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ASSETS = path.join(__dirname, '..', 'assets');

// ---------------------------------------------------------------- CLI ------
const argv = process.argv.slice(2);
const flags = { paper: 'letter', htmlOnly: false };
const positional = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--paper') flags.paper = (argv[++i] || 'letter').toLowerCase();
  else if (a === '--html-only') flags.htmlOnly = true;
  else if (a === '--chrome') flags.chrome = argv[++i];
  else positional.push(a);
}
if (positional.length < 2) {
  console.error('usage: generate-proposal-html.js <data.json> <out.html> [<out.pdf>] [--paper letter|a4] [--html-only]');
  process.exit(2);
}
const [dataPath, htmlPath] = positional;
const pdfPath = positional[2] || htmlPath.replace(/\.html?$/i, '') + '.pdf';
if (!['letter', 'a4'].includes(flags.paper)) {
  console.error(`unknown --paper "${flags.paper}" (letter|a4)`);
  process.exit(2);
}

const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// ------------------------------------------------------------- helpers ----
const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const b64 = (p) => fs.readFileSync(p).toString('base64');

// Sentence-case an ALL-CAPS heading ("DEFINITION OF DONE" -> "Definition of done");
// mixed-case headings pass through untouched.
const displayHeading = (h) => {
  const s = String(h || '');
  if (s === s.toUpperCase() && /[A-Z]/.test(s)) {
    return s.charAt(0) + s.slice(1).toLowerCase();
  }
  return s;
};

// Voice-rule guard (knowledge/voice/copy-rules.md): em and en dashes are banned
// in fresh client copy. Warn loudly with locations; do not rewrite data.
// Written as unicode escapes on purpose. The ban covers this repo's own source,
// so the one check that hunts these characters must not carry a literal copy of
// either: U+2014 is the em dash, U+2013 the en dash.
const EM = '\u2014';
const DASH_RE = /[\u2013\u2014]/;
(function dashAudit(node, trail) {
  if (typeof node === 'string') {
    if (DASH_RE.test(node)) {
      console.warn(`WARN dash: ${trail} contains ${node.includes(EM) ? 'an em dash' : 'an en dash'} -> "${node.slice(0, 70)}..." (copy-rules ban; fix the data JSON)`);
    }
    return;
  }
  if (Array.isArray(node)) node.forEach((v, i) => dashAudit(v, `${trail}[${i}]`));
  else if (node && typeof node === 'object') {
    for (const k of Object.keys(node)) {
      if (k === 'scopeTrace') continue; // reviewer sidecar, renders nothing
      dashAudit(node[k], `${trail}.${k}`);
    }
  }
})(data, 'data');

const hasDoD = (data.customSections || []).some(
  (s) => /definition of done/i.test(s.heading || '')
);
if (!hasDoD) {
  console.warn('WARN schema: no DEFINITION OF DONE custom section (required on every proposal per SKILL.md; only historical re-renders get a pass)');
}

// --------------------------------------------------------- derived text ----
const clientName = data.clientName || 'Client';
const clientEntity = data.clientEntity || clientName;
const sentBy = data.sentBy || 'Sam Rivera';
const contactEmail = data.contactEmail || 'sam@northwindlabs.example';
const kicker = `${data.proposalType || 'Project proposal'} · ${data.date || ''}`;
const coverTitle = data.coverTitle || data.projectTitle || '';
const coverLede = data.coverLede || data.projectDescription || '';
const projectTag = data.projectTag || `${clientName} · ${data.projectTitle || ''}`;
const boldItem = ((data.investment || {}).lineItems || []).filter((li) => li.bold).pop();
const totalInvestment = data.totalInvestment || (boldItem ? `${boldItem.amount} USD` : '');
const engagement = data.engagement || 'Fixed scope, fixed price';
const preparedFor = (data.meta && data.meta.preparedFor) || clientEntity;
const footerRight = data.footerRight || 'Northwind Labs · operating under Rivera Holdings LLC';
const confidentialLine = data.confidential === false
  ? null
  : (data.confidentialLine || `${clientEntity} · Commercial in confidence`);

// ------------------------------------------------------------ fragments ----
// House mark: a geometric N drawn in a 100x180 design box. Same geometry as
// assets/logo.png (the legacy docx generator's raster copy), so the two brand
// surfaces cannot drift apart. Swap both together when the brand changes.
const MARK = '<svg viewBox="0 0 100 180" width="10" height="18" style="display:block;color:#0b0a09;" aria-hidden="true"><path fill="currentColor" d="M0 180V0H20L80 120V0H100V180H80L20 60V180Z"></path></svg>';

const CHECK = '<svg viewBox="0 0 12 12" width="11" height="11" class="tick" aria-hidden="true"><path d="M1.5 6.4 4.4 9.2 10.5 3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square"></path></svg>';

const pad2 = (n) => String(n).padStart(2, '0');

function secHead(num, title, tight) {
  return `<div class="sec-head${tight ? ' tight' : ''}"><span class="sec-num">${pad2(num)}</span><h2>${esc(title)}</h2></div>`;
}

// Two-column key/description table with mono uppercase column headers.
function dtable(headers, rows, col1Pct) {
  const w = col1Pct || 29;
  const head = headers
    ? `<thead><tr><th class="c1" style="width:${w}%;">${esc(headers[0])}</th><th>${esc(headers[1])}</th></tr></thead>`
    : '';
  const body = rows.map(([k, v]) =>
    `<tr><td class="k">${esc(k)}</td><td class="v">${esc(v)}</td></tr>`).join('\n');
  return `<table class="dtable">${head}<tbody>\n${body}\n</tbody></table>`;
}

// Accent-numbered row list (payment terms, sequencing-style content arrays).
// Items are strings, or { text, amount } objects; any amount in the list adds
// the design's right-aligned mono amount column (empty cell for plain rows).
function numRows(items) {
  const hasAmount = items.some((it) => it && typeof it === 'object' && it.amount);
  const body = items.map((it, i) => {
    const text = it && typeof it === 'object' ? it.text : it;
    const amount = it && typeof it === 'object' ? it.amount : null;
    const amtCell = hasAmount ? `<td class="a">${amount ? esc(amount) : ''}</td>` : '';
    return `<tr><td class="n">${pad2(i + 1)}</td><td class="t">${esc(text)}</td>${amtCell}</tr>`;
  }).join('\n');
  return `<table class="numrows"><tbody>\n${body}\n</tbody></table>`;
}

function paragraphs(items, cls) {
  return items.filter(Boolean).map((p) => `<p class="${cls || 'body'}">${esc(p)}</p>`).join('\n');
}

// ------------------------------------------------------------- sections ----
let secNum = 0;
const sections = [];
const breaks = new Set(data.pageBreaks || ['scope', 'investment', 'acceptance']);
const secOpen = (key, keep) => {
  const cls = ['sec'];
  if (breaks.has(key)) cls.push('pb');
  if (keep) cls.push('keep');
  return `<section class="${cls.join(' ')}">`;
};

// 01 Overview
secNum++;
sections.push(`${secOpen('overview')}
${secHead(secNum, 'Overview')}
${paragraphs([data.overview, data.overviewExtra])}
</section>`);

// 02 Scope of work
if (data.scopeSections && data.scopeSections.length) {
  secNum++;
  const subs = data.scopeSections.map((ss, i) => {
    const headers = ss.headers || ['Deliverable', 'Description'];
    const rows = (ss.services || []).map((s) => [s.service, s.description]);
    return `<h3 class="sub">${secNum}.${i + 1} ${esc(ss.title)}</h3>\n${dtable(headers, rows)}`;
  }).join('\n');
  sections.push(`${secOpen('scope')}
${secHead(secNum, 'Scope of work', true)}
${subs}
</section>`);
}

// 03 Investment (+ payment terms subsection + note)
if (data.investment && data.investment.lineItems) {
  secNum++;
  const rows = data.investment.lineItems.map((li) => li.bold
    ? `<tr class="total"><td class="d">${esc(li.description)}</td><td class="a">${esc(li.amount)}</td></tr>`
    : `<tr><td class="d">${esc(li.description)}</td><td class="a">${esc(li.amount)}</td></tr>`
  ).join('\n');
  let inner = `<table class="inv"><thead><tr><th>Description</th><th class="amt">Amount (USD)</th></tr></thead><tbody>\n${rows}\n</tbody></table>`;
  if (data.paymentTerms && data.paymentTerms.length) {
    inner += `\n<h3 class="sub gap">${secNum}.1 Payment terms</h3>\n${numRows(data.paymentTerms)}`;
  }
  if (data.investment.note) {
    inner += `\n<p class="note">${esc(data.investment.note)}</p>`;
  }
  sections.push(`${secOpen('investment')}
${secHead(secNum, 'Investment')}
${inner}
</section>`);
}

// 04 What this covers
if (data.whatThisCovers && data.whatThisCovers.length) {
  secNum++;
  const lis = data.whatThisCovers.map((it) =>
    `<li>${CHECK}<span>${esc(it)}</span></li>`).join('\n');
  sections.push(`${secOpen('covers', true)}
${secHead(secNum, 'What this covers')}
<ul class="checkgrid">
${lis}
</ul>
</section>`);
}

// 05 Out of scope / Additional work
if (data.outOfScope && data.outOfScope.length) {
  secNum++;
  const rows = data.outOfScope.map((o) =>
    `<tr><td class="k">${esc(o.item)}</td><td class="v">${esc(o.note)}</td></tr>`).join('\n');
  sections.push(`${secOpen('outofscope', true)}
${secHead(secNum, 'Out of scope')}
${data.additionalWork ? `<p class="body intro">${esc(data.additionalWork)}</p>` : ''}
<table class="kv"><tbody>
${rows}
</tbody></table>
</section>`);
} else if (data.additionalWork) {
  secNum++;
  sections.push(`${secOpen('additional', true)}
${secHead(secNum, 'Additional work')}
<p class="body">${esc(data.additionalWork)}</p>
</section>`);
}

// Custom sections
for (const cs of data.customSections || []) {
  secNum++;
  let inner = '';
  if (typeof cs.content === 'string') inner += `<p class="body${cs.table ? ' intro' : ''}">${esc(cs.content)}</p>\n`;
  else if (Array.isArray(cs.content)) inner += numRows(cs.content) + '\n';
  if (cs.table) {
    const pct = cs.table.col1Width ? Math.round((cs.table.col1Width / 9360) * 100) : 29;
    inner += dtable(cs.table.headers, cs.table.rows, pct) + '\n';
  }
  sections.push(`${secOpen(`custom:${cs.heading}`, true)}
${secHead(secNum, displayHeading(cs.heading))}
${inner}</section>`);
}

// Terms and conditions
if (data.termsAndConditions && data.termsAndConditions.length) {
  secNum++;
  const lis = data.termsAndConditions.map((t, i) =>
    `<li><span class="n">${secNum}.${i + 1}</span><span>${esc(t)}</span></li>`).join('\n');
  sections.push(`${secOpen('terms')}
${secHead(secNum, 'Terms and conditions')}
<ol class="tc">
${lis}
</ol>
</section>`);
}

// Acceptance (signature block)
secNum++;
const acceptanceText = data.acceptanceText ||
  'By signing below, both parties agree to the scope of work, pricing, and terms outlined in this proposal.';
const closingNote = data.closingNote ||
  `Questions or clarifications on any part of this proposal: contact ${sentBy} at ${contactEmail}.`;
const sigLine = '<div class="sigline"></div>';
sections.push(`${secOpen('acceptance', true)}
${secHead(secNum, 'Acceptance')}
<p class="body accept">${esc(acceptanceText)}</p>
<table class="sig">
<thead><tr><th class="l">Client · ${esc(clientEntity)}</th><th class="r">Northwind Labs · Rivera Holdings LLC</th></tr></thead>
<tbody>
<tr><td class="line l">${sigLine}</td><td class="line r">${sigLine}</td></tr>
<tr><td class="lab l">Signature</td><td class="lab r">Signature</td></tr>
<tr><td class="line l">${sigLine}</td><td class="line r">${sigLine}</td></tr>
<tr><td class="lab l">Name and title</td><td class="lab r">Name and title</td></tr>
<tr><td class="line l">${sigLine}</td><td class="line r">${sigLine}</td></tr>
<tr><td class="lab l">Date</td><td class="lab r">Date</td></tr>
</tbody>
</table>
<p class="closing">${esc(closingNote)}</p>
</section>`);

// ------------------------------------------------------------------ CSS ----
const accent = data.accent || '#e89b5c';
const bs = { compact: '0.94', standard: '1', relaxed: '1.06' }[data.density || 'standard'] || '1';

const css = `
@font-face { font-family: 'Space Grotesk'; src: url(data:font/woff2;base64,${b64(path.join(ASSETS, 'fonts', 'SpaceGrotesk-var-latin.woff2'))}) format('woff2'); font-weight: 300 700; font-style: normal; }
@font-face { font-family: 'Inter Tight'; src: url(data:font/woff2;base64,${b64(path.join(ASSETS, 'fonts', 'InterTight-var-latin.woff2'))}) format('woff2'); font-weight: 300 700; font-style: normal; }
@font-face { font-family: 'JetBrains Mono'; src: url(data:font/woff2;base64,${b64(path.join(ASSETS, 'fonts', 'JetBrainsMono-var-latin.woff2'))}) format('woff2'); font-weight: 100 800; font-style: normal; }

:root { --acc: ${accent}; --bs: ${bs}; }
html, body { margin: 0; padding: 0; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
doc-page:not(:defined) { visibility: hidden; }
a { color: #2a241d; text-decoration: underline; text-underline-offset: 2px; }
a:hover { color: var(--acc); }

/* running header / footer */
.hdr { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding-bottom: 8px; border-bottom: 1px solid #2a241d; font-family: 'Inter Tight', system-ui, sans-serif; }
.hdr .brand { display: flex; align-items: center; gap: 7px; }
.hdr .word { font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 12.5px; letter-spacing: 0.01em; color: #0b0a09; white-space: nowrap; }
.hdr .tag { font-family: 'JetBrains Mono', monospace; font-size: 8.5px; letter-spacing: 0.13em; text-transform: uppercase; color: #6b6358; white-space: nowrap; }
.ftr { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding-top: 8px; border-top: 1px solid rgba(42,36,29,0.2); font-family: 'JetBrains Mono', monospace; font-size: 8.5px; letter-spacing: 0.11em; text-transform: uppercase; color: #6b6358; }

/* cover */
header.cover { margin: 0 0 30px; }
.kicker { display: flex; align-items: center; gap: 10px; margin: 0 0 18px; }
.kicker .dot { width: 5px; height: 5px; background: var(--acc); display: block; }
.kicker .kt { font-family: 'JetBrains Mono', monospace; font-size: 9.5px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: #6b6358; }
h1.title { margin: 0 0 14px; font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 36px; line-height: 1.06; letter-spacing: -0.035em; color: #0b0a09; max-width: 20ch; }
p.lede { margin: 0; font-size: calc(15.5px * var(--bs)); line-height: 1.6; letter-spacing: -0.005em; color: #2a241d; max-width: 62ch; text-wrap: pretty; }

/* meta strip */
table.meta { width: 100%; border-collapse: collapse; margin: 0 0 34px; border-top: 1px solid #2a241d; border-bottom: 1px solid #2a241d; }
table.meta td { width: 25%; padding: 13px 16px; vertical-align: top; }
table.meta td:first-child { padding-left: 0; }
table.meta td:last-child { padding-right: 0; }
table.meta td + td { border-left: 1px solid rgba(42,36,29,0.15); }
.meta .ml { font-family: 'JetBrains Mono', monospace; font-size: 8.5px; letter-spacing: 0.15em; text-transform: uppercase; color: #6b6358; margin: 0 0 5px; }
.meta .mv { font-size: 13px; line-height: 1.4; color: #0b0a09; font-weight: 500; }
.meta .ms { font-size: 12px; line-height: 1.4; color: #6b6358; }

/* sections */
section.sec { margin: 0 0 26px; }
section.sec:last-child { margin-bottom: 0; }
section.keep { break-inside: avoid; }
@media print { section.pb { break-before: page; } }
.sec-head { display: flex; align-items: baseline; gap: 12px; margin: 0 0 14px; padding-bottom: 9px; border-bottom: 1px solid #2a241d; }
.sec-head.tight { margin-bottom: 6px; }
.sec-num { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 500; letter-spacing: 0.1em; color: var(--acc); }
.sec-head h2 { margin: 0; font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 19px; letter-spacing: -0.02em; color: #0b0a09; }
h3.sub { margin: 20px 0 0; font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 14.5px; letter-spacing: -0.01em; color: #0b0a09; }
h3.sub.gap { margin: 22px 0 10px; }
p.body { margin: 0 0 12px; font-size: calc(14px * var(--bs)); line-height: 1.62; color: #2a241d; text-wrap: pretty; }
p.body.intro { margin-bottom: 14px; }
p.note { margin: 0; font-size: calc(13px * var(--bs)); line-height: 1.55; color: #6b6358; }

/* deliverable tables */
table.dtable { width: 100%; border-collapse: collapse; margin: 12px 0 26px; }
table.dtable th { padding: 0 18px 8px 0; border-bottom: 1px solid #2a241d; text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 8.5px; font-weight: 500; letter-spacing: 0.13em; text-transform: uppercase; color: #6b6358; }
table.dtable th:last-child { padding-right: 0; }
table.dtable td { padding: 12px 18px 12px 0; border-bottom: 1px solid rgba(42,36,29,0.13); vertical-align: top; }
table.dtable td:last-child { padding-right: 0; }
table.dtable td.k { font-size: calc(13.5px * var(--bs)); line-height: 1.45; font-weight: 500; color: #0b0a09; }
table.dtable td.v { font-size: calc(13.5px * var(--bs)); line-height: 1.55; color: #2a241d; text-wrap: pretty; }

/* investment table */
table.inv { width: 100%; border-collapse: collapse; margin: 0 0 16px; }
table.inv th { padding: 0 18px 8px 0; border-bottom: 1px solid #2a241d; text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 8.5px; font-weight: 500; letter-spacing: 0.13em; text-transform: uppercase; color: #6b6358; }
table.inv th.amt { width: 22%; padding: 0 0 8px; text-align: right; }
table.inv td { border-bottom: 1px solid rgba(42,36,29,0.13); }
table.inv td.d { padding: 12px 18px 12px 0; font-size: calc(13.5px * var(--bs)); line-height: 1.5; color: #2a241d; }
table.inv td.a { padding: 12px 0; text-align: right; font-family: 'JetBrains Mono', monospace; font-size: calc(13px * var(--bs)); color: #0b0a09; }
table.inv tr.total td { border-bottom: 1px solid #2a241d; }
table.inv tr.total td.d { padding: 14px 18px 14px 0; font-weight: 600; color: #0b0a09; }
table.inv tr.total td.a { padding: 14px 0; font-size: calc(15px * var(--bs)); font-weight: 500; }

/* accent-numbered rows */
table.numrows { width: 100%; border-collapse: collapse; margin: 0 0 12px; }
table.numrows td { border-bottom: 1px solid rgba(42,36,29,0.13); vertical-align: top; }
table.numrows td.n { width: 34px; padding: 11px 0; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--acc); }
table.numrows td.t { padding: 11px 0 11px 0; font-size: calc(13.5px * var(--bs)); line-height: 1.5; color: #2a241d; }
table.numrows td.t:not(:last-child) { padding-right: 18px; }
table.numrows td.a { width: 22%; padding: 11px 0; text-align: right; font-family: 'JetBrains Mono', monospace; font-size: calc(13px * var(--bs)); color: #0b0a09; }

/* checklist grid */
ul.checkgrid { margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 10px 28px; }
ul.checkgrid li { display: flex; gap: 9px; align-items: flex-start; font-size: calc(13.5px * var(--bs)); line-height: 1.5; color: #2a241d; }
ul.checkgrid .tick { flex: none; margin-top: 4px; color: var(--acc); }

/* key/note table (out of scope) */
table.kv { width: 100%; border-collapse: collapse; }
table.kv td { padding: 11px 18px 11px 0; border-top: 1px solid rgba(42,36,29,0.13); vertical-align: top; }
table.kv td:last-child { padding-right: 0; }
table.kv tr:last-child td { border-bottom: 1px solid rgba(42,36,29,0.13); }
table.kv td.k { width: 31%; font-size: calc(13.5px * var(--bs)); line-height: 1.45; font-weight: 500; color: #0b0a09; }
table.kv td.v { font-size: calc(13.5px * var(--bs)); line-height: 1.55; color: #2a241d; }

/* terms and conditions */
ol.tc { margin: 0; padding: 0; list-style: none; }
ol.tc li { display: flex; gap: 14px; padding: 11px 0; border-bottom: 1px solid rgba(42,36,29,0.13); font-size: calc(13.5px * var(--bs)); line-height: 1.55; color: #2a241d; text-wrap: pretty; }
ol.tc .n { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #6b6358; flex: none; width: 20px; }

/* acceptance */
p.accept { margin-bottom: 30px; max-width: 66ch; }
table.sig { width: 100%; border-collapse: collapse; }
table.sig th { width: 50%; padding: 0 26px 10px 0; border-bottom: 1px solid #2a241d; text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 8.5px; font-weight: 500; letter-spacing: 0.13em; text-transform: uppercase; color: #6b6358; }
table.sig td { padding: 0; }
table.sig th.r, table.sig td.r { padding-left: 26px; padding-right: 0; }
table.sig td.l { padding-right: 26px; padding-left: 0; }
table.sig td.line { padding-top: 34px; padding-bottom: 8px; vertical-align: bottom; }
.sigline { border-bottom: 1px solid #2a241d; height: 1px; }
table.sig td.lab { font-family: 'JetBrains Mono', monospace; font-size: 8.5px; letter-spacing: 0.13em; text-transform: uppercase; color: #6b6358; }
p.closing { margin: 34px 0 0; padding-top: 14px; border-top: 1px solid rgba(42,36,29,0.2); font-size: calc(13px * var(--bs)); line-height: 1.55; color: #6b6358; }
`;

// ------------------------------------------------------------ document ----
// Escape </script sequences (doc-page.js carries them inside comments) so the
// inline tag cannot terminate early; <\/ is identical to </ in JS source.
const docPageJs = fs.readFileSync(path.join(ASSETS, 'doc-page.js'), 'utf8')
  .replace(/<\/script/gi, '<\\/script');
const metaCell = (label, value, sub) =>
  `<td><div class="ml">${esc(label)}</div><div class="mv">${esc(value)}</div>${sub ? `<div class="ms">${esc(sub)}</div>` : ''}</td>`;

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(clientName)} - ${esc(data.projectTitle || 'Proposal')}</title>
<style>${css}</style>
<!-- Deliberate @page size pin: headless Chrome's CLI has no paper flag, so this
     generator plays the export-path role doc-page.js reserves for the host app
     (its own injected rule carries margins only for flowing docs, and the @page
     cascade is per-descriptor, so the size below survives). -->
<style id="paper-pin">@page { size: ${flags.paper === 'a4' ? 'A4' : 'letter'}; }</style>
</head>
<body>
<doc-page size="${flags.paper}" margin="0.68in" style="font-family:'Inter Tight',system-ui,sans-serif;">

<div slot="header" class="hdr">
  <div class="brand">${MARK}<span class="word">Northwind Labs</span></div>
  <span class="tag">${esc(projectTag)}</span>
</div>

<div slot="footer" class="ftr">
  ${confidentialLine ? `<span>${esc(confidentialLine)}</span>` : '<span></span>'}
  <span>${esc(footerRight)}</span>
</div>

<header class="cover">
  <div class="kicker"><span class="dot"></span><span class="kt">${esc(kicker)}</span></div>
  <h1 class="title">${esc(coverTitle)}</h1>
  <p class="lede">${esc(coverLede)}</p>
</header>

<table class="meta"><tbody><tr>
${metaCell('Prepared for', preparedFor)}
${metaCell('Prepared by', sentBy, 'Northwind Labs')}
${metaCell('Engagement', engagement)}
${metaCell('Total investment', totalInvestment)}
</tr></tbody></table>

${sections.join('\n\n')}

</doc-page>
<script>
${docPageJs}
</script>
</body>
</html>
`;

fs.mkdirSync(path.dirname(path.resolve(htmlPath)), { recursive: true });
fs.writeFileSync(htmlPath, html);
console.log(`HTML written: ${htmlPath} (${(fs.statSync(htmlPath).size / 1024).toFixed(0)} KB, self-contained)`);

// ---------------------------------------------------------------- PDF ------
if (flags.htmlOnly) process.exit(0);

// --chrome, then CHROME_BIN, then the usual macOS and Linux install paths.
// Same candidate list as the invoice generator; keep the two in step.
const chromeCandidates = [
  flags.chrome,
  process.env.CHROME_BIN,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/snap/bin/chromium',
].filter(Boolean);
const chrome = chromeCandidates.find((c) => fs.existsSync(c));
if (!chrome) {
  console.error('FAIL: no Chrome binary found (set CHROME_BIN or pass --chrome; looked in the default macOS and Linux paths for google-chrome, google-chrome-stable, chromium, chromium-browser). HTML was written; PDF was not.');
  process.exit(1);
}

const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'operator-os-proposal-chrome-'));
const printStart = Date.now();
try {
  execFileSync(chrome, [
    '--headless',
    '--disable-gpu',
    '--hide-scrollbars',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    `--user-data-dir=${profile}`,
    '--virtual-time-budget=10000',
    '--no-pdf-header-footer',
    `--print-to-pdf=${path.resolve(pdfPath)}`,
    'file://' + path.resolve(htmlPath),
  ], { stdio: ['ignore', 'pipe', 'pipe'], timeout: 45000 });
} catch (e) {
  // Headless Chrome sometimes lingers after the PDF is fully written and the
  // timeout kills it. The exit is not the evidence; the file is. Verify the
  // PDF appeared during this run and is plausibly sized, else re-throw.
  const fresh = fs.existsSync(pdfPath)
    && fs.statSync(pdfPath).mtimeMs >= printStart
    && fs.statSync(pdfPath).size > 10 * 1024;
  if (!fresh) throw e;
  console.warn('WARN chrome: process lingered past the timeout after writing the PDF; output verified fresh, continuing');
} finally {
  fs.rmSync(profile, { recursive: true, force: true });
}

const pdfSize = fs.existsSync(pdfPath) ? fs.statSync(pdfPath).size : 0;
if (pdfSize < 10 * 1024) {
  console.error(`FAIL: PDF missing or suspiciously small (${pdfSize} bytes): ${pdfPath}`);
  process.exit(1);
}
console.log(`PDF written: ${pdfPath} (${(pdfSize / 1024).toFixed(0)} KB)`);
console.log(`Next: scripts/pdf-check "${pdfPath}" (mandatory before delivery)`);
