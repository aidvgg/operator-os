# Pricing outcomes: the calibration ledger

One row per quote. Opened by `skills/proposal-creator` on send, closed by `skills/invoice-creator`
on collection. Both writes are sanctioned; nothing else in `knowledge/` is, for these skills.

**What this file is for.** So `.claude/agents/price-attack.md` can argue from Sam's own record
instead of from doctrine. A general claim that solo operators underprice is a hunch. Four rows
showing what was quoted, what the buyer actually said, and what came in, is evidence.

**No time-tracking columns, by design.** A solo operator never back-fills hours honestly. The job
of this file is price-versus-reaction calibration, not utilisation.

**These figures are history, not prices.** Every number in the table below is a record of what
was said on a date. None of it is quotable. Live prices come from the authority every time:
`knowledge/business/outbound-offer.md` for the productized offer,
`knowledge/clients/<client>/roadmap.md` for a client engagement. If a row's number and the
authority disagree, the authority is right and the row is just old.

---

## Append format

Append a new row at the bottom. Never reorder, never rewrite a closed row to make the record look
better than it was.

```
| YYYY-MM-DD | <client> + short scope | <what was quoted> | <what they said, verbatim where possible> | <what came in> | <one line, transferable> |
```

- **Date** - the send date, not the drafting date.
- **Deal** - client plus enough scope that a stranger can tell the rows apart.
- **Quoted** - the number that actually left. If it changed mid-negotiation, say so, and put the
  retired figure in `ai/TOMBSTONES.md` rather than re-typing it here.
- **Reaction** - what the buyer said. Their words beat your summary of their words.
- **Final** - what was collected, with the date. `-` while the row is open.
- **Lesson** - one line, and only if it transfers to the next quote. `-` is an honest answer.

An open row has `pending` in Reaction and `-` in Final and Lesson. It stays open until the money
lands or the deal dies. A row that dies gets `lost` in Final and the reason in Lesson, because a
loss is the more useful half of a calibration record.

---

## Ledger

| Date | Deal | Quoted | Reaction | Final | Lesson |
|---|---|---|---|---|---|
| 2026-07-01 | Acme Retail, inventory-sync Phase 1 discovery (map both systems, document the reconciliation, name the failure points) | $2,500 | accepted same day, no pushback, asked only when it could start | $2,500, collected 2026-07-10 | a small paid discovery clears without a negotiation. Free would have cost the same two weeks and bought no commitment |
| 2026-07-07 | Acme Retail, inventory-sync Phase 2 build (nightly two-way sync, reconciliation report, alerting) | first number superseded before the build started; the retired string is in `ai/TOMBSTONES.md` and is deliberately not re-typed here. Final number below | two additions went in before any code was written, both agreed in writing: the alerting layer after a discovery finding, and a third store that opened mid-scope. Re-quoted on the spot. No pushback on the higher number | $7,500, collected 2026-07-28 | re-quote when scope moves, and do it before the build starts. Absorbing it would have been a discount nobody asked for and a precedent on the next phase. A price that moves after work has begun is a different and much worse conversation |
| 2026-07-24 | Beacon Health, intake scoping diagnostic (two systems, re-typed patient intake) | $1,500 | agreed 2026-07-27. Asked for net 30, held net 14, they took it without a second message | $1,500 invoiced 2026-07-31, open at time of writing | the paid diagnostic is the qualifier. They negotiated terms, not price, which is what a committed buyer does. It also means the first money conversation happened before the build conversation |
| 2026-08-01 | Acme Retail, Phase 3 ops dashboard (live stock view, exception queue, per-location drilldown) | $9,000 | pending | - | - |

One row is open (Phase 3). The decision date on it is owned by
`knowledge/clients/acme-retail/roadmap.md`, not by this file, so the clock lives there and this
row just says `pending`.

---

## Cross-row calibration

The table is per-quote. This section is the pattern across quotes, which is the thing
`price-attack` cannot see from any single row. It reads the record and rules nothing. Re-check it
whenever a Final lands.

**Finding 1: nobody has pushed back on a number yet.** Four quotes, zero price objections. One
buyer negotiated payment terms and lost. That is either a well-calibrated price or a price that is
too low to be worth arguing about, and four rows cannot tell the difference. It is recorded as an
open question rather than as validation, because reading "no pushback" as "correctly priced" is
how a floor becomes permanent.

**Finding 2: the only number that moved, moved up, and it moved because scope moved.** Phase 2 is
the single re-quote on file and it was driven by discovery output, not by nerve. That is the
behaviour to keep. It is also the only row where the process worked exactly as written: scope
changed, the quote changed, the old figure got tombstoned the same day.

**Finding 3: the productized offer has no row at all.** Zero sprints quoted, zero sold. Every
sprint-price argument is therefore theoretical, and `price-attack` should say so out loud rather
than reasoning from the client-build rows, which are a different shape of work with a different
buyer conversation. The gate that will produce the first sprint row is in
`knowledge/business/outbound-offer.md`.

**Falsifier for this whole section:** the first sprint quote draws a real price objection. That
would mean the client-build calm has nothing to say about the productized motion, and Finding 1's
open question resolves toward "the builds are underpriced and the sprint is not". If it lands
clean too, the read is that the buyer set is simply not price-sensitive at this size, and the raise
rule in `outbound-offer.md` is the thing to fire.
