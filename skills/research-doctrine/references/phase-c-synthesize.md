# Phase C - Synthesize Template

Chat: paste the contents of `SKILL.md` (below the YAML frontmatter) into your system prompt before starting this chat, or use the skill if installed. Agentic harness: invoke the skill and pass the Phase B artifact's file path as the only inherited input.

---

```
MODE: Research
PHASE: C-Synthesize
```

In this phase, Research mode means: the Phase B artifact and project files only. No web.

## Phase B artifact
[Paste the Phase B artifact here, or give its file path.]

## Synthesize instructions

Pattern-match across the gathered data. Draw inferences and label them. No new research in this context, and no new claims: no empirical claim may enter the synthesis that was not in the Phase B artifact.

[TRAINING] claims may be used only to frame or question, never as a premise of a draft conclusion. Any such use is listed under Open questions as a return-to-B item.

Every inference names its premises by Phase B claim ID: `[INFERENCE from: B3, B7]`. An inference's confidence may not exceed the lowest confidence among its premises; any [TRAINING] or [UNKNOWN] premise caps it at 5.

The valve: if a draft conclusion requires a fact Phase B did not gather, stop and recommend returning to Phase B for that sub-question rather than filling the hole from recall. In an agentic harness the return is cheap, one gather subagent re-run on one sub-question.

Output structure:

1. Patterns observed across sources
2. Inferences (labeled `[INFERENCE from: ...]` with propagated confidence)
3. Tensions and contradictions in the data
4. Draft conclusions (each listing the claim IDs and inferences it rests on; still labeled, not yet adversarially tested)
5. Open questions, including every return-to-B item

End with the structured artifact for Phase D.
