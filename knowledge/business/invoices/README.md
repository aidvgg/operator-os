# Invoices - what lives here and who owns what

This folder is the money register. Parts of it are parsed by code, so the formats below are a
contract, not a style preference. Break one and `scripts/money` refuses to write, which blocks the
commit that touched `SUMMARY.md`.

## One owner per fact

| File | Owns | Never holds |
|---|---|---|
| `INVOICE-LEDGER.md` | the next invoice number and the numbering rules | cash totals |
| `SUMMARY.md` | the register: every invoice, its amount, its status, the cash totals | numbering rules |
| `NL-YYYY-NNN.md` | one invoice: what was billed, why, the terms, the armed receivable clock | wire numbers |
| `PAYMENT-DETAILS.template.md` | the placeholder scaffold for the wire block | real values |
| `PAYMENT-DETAILS.md` (local only, gitignored) | the live wire block, read by `skills/invoice-creator` | anything else |
| `knowledge/business/MONEY.md` | the computed rollup: run-rate, floor gate, concentration | hand edits |

The engagement price is owned by the client file (`knowledge/clients/<client>/`), not by anything
here. An invoice record states the amount it billed and points at the file the amount came from.
Re-derive at issue, never recall.

## The flow, end to end

**Issue**

1. Read `INVOICE-LEDGER.md`. Use the number in the `NEXT INVOICE NUMBER` block. Never guess one.
2. Re-derive the amount from the client file. Read the wire block from `PAYMENT-DETAILS.md`.
3. Generate with `skills/invoice-creator`, validate the PDF with `scripts/pdf-check`, run the
   skill's `fact-check` gate. If the amount never went through a proposal, run `price-attack` too:
   billing is the last moment underpricing can be caught.
4. Write the record `NL-YYYY-NNN.md`, append the ledger row, bump `NEXT INVOICE NUMBER` by one.
5. Add the row to the `## Register` table in `SUMMARY.md` and update `## Cash status`.
6. **Arm the receivable clock** in the record file (see below).
7. Run `scripts/money`. Commit `SUMMARY.md` and `MONEY.md` together.
8. Sending is Sam's call. The checks are quality gates, not send authority.

**Collect**

1. Put `**PAID YYYY-MM-DD**` in the Status cell of `SUMMARY.md`, the ledger row, and the record.
   The date sits immediately after the `PAID` token, because that anchor is what the parser reads.
2. Strike the record's `**Due:**` line with the outcome. Never delete it.
3. Update `## Cash status`, rerun `scripts/money`, commit both files.

## The format contract

`scripts/money` is the only parser of the register. It fails loud and writes nothing rather than
publish a number it had to guess at. What it requires:

- A `## Register` heading, then a pipe table whose header carries the strings `Invoice`,
  `Date issued`, `Amount`, `Bill to` and `Status`. Column order does not matter, those substrings do.
- An issue date a human would write: `6 Jul 2026` or `6 July 2026`. Not ISO, not `07/06`.
- Paid means the Status cell carries a bold `**PAID YYYY-MM-DD**`. Anything else is open. A PAID
  cell with no date is a hard failure: the run-rate and the cash floor gate bucket by payment
  month, and a missing date would silently bucket the cash into the wrong month.
- A payment date in the future is a hard failure. Collected means the cash arrived.
- A row whose Invoice cell is wrapped in `~~` is skipped. That is how a voided or superseded
  invoice stays visible in the register without polluting the totals.
- Two bolded lines under `## Cash status`, exactly `**Collected: $N**` and `**Outstanding: $N**`.
  The script recomputes both from the table and refuses to write if they disagree with what the
  register claims about itself. That cross-check is the whole point: two independent statements of
  the same number, and a mismatch means one of them is a lie.

## The receivable clock

Every open invoice must carry a live `**Due:**` line **in its own record file**, at line start:

```
**Due:** YYYY-MM-DD - NL-YYYY-NNN $N payment due from <client>. Confirm receipt or chase.
```

`scripts/money` fails if an open row has no such line. It looks only in this directory, only in
`<number>.md`, and the line must name that number. A Due line armed in a client roadmap satisfies
`scripts/horizon` but not this check, on purpose: the clock has to point at the invoice, not near it.

A due date that lives only in the register's `Due` column is invisible to the clock. Money owed to
you goes unchased exactly as easily as a promise you made goes unkept, and unchased money is the
cheaper failure to prevent.

Resolve a Due line by striking it, never by deleting it:

```
~~**Due:** YYYY-MM-DD - ...~~ PAID YYYY-MM-DD, cleared.
```

The strikethrough is judged per token, not per line, so the rollover shape
`~~**Due:** <old>~~ **Due:** <new>` reads as one resolved commitment and one live one.

## What never goes in this folder

Bank numbers. Account numbers, routing numbers, IBAN, SWIFT. They live in the gitignored
`PAYMENT-DETAILS.md` and nowhere else. `scripts/repo-doctor` blocks wire-shaped strings in any
tracked file and hard-blocks that filename at any depth, so the guard does not depend on anybody
remembering this paragraph.

Issued invoice files also stay out of git: `outputs/invoices/` is gitignored, because a rendered
invoice embeds the wire block by design. Archive them in whatever drive folder you keep client
documents in.
