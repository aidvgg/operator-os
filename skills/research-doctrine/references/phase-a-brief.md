# Phase A - Brief Template

Chat: paste the contents of `SKILL.md` (below the YAML frontmatter) into your system prompt before starting this chat, or use the skill if installed. Agentic harness: invoke the skill; this phase has no prior artifact, so its only inputs are the user's question and the canonical project files named below.

---

```
MODE: [Strategic | Research | Critique]
PHASE: A-Brief
```

Builder is deliberately absent from this template: a brief is not an execution spec, and Builder has no phase. Declare Builder only to stand the doctrine down.

## Question
[State the question or problem you need researched.]

## Why this question now
[What decision will the output inform? What's the cost of getting it wrong? This becomes the Stakes field.]

## Initial brief draft

- **Role:** [Who is the assistant playing - strategist, market analyst, technical architect?]
- **Context:** [Background the assistant needs to know, including canonical files it should read.]
- **Deliverable:** [What artifact should phase work produce?]
- **Rules:** [Constraints - sources, methods, formats to use or avoid; the per-sub-question source budget if capped.]
- **Sub-questions:** [Numbered. Phase B gathers and reports per sub-question. Group into lanes if clusters share the decision but not their sources.]
- **Stakes:** [The decision this informs, and the cost or reversibility of getting it wrong.]
- **Decision date and freshness horizon:** [When the decision happens; how current a claim must be to support it.]
- **Success criteria:** [Concrete, testable. No "good", "comprehensive", "useful".]
- **Failure criteria:** [What does a bad output look like?]
- **Out of scope:** [What you do NOT want analyzed.]
- **Settled inputs, do not reopen:** [Each with decision date, review date, and pre-registered kill threshold. From your decision ledger if you keep one. May be empty.]
- **Prior state under test:** [Refresh runs only: standing claims with value, source, verification date, prior confidence. Drives `phase-b-refresh.md`.]

---

The assistant will respond by either accepting the brief or refusing fields that don't meet the testable-criterion standard. Iterate until the brief is approved. Do not advance to Phase B in this chat. Close with the standard artifact ending (next phase: B).
