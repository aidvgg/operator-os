# Phase B - Gather Template

Chat: paste the contents of `SKILL.md` (below the YAML frontmatter) into your system prompt before starting this chat, or use the skill if installed. Agentic harness: invoke the skill and pass the Phase A artifact's file path as the only inherited input.

For a refresh run (re-verifying standing claims rather than answering a new question), use `phase-b-refresh.md` instead.

---

```
MODE: Research
PHASE: B-Gather
```

## Approved brief from Phase A
[Paste the Phase A artifact here, or give its file path.]

## Gather instructions

Collect sourced data only. No conclusions, no recommendations. Every empirical claim gets a numbered ID (B1, B2, ...) and one of the labels from SKILL.md's claim-labeling scheme, with source tier (P1/P2/P3), published/effective date, and accessed date. A [SOURCE] label requires the page body read in this context and a verbatim supporting passage of 25 words or fewer in the artifact.

**The gather floor. All five are mandatory:**

1. **Decompose first.** Confirm the brief's numbered sub-questions before any search. A sub-question with zero sources is reported as a gap, never silently merged into another.
2. **Search to disconfirm.** For each sub-question, run at least one query framed to falsify the expected answer, and record it even when it returns nothing.
3. **Trace to primary.** At least one claim per sub-question traced to its P1 source. Deadlines, fee schedules, eligibility rules, and program pricing are P1-only claims.
4. **Stopping rule.** Per sub-question, stop when two consecutive new sources add no new claims, or when the source budget from the brief is spent, and state which condition ended the gather.
5. **Log the searches.** A "searches run" table (query, date, purpose) so Phase D can audit coverage, not just conclusions.

Repeated citations of one primary count as one source. Mark every perishable claim [PERISHABLE] with what makes it rot.

Output structure:

1. Source list (URLs, titles, published/effective dates, dates accessed, tier)
2. Claim table: ID, claim, label, tier, dates, confidence, one-line evidence basis, verbatim passage
3. Searches-run log
4. Gaps and unknowns, per sub-question
5. Stopping-rule verdict per sub-question

End with the structured artifact for Phase C.
