# {{BUSINESS}} - canonical memory

## What this file is

The first file every session reads, and the only one loaded whether or not the task needs it.
Three rules hold here that hold nowhere else.

- **It names where a fact lives. It does not restate the fact.** Prices, cash figures and deal
  amounts live in the file that owns them. `repo-doctor`'s `core-restatement` check reads the
  Clients and Money regions below and flags any currency figure inside either one.
- **It stays bounded.** `core-bloat` nags when the file crosses its byte floor or a line runs
  long. When a section grows a narrative, the narrative moves to its topic file and a one-line
  pointer stays behind.
- **It owns no commitments.** A `**Due:**` line lives in the file that owns the thing being
  promised, so `scripts/horizon` reports it once.

Precedence: `CLAUDE.md` -> this file -> topic files -> everything else. A dated update beats an
undated claim from a higher tier, and an `ai/DECISIONS.md` row beats any restatement of it
elsewhere.

## Who / what

{{FULL_NAME}}, sole operator of {{BUSINESS}}{{ENTITY_CLAUSE}}. {{WHAT_YOU_SELL}}
Sells to: {{WHO_YOU_SELL_TO}}

Positioning, promise and the words used to say it: `knowledge/business/brand_foundation.md`.
Machine-readable profile: `knowledge/business/operator-business-profile.json`.

Billing is in {{CURRENCY}}. Timezone: {{TIMEZONE}}.

## Current state

### Motions

{{MOTIONS_BLOCK}}

### Clients

One block per client: status, shape of the work, and the file that owns the detail. No prices
in this region, ever. A price belongs to the client's own file under `knowledge/clients/`.

No clients recorded yet. Add one block here per client as engagements start, and create the
client's folder per `knowledge/clients/README.md`.

### Money

- Cash is computed, never restated here. The register is
  `knowledge/business/invoices/SUMMARY.md`, the generated rollup is
  `knowledge/business/MONEY.md`, invoice numbering is `knowledge/business/invoices/INVOICE-LEDGER.md`.
- How the business charges, in words: {{HOW_YOU_CHARGE}} The numbers themselves live in
  `knowledge/business/outbound-offer.md` (the standard offer) and in each client's roadmap file.
- Bank and wire values exist only in the gitignored
  `knowledge/business/invoices/PAYMENT-DETAILS.md`. Committed files cite that path and never
  restate what is in it.

### Open questions

The live unknowns. Each one names what would close it. A closed question becomes a decision row
or dies; it does not sit here as scenery.

1. TODO(onboard): {{FIRST_NAME}} has not named an open question yet. Replace this line with the
   first real one, or delete it.

## Key people

Solo operation. Client-side contacts are referred to by role rather than by name, so a status
claim cannot rot into a personal fact. A personal name lives in that client's file if it lives
anywhere.

## Where the operating rules live

- `CLAUDE.md` - the contract. Precedence, write licences, the pre-send checklist, voice rules,
  hard-task tiers. Highest tier; nothing here overrides it.
- `ai/DECISIONS.md` - settled rulings, each with a falsifiable prediction and a review date.
  Read before any decision-shaped move.
- `ai/ERRORS.md` - every mistake that reached {{FIRST_NAME}} or a client, one line each, with the
  control that now prevents it.
- `ai/TOMBSTONES.md` - dead values. `repo-doctor` blocks them from reappearing un-bannered.
- `knowledge/voice/copy-rules.md` and `knowledge/voice/channel-voice.md` - how things are
  written, globally and per channel.
- `knowledge/doctrine/principles.md` - the operating principles that survive a change of client.

## Tools and stack

Full inventory and costs: `knowledge/ops/tools-and-stack.md`. The repo's own organs:

- `scripts/horizon` - the clock. Reads `**Due:**` tokens, `Stale after:` lines and decision
  review dates.
- `scripts/money` -> `knowledge/business/MONEY.md` - the cash rollup, generated from the register.
- `scripts/repo-doctor` - the guardrail suite. Pre-commit on the staged set, pre-push across
  every commit in the transferred range.
- `scripts/backup-sensitive` and `scripts/weekly-backup` - encrypted backup of the local-only set.
- `scripts/morning-brief` - assembles the workday brief on a schedule. Read-only, seeds no tasks.
- `scripts/x-fetch`, `scripts/li-fetch`, `scripts/reddit-scan` - read-only fetch tools. Their
  keys live in the gitignored provider key file at the repo root that no AI tool may read.
- Daily operating ledger: `knowledge/ops/logbook/` (`LOGBOOK.md` cursor, `STATS.md` rollup,
  `HABITS.md`). Plan, log and retro run through `skills/daily-log`.

## On the horizon

- TODO(onboard): nothing recorded yet. Add the next one or two things that matter, each pointing
  at the file that owns its date.
- Improvement direction for the OS itself: `knowledge/ops/os-roadmap.md`.
