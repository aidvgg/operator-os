#!/usr/bin/env node
/**
 * generate-invoice-html.js - Northwind Labs invoice generator (HTML -> PDF).
 *
 * Renders the brand invoice design (design source of record:
 * ../references/design-standard-2026-08-02.dc.html, adopted as the standard
 * 2026-08-02) from a data JSON into:
 *   1. a fully self-contained .html (fonts, logo, doc-page.js inlined as data
 *      URIs / inline script - opens offline in any browser, copy buttons work
 *      on screen and vanish in print), and
 *   2. a .pdf printed from that HTML by headless Chrome (US Letter, the
 *      client-facing deliverable).
 *
 * Usage:
 *   node generate-invoice-html.js <data.json> <output.pdf>
 * The output path must end in .pdf; the .html lands next to it (same
 * basename). No npm dependencies.
 *
 * The wire block comes from the data JSON at generation time (the skill fills
 * it from knowledge/business/invoices/PAYMENT-DETAILS.md). This script and its
 * template carry no bank data.
 *
 * The invoice NUMBER must come from
 *   knowledge/business/invoices/INVOICE-LEDGER.md  (the "NEXT INVOICE NUMBER" block).
 * Never hardcode or guess it. See that file's protocol.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { pathToFileURL } = require('url');
const { spawn } = require('child_process');

const ASSETS = path.join(__dirname, '..', 'assets');
const PDF_SIZE_FLOOR = 10 * 1024;
const PRINT_DEADLINE_MS = 45000;

const STATUS_COLORS = {
  draft: '#a8a095',
  sent: '#d97757',
  paid: '#4f8a5b',
  overdue: '#b03d2e',
};

function esc(s) {
  if (s === null || s === undefined) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Escaped text with **bold** spans rendered as dark strong tags (the design's
// inline-emphasis idiom for references and key values in running copy). The
// design weights these 600 in the payment intro but 500 inside Notes.
function rich(s, weight = 600) {
  return esc(s).replace(
    /\*\*([^*]+)\*\*/g,
    `<strong style="color:#16130f; font-weight:${weight}">$1</strong>`
  );
}

function dataUri(file, mime) {
  const p = path.join(ASSETS, file);
  let buf;
  try {
    buf = fs.readFileSync(p);
  } catch (e) {
    fail(`missing skill asset: ${p} (${e.code || e.message})`);
  }
  return `data:${mime};base64,${buf.toString('base64')}`;
}

function fail(msg) {
  console.error(`generate-invoice-html: ${msg}`);
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Data validation - every defect fails loudly here, never as a stack trace or
// as the string "null"/"undefined" printed onto a client-facing invoice.
// ---------------------------------------------------------------------------

function validate(d) {
  const isStr = (v) => typeof v === 'string' && v.trim() !== '';
  const need = (cond, msg) => { if (!cond) fail(`data JSON invalid: ${msg}`); };

  for (const f of ['invoiceNumber', 'dateIssued', 'dueDate', 'terms', 'subtotal', 'total', 'paymentIntro']) {
    need(isStr(d[f]), `"${f}" must be a non-empty string`);
  }
  need(d.from && typeof d.from === 'object', '"from" must be an object');
  need(isStr(d.from.name), '"from.name" must be a non-empty string');
  need(Array.isArray(d.from.lines) && d.from.lines.length > 0 && d.from.lines.every(isStr),
    '"from.lines" must be a non-empty array of strings');
  need(isStr(d.from.email), '"from.email" must be a non-empty string');
  need(d.billTo && typeof d.billTo === 'object', '"billTo" must be an object');
  need(isStr(d.billTo.name), '"billTo.name" must be a non-empty string');
  need(d.billTo.lines === undefined || (Array.isArray(d.billTo.lines) && d.billTo.lines.every(isStr)),
    '"billTo.lines" must be an array of strings when present');
  need(Array.isArray(d.lineItems) && d.lineItems.length > 0,
    '"lineItems" must be a non-empty array (an invoice with no line items describes nothing)');
  d.lineItems.forEach((it, i) => {
    need(it && isStr(it.title) && isStr(it.amount), `lineItems[${i}] needs "title" and "amount" strings`);
  });
  need(Array.isArray(d.paymentTable) && d.paymentTable.length > 0,
    '"paymentTable" must be a non-empty array (fill from PAYMENT-DETAILS.md)');
  d.paymentTable.forEach((r, i) => {
    need(r && isStr(r.label) && isStr(r.value), `paymentTable[${i}] needs "label" and "value" strings`);
  });
  if (d.schedule !== undefined) {
    need(d.schedule && typeof d.schedule === 'object', '"schedule" must be an object when present');
    need(Array.isArray(d.schedule.rows) && d.schedule.rows.length > 0,
      '"schedule.rows" must be a non-empty array when schedule is present');
    d.schedule.rows.forEach((r, i) => {
      need(r && isStr(r.label) && isStr(r.period) && isStr(r.status) && isStr(r.amount),
        `schedule.rows[${i}] needs "label", "period", "status", "amount" strings`);
    });
    need(isStr(d.schedule.contractTotal), '"schedule.contractTotal" must be a non-empty string');
  }
  need(d.notes === undefined || (Array.isArray(d.notes) && d.notes.every(isStr)),
    '"notes" must be an array of strings when present');
  need(d.tagline === undefined || (Array.isArray(d.tagline) && d.tagline.every(isStr)),
    '"tagline" must be an array of strings when present');
  if (d.status !== undefined) {
    need(isStr(d.status) && Object.prototype.hasOwnProperty.call(STATUS_COLORS, d.status.toLowerCase()),
      `"status" must be one of Draft, Sent, Paid, Overdue (got ${JSON.stringify(d.status)})`);
  }
  for (const f of ['tax', 'currency', 'payableByNote', 'closingNote', 'signName', 'signTitle', 'footerLeft']) {
    need(d[f] === undefined || isStr(d[f]), `"${f}" must be a non-empty string when present`);
  }

  const flat = JSON.stringify(d);
  if (/[—–]/.test(flat)) {
    fail('data JSON contains an em or en dash; both are banned everywhere (knowledge/voice/copy-rules.md)');
  }
}

// ---------------------------------------------------------------------------
// Template fragments
// ---------------------------------------------------------------------------

const MONO = "'JetBrains Mono',monospace";
const SANS = "'Inter Tight',sans-serif";
const DISPLAY = "'Space Grotesk',sans-serif";
const LABEL_STYLE = `font-family:${MONO}; font-size:10px; font-weight:500; letter-spacing:0.13em; text-transform:uppercase; color:#8a8177`;

function copyBtn() {
  return `<button type="button" data-copybtn="1" class="no-print copy-btn" style="margin-left:10px; padding:1px 7px; border:1px solid #e5e0d8; border-radius:3px; background:#fff; font-family:${MONO}; font-size:9.5px; letter-spacing:0.08em; text-transform:uppercase; color:#8a8177; cursor:pointer">Copy</button>`;
}

function paymentRow(row, i, isLast) {
  const border = isLast ? '' : ' border-bottom:1px solid #e5e0d8;';
  // Mirrors the design's per-row styling: `strong` is the payment-reference
  // row's 500 weight, `multiline` is the address rows' line-height:1.5, and
  // width:38% sits only on the first label cell (border-collapse makes the
  // first row govern the column).
  const weight = row.strong ? ' font-weight:500;' : '';
  const valueStyle = row.mono
    ? `font-family:${MONO}; font-size:14px;${weight} letter-spacing:0.02em; color:#16130f`
    : `font-family:${SANS}; font-size:14px;${weight}${row.multiline ? ' line-height:1.5;' : ''} color:#16130f`;
  const width = i === 0 ? 'width:38%; ' : '';
  return `      <tr>
        <td style="${width}padding:9px 14px;${border} background:#faf8f5; font-family:${SANS}; font-size:13.5px; color:#6b6358">${esc(row.label)}</td>
        <td style="padding:9px 14px;${border} ${valueStyle}"><span data-copy="1">${esc(row.value)}</span>${copyBtn()}</td>
      </tr>`;
}

function lineItemRow(item) {
  const detail = item.detail
    ? `\n        <div style="font-family:${SANS}; font-size:14px; line-height:1.6; color:#6b6358; margin-top:5px; max-width:62ch">${rich(item.detail)}</div>`
    : '';
  return `    <tr style="break-inside:avoid">
      <td style="padding:16px 24px 16px 0; border-bottom:1px solid #e5e0d8; vertical-align:top">
        <div style="font-family:${SANS}; font-size:15px; font-weight:600; color:#16130f; line-height:1.4">${rich(item.title)}</div>${detail}
      </td>
      <td style="padding:16px 0; border-bottom:1px solid #e5e0d8; vertical-align:top; text-align:right; font-family:${MONO}; font-size:15px; color:#16130f; white-space:nowrap">${esc(item.amount)}</td>
    </tr>`;
}

function scheduleRow(row) {
  const ink = row.current ? '#16130f' : '#6b6358';
  const firstWeight = row.current ? ' font-weight:600;' : '';
  const statusWeight = row.current ? ' font-weight:600;' : '';
  const amountWeight = row.current ? ' font-weight:500;' : '';
  return `      <tr>
        <td style="padding:10px 14px; border-bottom:1px solid #e5e0d8; font-family:${SANS}; font-size:14px;${firstWeight} color:${ink}">${esc(row.label)}</td>
        <td style="padding:10px 14px; border-bottom:1px solid #e5e0d8; font-family:${SANS}; font-size:14px; color:${ink}">${esc(row.period)}</td>
        <td style="padding:10px 14px; border-bottom:1px solid #e5e0d8; font-family:${SANS}; font-size:14px;${statusWeight} color:${ink}">${esc(row.status)}</td>
        <td style="padding:10px 14px; border-bottom:1px solid #e5e0d8; text-align:right; font-family:${MONO}; font-size:14px;${amountWeight} color:${ink}">${esc(row.amount)}</td>
      </tr>`;
}

function scheduleSection(schedule) {
  if (!schedule) return '';
  const th = (label, right) =>
    `<th style="text-align:${right ? 'right' : 'left'}; padding:9px 14px; border-bottom:1px solid #e5e0d8; font-family:${MONO}; font-size:10px; font-weight:500; letter-spacing:0.1em; text-transform:uppercase; color:#4a443c">${label}</th>`;
  const note = schedule.note
    ? `\n  <p style="margin:10px 0 0; font-family:${SANS}; font-size:13.5px; line-height:1.6; color:#6b6358; orphans:3; widows:3">${rich(schedule.note)}</p>`
    : '';
  return `
<section style="margin-bottom:26px; break-inside:avoid">
  <div style="${LABEL_STYLE}; padding-bottom:10px">${esc(schedule.heading || 'Instalment schedule')}</div>
  <table style="width:100%; border-collapse:collapse; border:1px solid #e5e0d8">
    <thead>
      <tr style="background:#f7f5f1">
        ${th('Instalment')}
        ${th('Billing period')}
        ${th('Status')}
        ${th('Amount', true)}
      </tr>
    </thead>
    <tbody>
${schedule.rows.map(scheduleRow).join('\n')}
      <tr style="background:#f7f5f1">
        <td colspan="3" style="padding:10px 14px; font-family:${SANS}; font-size:14px; font-weight:600; color:#16130f">Contract total</td>
        <td style="padding:10px 14px; text-align:right; font-family:${MONO}; font-size:14px; font-weight:500; color:#16130f">${esc(schedule.contractTotal)}</td>
      </tr>
    </tbody>
  </table>${note}
</section>
`;
}

function buildHtml(d) {
  const statusLabel = d.status || 'Sent';
  const statusColor = STATUS_COLORS[statusLabel.toLowerCase()];
  const currency = d.currency || 'USD';
  const payableBy = d.payableByNote || `Payable by ${d.dueDate}`;
  const signName = d.signName || 'Sam Rivera';
  const signTitle = d.signTitle || 'Founder, Northwind Labs';
  // The design's sample sign-off carried a tagline block. Slogan copy on a
  // client document reads as filler and undercuts the number next to it, so
  // there is no default: a tagline renders only if the data provides one.
  const tagline = d.tagline || [];
  const closingNote = d.closingNote || 'Thank you for the work.';
  const footerLeft = d.footerLeft ? esc(d.footerLeft) : 'Rivera Holdings LLC &nbsp;·&nbsp; dba Northwind Labs';
  const notes = d.notes || [];

  const fonts = {
    spaceGrotesk: dataUri('fonts/SpaceGrotesk-var-latin.woff2', 'font/woff2'),
    interTight: dataUri('fonts/InterTight-var-latin.woff2', 'font/woff2'),
    jetbrainsMono: dataUri('fonts/JetBrainsMono-var-latin.woff2', 'font/woff2'),
  };
  // Swap assets/logo.png for your own mark. It ships as a neutral placeholder
  // so a fresh clone renders a real invoice on the first run.
  const logo = dataUri('logo.png', 'image/png');
  // The usage comment inside doc-page.js contains literal </script> tags;
  // break them so the inline embedding survives HTML parsing.
  const docPageJs = fs
    .readFileSync(path.join(ASSETS, 'doc-page.js'), 'utf8')
    .replace(/<\/script/g, '<\\/script');

  const billToEmail = d.billTo.email
    ? `<a href="mailto:${esc(d.billTo.email)}">${esc(d.billTo.email)}</a><br />`
    : '';

  // font-display: block (design says swap): deliberate for headless print -
  // block waits for the inlined faces instead of flashing a fallback into the
  // PDF; data-URI fonts decode instantly so screens never notice.
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Invoice ${esc(d.invoiceNumber)} · Northwind Labs</title>
<style>
@font-face { font-family: 'Space Grotesk'; src: url('${fonts.spaceGrotesk}') format('woff2'); font-weight: 100 900; font-style: normal; font-display: block; }
@font-face { font-family: 'Inter Tight'; src: url('${fonts.interTight}') format('woff2'); font-weight: 100 900; font-style: normal; font-display: block; }
@font-face { font-family: 'JetBrains Mono'; src: url('${fonts.jetbrainsMono}') format('woff2'); font-weight: 100 900; font-style: normal; font-display: block; }
doc-page:not(:defined) { visibility: hidden; }
body { margin: 0; }
a { color: #b8623c; text-decoration: none; }
a:hover { color: #d97757; text-decoration: underline; }
.copy-btn:hover { border-color: #d97757 !important; color: #d97757 !important; }
@media print { .no-print { display: none !important; } }
</style>
</head>
<body>
<doc-page margin="0.6in">

<div slot="footer" style="display:flex; justify-content:space-between; align-items:baseline; gap:16px; border-top:1px solid #e5e0d8; padding-top:8px; font-family:${MONO}; font-size:9.5px; letter-spacing:0.06em; text-transform:uppercase; color:#8a8177">
  <span>${footerLeft}</span>
  <span>Invoice ${esc(d.invoiceNumber)}</span>
  <span>${esc(d.from.email)}</span>
</div>

<header style="display:flex; align-items:flex-start; justify-content:space-between; gap:40px; padding-bottom:22px; border-bottom:2px solid #16130f">
  <div>
    <div style="display:flex; align-items:center; gap:10px">
      <img src="${logo}" alt="" style="width:24px; height:24px; display:block" />
      <span style="font-family:${DISPLAY}; font-size:18px; letter-spacing:0.01em; color:#16130f; line-height:1">Northwind Labs</span>
    </div>
    <div style="margin-top:14px; font-family:${SANS}; font-size:13px; line-height:1.6; color:#6b6358">
      ${esc(d.from.name)}<br />${d.from.lines.map(esc).join('<br />')}<br /><a href="mailto:${esc(d.from.email)}">${esc(d.from.email)}</a>
    </div>
  </div>
  <div style="text-align:right; flex-shrink:0">
    <div style="font-family:${DISPLAY}; font-size:34px; font-weight:500; letter-spacing:-0.03em; line-height:1; color:#16130f">Invoice</div>
    <div style="margin-top:8px; font-family:${MONO}; font-size:14px; letter-spacing:0.04em; color:#16130f">${esc(d.invoiceNumber)}</div>
    <div style="margin-top:12px; display:inline-flex; align-items:center; gap:7px; padding:4px 11px; border:1px solid #d5cec3; border-radius:3px">
      <span style="width:6px; height:6px; border-radius:50%; display:block; background:${statusColor}"></span>
      <span style="font-family:${MONO}; font-size:10px; font-weight:500; letter-spacing:0.13em; text-transform:uppercase; color:#4a443c">${esc(statusLabel)}</span>
    </div>
  </div>
</header>

<section style="display:grid; grid-template-columns:1.15fr 1fr; gap:36px; padding:24px 0 26px; border-bottom:1px solid #e5e0d8; break-inside:avoid">
  <div>
    <div style="${LABEL_STYLE}; padding-bottom:9px">Bill to</div>
    <div style="font-family:${SANS}; font-size:15px; font-weight:600; color:#16130f; line-height:1.4">${esc(d.billTo.name)}</div>
    <div style="font-family:${SANS}; font-size:14px; line-height:1.6; color:#6b6358; margin-top:3px">
      ${billToEmail}${(d.billTo.lines || []).map(esc).join('<br />')}
    </div>
  </div>
  <div style="display:grid; grid-template-columns:auto 1fr; gap:7px 18px; align-content:start; font-family:${SANS}; font-size:14px; line-height:1.5">
    <span style="color:#8a8177">Invoice number</span><span style="font-family:${MONO}; font-size:13px; color:#16130f; text-align:right">${esc(d.invoiceNumber)}</span>
    <span style="color:#8a8177">Date issued</span><span style="color:#16130f; text-align:right">${esc(d.dateIssued)}</span>
    <span style="color:#8a8177">Due date</span><span style="color:#16130f; font-weight:600; text-align:right">${esc(d.dueDate)}</span>
    <span style="color:#8a8177">Terms</span><span style="color:#16130f; text-align:right">${esc(d.terms)}</span>
    <span style="color:#8a8177">Currency</span><span style="color:#16130f; text-align:right">${esc(currency)}</span>
  </div>
</section>

<section style="display:flex; align-items:center; justify-content:space-between; gap:24px; margin:22px 0 28px; padding:18px 22px; background:#f7f5f1; border:1px solid #e5e0d8; border-left:3px solid #d97757; break-inside:avoid">
  <div>
    <div style="${LABEL_STYLE}">Amount due</div>
    <div style="font-family:${SANS}; font-size:13px; color:#6b6358; margin-top:4px">${esc(payableBy)}</div>
  </div>
  <div style="font-family:${DISPLAY}; font-size:32px; font-weight:600; letter-spacing:-0.03em; color:#16130f; line-height:1; white-space:nowrap">${esc(d.total)}</div>
</section>

<table style="width:100%; border-collapse:collapse; margin-bottom:26px">
  <thead>
    <tr>
      <th style="text-align:left; padding:0 0 8px; border-bottom:1px solid #16130f; font-family:${MONO}; font-size:10px; font-weight:500; letter-spacing:0.13em; text-transform:uppercase; color:#4a443c">Description</th>
      <th style="text-align:right; padding:0 0 8px; border-bottom:1px solid #16130f; font-family:${MONO}; font-size:10px; font-weight:500; letter-spacing:0.13em; text-transform:uppercase; color:#4a443c; white-space:nowrap">Amount (${esc(currency)})</th>
    </tr>
  </thead>
  <tbody>
${d.lineItems.map(lineItemRow).join('\n')}
    <tr>
      <td style="padding:12px 24px 0 0; text-align:right; font-family:${SANS}; font-size:14px; color:#6b6358">Subtotal</td>
      <td style="padding:12px 0 0; text-align:right; font-family:${MONO}; font-size:14px; color:#6b6358; white-space:nowrap">${esc(d.subtotal)}</td>
    </tr>
    <tr>
      <td style="padding:6px 24px 12px 0; text-align:right; font-family:${SANS}; font-size:14px; color:#6b6358">Tax</td>
      <td style="padding:6px 0 12px; text-align:right; font-family:${MONO}; font-size:14px; color:#6b6358; white-space:nowrap">${esc(d.tax || '0.00')}</td>
    </tr>
    <tr>
      <td style="padding:12px 24px 0 0; border-top:2px solid #16130f; text-align:right; font-family:${SANS}; font-size:15px; font-weight:600; color:#16130f">Total due (${esc(currency)})</td>
      <td style="padding:12px 0 0; border-top:2px solid #16130f; text-align:right; font-family:${MONO}; font-size:17px; font-weight:500; color:#16130f; white-space:nowrap">${esc(d.total)}</td>
    </tr>
  </tbody>
</table>
${scheduleSection(d.schedule)}
<section style="margin-bottom:24px; break-inside:avoid">
  <div style="${LABEL_STYLE}; padding-bottom:10px">Payment details</div>
  <p style="margin:0 0 12px; font-family:${SANS}; font-size:14px; line-height:1.6; color:#6b6358">${rich(d.paymentIntro)}</p>
  <table style="width:100%; border-collapse:collapse; border:1px solid #e5e0d8">
    <tbody id="payment-rows">
${d.paymentTable.map((row, i) => paymentRow(row, i, i === d.paymentTable.length - 1)).join('\n')}
    </tbody>
  </table>
</section>

${notes.length ? `<section style="margin-bottom:26px; break-inside:avoid">
  <div style="${LABEL_STYLE}; padding-bottom:8px">Notes</div>
  <ul style="margin:0; padding-left:18px; font-family:${SANS}; font-size:13.5px; line-height:1.65; color:#6b6358">
${notes.map((n, i) => `    <li${i < notes.length - 1 ? ' style="margin-bottom:5px"' : ''}>${rich(n, 500)}</li>`).join('\n')}
  </ul>
</section>

` : ''}<section style="display:flex; align-items:flex-end; justify-content:space-between; gap:32px; padding-top:20px; border-top:1px solid #e5e0d8; break-inside:avoid">
  <div>
    <p style="margin:0; font-family:${SANS}; font-size:14px; line-height:1.6; color:#6b6358; max-width:52ch">${rich(closingNote)} Questions about this invoice, reply to <a href="mailto:${esc(d.from.email)}">${esc(d.from.email)}</a>.</p>
    <div style="margin-top:14px; font-family:${SANS}; font-size:14px; font-weight:600; color:#16130f">${esc(signName)}</div>
    <div style="font-family:${SANS}; font-size:13px; color:#8a8177">${esc(signTitle)}</div>
  </div>
${tagline.length ? `  <div style="text-align:right; flex-shrink:0; font-family:${MONO}; font-size:9.5px; letter-spacing:0.1em; text-transform:uppercase; color:#a8a095; line-height:1.7">
    ${tagline.map(esc).join('<br />')}
  </div>
` : ''}</section>

</doc-page>
<script>
${docPageJs}
</script>
<script>
// Screen-only copy buttons on the wire table (hidden in print via .no-print).
document.getElementById('payment-rows').addEventListener('click', (e) => {
  const btn = e.target.closest('[data-copybtn]');
  if (!btn) return;
  const cell = btn.closest('td');
  const val = cell && cell.querySelector('[data-copy]');
  if (!val) return;
  const text = val.textContent.trim();
  const done = () => {
    const prev = btn.textContent;
    btn.textContent = 'Copied';
    btn.style.color = '#4f8a5b';
    btn.style.borderColor = '#4f8a5b';
    setTimeout(() => { btn.textContent = prev; btn.style.color = '#8a8177'; btn.style.borderColor = '#e5e0d8'; }, 1400);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => {});
  } else {
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done(); } catch (err) {}
    document.body.removeChild(ta);
  }
});
</script>
</body>
</html>
`;
}

// ---------------------------------------------------------------------------
// PDF printing
// ---------------------------------------------------------------------------

function findChrome() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) {
    return process.env.CHROME_BIN;
  }
  // Same candidate list as the proposal generator; keep the two in step.
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/snap/bin/chromium',
  ];
  const found = candidates.find((p) => fs.existsSync(p));
  if (!found) fail('no Chrome/Chromium found (set CHROME_BIN to override; looked in the default macOS and Linux paths for google-chrome, google-chrome-stable, chromium, chromium-browser)');
  return found;
}

/** True once the PDF at pdfPath is complete: written during this run, over the
 *  size floor, stable across two polls, and carrying the %%EOF trailer. */
function pdfComplete(pdfPath, printStart, lastSize) {
  let st;
  try {
    st = fs.statSync(pdfPath);
  } catch {
    return { done: false, size: -1 };
  }
  if (st.mtimeMs < printStart || st.size < PDF_SIZE_FLOOR || st.size !== lastSize) {
    return { done: false, size: st.size };
  }
  const fd = fs.openSync(pdfPath, 'r');
  try {
    const tail = Buffer.alloc(Math.min(2048, st.size));
    fs.readSync(fd, tail, 0, tail.length, st.size - tail.length);
    return { done: tail.includes('%%EOF'), size: st.size };
  } finally {
    fs.closeSync(fd);
  }
}

/** Print htmlPath to pdfPath with headless Chrome. Chrome regularly lingers
 *  long after the PDF is fully written, so the exit is not the signal; the
 *  file is. Poll for a complete PDF, then terminate Chrome ourselves. */
function printPdf(htmlPath, pdfPath) {
  const chrome = findChrome();
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'invoice-chrome-'));
  const printStart = Date.now();
  return new Promise((resolve, reject) => {
    const child = spawn(
      chrome,
      [
        '--headless',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-extensions',
        '--disable-sync',
        '--hide-scrollbars',
        `--user-data-dir=${profile}`,
        '--virtual-time-budget=10000',
        '--no-pdf-header-footer',
        `--print-to-pdf=${pdfPath}`,
        pathToFileURL(htmlPath).href,
      ],
      { stdio: 'ignore' }
    );
    let lastSize = -1;
    let settled = false;
    const finish = (err) => {
      if (settled) return;
      settled = true;
      clearInterval(poller);
      clearTimeout(deadline);
      const cleanup = () => {
        fs.rmSync(profile, { recursive: true, force: true });
        err ? reject(err) : resolve();
      };
      if (child.exitCode === null) {
        // Remove the profile only after Chrome is dead, or it re-creates it.
        child.once('exit', cleanup);
        child.kill('SIGTERM');
        setTimeout(() => { if (child.exitCode === null) child.kill('SIGKILL'); }, 2000).unref();
      } else {
        cleanup();
      }
    };
    const poller = setInterval(() => {
      const { done, size } = pdfComplete(pdfPath, printStart, lastSize);
      lastSize = size;
      if (done) finish();
    }, 300);
    const deadline = setTimeout(() => {
      finish(new Error(`Chrome produced no complete PDF at ${pdfPath} within ${PRINT_DEADLINE_MS / 1000}s`));
    }, PRINT_DEADLINE_MS);
    child.on('exit', () => {
      // Chrome exited on its own: give the poller one final synchronous look.
      const first = pdfComplete(pdfPath, printStart, -1);
      const second = pdfComplete(pdfPath, printStart, first.size);
      if (second.done) finish();
      else finish(new Error(`Chrome exited without writing a complete PDF at ${pdfPath}`));
    });
    child.on('error', (e) => finish(e));
  });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const [dataPath, pdfPath] = process.argv.slice(2);
  if (!dataPath || !pdfPath) {
    fail('usage: node generate-invoice-html.js <data.json> <output.pdf>');
  }
  if (!/\.pdf$/i.test(pdfPath)) {
    fail(`output path must end in .pdf (got ${pdfPath})`);
  }
  let d;
  try {
    d = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  } catch (e) {
    fail(`cannot read data JSON at ${dataPath}: ${e.message}`);
  }
  validate(d);

  const absPdf = path.resolve(pdfPath);
  const htmlPath = absPdf.replace(/\.pdf$/i, '.html');
  fs.mkdirSync(path.dirname(absPdf), { recursive: true });
  fs.writeFileSync(htmlPath, buildHtml(d));
  console.log(`html: ${htmlPath}`);
  await printPdf(htmlPath, absPdf);
  console.log(`pdf:  ${absPdf} (${fs.statSync(absPdf).size} bytes)`);
  console.log('next: scripts/pdf-check must PASS before anything leaves.');
}

main().catch((e) => fail(e.message));
