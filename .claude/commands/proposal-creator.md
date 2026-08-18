---
description: Generate a branded proposal, quote or SOW in the HTML->PDF document standard by running the proposal-creator skill end to end, including its two mandatory fresh-context verification gates.
---
Create a client proposal for: $ARGUMENTS

1. **Read `skills/proposal-creator/SKILL.md` in full and follow it exactly**, then
   `skills/proposal-creator/references/data-schema.md`. Those files own the procedure. Do not
   restate it, do not re-derive it, do not improvise a shorter version.
2. **The two things this command exists so they stop being skipped:**
   - **Verification is not optional and not skippable for "quick" work.** `fact-check` and
     `price-attack` are fresh-context subagents. The two gates are NOT symmetrical, and the easy
     mistake is to blur them into one overrule path that `SKILL.md` does not grant:
     - `fact-check` has no overrule. It checks whether numbers, dates and entity names match
       the canonical files, which is a question of fact, not judgment. `SKILL.md` says fix and
       re-run until `VERDICT: PASS`, and that is the binding wording under CLAUDE.md's
       precedence carve-out (SKILL.md wins on execution mechanics).
     - `price-attack` objections MAY be overruled, because pricing is Sam's call and the repo
       has a standing ruling that live buyer signal beats repo comps. Overruling requires Sam's
       explicit word on that objection, and the draft records which objections were overruled
       and why.
     A draft carrying an un-passed `fact-check` is UNVERIFIED and may not be labelled final or
     send-ready, whatever else has been agreed.
   - **Send authority is separate from the quality gates.** A clean checklist is not a yes.
     Nothing goes to the client without Sam's explicit go on that specific artifact.
3. Report the output path, the price, and the verifier verdicts in plain text.
