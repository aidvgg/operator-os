---
description: Update the operator business profile JSON by read-and-merge. Reads the existing profile and memory.md before asking anything, diffs field by field, and never blank-slate overwrites.
---
Update the business profile: $ARGUMENTS

1. **Read `skills/business-profile-creator/SKILL.md` in full and follow it exactly**, starting
   with its hard-rules section. That file owns the procedure.
2. **The two things this command exists so they stop being skipped:**
   - **Read before you ask.** Load the existing
     `knowledge/business/operator-business-profile.json` and `knowledge/memory.md` first.
     A blank-slate interview is a defect, not a refresh.
   - **Diff, never replace.** Show the field-level diff and get Sam's yes before writing.
3. Report the diff and the output path in plain text.
