---
description: Issue a branded invoice in the HTML->PDF document standard by running the invoice-creator skill end to end, including the ledger-number rule, the wire-block rule, the pdf-check gate and the mandatory fresh-context fact-check gate.
---
Invoice: $ARGUMENTS

1. **Read `skills/invoice-creator/SKILL.md` in full and follow it exactly.** That file owns the
   procedure, including the number, the wire block, the record-and-advance sequence and the
   collection loop. Do not restate it here.
2. **The two things this command exists so they stop being skipped:**
   - **The number is read, never recalled.** It comes from
     `knowledge/business/invoices/INVOICE-LEDGER.md`. A recalled number is exactly the class of
     mistake `ai/ERRORS.md` exists to stop repeating.
   - **The wire block is copied from `knowledge/business/invoices/PAYMENT-DETAILS.md` only**,
     never typed from memory and never inlined into a committed file.
3. Report the invoice number, the amount, the output path and the `fact-check` verdict in plain
   text.
