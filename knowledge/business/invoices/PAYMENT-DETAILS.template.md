# PAYMENT DETAILS - template scaffold (committed, placeholders only)

> **This is not the file invoices read.** It is the empty shape of that file, kept in git so a
> fresh clone knows which fields exist.
>
> The real file is `PAYMENT-DETAILS.md`, in this same folder. It is **gitignored**, and
> `scripts/repo-doctor` hard-blocks that basename at any depth, so it cannot be committed by
> accident or on purpose. It is the **only** place live bank values exist in this system.
>
> `skills/invoice-creator` **reads** it field by field when it renders an invoice, and writes it
> **never**. It is deliberately absent from the sanctioned-write set in `CLAUDE.md`, and adding it
> there would hand an agent write access to the one file that must only ever be read. If a value
> needs to change, Sam edits it by hand.

## Setup, once per machine

```
cp knowledge/business/invoices/PAYMENT-DETAILS.template.md \
   knowledge/business/invoices/PAYMENT-DETAILS.md
```

Then fill every placeholder in the copy. Leave nothing in angle brackets in the real file: a
placeholder that survives into a rendered invoice reaches a client looking like a bug, and a
client who cannot pay you is a slower failure than a client who will not.

## Wire block

| Field | Value |
|---|---|
| Beneficiary name | `<LEGAL ENTITY NAME, e.g. Rivera Holdings LLC>` |
| Beneficiary address | `<REGISTERED STREET, CITY, COUNTRY>` |
| Bank name | `<BANK NAME>` |
| Bank address | `<BANK STREET, CITY, COUNTRY>` |
| Account number | `<ACCOUNT NUMBER>` |
| ACH routing | `<ACH ROUTING NUMBER>` |
| Wire routing, if different | `<WIRE ROUTING NUMBER>` |
| SWIFT / BIC | `<SWIFT OR BIC>` |
| Currency | USD |
| Payment reference | the invoice number, one per invoice |

Add a second block if the entity holds more than one account, and label each block with the entity
and currency it belongs to. `invoice-creator` picks the block by matching the from-entity on the
invoice, so an unlabelled second block is a coin toss.

## Why there are no example numbers here

`scripts/repo-doctor` blocks wire-shaped strings in every tracked text file: a routing or account
keyword near a long digit run, a BIC-shaped token, an IBAN, a phone number. Realistic sample values
in this file would make the template fail its own gate on the first commit. That is the check
working, not the check being awkward, so the placeholders stay word-shaped.

The same rule is why no invoice record in this folder carries a wire block. Records are committed.
The wire block belongs on the rendered PDF and in the local file, and nowhere else.

## When the numbers change

A bank changing partner banks, or an entity moving accounts, invalidates every invoice already
sitting unpaid in somebody's inbox.

1. Update the local `PAYMENT-DETAILS.md` first, before issuing anything else.
2. Reissue every open invoice with the corrected block, same number and same amount. A reissue is
   a correction, not a new invoice, so `INVOICE-LEDGER.md` does not advance.
3. Note the reissue in each affected record file, and say plainly that the old details are dead.
   Somebody will try to pay the old block otherwise.
