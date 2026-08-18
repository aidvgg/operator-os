# Phase B - Refresh Template (re-verifying standing claims)

Chat: paste the contents of `SKILL.md` (below the YAML frontmatter) into your system prompt before starting this chat, or use the skill if installed. Agentic harness: invoke the skill and pass the Phase A artifact's file path as the only inherited input.

Use this template when the brief carries a "Prior state under test" table: claims that were researched before and need re-verification, not greenfield discovery. The standard gather floor from `phase-b-gather.md` applies here too.

---

```
MODE: Research
PHASE: B-Gather (refresh)
```

## Approved brief from Phase A
[Paste the Phase A artifact here, or give its file path. It must include the Prior state under test table: claim, value, source, verification date, prior confidence.]

## Refresh instructions

The unit of work is the prior claim, not the topic. For every row in the Prior state under test table, re-verify against the current primary source and return exactly one verdict:

- **CONFIRMED unchanged** - the current P1 source states the same value. Cite it fresh: a verdict of "unchanged" needs a source and date behind it, same as a change.
- **CHANGED** - old value -> new value, with the current source, its published/effective date, and, where visible, when the change took effect.
- **SUPERSEDED** - the rule, program, or page no longer exists in that form; name what replaced it.
- **NOW UNVERIFIABLE** - the source is gone or no longer states it, and no current primary could be found. Demote to [UNKNOWN].
- **NEW** - a claim not in the prior table that materially bears on the same sub-question. Gather it per the standard floor.

Rules:

1. Every verdict carries the same labeling discipline as a fresh gather: tier, dates, verbatim passage, confidence, evidence basis.
2. Prior verification provenance travels with the row: a claim previously verified against P1 that this pass can only re-verify against P2 is a DOWNGRADE and must say so, never a silent "confirmed".
3. Do not relitigate rows the brief marks as settled inputs; they are not claims under test.
4. A prior claim the pass did not reach is listed as NOT CHECKED, never silently dropped.

Output structure:

1. Verdict table: one row per prior claim (ID, claim, old value, verdict, new value if any, source, tier, dates, confidence)
2. Delta summary: what changed, what was superseded, what became unverifiable
3. NEW claims table (standard gather format)
4. Searches-run log
5. Gaps, unknowns, and NOT CHECKED rows

End with the structured artifact for Phase C.
