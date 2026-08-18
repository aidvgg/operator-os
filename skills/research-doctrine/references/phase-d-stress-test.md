# Phase D - Stress-test Template

Chat: paste the contents of `SKILL.md` (below the YAML frontmatter) into your system prompt before starting this chat, or use the skill if installed. Agentic harness: invoke the skill and pass the Phase C artifact's file path as the only inherited input; run step 0 as its own subagent seeded with the claim table and URLs only, never the Phase C reasoning.

---

```
MODE: Critique
PHASE: D-Stress-test
```

Critique mode here is read-only on the artifact AND its cited sources: re-fetching a cited URL and searching for direct counter-evidence to a stated claim is permitted and required. Opening new lines of inquiry is not.

## Phase C artifact
[Paste the Phase C artifact here, or give its file path.]

## Stress-test instructions

Adversarially critique the Phase C synthesis. The default stance is hostile. Goal: find every reason this analysis could be wrong before a decision is made.

**Step 0 - Citation audit (before any counter-argument work):**

For each load-bearing [SOURCE] claim, re-fetch the URL and confirm the verbatim passage still exists and still says what the claim says. Verdict per claim: CONFIRMS / CONTRADICTS / DEAD. Any failure demotes the claim to [UNKNOWN] on the spot. Resolve every [RELAY] to [SOURCE] or [UNKNOWN]. Check every [PERISHABLE] claim's source date against the freshness horizon; apply [STALE-SOURCE] where it fails. When a source or claim is demoted, list every inference and draft conclusion that cited it and re-rate each.

**Then the required outputs:**

1. Citation audit table (claim ID, verdict, demotions, re-rated dependents)
2. Strongest counter-argument to each draft conclusion
3. Pre-mortem: "if this conclusion is wrong in 6 months, the most likely reason is X"
4. Sources or claims that don't survive adversarial check, including sampling critique: sub-questions with thin or one-sided coverage, per the Phase B searches-run log
5. Falsification tests: what evidence would change each conclusion?
6. Surviving conclusions (the ones that hold up under critique, with their post-audit confidence)

Settled inputs from the brief are constraints, not targets: test their pre-registered kill threshold or note new evidence as a delta; otherwise report "no trigger met".

If most conclusions don't survive, recommend returning to Phase B for more data rather than advancing to Phase E.

End with the structured artifact for Phase E.
