# Northwind Labs - canonical memory

*(This is the template's worked example, dated 2026-08-04, written so a fresh clone has real
state for every script and skill to run against. Delete the demo facts and write your own.
Keep the shape. The four `###` headings under Current state are load-bearing: `scripts/repo-doctor`
anchors checks on them by exact text. `SETUP.md` walks the rebrand.)*

## What this file is

The first file every session reads, and the only one loaded whether or not the task needs it.
That makes it a read cost paid every single time, so three rules hold here that hold nowhere else.

- **It names where a fact lives. It does not restate the fact.** Prices, cash figures, deal
  amounts and instalment shapes live in the file that owns them. `repo-doctor`'s
  `core-restatement` check reads the Clients and Money regions below and flags any currency
  figure sitting inside either one, because a pointer carrying a number is a second copy of
  that number waiting to go stale.
- **It stays bounded.** `core-bloat` nags when the file crosses its byte floor or a line runs
  long. When a section grows a narrative, the narrative moves to its topic file and a one-line
  pointer stays behind.
- **It owns no commitments.** A `**Due:**` line lives in the file that owns the thing being
  promised, so `scripts/horizon` reports it once and one file is responsible for resolving it.

Precedence: `CLAUDE.md` -> this file -> topic files -> everything else. A dated update beats an
undated claim from a higher tier, and an `ai/DECISIONS.md` row beats any restatement of it
elsewhere. When either exception fires, fix the higher tier in the same session.

## Who / what

Sam Rivera (they/them), sole operator of Northwind Labs, operating under Rivera Holdings LLC.
Remote. No staff, no contractors, no co-founder.

Northwind builds internal tools, data plumbing and automations for small and mid-size
businesses. The work starts where two systems a business already pays for refuse to talk to
each other and somebody is closing the gap by hand every week. The thing sold is the removed
manual process, never "AI" as a category. Positioning, promise and the words used to say it:
`knowledge/business/brand_foundation.md`. Machine-readable profile:
`knowledge/business/operator-business-profile.json`.

Billing is USD through Rivera Holdings LLC.

## Current state

### Motions

Three, listed in the order they were started.

1. **Client builds.** Phased and fixed-price, discovery always first. **This is the motion that
   pays today**: every dollar collected so far came from it. Phase scope and phase pricing are
   owned per client under `knowledge/clients/`.
2. **Content-driven outbound.** X and LinkedIn. Manual sourcing, manual sends, no tooling.
   Ruled 2026-07-26 (`ai/DECISIONS.md`): the motion stays manual until 30 real conversations
   are logged, because automating a motion nobody has proven by hand only scales the mistake.
   Account-safety envelope: `knowledge/business/linkedin-safety-rules.md`. The qualification
   ladder the briefs apply: `outputs/outbound/prospect-gate.md`.
3. **Productized retainer, the Ops Automation Sprint.** Newest. Two weeks, one integration or
   one manual process removed, delivered working with a runbook, optional care retainer after.
   Not yet a meaningful share of income. Offer, price and the flat-price ruling live in
   `knowledge/business/outbound-offer.md`, which is the pricing authority for this motion.

The intended chain is 2 feeds 3, and 3 becomes the front door to 1. That is the plan, not the
evidence: no sprint has yet been sold to someone who arrived cold.

### Clients

One block per client: status, shape of the work, and the file that owns the detail. No prices
in this region, ever. A price belongs to the client's own file.

**Acme Retail - ACTIVE, delivering.** A 40-person multi-location retailer. Their point-of-sale
and their warehouse system do not talk, so stock counts are reconciled by hand every week.
Phase 1 (discovery: map both systems, document the reconciliation, name the failure points) and
Phase 2 (nightly two-way inventory sync with a reconciliation report and alerting) are
delivered, signed off and paid. Phase 3 (ops dashboard: live stock view, exception queue,
per-location drilldown) was proposed 2026-08-01 and sits with them. Decision expected
2027-09-11 (demo date); the `**Due:**` line that chases it belongs to the roadmap, not here. Scope, phase
history and current phase pricing: `knowledge/clients/acme-retail/roadmap.md`. The working
contact is the ops lead; the owner signs.

**Beacon Health - SCOPING.** A 12-person allied-health clinic group. Every patient intake is
typed once into the practice-management system and again into the billing system, because the two
do not integrate. A paid scoping diagnostic was delivered and invoiced 2026-07-31; the readout
call is 2027-09-08 (demo date). Nothing built, nothing scoped or priced beyond the diagnostic. Owner file:
`knowledge/clients/beacon-health/README.md`.

**Ridgeline Freight - PROSPECT, not a client.** Present only as the worked outbound example.
No engagement, no quote, no relationship. Named here so nobody promotes it by accident.

### Money

This region routes. It holds no figure.

- **Cash position** (collected, outstanding, trailing run-rate, concentration share, monthly
  fixed burn): `knowledge/business/MONEY.md`, generated by `scripts/money`. Never hand-edited.
  Regenerate it after any register change; the doctor blocks a register commit that skipped it.
- **The register** is `knowledge/business/invoices/SUMMARY.md`. It is the authority on what was
  issued and what cleared. `MONEY.md` is derived from it, so the two disagreeing means the
  rollup is stale, not that the register is wrong.
- **Invoice numbering** is owned by `knowledge/business/invoices/INVOICE-LEDGER.md`. Read the
  `NEXT INVOICE NUMBER` there, use it, increment after issuing. Never guess a number.
- **Targets** (monthly recurring, cash buffer) are constants at the top of `scripts/money` and
  print at the bottom of `MONEY.md` with the gap to each. Changing a target is a code edit on
  purpose, so it has to be a decision rather than a mood.
- **Cost base**: the fixed monthly line items are owned by `knowledge/ops/tools-and-stack.md`
  and mirrored into `scripts/money` with a citation next to each one. A new subscription is
  added there first, then mirrored.
- **Outstanding**: one invoice is open. Its amount and status are owned by
  `knowledge/business/invoices/SUMMARY.md`; the armed chase line is owned by that invoice's own
  record file in the same folder, which is where `scripts/money` requires it.
- **Concentration is the live risk.** All collected revenue to date traces to a single client.
  `scripts/money` computes the share and prints it. The fix is not a better spreadsheet, it is
  motion 2 and motion 3 producing a second paying logo. Any month where that share does not
  fall is a bad month regardless of the total.
- Bank and wire values exist only in the gitignored
  `knowledge/business/invoices/PAYMENT-DETAILS.md`. Committed files cite that path and never
  restate what is in it.

### Open questions

The live unknowns. Each one names what would close it. A closed question becomes a decision row
or dies; it does not sit here as scenery.

1. **Does Acme Phase 3 close, and does the account survive if it does not?** Phases 1 and 2 both
   closed within a week of proposal, both under a buyer with no alternative use for the budget.
   Phase 3 is the first one that competes with something else. Resolves on the 2027-09-11
   decision tracked in the Acme roadmap. If it slips past the chase, the real question is
   whether the account is finished, not whether the proposal was wrong.
2. **Is the Ops Automation Sprint priced right, and can it be sold cold?** Nobody outside a warm
   conversation has bought one. Two independent resolvers: three logged quote outcomes in
   `knowledge/business/pricing-outcomes.md`, and one sprint sold to a prospect who arrived
   through motion 2 rather than a referral. Until both, the price is a guess with a decision row
   attached.
3. **Does manual outbound produce conversations at a rate worth keeping?** The 2026-07-26 ruling
   holds the motion manual to 30 logged conversations, which makes the count the instrument.
   Resolves at 30: either the conversation-to-call rate justifies tooling, or the offer is wrong
   and tooling would have scaled the wrong offer faster. Running count:
   `knowledge/ops/logbook/STATS.md`.

## Key people

Solo operation. No staff, no partner, no equity holder. Client-side contacts are referred to by
role rather than by name, so a status claim cannot rot into a personal fact: the ops lead at
Acme Retail, the practice manager at Beacon Health. A personal name lives in that client's file
if it lives anywhere.

## Where the operating rules live

- `CLAUDE.md` - the contract. Precedence, write licences, the pre-send checklist, voice rules,
  hard-task tiers. Highest tier; nothing here overrides it.
- `ai/DECISIONS.md` - settled rulings, each with a falsifiable prediction and a review date.
  Read before any decision-shaped move. Settled rulings are not re-argued session by session.
- `ai/ERRORS.md` - every mistake that reached Sam or a client, one line each, with the control
  that now prevents it. A new rule or check has to trace to a row here or to a hazard named in
  that file. No speculative process.
- `ai/TOMBSTONES.md` - dead values. `repo-doctor` blocks them from reappearing un-bannered.
- `knowledge/voice/copy-rules.md` and `knowledge/voice/channel-voice.md` - how things are
  written, globally and per channel.
- `knowledge/doctrine/principles.md` - the operating principles that survive a change of client.
  `knowledge/doctrine/README.md` holds the adoption checklist for any external framework.

## Tools and stack

Full inventory, costs and account notes: `knowledge/ops/tools-and-stack.md`. The repo's own
organs, so a session knows what it is allowed to run:

- `scripts/horizon` - the clock. Reads `**Due:**` tokens, `Stale after:` lines and decision
  review dates. Runs at session start and inside `/plan` and `/weekly`.
- `scripts/money` -> `knowledge/business/MONEY.md` - the cash rollup, generated from the register.
- `scripts/repo-doctor` - the guardrail suite. Pre-commit on the staged set, pre-push across
  every commit in the transferred range.
- `scripts/backup-sensitive` and `scripts/weekly-backup` - encrypted backup of the local-only
  set, on a schedule, with a nag when the last backup gets old.
- `scripts/morning-brief` - assembles the workday brief on a schedule. Read-only, seeds no tasks.
- `scripts/x-fetch`, `scripts/li-fetch`, `scripts/reddit-scan` - the read rails onto the outside
  world. Provider-side, so no operator account is ever the actor. Their keys live in the
  gitignored root env file that no AI tool may read; agents call the scripts, never the file.
- Daily operating ledger: `knowledge/ops/logbook/` (`LOGBOOK.md` cursor, one row per day,
  `STATS.md` rollup, `HABITS.md`). Plan, log and retro run through `skills/daily-log`. It is the
  accountability and stats layer, not a capture inbox.

## On the horizon

- Beacon Health readout, then a fork: scoped build, one sprint, or nothing. Owner file carries
  the date.
- Acme Phase 3 decision, then either a fourth phase or a closed account. Owner file carries the
  date.
- A second paying client is the only structural fix for concentration. Everything else is
  comfort.
- Improvement direction for the OS itself, including the guardrail-fixture suite that tests
  whether the checks still fire: `knowledge/ops/os-roadmap.md`. Nothing there is deadline-armed.
