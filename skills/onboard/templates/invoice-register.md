# Invoice register - the cash and status authority

> **This table is the only cash authority in the repo.** `scripts/money` parses it and writes
> `knowledge/business/MONEY.md`, which holds every computed figure. Nothing is computed by hand
> here and nothing computed there is copied back.
>
> Numbering lives in `INVOICE-LEDGER.md`. To issue a new invoice, read the next number there.
> Never guess one.

## Register

| # | Invoice | Date issued | Due | Amount ({{CURRENCY}}) | Bill to | Project | Status |
|---|---|---|---|---:|---|---|---|

Register rules the parser depends on, so a row cannot be written wrong quietly:

- Amounts are written with a `$` sign before the number (`$1,500`); that is the shape
  `scripts/money` reads, whatever currency code the invoice itself shows.
- Paid means a bold `**PAID YYYY-MM-DD**` in the Status cell, date immediately after the token.
- A voided or superseded invoice keeps its row, with the Invoice cell wrapped in `~~`. The parser
  skips struck rows.
- The `Due` column is for humans. It is invisible to `scripts/horizon`. The chase lives in the
  invoice's own record file as an armed `**Due:**` line.

## Cash status (updated {{TODAY}})

- **Collected: $0**. No invoice issued yet.
- **Outstanding: $0**. No open receivable.

`scripts/money` recomputes both figures from the Register and refuses to write `MONEY.md` if they
disagree with the two lines above. Update the two lines in the same edit as any row change.

## Receivable clock

No open receivable. When one exists, its armed `**Due:**` line lives in that invoice's own record
file in this folder, never here. `scripts/money` refuses to write `MONEY.md` unless every open
row in the Register has one.

## Concentration

`scripts/money` computes client concentration into `knowledge/business/MONEY.md` once there are
rows. The number is not restated here.
