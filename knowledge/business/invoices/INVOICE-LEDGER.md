# Invoice ledger - the single source of truth for invoice numbers

> **Read this file before issuing any invoice, every time, in every chat.** The number to use is
> the one in the `NEXT INVOICE NUMBER` block below. Do not compute it, do not derive it from the
> last file you happened to open, and do not remember it from a conversation. Read it here.
> After the invoice is issued, append the row and increment the block by exactly one.
>
> This is the mechanism that keeps numbering consistent across a thousand separate sessions that
> share no memory. A guessed number is a duplicate waiting to happen, and a duplicate invoice
> number is the kind of mistake a client notices before you do.

## NEXT INVOICE NUMBER

```
NL-2026-004
```

*(Last issued: NL-2026-003 on 2026-07-31. The next invoice you create is NL-2026-004.)*

## Numbering protocol

1. **Read this file.** The number is the one in the block above. There is no other source.
2. **Format:** `NL-{YYYY}-{NNN}`, where `{NNN}` is the global sequence zero-padded to at least
   three digits and `{YYYY}` is the issue year of that specific invoice.
3. **The sequence is global and monotonic. It does not reset each year.** After `NL-2026-009` the
   next is `NL-2026-010`. If that one is issued in 2027 it is `NL-2027-010`. The number only ever
   goes up by one. Only the year prefix tracks the calendar.
4. **After issuing:**
   a. Append the row to the **Issued** table below.
   b. Set the `NEXT INVOICE NUMBER` block to current plus one, and update the "Last issued" line.
   c. Write the per-invoice record `NL-YYYY-NNN.md` in this folder, with its armed `**Due:**` line.
   d. Add the row to `SUMMARY.md`, which is the cash and status register.
   e. Run `scripts/money`.
5. **Never reuse a number.** If an invoice is voided or superseded, keep its row here, mark it
   VOID or SUPERSEDED, wrap the number in `~~` in the `SUMMARY.md` register so the parser skips it
   from the totals, and still advance NEXT. A number that has left the building is spent.
6. **One invoice, one number.** Do not burn a number on a draft. Allocate only when issuing.
7. **A reissue is not a new invoice.** Correcting a wire block, a typo or a date on an already
   sent invoice keeps the same number and the same amount. Note the reissue in the record file and
   leave NEXT alone.

## Issued

| Invoice | Issued | Due | Amount (USD) | Bill to | Project | Status |
|---|---|---|---:|---|---|---|
| NL-2026-001 | 6 Jul 2026 | 14 Jul 2026 | $2,500.00 | Acme Retail | Inventory-sync Phase 1, discovery and failure-point map | **PAID 2026-07-10** |
| NL-2026-002 | 20 Jul 2026 | 28 Jul 2026 | $7,500.00 | Acme Retail Group | Inventory-sync Phase 2, nightly two-way sync with reconciliation report and alerting | **PAID 2026-07-28** |
| NL-2026-003 | 31 Jul 2026 | 14 Aug 2026 | $1,500.00 | Beacon Health | Intake scoping diagnostic | **OPEN**, sent 31 Jul 2026 |

*(Status here is a convenience copy of what `SUMMARY.md` holds. `SUMMARY.md` is the cash
authority and the only file `scripts/money` parses. If the two ever disagree, the register wins
and this table gets fixed in the same session.)*

## Notes on the numbering that exist because they bit somebody

- **The bill-to name can drift and the number cannot.** Invoices 001 and 002 are the same payer
  under two spellings, "Acme Retail" and "Acme Retail Group", because that is what their accounts
  payable asked for on the second one. `scripts/money` collapses both to one owner through its
  alias map so the concentration figure stays honest. Two spellings must never look like two
  clients.
- **Update the ledger in the same session you send.** An invoice sent on Tuesday and a ledger
  updated on Thursday means the ledger advertised a free number for two days that was not free.
  That is exactly the reuse this file exists to prevent, and it is easy to do while feeling
  organised.
