# knowledge/ - curated, trusted, authoritative

This tree is what the business actually knows. Read from here by default. When anything else in
the repo disagrees with a file in here, this tree wins, subject to the precedence chain in
`CLAUDE.md`.

Two sentences hold the whole distinction:

- **`knowledge/` is state and doctrine.** It is what is true, what was decided, and how the
  work is done. It is written to be re-read for years.
- **`outputs/` is product.** Proposals, invoices, posts, briefs, research runs. Every file in
  it is disposable relative to this tree: delete `outputs/` and the business still knows who
  its clients are, what they were charged, what was decided and why. Delete `knowledge/` and
  the repo is a folder of old PDFs.

So: a session writes deliverables to `outputs/` and facts to `knowledge/`. A number that only
exists in a deliverable is not known by the business yet.

## The map

| Path | Owns |
|---|---|
| `knowledge/memory.md` | The canonical state snapshot. Loaded every session. Pointers, not values. |
| `knowledge/business/` | The business itself: positioning, the offer, pricing history, cash. |
| `knowledge/business/invoices/` | The invoice register, the numbering ledger, one record per issued invoice. |
| `knowledge/clients/` | One folder per client. Scope, phase pricing, delivery record, live status. |
| `knowledge/doctrine/` | Operating principles, plus the slot where a formally adopted external framework lives. |
| `knowledge/ops/` | How the operation runs: tools, costs, the OS roadmap, the daily logbook. |
| `knowledge/pain-points/` | The pain-point bank that feeds outbound, content and discovery questions. |
| `knowledge/research/` | Research that a decision was, or will be, made on. Usually perishable. |
| `knowledge/voice/` | How things are written. The copy rules and the per-channel voice. |

Each subdirectory carries its own `README.md` saying what it owns and what it refuses to hold.
Read that before adding a file to it.

## Authoritative vs generated

Not every file here is hand-written, and the difference matters because editing a generated file
is work that gets erased on the next run.

| File | Kind | Rule |
|---|---|---|
| `knowledge/business/invoices/SUMMARY.md` | authoritative | The cash register. Hand-maintained by `skills/invoice-creator` after issuing. |
| `knowledge/business/MONEY.md` | generated | Written by `scripts/money` from `SUMMARY.md`. Never hand-edit. Regenerate after any register change; `repo-doctor` blocks a register commit that skipped it. |
| `knowledge/business/invoices/INVOICE-LEDGER.md` | authoritative | The numbering authority. Read `NEXT INVOICE NUMBER` here, never guess it. |
| `knowledge/business/operator-business-profile.json` | authoritative, tool-maintained | Updated by `skills/business-profile-creator` through read-and-merge. Never blank-slate rebuilt. |
| `knowledge/ops/logbook/STATS.md` | generated | Recomputed by `skills/daily-log` from the day files. Edit the day files, not the rollup. |
| `knowledge/ops/logbook/days/` and `knowledge/ops/logbook/reviews/` | authoritative, frozen | Once a day is closed, its row is history. Correct forward in a later entry, never rewrite an old one. |
| everything else | authoritative | Hand-curated. Changed when the fact changes. |

The same distinction exists outside this tree: `AGENTS.md`, `GEMINI.md` and the adapter skill
folders are generated views of `CLAUDE.md` plus `ai/AGENT_ROUTES.json`. Same rule, same reason.

## One owner per state fact

A price, a deal stage, a KPI, a status: each lives in exactly one file. Every other file that
needs it links to the owner instead of repeating the value.

This is the rule the rest of the tree is shaped around, and it is not tidiness. A number copied
into four files is four chances to quote a dead price to a client, and the copy that is wrong is
never the one being read. `knowledge/memory.md` is the extreme case: it is loaded every session
and it deliberately carries no figures at all, which `repo-doctor` enforces on its Clients and
Money regions.

When a value changes, the same session does all of it: update the owner, strike or banner every
live-sounding restatement found by grepping the dead value, and add that dead string to
`ai/TOMBSTONES.md` so it cannot come back un-bannered.

## Conventions every file in here follows

- **Status banners.** A superseded file gets a bolded `SUPERSEDED - see <path>` line at the top.
  A superseded number gets ~~struck through~~ in place. A file that dies with no successor gets
  `**DEAD - <why>**` at the top, in the same session its owner file rules it dead. Never leave a
  stale claim sounding current.
- **`**Stale after:** YYYY-MM-DD`** near the top of anything perishable: web-sourced pricing,
  platform limits, vendor comparisons, eligibility research. `repo-doctor` flags an expired page
  so the staleness announces itself. Re-verify or supersede it, do not just push the date out.
- **`**Due:** YYYY-MM-DD - <what happens>`** in the file that owns the commitment, and only
  there. `scripts/horizon` reads these and is the OS's clock. Resolve one by striking it through
  with the outcome, never by deleting it. A deadline written as prose is invisible to the clock,
  and so is one parked in a table column.
- **No em dashes.** Comma, period, or a single hyphen. The rule and its enforcement live in
  `knowledge/voice/copy-rules.md`.
- **A file name starting with `extracted-`** means the content was machine-extracted from `raw/`
  rather than hand-curated. It is usable context at lower trust, and curated content wins any
  conflict with it.

## What does not belong in here

- **Deliverables.** A proposal, an invoice PDF, a post, a brief: those are `outputs/`.
- **Unprocessed input.** Exports, transcripts, third-party documents: `raw/`, which is
  quarantined and is not treated as truth until a session distils it into here.
- **Secrets.** Bank and wire values exist only in the gitignored
  `knowledge/business/invoices/PAYMENT-DETAILS.md`. The committed
  `knowledge/business/invoices/PAYMENT-DETAILS.template.md` is the placeholder scaffold. A
  committed file may cite the local-only path; it may never restate its contents. Provider API
  keys live only in the gitignored root env file.
- **Personal material.** Tax paperwork, statements, banking notes: `personal/`, gitignored.
- **Inferences dressed as state.** A write into this tree records something the operator
  actually said or a source file actually shows. A plausible guess written in the present tense
  becomes a fact nobody remembers inventing.

## Who may write here

Sessions update curated knowledge as facts change, without asking first. Two limits: the write
records something real (see the last bullet above), and a canonical rewrite of
`knowledge/memory.md` or any reorganization of this tree is Tier-2 work that runs `/hard-task`
first.

Skills carry narrower, explicit licences: the profile JSON, the invoice ledger plus `SUMMARY.md`
plus per-invoice records, `knowledge/business/pricing-outcomes.md`, and the five logbook paths.
That set is listed in `CLAUDE.md` and it is a ceiling, not a starting point.

A session that wrote into this tree ends with a commit and a push. Git is the audit trail for
the repo that is the business.
