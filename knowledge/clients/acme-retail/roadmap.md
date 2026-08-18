# Acme Retail - inventory sync and ops dashboard

**Owner:** Sam · **Client:** Acme Retail (bill-to: Acme Retail Group) · **Last updated:** 2026-08-04

**This file owns the phase prices for this engagement.** Nothing else in the repo restates them.
Relationship, cadence and standing rules live in `knowledge/clients/acme-retail/README.md`.

**Status 2026-08-04.** Phases 1 and 2 delivered, signed off and paid. The nightly sync has run every
night since 2026-07-18 with two incidents, both below. Phase 3 proposed 2026-08-01, undecided.

## Phases

| Phase | Scope | Price | Status |
|---|---|---|---|
| 1 | Discovery: map both systems, document the weekly reconciliation, name the failure points | $2,500 | Delivered 2026-07-05. Invoiced NL-2026-001, paid |
| 2 | Build: nightly two-way inventory sync, reconciliation report, alerting | $7,500 | Delivered 2026-07-18, signed off. Invoiced NL-2026-002, paid |
| 3 | Ops dashboard: live stock view, exception queue, per-location drilldown | $9,000 | Proposed 2026-08-01. Undecided |

Phase 3's price is a live quote, not an agreement. It moves only through the change rule at the
bottom of this file.

---

## Systems baseline (do not re-derive this)

- **Point of sale.** Cloud, per-till, three stores. REST API behind an OAuth client credential.
  Rate limited, and there is **no bulk stock endpoint**: adjustments post one SKU at a time. That
  single fact is the main constraint on everything built here and everything proposed.
- **Warehouse system.** On-premises, no public API, vendor is not interested in providing one.
  Two access paths, both granted in Phase 1: a CSV export dropped on an SFTP share nightly at
  about 23:40 local, and a read-only SQL view for spot checks.
- **What "two-way" actually means.** Each system is authoritative for one direction and neither is
  authoritative for both.
  - **A: point of sale -> warehouse.** The day's sales, posted as depletions against the warehouse
    ledger.
  - **B: warehouse -> point of sale.** Corrected on-hand per SKU per location, written back to
    the tills.
  - **Ordering is load-bearing.** A must finish before B, or B writes back an on-hand figure that
    does not know about today's sales and every store opens on a wrong number. The job is strictly
    sequential for that reason, which is also why it takes as long as it does.
- **Identity.** The point of sale uses its own internal product ids, the warehouse uses supplier
  SKUs. A mapping table bridges them, seeded in Phase 1 from a spreadsheet the ops lead had been
  maintaining by hand. Anything unmapped lands on an exception list, which today is a CSV attached
  to the morning reconciliation email.
- **Where it runs.** A small VPS we own, not client infrastructure. One cron entry at 00:15, one
  sequential run, logs to disk with 30-day retention. Cost line in
  `knowledge/ops/tools-and-stack.md`.
- **Alerting.** Job failure, non-zero exit, and variance above the agreed threshold route to email
  **and** a chat webhook the ops lead watches. Both, deliberately. A single channel that fails
  quietly is the exact failure Phase 1 found in their old process.
- **Credentials.** SFTP key and point-of-sale client secret live in the password manager under
  named entries. Named here, never valued here, never pasted into a message or an invoice.

---

## 2026-07-05 - Phase 1 delivered: what discovery actually found

Four failure points, ordered by what they cost:

1. **The weekly reconciliation ate most of a day, every week**, and produced a number that was
   already out of date when it finished. The ops lead did it personally.
2. **Counts drifted within about 48 hours of any manual adjustment**, because staff enter an
   adjustment in whichever system they happen to be standing at, and neither system tells the
   other.
3. **Nothing alerted on anything.** Their pre-existing overnight export had been failing for eleven
   days when discovery started. Nobody knew. This is why alerting is not an optional line on
   anything we build for them.
4. **No per-location view existed.** Head office saw a group total; a store manager could not see
   their own on-hand without asking someone. Phase 3's case was written by their own problem, not
   by us, and that is why it is a strong proposal.

Delivered as a written map plus a walkthrough, flat priced, no hourly component. Invoiced the same
week as NL-2026-001.

---

## 2026-07-18 - Phase 2 delivered and signed off

~~**Due:** 2026-07-18 - Acme Phase 2 delivery~~ delivered 2026-07-18, signed off. The ops lead
confirmed in writing the same day.

**Price: ~~$6,750~~ $7,500 after scope was added.** The original quote covered two locations and
the nightly sync with a reconciliation report. Two things went in before any code was written, both
agreed in writing: the alerting layer, added once discovery finding 3 landed, and the third store,
which opened mid-scope. The dead figure is retired in `ai/TOMBSTONES.md`, and this struck occurrence
is the only place in the repo it still appears.

The sequence matters more than the number. Scope moved, the price moved, and the client agreed,
all **before** the build started. A price that moves after work has started is a different and far
worse conversation, and this engagement has never had one.

**What shipped:**

- The sequential nightly job, directions A then B, with a bounded run window.
- The reconciliation report: per SKU, per location, warehouse figure against till figure, variance
  column, emailed each morning with the exception CSV attached.
- Alerting on failure and on variance, to both channels.
- The SKU mapping table plus a one-off import of the ops lead's spreadsheet.
- A runbook: what the job does, what each alert means, what to do when the file is late, how to
  re-run by hand.

**Sign-off** was a live walkthrough of one morning's report against a hand count the ops lead ran in
parallel. That was their idea and it was the right test. Paid as NL-2026-002; cash detail lives in
`knowledge/business/invoices/SUMMARY.md`.

---

## Since go-live: what has actually happened

Two incidents, both caught by the alerting rather than by the client.

- **2026-07-21, late export.** The warehouse file landed at 23:58 instead of the usual 23:40. The
  job started, found no input and exited. The alert fired, the job was re-run by hand at 07:10, and
  the morning report went out about two hours late. Fix shipped 2026-07-22: the job now waits for
  the file inside a bounded retry window and alerts only if it never lands.
- **2026-07-27, mapping break.** 41 SKUs hit the exception list in one night after the warehouse
  renamed a supplier range. Nothing was wrong, the SKUs simply stopped mapping. The ops lead
  cleared them by hand in about an hour. This is the Phase 3 case restated in one night: an
  exception list attached to an email is not a queue, and it costs the champion an hour every time
  a supplier does something ordinary.

Steady state otherwise: warehouse and till on-hand agree on the great majority of SKUs any given
morning, and the residual disagreement is almost entirely the unmapped set rather than sync error.

---

## Open technical risks

Carry these into any Phase 3 conversation. They are why the number is what it is.

1. **The nightly window is the real ceiling.** No bulk stock endpoint means direction B posts one
   SKU at a time under a rate limit. At three stores the run finishes with room to spare. It scales
   with locations and with catalogue size, roughly linearly, and a fourth location is already being
   talked about internally. Named here so nobody says a fourth location is free.
2. **The export is a file, and files are late or wrong.** The bounded retry covers late. It does
   not cover truncated: the export carries no checksum and no row count, so a half-written file is
   indistinguishable from a quiet day. The mitigation is a row-count floor agreed with a human who
   knows their volumes. It is deliberately unbuilt, because a floor set by guessing produces false
   alarms and false alarms train people to ignore alerts, which is worse than no alert.
3. **SKU mapping is manual and has no owner on their side.** Today the ops lead does it because the
   ops lead does everything. It is the single point where the whole system quietly stops being
   correct, and it degrades without failing, which is the worst shape.
4. **One-way boundaries hold only as well as the people do.** Staff can still adjust on-hand
   directly at the till. The sync will overwrite that adjustment overnight, correctly, and to the
   person who typed it that looks like the system eating their work. Phase 1 documented it. It is a
   training problem, not a code problem, and it will come back at least once as a bug report.
5. **There is no client-side staging.** Changes are tested against a copy of the export and a
   point-of-sale sandbox account. The sandbox does not enforce production rate limits, so timing
   bugs are only observable in production. Accepted, stated here so it is not re-discovered as a
   surprise.

---

## Phase 3 - proposed 2026-08-01, undecided

**Price: $9,000.** Live stock view, an exception queue that replaces the emailed CSV, per-location
drilldown. Generated with `skills/proposal-creator`; both of that skill's mandatory gates, the
fresh-context fact-check and the price-attack, ran on 2026-08-01 before it went out. Artifact in
`outputs/proposals/`.

~~**Due:** 2026-08-01 - send the Phase 3 proposal~~ sent 2026-08-01 after both gates passed.

~~**Due:** 2026-08-11~~ **Due:** 2027-09-11 - Acme Phase 3 decision expected (demo commitment, re-dated a year out
so a fresh clone's clock stays quiet; the setup wipe removes this file). If nothing has come back, chase the ops lead
once, in one line, with no new number and no discount attached. Silence from this client has twice
meant workload and has never meant no.

**What Phase 3 needs before a build can start.** All of it is on their side and none of it is in
our control, which is exactly why it is written down before the yes rather than discovered after:

1. **A named owner for SKU mapping who is not the ops lead.** The queue makes the work visible and
   fast. It does not make it somebody's job. If nobody is named, Phase 3 buys a nicer view of a
   problem that still has no owner.
2. **A visibility decision.** Whether a store manager can see other stores' stock is a policy call
   for the owner, not a feature toggle we pick. It changes the drilldown and it is the kind of thing
   that gets raised late and stalls a build.
3. **A hosting decision.** Dashboard on our VPS behind auth, or on their infrastructure. Theirs
   means their patching, their outage and their support path. The quoted number assumes ours. If
   they want theirs, the number changes before work starts.
4. **The row-count floor from risk 2**, agreed with someone who knows their volumes. Without it the
   exception queue inherits the same blind spot the report has today.

**Explicitly not in Phase 3**, and say so plainly if it comes up on the call: purchase-order
automation, supplier feeds, demand forecasting, anything touching their accounting package. Each is
its own phase with its own number.

**No timeline has been given and none should be.** The proposal carries phases and price only. The
settled ruling is the 2026-07-19 row in `ai/DECISIONS.md`: no date reaches a client until it has
been personally verified.

---

## Pricing (USD)

- **Flat per phase, never hourly.** Same reasoning as the sprint row in `ai/DECISIONS.md`
  (2026-07-08): hourly invites scope haggling and caps the upside on work that gets faster with
  reps.
- **One price change in this engagement so far**, the Phase 2 re-price above, and it happened before
  the build started. That is the only shape a change is allowed to take here.
- **Underprice watch.** Phase 3 is the first phase with a user interface, an auth story and an
  ongoing support surface. It is priced above Phase 2 for those reasons and not by feel. If the
  hosting fork lands on their infrastructure, re-price it rather than absorbing the difference
  quietly. Complex work is the work that gets underpriced.
- **Nothing about the Phase 3 number goes into a message before they ask.** No justification
  unasked, per the voice rules in `CLAUDE.md`.
- **Change rule.** A price moves only by: strike the old value here, write the new one with the
  clause explaining what moved, ripple the dead string per
  `knowledge/clients/README.md`, add it to `ai/TOMBSTONES.md`. Same session, every time.

---

## Cross-refs

- Relationship, cadence, standing rules, public-reference gate: `knowledge/clients/acme-retail/README.md`
- Invoice records: `knowledge/business/invoices/NL-2026-001.md`, `knowledge/business/invoices/NL-2026-002.md`
- What was billed and what is outstanding: `knowledge/business/invoices/SUMMARY.md`
- Retired figures: `ai/TOMBSTONES.md`
- Recurring cost lines for the hosting this engagement runs on: `knowledge/ops/tools-and-stack.md`
- Rehearsal before a call or a send: `.claude/agents/client-sim.md`, grounded on this folder
