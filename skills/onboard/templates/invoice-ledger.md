# Invoice ledger - the single source of truth for invoice numbers

> **Read this file before issuing any invoice, every time, in every chat.** The number to use is
> the one in the `NEXT INVOICE NUMBER` block below. Do not compute it, do not derive it from the
> last file you happened to open, and do not remember it from a conversation. Read it here.
> After the invoice is issued, append the row and increment the block by exactly one.

## NEXT INVOICE NUMBER

```
{{PREFIX}}-{{YEAR}}-001
```

*(No invoice issued yet. The first invoice you create is {{PREFIX}}-{{YEAR}}-001.)*

## Numbering protocol

1. **Read this file.** The number is the one in the block above. There is no other source.
2. **Format:** `{{PREFIX}}-{YYYY}-{NNN}`, where `{NNN}` is the global sequence zero-padded to at
   least three digits and `{YYYY}` is the issue year of that specific invoice.
3. **The sequence is global and monotonic. It does not reset each year.** After `{{PREFIX}}-{{YEAR}}-009`
   the next is `{{PREFIX}}-{{YEAR}}-010`. If that one is issued the following year, only the year
   part changes. The number only ever goes up by one.
4. **After issuing:**
   a. Append the row to the **Issued** table below.
   b. Set the `NEXT INVOICE NUMBER` block to current plus one, and update the "Last issued" line.
   c. Write the per-invoice record `{{PREFIX}}-YYYY-NNN.md` in this folder, with its armed `**Due:**` line.
   d. Add the row to `SUMMARY.md`, which is the cash and status register.
   e. Run `scripts/money`.
5. **Never reuse a number.** If an invoice is voided or superseded, keep its row here, mark it
   VOID or SUPERSEDED, wrap the number in `~~` in the `SUMMARY.md` register so the parser skips it
   from the totals, and still advance NEXT.
6. **One invoice, one number.** Do not burn a number on a draft. Allocate only when issuing.
7. **A reissue is not a new invoice.** Correcting a wire block, a typo or a date on an already
   sent invoice keeps the same number and the same amount.

## Issued

| Invoice | Issued | Due | Amount ({{CURRENCY}}) | Bill to | Project | Status |
|---|---|---|---:|---|---|---|

*(Status here is a convenience copy of what `SUMMARY.md` holds. `SUMMARY.md` is the cash
authority and the only file `scripts/money` parses. If the two ever disagree, the register wins.)*
