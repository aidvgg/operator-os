# Invoice register - the cash and status authority

> **This table is the only cash authority in the repo.** `scripts/money` parses it and writes
> `knowledge/business/MONEY.md`, which holds every computed figure: run-rate, cash floor gate,
> concentration. Nothing is computed by hand here and nothing computed there is copied back.
>
> Numbering lives in `INVOICE-LEDGER.md`. To issue a new invoice, read the next number there.
> Never guess one.

## Register

| # | Invoice | Date issued | Due | Amount (USD) | Bill to | Project | Status |
|---|---|---|---|---:|---|---|---|
| 1 | NL-2026-001 | 6 Jul 2026 | 14 Jul 2026 | $2,500 | Acme Retail | Inventory-sync Phase 1, discovery | **PAID 2026-07-10** |
| 2 | NL-2026-002 | 20 Jul 2026 | 28 Jul 2026 | $7,500 | Acme Retail Group | Inventory-sync Phase 2, build | **PAID 2026-07-28** |
| 3 | NL-2026-003 | 31 Jul 2026 | 14 Aug 2026 | $1,500 | Beacon Health | Intake scoping diagnostic | **OPEN**, sent 31 Jul 2026 |

Register rules the parser depends on, so a row cannot be written wrong quietly:

- Paid means a bold `**PAID YYYY-MM-DD**` in the Status cell, date immediately after the token.
  An audit note in parentheses is not a payment date.
- A voided or superseded invoice keeps its row, with the Invoice cell wrapped in `~~`. The parser
  skips struck rows, so the history stays readable and the totals stay right.
- The `Due` column is for humans. It is invisible to `scripts/horizon`. The chase lives in the
  Receivable clock section below and in the invoice's own record file.

## Cash status (updated 2026-08-01)

- **Collected: $10,000** across NL-2026-001 and NL-2026-002, both cleared to the business bank.
- **Outstanding: $1,500** on NL-2026-003, sent 31 Jul 2026, first payment date 14 Aug 2026.
- Every invoice that has reached its payment date has been paid. NL-2026-003 has not reached one
  yet, so there is no collection history on Beacon Health to read anything into.

`scripts/money` recomputes both figures from the Register and refuses to write `MONEY.md` if they
disagree with the two lines above. That is deliberate duplication: one number stated twice, by a
human and by a parser, and a mismatch means one of them is wrong.

## Receivable clock

Open receivable: NL-2026-003, first payment date 14 Aug 2026. The armed commitment lives in
`NL-2026-003.md`, which owns it.

~~**Due:** 2026-07-28 - NL-2026-002 $7,500 payment due from Acme Retail Group. Confirm receipt or chase.~~ Resolved: paid on the payrun date, cleared, register updated the same day.

**One armed line per receivable, and it lives in the record file.** `scripts/money` refuses to
write `MONEY.md` unless every open row in the Register has an armed `**Due:**` line in that
invoice's own record, so the record file is the owner the machinery already forces. This section
points at it rather than restating it. An armed copy here would be a second owner of one
commitment, `scripts/horizon` would report the same payment twice, and the day the cash lands you
would have two lines to strike and one of them would get missed. That is the one-owner rule doing
real work, not bookkeeping.

The struck line above stays because a resolved commitment is history worth keeping, and `horizon`
ignores a struck token.

## Expected near-term cash

- **$1,500**, NL-2026-003, Beacon Health intake scoping diagnostic. First payment date 14 Aug 2026.
  Nothing further is scoped or priced for Beacon Health until the readout, per
  `knowledge/clients/beacon-health/README.md`.
- Acme Retail Phase 3 is proposed and undecided. No invoice exists against it and none should be
  raised before a signed go. The price and the decision date live in
  `knowledge/clients/acme-retail/roadmap.md`, which owns them.

## Concentration

Both collected invoices are the same payer under two spellings. That is one client, one
relationship and one email away from being the entire revenue line, and the two spellings must
never be read as two clients. `scripts/money` collapses them through its owner alias map and prints
the concentration figures in `knowledge/business/MONEY.md`. Read that section before treating this
register as diversified income. The number is not restated here, because a copied number is a
future stale line.
