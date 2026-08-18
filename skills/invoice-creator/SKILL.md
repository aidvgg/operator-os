---
name: invoice-creator
description: "Generate a branded Northwind Labs invoice in the 2026-08-02 design standard: print HTML rendered to PDF via headless Chrome (doc-page shell, logo mark + Space Grotesk wordmark, Space Grotesk display, Inter Tight body, JetBrains Mono labels, status chip, amount-due callout, optional instalment schedule, wire table with screen-only copy buttons). Use whenever Sam asks to invoice a client, bill for agreed work, or issue/reissue an invoice. ALWAYS takes the invoice number from the ledger - never guesses it."
---

# Northwind Labs Invoice Creator

Generates branded invoices in the **2026-08-02 design standard**: a self-contained print HTML rendered to PDF by headless Chrome. The PDF is the client-facing deliverable; the sibling HTML is the screen copy (copy buttons on the wire table, hidden in print). Pairs with the **invoice ledger** (the numbering authority) so numbers stay consistent and non-hallucinated across every chat.

Design source of record: `references/design-standard-2026-08-02.dc.html` (its header banner explains why its embedded numbers are dead and why its wire values are redacted). The runnable implementation is `scripts/generate-invoice-html.js`. The legacy docx generator (`scripts/generate-invoice.js`) survives only for a client who needs an editable `.docx`; validate that path with `scripts/docx-check` instead.

## Hard rule: the number comes from the ledger

`knowledge/business/invoices/INVOICE-LEDGER.md` is the single source of truth for invoice numbers. **Read it first**, use the value in its `NEXT INVOICE NUMBER` block, and after issuing, **increment** it. Never compute or recall a number any other way. Format: `NL-{YYYY}-{NNN}`, global monotonic sequence (does not reset per year), `{YYYY}` = issue year.

A guessed number is not a cosmetic error. It collides with a number already in the ledger, and two invoices carrying one reference is a payment the client's accounts payable cannot reconcile and you cannot chase.

## Steps

1. **Read the ledger** -> get the next number (e.g. `NL-2026-004`).
2. **Gather invoice facts** (pre-fill from `knowledge/`; don't re-ask what's known):
   - Bill-to entity + contact. Check the prior invoice for the same engagement and keep the billed entity continuous. A client who pays through more than one legal entity is normal, and switching mid-engagement is how an invoice gets bounced by their AP for not matching the PO.
   - From entity: **Rivera Holdings LLC (dba Northwind Labs)** - billing runs through the legal entity, the brand is the trading name. `CLAUDE.md` and `knowledge/memory.md` own that pairing; if the entity ever changes, they change first and this default follows.
   - Line item(s) + amount(s), **USD always**. Total.
   - Issue date, due date, terms (e.g. Net 7). Status starts as `Sent` (the chip: Draft / Sent / Paid / Overdue).
   - Instalment deals get the `schedule` block (rows + contract total + payrun note), single-shot invoices omit it.
   - Payment instructions / wire details: **read `knowledge/business/invoices/PAYMENT-DETAILS.md`** and put the matching entity's wire block in `paymentTable` (rows of `{label, value, mono, strong, multiline}`; `mono: true` on account/routing/SWIFT/reference rows, `strong: true` on the payment-reference row, `multiline: true` on the two address rows - the design's per-row styling). That file is gitignored and this skill only ever **reads** it: it is the one file holding live bank values, so nothing here writes it, and if it needs changing, ask Sam. On a fresh clone it does not exist yet - copy the committed sibling `PAYMENT-DETAILS.template.md` to `PAYMENT-DETAILS.md` and fill it in once. If a needed account is genuinely not in that file, leave a clearly-marked `‹fill before sending›` placeholder and flag it - **never invent bank/account numbers.**
   - No em or en dashes anywhere in the data (the generator refuses both; global rule, `knowledge/voice/copy-rules.md`).
3. **Write the data JSON** (schema below) to `outputs/invoices/<number>.json`.
4. **Generate:** `node skills/invoice-creator/scripts/generate-invoice-html.js outputs/invoices/<number>.json "outputs/invoices/<number>_<slug>.pdf"`
   - The output path must end in `.pdf`; the sibling `.html` lands next to it. Requires node (the generator is a `.js` script) and Google Chrome or Chromium on the machine (default macOS and Linux install paths are searched; `CHROME_BIN` overrides). No `npm install` for this path; `npm install docx` is only for the legacy docx generator.
5. **Verify** with the canonical validator - it must PASS:
   `scripts/pdf-check "outputs/invoices/<number>_<slug>.pdf" --expect "<number>" --expect "<total>" --expect "<bill-to name>" --expect "<from entity>" --expect "<due date>"`
   This is a real-app open test (header/trailer shape, poppler structural parse, non-empty extracted text, every font embedded, Quick Look render on darwin) plus mechanized content confirmation via `--expect`. A generated file is not a deliverable until something other than its own generator can open it: a malformed PDF and a PDF missing a fact both look fine to a string-grep on raw bytes (`ai/ERRORS.md`). Keep each `--expect` string short enough not to wrap in the rendered PDF (the number, the total, a surname); extraction inserts line breaks at wrap points.
6. **Verify (mandatory - never skip, even for reissues):** spawn the **`fact-check` subagent** (fresh context) with ONLY the `.pdf`/`.json` paths + client name - not your reasoning. It re-derives the number from the ledger, amounts/entities from the engagement records, checks date arithmetic, and compares the wire block field-by-field against `PAYMENT-DETAILS.md` (reporting match/mismatch only, no values). Fix failures and re-run until `VERDICT: PASS`. **If the amount never went through a proposal** (informal agreed work - `CLAUDE.md` allows invoicing without one), **also spawn `price-attack`** with the same inputs: billing time is the last moment the underpricing pattern can be caught.
7. **Record + advance:**
   - Write `knowledge/business/invoices/NL-YYYY-NNN.md` (per-invoice record; match existing record style). **Never inline wire numbers in this record - it is committed; point to `PAYMENT-DETAILS.md`.**
   - Update the ledger: append the Issued row, bump `NEXT INVOICE NUMBER` (+1) and the "Last issued" line.
   - Add the row to `knowledge/business/invoices/SUMMARY.md` (cash/status register).
   - **Arm the receivable clock:** add a line-start `**Due:** YYYY-MM-DD - <number> $<amount> payment due from <client>. Confirm receipt or chase.` line to **the per-invoice record in `knowledge/business/invoices/`**, dated the invoice's due date. `scripts/horizon` sees line-start `Due:` lines and mid-line bold `**Due:**` tokens, but a due date that lives only in a table column is invisible to the clock, and `scripts/money` looks only in that directory, so a Due line armed in a client roadmap file does not satisfy it. `scripts/money` FAILS if an open Register row has no armed Due line, so this is not optional. An unclocked receivable is money nobody chases.
   - **Run `scripts/money` to regenerate `MONEY.md`** - the doctor blocks a `SUMMARY.md` commit when `MONEY.md` isn't regenerated alongside it (staged SUMMARY without staged MONEY = HARD fail).
   - **If this collects a proposal-tracked deal, close its `pricing-outcomes.md` row:** fill `Final` (what actually came in), `Reaction` (how the client responded to the quote), and a one-line `Lesson`. Sanctioned ledger write, same as the proposal skill's open.
8. **Deliver:** present the `.pdf` to Sam (the `.html` is the on-screen copy if the copy buttons help); flag any `‹fill before sending›` fields and the bill-to / from-entity choice. Sending is Sam's call, never the skill's, however clean the checks came back. Note `outputs/invoices/` is gitignored by design (issued invoices carry the live wire block) - keep the archive outside git, in whatever drive folder holds issued invoices.

9. **On collection (the step that closes the loop):**
   - Record the payment date as `**PAID YYYY-MM-DD**` in the Status cell of `SUMMARY.md`, of `INVOICE-LEDGER.md`, and of the per-invoice record. The date must sit **immediately after** the `PAID` token. That anchor is what `scripts/money` parses, and an audit note in parentheses is not a payment date.
   - Strike the receivable's `**Due:**` line with the outcome (`~~**Due:** ...~~ PAID YYYY-MM-DD`). Never delete it.
   - Update the `## Cash status` lines in `SUMMARY.md` (Collected and Outstanding), then run `scripts/money`. It cross-checks both totals against the register and refuses to write if they disagree.
   - Close the `pricing-outcomes.md` row per step 7 if this collects a proposal-tracked deal.
   - A reissue for the records can regenerate with `"status": "Paid"`.

## Data JSON schema

```json
{
  "invoiceNumber": "NL-2026-004",
  "status": "Sent",
  "dateIssued": "25 July 2026",
  "dueDate": "31 July 2026",
  "terms": "End-of-month payrun",
  "currency": "USD",
  "from": { "name": "Rivera Holdings LLC (dba Northwind Labs)", "lines": ["‹registered address, from PAYMENT-DETAILS.md›"], "email": "sam@northwindlabs.example" },
  "billTo": { "name": "Acme Retail", "email": "ap@acmeretail.example", "lines": ["Accounts payable"] },
  "lineItems": [ { "title": "…", "detail": "optional second line", "amount": "2,500.00" } ],
  "subtotal": "2,500.00",
  "tax": "0.00",
  "total": "$2,500.00",
  "schedule": {
    "rows": [ { "label": "1 of 3", "period": "End of July 2026", "status": "This invoice", "amount": "2,500.00", "current": true } ],
    "contractTotal": "7,500.00",
    "note": "optional paragraph under the table"
  },
  "paymentIntro": "Payable by international wire transfer in USD. Quote reference **NL-2026-004** on the payment.",
  "paymentTable": [ { "label": "Bank name", "value": "‹from PAYMENT-DETAILS.md›" }, { "label": "Bank address", "value": "‹from PAYMENT-DETAILS.md›", "multiline": true }, { "label": "Account number", "value": "‹from PAYMENT-DETAILS.md›", "mono": true }, { "label": "Payment reference", "value": "NL-2026-004", "mono": true, "strong": true } ],
  "notes": ["optional bullets under the wire table"],
  "closingNote": "Thank you for the work.",
  "signName": "Sam Rivera",
  "signTitle": "Founder, Northwind Labs"
}
```

Amounts are pre-formatted strings: body amounts without the `$` (line items, subtotal, tax, schedule), the `total` with it. `**bold**` inside `paymentIntro`, `notes`, `detail`, and `closingNote` renders as dark emphasis. `schedule`, `notes`, `billTo.email`, `tax`, `currency`, `status`, `closingNote`, `signName`, `signTitle` are optional; sensible defaults apply. Three more overridable defaults never appear in a minimal JSON but DO print on every invoice, so review them as client-facing copy: `payableByNote` (defaults to "Payable by <dueDate>"), `footerLeft` (defaults to "Rivera Holdings LLC · dba Northwind Labs"), and `schedule.heading` (defaults to "Instalment schedule"). `tagline` renders nothing unless data provides one: slogan copy does not belong on a document whose job is to state a number, so it is opt-in and never a default. US Letter, 0.6in margin, running footer on every page. `assets/doc-page.js` is a vendored scaffold inlined verbatim into the `.html` (its comments carry em dashes; it regenerates from upstream, never hand-edit it). `assets/logo.png` ships as a neutral placeholder mark - swap in your own and the wordmark text in the generator's header block.

## Local-run caveat
Authored to run locally, on a real machine. Requirements for the standard path: node (runs the generator), Google Chrome or Chromium (PDF printing; default macOS and Linux install paths are searched, `CHROME_BIN` overrides), and poppler for `scripts/pdf-check` (`brew install poppler` on macOS, `apt install poppler-utils` on Debian/Ubuntu). No `npm install` is needed for this path; `npm install docx` (repo root) is only for the legacy docx generator. Assets are bundled in `skills/invoice-creator/assets/`; output goes to `outputs/invoices/`.
