# Phase E - Decide Template

Chat: paste the contents of `SKILL.md` (below the YAML frontmatter) into your system prompt before starting this chat, or use the skill if installed. Agentic harness: invoke the skill and pass the Phase D artifact's file path as the only inherited input.

---

```
MODE: Strategic
PHASE: E-Decide
```

In Phase E the Strategic pushback obligation is discharged by the Phase D artifact: carry its surviving counter-arguments into Risks accepted and Kill thresholds; do not regenerate them. Strategic tool use is verification-only: re-check a carried claim against its cited source when its staleness would change the recommendation.

## Phase D artifact
[Paste the Phase D artifact here, or give its file path.]

## Decide instructions

Produce a decision document. No hedged language, no "could consider". A labeled confidence figure is not hedging; stripping labels is falsification. The decision is the user's; this artifact gives them what they need to make it cleanly.

**Step 0 - Staleness pass:** identify carried claims whose staleness would flip the recommendation; re-check them against their cited source or state flatly that they are accepted as stale.

Output structure:

1. Recommendation (one sentence)
2. Reasoning (the surviving conclusions from Phase D)
3. Load-bearing claims (each with label, source tier, as-of date, confidence)
4. Action items (concrete next steps, each with a date)
5. Risks accepted by this decision
6. Kill thresholds (what would make this decision wrong, and how you would detect it)
7. Decided despite (unresolved contradictions and open questions carried from Phase D, stated flatly)
8. Write-back plan (the enumerated edits the findings imply for your knowledge system: value changes, supersede banners, expiry updates, deadline lines. Producing the plan is this artifact's job; executing it is not)

If the decision is a fact-state update rather than a bet, this artifact is terminal: replace "Recommended next phase" with "Terminal - no Phase F" and a re-verify-by date. Otherwise end with the structured artifact for Phase F.

---

## E-draft variant (expert-routed domains: legal, tax, immigration, medical, investment)

Phases A through D run in full. This variant replaces the decision document. It is draft-grade by definition and says so in its header.

Output structure:

1. Verified fact base (every load-bearing claim with label, tier, published/effective and accessed dates, confidence)
2. Options and what each turns on (no recommendation)
3. Consultation question bank for [expert category]: numbered questions, each tagged with the claim it resolves and what changes depending on the answer
4. Not-advice line: "Draft-grade research for preparation only. Decision-grade requires [expert category]."
5. Do-not-act list: what must not be acted on before the consult
6. Write-back plan (the enumerated edits the verified fact base implies for your knowledge system; producing the plan is this artifact's job, executing it is not)

No go/no-go recommendation. No action item that creates legal, tax, or immigration exposure before the named expert has ruled.
