---
name: proposal-creator
description: "Generate professional Northwind Labs client proposals as print-ready HTML rendered to PDF in the 2026-08-02 design standard. Use this skill whenever the user wants to create a proposal, quote, SOW (scope of work), service agreement, or project bid for a client. Triggers include: 'create a proposal', 'write a proposal for [client]', 'generate a quote', 'make a proposal doc', 'SOW for [project]', 'proposal for [client name]', any mention of creating a client-facing proposal document, or references to past proposals like 'similar to the Acme Retail proposal'. Also use when the user provides client details and project scope and wants it formatted as a professional deliverable. This skill produces a self-contained HTML file plus a PDF that exactly match the Northwind Labs proposal design standard: doc-page print shell, house mark + wordmark, Space Grotesk display type, JetBrains Mono labels, accent-numbered sections, and the signature block."
---

# Northwind Labs Proposal Creator

Generate branded proposals in the Northwind Labs design standard adopted 2026-08-02. The
deliverable is a PDF printed from a self-contained HTML file; the HTML is the working artifact,
the PDF is what the client gets.

**Design source of record:** `references/design-standard-2026-08-02.dc.html`. Read its header
banner before trusting its content: the design is normative, the numbers in it are dead.

## When to Use

- User wants to create a new client proposal
- User mentions writing a quote, SOW, or project bid
- User provides client info + scope and wants it formatted
- User references "the Acme Retail proposal" or "a proposal like [existing one]"

## Quick Start

1. **Gather proposal details** from the user (see Interview section below)
2. **Read the data schema**: `references/data-schema.md` (relative to this skill) for the complete JSON structure and examples
3. **Run the scope-discipline gate** (section below), then **build the JSON** data object, including the required `DEFINITION OF DONE` section
4. **Run the generator**: `scripts/generate-proposal-html.js` (HTML + PDF in one run)
5. **Verify** (mandatory - see Verification section; `scripts/pdf-check` + fresh-context `fact-check` + `price-attack` subagents)
6. **Present** the PDF to the user

## Interview: What to Gather

Before generating, collect these details from the user. Use context from `knowledge/` and past conversations to pre-fill what you can.

### Required Fields
- **Client name** - Who is this for?
- **Project title** - Short title (also feeds the header tag and cover fallbacks)
- **Project description** - Longer description (cover lede fallback)
- **Date** - Proposal date (default to today)
- **Scope of work** - Services being offered, grouped into sections. Each section has a title and a table of deliverable + description pairs.
- **Pricing** - Line items with descriptions and amounts. Mark totals as bold.
- **Definition of done**, for each priced phase (or for the single phase): the named deliverables AND the acceptance criteria that make each one done. Ships as a `customSections` entry with `"heading": "DEFINITION OF DONE"`, normally a two-column table (`Phase` / `Deliverables and acceptance`). No proposal ships without it. This traces to a real incident in `ai/ERRORS.md`: a draft priced already-live infrastructure as new build and promoted never-discussed items into client scope, partly because nothing in the schema forced the drafter to write down what each line delivers and how the client accepts it.

### Optional Fields (have sensible defaults)
- **Sent by** - Defaults to "Sam Rivera"
- **Contact email** - Defaults to "sam@northwindlabs.example"
- **Proposal type** - "Service Retainer Proposal", "Project Proposal", or "Infrastructure Build Proposal" (renders in the cover kicker)
- **Client entity** - Legal entity for the footer confidence line and the acceptance block (defaults to client name; check the invoice ledger for the billing entity)
- **Cover title / cover lede** - The big Space Grotesk sentence and the paragraph under it (fall back to project title / description)
- **Overview text**, **What This Covers**, **Additional Work / Out of scope**, **Payment Terms**, **Terms & Conditions**, **custom sections** (Timeline, Sequencing, Ongoing platform costs, Decisions required, etc.)
- **accent / paper / density** - design props (defaults: `#e89b5c`, letter, standard). Use `--paper a4` for a clearly metric client.

### Pre-fill Defaults

Always use these Northwind Labs defaults unless the user specifies otherwise:
- Sent by: "Sam Rivera"
- Contact email: "sam@northwindlabs.example"
- Legal entity note: "Northwind Labs (operating under Rivera Holdings LLC)" (the footer renders "Northwind Labs · operating under Rivera Holdings LLC" on every page)
- Standard T&C includes: 30-day termination notice, transferability, data ownership, scope change agreement
- Standard additional work: out-of-scope billed at agreed hourly rate, quoted before commencement

### Voice

No em dashes and no en dashes anywhere in proposal copy (`knowledge/voice/copy-rules.md`).
Comma, period, or single hyphen; write ranges as `15-30%`. The generator warns once per
offending data string; fix the data, never ship the warning.

## Scope discipline (do this before building the JSON)

Two checks, both from the scope-inflation entry in `ai/ERRORS.md`. Run them on the scope list
before a single line reaches the JSON.

1. **Nothing sized as new build may already be live.** Read the client file's own recorded infra
   facts (`knowledge/clients/<client>/`) and reconcile every workstream against them. The draft
   behind that entry priced a production email backend and its sender-domain DNS as new work
   inside a paid readiness phase, while the same client file's own infrastructure section already
   recorded that backend as live and running.
2. **Every scope line traces to the client's ask or to Sam's explicit addition.** Repo-internal
   security residuals, hardening-report leftovers and reviewer best-practice items never
   auto-promote into client scope. Remediation of work Northwind Labs already delivered is never
   billed.

Record the trace, do not just think it. Put a top-level `scopeTrace` array in the data JSON, one
entry per scope line, each with an origin: `asked by client YYYY-MM-DD` / `Sam added YYYY-MM-DD`
/ `already live, not billable`. The generator reads only the documented keys, so `scopeTrace`
renders nothing into the deliverable; it exists so `price-attack`, which is handed this sidecar in
fresh context, can attack the provenance of the scope and not only the price. If a line has no
origin, it is not scope. Schema in `references/data-schema.md`.

## Generation Steps

Runs locally in this repo (no sandbox, no npm dependencies for this generator). Requirements:
node (the generator is a `.js` script), Google Chrome or Chromium for PDF printing (default macOS
and Linux install paths are searched; `CHROME_BIN` or `--chrome <path>` overrides), and poppler for
`scripts/pdf-check`. `npm install docx` is only for the legacy docx generator. The script
resolves brand assets via `../assets/` relative to itself (fonts + the vendored `doc-page.js`
print shell) - run it in place, never move it out of the skill folder.

### Step 1: Create proposal data JSON

Write the proposal data per `references/data-schema.md` to `outputs/proposals/<slug>-data.json`.

### Step 2: Generate the HTML + PDF

```bash
node skills/proposal-creator/scripts/generate-proposal-html.js \
  "outputs/proposals/<slug>-data.json" \
  "outputs/proposals/<Client> - <Title>.html"
```

The PDF lands next to the HTML (same name, `.pdf`). Read the generator's warnings: it flags
banned dashes in the data and a missing `DEFINITION OF DONE` section.

### Step 3: Verify file integrity

Run the canonical validator - it must PASS:

```bash
scripts/pdf-check "outputs/proposals/<Client> - <Title>.pdf" \
  --expect "<client name>" --expect "<total>"
```

`pdf-check` is a real-app open test (PDF structure, poppler parse, page count, non-empty text
extraction, every font embedded, macOS Quick Look render) - it catches malformed or blank files
that a byte-size check can't. That failure class is real: a generated document once passed a
size check, was delivered, and would not open. The `--expect` strings prove the client name and
total actually rendered. Then open the PDF pages visually (Read the file) and confirm the design
landed: header wordmark, accent-numbered sections, signature block, no clipped or overlapping
text.

## Verification (mandatory - never skip, even for "quick" or informal work)

1. **`fact-check` subagent** (fresh context): pass ONLY the draft PDF path + client name - not your reasoning. It re-derives every number, date, and entity from canonical files. Fix failures and re-run until `VERDICT: PASS`.
2. **`price-attack` subagent** (fresh context): pass ONLY the draft paths - the PDF AND its `-data.json` sidecar - plus the client name. It attacks price and scope against the pricing authority (the client roadmap for a client engagement, `knowledge/business/outbound-offer.md` for the outbound offer). Address each objection, or record Sam's explicit word overruling it and why. Telling them afterwards is not the same as consent: pricing is Sam's call, so an overrule needs Sam, and this file is the one that binds under CLAUDE.md's precedence carve-out.
3. **Pre-send checklist** in `CLAUDE.md` (USD, phase-and-price, no unverified timelines, channel voice, no unasked price justification).
4. **On SEND, open a pricing-outcomes row** (sanctioned ledger write): append a row to `knowledge/business/pricing-outcomes.md` - `Date` = send date, `Deal` = client + short scope, `Quoted` = the price, `Reaction` = `pending`, `Final` = `-`, `Lesson` = `-`. The row stays open until the deal collects (the invoice skill closes it). This one write into `knowledge/` is sanctioned as a ledger append - nothing else in `knowledge/` is.
5. **Definition of done present and specific.** The `DEFINITION OF DONE` section exists, covers every priced phase, and each row states an acceptance test the client could run unaided. "Delivered" is not an acceptance criterion. A phase priced without a definition of done is a scope dispute already in progress.
6. **Scope trace complete.** Every scope line in the deliverable has an entry in the sidecar's `scopeTrace`, and no entry reads `already live, not billable` while still being priced. That is the scope-inflation failure in one check.

## Design Reference (2026-08-02 standard)

One flowing doc-page document, letter paper (a4 on request), 0.68in margin, running header and
footer on every page. Anatomy, in order:

```
header slot   house mark + "Northwind Labs" (Space Grotesk) | PROJECT TAG (mono, uppercase)
cover         accent square + kicker "PROJECT PROPOSAL · <date>" (mono)
              cover title (Space Grotesk 36px, sentence with period)
              cover lede paragraph
meta strip    4 columns: Prepared for / Prepared by / Engagement / Total investment
01 Overview   paragraphs
02 Scope of work        n.1, n.2 subsections, Deliverable/Description tables
03 Investment           line items + right-aligned mono amounts, total row,
                        n.1 Payment terms (accent-numbered rows), muted note
04 What this covers     two-column checklist grid, accent ticks
05 Out of scope / Additional work
NN custom sections      paragraph, accent-numbered rows, or table
NN Terms and conditions NN.1-style numbered rows
NN Acceptance           two-party signature block + closing contact line
footer slot   "<Client entity> · Commercial in confidence" | "Northwind Labs · operating under Rivera Holdings LLC"
```

Sections 02, 03 and Acceptance start on a fresh page by default (`pageBreaks` in the data JSON
overrides). Section headings carry an accent mono number (01, 02, ...) over a full-width rule.

## Typography & Colors

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Body / tables | Inter Tight | 13.5-14px | 400 | #2a241d |
| Cover title | Space Grotesk | 36px | 500 | #0b0a09 |
| Section heading | Space Grotesk | 19px | 500 | #0b0a09 |
| Sub-heading | Space Grotesk | 14.5px | 500 | #0b0a09 |
| Wordmark | Space Grotesk | 12.5px | 500 | #0b0a09 |
| Labels / kickers / amounts | JetBrains Mono | 8.5-10px | 400-500 | #6b6358 |
| Section numbers, ticks, dots | JetBrains Mono | 10px | 500 | accent #e89b5c |
| Strong rules | - | 1px | - | #2a241d |
| Light rules | - | 1px | - | rgba(42,36,29,0.13) |

Fonts are embedded into the HTML as base64 (latin-subset variable woff2 from `assets/fonts/`), so
the artifact renders identically offline and the PDF embeds every font. All three are
open-licensed, which is why they can ship inside a client deliverable at all; a licensed display
face would not be, so the wordmark rides on Space Grotesk rather than a bought font.

The house mark is a geometric N, drawn as an inline SVG in the HTML generator and as
`assets/logo.png` for the legacy docx generator. Both carry the same geometry. Replace them
together, or the two output formats drift.

## Legacy .docx generator (superseded as the standard)

**SUPERSEDED as the proposal standard 2026-08-02 - see the design standard above.**
`scripts/generate-proposal.js` (Open Sans docx house style) remains runnable for one case only:
a client who needs an editable `.docx`. If used, validate with `scripts/docx-check` and run the
same Verification section. Never use it because it feels faster; the standard is the PDF.

## Notes

- The generator auto-handles all formatting: provide clean text content in the JSON
- `customSections` render in the same visual language automatically: string content becomes a paragraph, array content becomes accent-numbered rows, `table` becomes a Deliverable/Description-style table (`col1Width` in DXA still respected, converted to a percentage)
- `paymentTerms` items can be `{ "text": ..., "amount": "$4,500" }` objects - amounts then render in the design's right-aligned mono column; plain strings still work
- Known simplification vs the design source: bespoke three-column anatomies (the design's Sequencing table) render through the generic two-column forms; per-section page breaks are available via `pageBreaks` keys (`custom:<HEADING>`)
- ALL-CAPS headings in data ("DEFINITION OF DONE") display sentence-cased ("Definition of done"); the JSON keeps the caps form for schema compatibility
- The HTML is self-contained and click-editable in a browser for a quick visual pass, but the data JSON is the source of truth: edit the JSON and regenerate, never hand-edit the HTML
