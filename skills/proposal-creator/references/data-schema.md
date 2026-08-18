# Proposal Data Schema

Both generators read this schema: `generate-proposal-html.js` (the 2026-08-02 design standard,
HTML rendered to PDF - the default) and the legacy `generate-proposal.js` (docx, superseded as
the standard, kept for editable-docx requests). All fields marked **required** must be present.
Optional fields can be omitted. The design-standard generator adds the optional fields in the
"2026-08-02 design-standard fields" section below; the legacy docx generator ignores them.

## The examples are billed to nobody, on purpose

Every example on this page names **Kestrel Wholesale**, which is not a client. It has no folder
under `knowledge/clients/`, no roadmap, and no row in the invoice ledger, and it never gets one.
That absence is the control. A schema illustration written against a real client ends up holding a
second price for an engagement that already has an owner file, and then the repo states two numbers
for one deal with no rule saying which is real. An illustration that owns nothing cannot contradict
anything, so the numbers below can never rot.

So: never put a live client's name in an example on this page, and never quote a number from this
page at a client. Pricing authority is `knowledge/business/outbound-offer.md` for the outbound offer
and the client's own roadmap file under `knowledge/clients/` for a client engagement.

The two examples are two engagements for that one illustration, a build and then a retainer. The
build example is the same document the design standard renders
(`design-standard-2026-08-02.dc.html`), with the same scope and the same figures, so you can read
the input here and see the output there.

## Full Schema

```json
{
  "clientName": "REQUIRED - Client/company name (e.g., 'Kestrel Wholesale')",
  "projectTitle": "REQUIRED - Short title shown under company name on cover (e.g., '12-Month Ops Automation Retainer')",
  "projectDescription": "REQUIRED - Longer project line in meta section (e.g., 'Ops automation and reporting upkeep, 12-month retainer')",
  "date": "REQUIRED - Proposal date (e.g., '24 Jul 2026')",
  "sentBy": "Sender name; the design-standard generator defaults it to 'Sam Rivera', the legacy docx generator requires it",
  "contactEmail": "Optional - Contact email for footer link (default: 'sam@northwindlabs.example')",
  "proposalType": "Optional - 'Project Proposal', 'Service Retainer Proposal', or 'Infrastructure Build Proposal'. Design-standard generator: renders uppercase in the cover kicker, default 'Project proposal' - set it explicitly on anything that is not a project build. Legacy docx generator: footer descriptor, default 'Service Retainer Proposal'",

  "overview": "REQUIRED - Main overview paragraph text",
  "overviewExtra": "Optional - Second overview paragraph",

  "scopeSections": [
    {
      "title": "REQUIRED - Sub-section heading (e.g., 'Inventory sync')",
      "services": [
        {
          "service": "REQUIRED - Service name for left column",
          "description": "REQUIRED - Service description for right column"
        }
      ]
    }
  ],

  "investment": {
    "lineItems": [
      {
        "description": "REQUIRED - Line item description",
        "amount": "REQUIRED - Amount string (e.g., '$2,000')",
        "bold": false
      }
    ],
    "note": "Optional - Note below table (e.g., 'All amounts are in US Dollars...')"
  },

  "whatThisCovers": [
    "Optional - Array of strings for the 'What This Covers' bullet list"
  ],

  "additionalWork": "Optional - Paragraph text for 'Additional Work' section",

  "paymentTerms": [
    "Optional - Array of numbered payment terms. Plain strings, or (design-standard generator) { \"text\": \"Due at project kick-off\", \"amount\": \"$13,000\" } objects - any amount in the list adds the design's right-aligned mono amount column"
  ],

  "termsAndConditions": [
    "Optional - Array of strings for bulleted terms"
  ],

  "customSections": [
    {
      "heading": "REQUIRED - Section heading text (e.g., 'TIMELINE')",
      "content": "String for paragraph OR Array of strings for bullets",
      "table": {
        "headers": ["Col1 Header", "Col2 Header"],
        "rows": [["col1", "col2"]],
        "col1Width": 3000
      }
    }
  ],

  "scopeTrace": [
    {
      "line": "Optional to the generator, expected by the skill - the scope line as the client reads it",
      "origin": "Where it came from: 'asked by client YYYY-MM-DD' / 'Sam added YYYY-MM-DD' / 'already live, not billable'. A client ask that Sam then extended is written 'asked by client YYYY-MM-DD, extended by Sam' so the mixed case is visible instead of being rounded to whichever half is more flattering.",
      "evidence": "Required. Where that origin is RECORDED, as a stable anchor: the owning file plus a section heading plus a quoted fragment. Never a bare line number: line numbers in the client files move within days, and nothing in the repo validates them, so a trace anchored to `file:114` reads green while pointing at unrelated text."
    }
  ]
}
```

## 2026-08-02 design-standard fields (HTML generator only, all optional)

```json
{
  "clientEntity": "Legal entity for the footer confidence line and the acceptance block (default: clientName). Entities differ PER ENGAGEMENT, not per client: check the invoice ledger and the engagement's own bill-to record before naming one, because the same contact can sign one piece of work personally and bill another through a company. When the contracting party is unclear, omit the field - the plain client name is always safe.",
  "coverTitle": "The big Space Grotesk cover sentence, with period (default: projectTitle)",
  "coverLede": "Paragraph under the cover title (default: projectDescription)",
  "projectTag": "Right side of the running header, rendered uppercase (default: '<clientName> · <projectTitle>')",
  "engagement": "Meta-strip cell (default: 'Fixed scope, fixed price')",
  "totalInvestment": "Meta-strip cell (default: derived from the bold investment line item + ' USD')",
  "meta": { "preparedFor": "Meta-strip override (default: clientEntity)" },
  "confidential": "false suppresses the footer confidence line (default true)",
  "confidentialLine": "Footer-left override (default: '<clientEntity> · Commercial in confidence')",
  "footerRight": "Footer-right override (default: 'Northwind Labs · operating under Rivera Holdings LLC')",
  "outOfScope": [ { "item": "Named exclusion", "note": "Why it is excluded / where it lives instead" } ],
  "additionalWork": "With outOfScope present, renders as the intro paragraph of an 'Out of scope' section; alone, renders as its own 'Additional work' section",
  "acceptanceText": "Acceptance intro override",
  "closingNote": "Closing contact line override",
  "accent": "Accent hex (default '#e89b5c'; design options: '#e89b5c', '#d97757', '#2a241d')",
  "density": "compact | standard | relaxed (body-size scale 0.94 / 1 / 1.06)",
  "pageBreaks": ["scope", "investment", "acceptance", "custom:SEQUENCING"],
  "_provenance": "Free-text note about what the file is; never rendered"
}
```

CLI flags: `--paper letter|a4` (default letter), `--html-only` (skip the Chrome PDF step),
`--chrome <path>` (Chrome binary override; `CHROME_BIN` env also works).

`pageBreaks` keys: `overview`, `scope`, `investment`, `covers`, `outofscope`, `additional`,
`terms`, `acceptance`, plus `custom:<HEADING>` for any custom section (heading as written in the
JSON). The default is `["scope", "investment", "acceptance"]`.

Copy rules: no em dashes, no en dashes anywhere in the data strings
(`knowledge/voice/copy-rules.md`); write ranges as `15-30%`. The generator warns per offending
string and the warning is a defect to fix, not to ship.

### Required custom section: DEFINITION OF DONE

`customSections` is optional as a container, but one entry inside it is **required on every
proposal**: `"heading": "DEFINITION OF DONE"`. Use the two-column table form so phased work
reads one row per phase.

```json
{
  "heading": "DEFINITION OF DONE",
  "table": {
    "headers": ["Phase", "Deliverables and acceptance"],
    "rows": [
      [
        "Phase 1 - Inventory sync",
        "Deliverables: both connectors, the one-off backfill, the scheduled sync, conflict rules and run alerting. Accepted when your team changes stock in either system on ten SKUs of their choosing and both systems agree within one sync window, with no spreadsheet step and no Northwind Labs access at any point."
      ]
    ],
    "col1Width": 2600
  }
}
```

Every priced phase gets a row. Each row names its deliverables and states an acceptance test the
client could run unaided, on their own systems. "Delivered", "complete" and "handed over" are not
acceptance criteria.

No generator change is needed: both generators render `customSections` headings, tables and
`col1Width` (the design-standard generator converts `col1Width` DXA to a column percentage).

### `scopeTrace`: where every scope line came from

The generator reads only the keys documented above, so `scopeTrace` renders nothing into the
deliverable. It is written for the reviewer: `price-attack` is handed this sidecar in fresh context, so
a scope line with no origin, or one marked `already live, not billable` that is still priced,
gets caught by someone who was not in the room when it was drafted. Provenance is the
scope-inflation entry in `ai/ERRORS.md`. The gate itself is in `SKILL.md` under "Scope
discipline".

```json
"scopeTrace": [
  { "line": "Store platform connector", "origin": "asked by client 2026-07-22", "evidence": "call notes 2026-07-22, the ops lead named the connector as the blocker" },
  { "line": "Run health alerting", "origin": "Sam added 2026-07-23", "evidence": "no client ask; proposed because the previous phase shipped with no failure signal" },
  { "line": "Managed database", "origin": "already live, not billable", "evidence": "knowledge/clients/<client>/roadmap.md, section 'Phase 2 delivered and signed off': 'the sequential nightly job'" }
]
```

The `<client>` in that path is a placeholder and stays one. On a real proposal it is the actual
folder, and the heading and the quoted fragment are copied from the file as they stand, so the
anchor can be checked by opening it. It cannot be a real path here, because the example client owns
no folder and a real one would put a live client back on this page. What the example is teaching is
the shape: file, then heading, then the words you are relying on.

## Example: Retainer Proposal

```json
{
  "clientName": "Kestrel Wholesale",
  "projectTitle": "12-Month Ops Automation Retainer",
  "projectDescription": "Ops automation and reporting upkeep, 12-month retainer",
  "date": "28 Jul 2026",
  "sentBy": "Sam Rivera",
  "contactEmail": "sam@northwindlabs.example",
  "proposalType": "Service Retainer Proposal",
  "overview": "This proposal outlines a 12-month retainer covering the automations and internal reporting Northwind Labs runs for Kestrel Wholesale. The engagement covers monitoring, failure triage, small changes, and the monthly reporting pack.",
  "overviewExtra": "All services are delivered by Northwind Labs (operating under Rivera Holdings LLC) on a fixed monthly retainer, billed at the start of each calendar month.",
  "scopeSections": [
    {
      "title": "Automation upkeep",
      "services": [
        { "service": "Run monitoring", "description": "Every scheduled job is watched. Failures raise an alert to your channel and are triaged the same working day." },
        { "service": "Failure triage", "description": "Root cause, fix, and a one-line note in the shared log for every failure, so a repeat is recognised rather than rediscovered." },
        { "service": "Small changes", "description": "Up to 5 hours per month of adjustments to existing automations: new fields, changed schedules, new recipients, changed thresholds." },
        { "service": "Credential rotation", "description": "Scheduled rotation of every API credential the automations hold, with the runbook updated in the same pass." },
        { "service": "Quarterly review", "description": "A short written review each quarter: what ran, what broke, what is worth retiring, and what is worth building next." }
      ]
    },
    {
      "title": "Reporting",
      "services": [
        { "service": "Monthly pack", "description": "The standing report set, generated and delivered in the first three working days of each month." },
        { "service": "Data checks", "description": "Automated checks that each source has fresh data before a report is generated, so a stale feed cannot silently produce a confident wrong number." },
        { "service": "Ad-hoc pulls", "description": "Up to 2 one-off data pulls per month against the existing warehouse tables." },
        { "service": "Access management", "description": "Report access added and removed as your team changes, on your single sign-on." }
      ]
    }
  ],
  "investment": {
    "lineItems": [
      { "description": "Monthly automation upkeep", "amount": "$1,750" },
      { "description": "Monthly reporting", "amount": "$800" },
      { "description": "Monthly retainer total", "amount": "$2,550", "bold": true },
      { "description": "12-month contract total", "amount": "$30,600", "bold": true }
    ],
    "note": "All amounts are in US Dollars (USD). Invoiced monthly at the start of each calendar month. Payment terms: 14 days from invoice date."
  },
  "whatThisCovers": [
    "Monitoring and same-day triage on every scheduled job",
    "Up to 5 hours per month of changes to existing automations",
    "Up to 2 ad-hoc data pulls per month",
    "The monthly reporting pack, delivered in the first 3 working days",
    "Freshness checks on every reporting source",
    "Scheduled credential rotation with runbook updates",
    "A written quarterly review"
  ],
  "additionalWork": "Any work beyond the scope outlined above is quoted separately before commencement. Additional hours beyond the included 5 hours per month are billed at $165 USD per hour.",
  "paymentTerms": [
    "$2,550 USD per month, invoiced at the start of each calendar month",
    "Payment due within 14 days of invoice date",
    "12-month contract term from the effective start date"
  ],
  "termsAndConditions": [
    "Either party may terminate with 30 days' written notice. Early termination does not affect fees already invoiced.",
    "Services are transferable to a new owner or entity upon written notice from the current account holder.",
    "All system credentials are held in your own secret store. Changes to access are coordinated with the designated account contact.",
    "Northwind Labs retains no ownership of client data, content, or delivered systems.",
    "Scope changes or additional services will be quoted and agreed upon in writing before work begins."
  ]
}
```

## Example: Build Proposal

```json
{
  "clientName": "Kestrel Wholesale",
  "projectTitle": "Inventory Sync and Ops Dashboard",
  "projectDescription": "Two-system inventory sync plus an ops dashboard, one-time build",
  "date": "24 Jul 2026",
  "sentBy": "Sam Rivera",
  "proposalType": "Project Proposal",
  "overview": "This proposal covers a scheduled inventory sync between the store platform and the warehouse system, and an ops dashboard built on top of it. Today the two systems are reconciled by hand from CSV exports each morning, and they have drifted again by the time the reconciliation is finished.",
  "overviewExtra": "All work is delivered by Northwind Labs (operating under Rivera Holdings LLC). The infrastructure is yours to own, run, and modify after delivery.",
  "scopeSections": [
    {
      "title": "Inventory sync",
      "services": [
        { "service": "Store platform connector", "description": "Read and write against the store platform's inventory API, with rate limiting, retries and a resume point." },
        { "service": "Warehouse connector", "description": "The same on the warehouse side. SKU mapping is built from your current mapping sheet and then owned by the sync." },
        { "service": "Scheduled sync and backfill", "description": "A run every fifteen minutes plus a one-off backfill. Runs are idempotent, so a re-run after a failure cannot double-count an adjustment." },
        { "service": "Conflict handling", "description": "Rules for the cases that resolve themselves, and an exception queue for the ones a human should judge." },
        { "service": "Run health and alerting", "description": "A failed run, or a run that stops happening at all, raises an alert to a channel you choose." }
      ]
    },
    {
      "title": "Ops dashboard",
      "services": [
        { "service": "Stock and exception views", "description": "Current quantity per SKU across both systems, and the queue of unresolved conflicts with one-click resolution." },
        { "service": "Sync health panel", "description": "Last successful run, current lag, failures in the past day, volume moved." },
        { "service": "Access and export", "description": "Viewer and resolver roles on your existing single sign-on. Every view exports to CSV." },
        { "service": "Handover and runbook", "description": "Written runbook covering deploy, credential rotation, the three failure modes worth naming, and how to pause the sync safely." }
      ]
    }
  ],
  "investment": {
    "lineItems": [
      { "description": "Phase 1, inventory sync", "amount": "$17,000" },
      { "description": "Phase 2, ops dashboard", "amount": "$9,000" },
      { "description": "Project total", "amount": "$26,000", "bold": true }
    ],
    "note": "All amounts are in US Dollars (USD). 50% due at project kick-off, 50% on delivery and sign-off."
  },
  "paymentTerms": [
    { "text": "Due at project kick-off", "amount": "$13,000" },
    { "text": "Due on delivery and sign-off", "amount": "$13,000" }
  ],
  "termsAndConditions": [
    "Client owns all delivered code, configuration, and documentation.",
    "Northwind Labs retains no access to client data or systems after handover unless a retainer is engaged.",
    "The sync does not write to either system until the dry-run diff is approved in writing.",
    "Scope changes will be quoted and agreed upon in writing before work begins.",
    "30-day post-delivery support included for bug fixes and configuration adjustments."
  ],
  "customSections": [
    {
      "heading": "DEFINITION OF DONE",
      "table": {
        "headers": ["Phase", "Deliverables and acceptance"],
        "rows": [
          ["Phase 1 - Inventory sync", "Deliverables: both connectors, the backfill, the fifteen-minute schedule, conflict rules, the exception queue and run alerting. Accepted when your team changes stock in either system on ten SKUs of their choosing and both systems agree within one sync window, with no spreadsheet step, and when a deliberately failed run raises an alert in your channel."],
          ["Phase 2 - Ops dashboard", "Deliverables: stock view, exception queue, sync health panel, two roles on your single sign-on, CSV export, runbook and handover. Accepted when an ops lead who was not in the build resolves a real exception end to end from the dashboard alone, using only the runbook."]
        ],
        "col1Width": 2600
      }
    },
    {
      "heading": "TIMELINE",
      "content": [
        "Week 1: access, credentials, SKU mapping review",
        "Week 2-3: connectors and the sync engine, running in dry run",
        "Week 4: dry-run diff review, backfill, writes enabled",
        "Week 5-6: dashboard build and testing",
        "Week 7: runbook, handover walkthrough",
        "Week 8+: 30-day post-delivery support period"
      ]
    }
  ],
  "scopeTrace": [
    { "line": "Store platform connector", "origin": "asked by client 2026-07-22", "evidence": "knowledge/clients/<client>/roadmap.md, section 'What they asked for': 'stop the morning CSV reconciliation'" },
    { "line": "Run health and alerting", "origin": "Sam added 2026-07-23", "evidence": "knowledge/clients/<client>/roadmap.md, section 'Scope additions': 'a sync that dies quietly is worse than no sync'" }
  ]
}
```

## Legacy docx design specifications (for reference)

These are the formatting specs the legacy `generate-proposal.js` docx generator emits. They
describe the superseded docx house style, not the current PDF standard.

| Element | Font | Size | Color | Notes |
|---------|------|------|-------|-------|
| Body text | Open Sans | 11pt (22 hp) | #000000 | Default |
| Company name | Open Sans Bold | 26pt (52 hp) | #000000 | Cover page |
| Project title | Open Sans | 15pt (30 hp) | #666666 | Cover subtitle |
| Section heading | Open Sans Bold | 16pt (32 hp) | #000000 | With thin divider |
| Sub-heading | Open Sans Bold | 14pt (28 hp) | #434343 | Scope sub-sections |
| Table header | Open Sans Bold | 10.5pt (21 hp) | #ffffff | Background: #2d2d2d |
| Table body | Open Sans | 10.5pt (21 hp) | #000000 | Alt row: #f2f2f2 |
| Signature labels | Open Sans | 9pt (18 hp) | #666666 | Below signature lines |
| Footer text | Open Sans | 11pt (22 hp) | #434343 | Pipe separator text |

Page: US Letter (8.5in x 11in), 1in margins all sides. Table borders: #cccccc single 4px.
