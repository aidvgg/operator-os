# Pricing outcomes: the calibration ledger

One row per quote. Opened by `skills/proposal-creator` on send, closed by `skills/invoice-creator`
on collection. Both writes are sanctioned; nothing else in `knowledge/` is, for these skills.

**What this file is for.** So the `price-attack` pass can argue from {{FIRST_NAME}}'s own record
instead of from doctrine. Rows showing what was quoted, what the buyer actually said, and what
came in, are evidence.

**These figures are history, not prices.** Every number in the table below is a record of what
was said on a date. None of it is quotable. Live prices come from the authority every time:
`knowledge/business/outbound-offer.md` for the standard offer,
`knowledge/clients/<client>/roadmap.md` for a client engagement.

---

## Append format

Append a new row at the bottom. Never reorder, never rewrite a closed row.

```
| YYYY-MM-DD | <client> + short scope | <what was quoted> | <what they said, verbatim where possible> | <what came in> | <one line, transferable> |
```

An open row has `pending` in Reaction and `-` in Final and Lesson. A row that dies gets `lost` in
Final and the reason in Lesson.

---

## Ledger

| Date | Deal | Quoted | Reaction | Final | Lesson |
|---|---|---|---|---|---|

No quote sent yet.
