# Anti-Patterns Reference

Two lists. **Operator anti-patterns** are the most common ways the person running the research misuses it; they are detected in your input. **Research-integrity anti-patterns** are the most common ways the research itself goes wrong; they are detected in the assistant's own output and enforced by the Phase B gather floor and the Phase D citation audit.

Use both as a pre-flight checklist before starting any research project, and as a diagnostic during ongoing work.

---

## Operator anti-patterns (detected in your input)

### 1. Builder's trap

**Trigger phrases:** "let's build", "I want to make", "would be useful to have"

**What it looks like:** Proposing to build a tool, system, or automation before any evidence of demand.

**Defense required:** Show evidence that the thing being built will be used or paid for. "I think people would want this" is not evidence.

**Fix:** Run a Phase F market-test on the demand before scoping the build.

### 2. Engineering-as-sales-substitute

**Trigger:** Proposing internal automation, tooling, or infrastructure work while outbound sales pipeline is below target.

**What it looks like:** "I'll build a tool to do X better, then I can sell more." Building is more comfortable than selling.

**Defense required:** Show recent outbound sales metrics. If they're below the target recorded in your brief or ledger, the build is procrastination.

**Fix:** Complete one full outbound working block, or produce last week's outbound numbers, before any internal build work.

### 3. Mega-chat (process violation, no defense)

**Chat triggers:** Chat exceeds 30 conversational turns. Spans multiple phases. User references "earlier when we talked about X" for material no longer in the artifact.

**Harness triggers:** the context holds artifacts for two different phases; the context has been compacted or summarized since the brief was fixed; the approved brief is no longer verbatim in context. Tool-call turns never count toward any length threshold, and Phase A brief iteration is exempt.

**What it looks like:** A single context trying to do brief, research, synthesis, and decision together. Output quality degrades nonlinearly past phase boundaries.

**Fix:** Start a fresh context. Seed it with the most recent artifact. Declare mode and phase.

### 4. First-pass acceptance

**Trigger:** User accepts the assistant's initial strategic output and moves immediately to execution.

**What it looks like:** "Great, that's exactly what I needed. Let me get started." First-pass output in strategic mode is almost always under-tested.

**Defense required:** Explicitly request a Phase D stress-test before accepting any strategic output.

**Fix:** Open a fresh context in MODE: Critique with the strategic output as input.

### 5. Vague brief

**Trigger phrases:** "good", "comprehensive", "thorough", "best", "high-quality", "useful", "valuable" appearing in success criteria.

**What it looks like:** A brief that cannot be falsified because the success criteria are unmeasurable.

**Defense required:** Replace each vague criterion with one that could be marked pass/fail by an outside observer.

**Fix:** Return to Phase A. Do not advance until the brief is testable.

### 6. Mode mixing (process violation, no defense)

**Trigger:** Single prompt asks for execution + strategy + critique together. Example: "Research X, tell me what to do, and start building."

**What it looks like:** The model tries to satisfy all three modes in one response. None of them gets done well.

**Fix:** Three separate contexts. One per mode. Artifacts pass between them.

### 7. Shiny object pivot

**Trigger:** User proposes pivot, new niche, or new direction before completing a full cycle on the current focus.

**What it looks like:** "Maybe I should focus on X instead." X is usually whatever the user was reading about that morning.

**Defense required:** Show what was learned from the current focus. Show the kill threshold that was hit. If neither exists, the pivot is avoidance.

**Fix:** Complete the current cycle through Phase F. Then make the pivot decision in Phase E based on real data.

### 8. Sales-problem-as-engineering-problem

**Trigger:** User proposes building software to solve a problem that is fundamentally about distribution, sales, or messaging.

**What it looks like:** "I'll build a better X and the customers will come." Or: "I'll automate my outbound." (When you don't have outbound to automate.)

**Defense required:** Articulate the sales problem in plain language. Show why software solves it better than direct sales activity.

**Fix:** Run a sales experiment first. The build, if needed, comes after.

### 9. Settled-decision relitigation

**Trigger:** The request re-argues a ruling listed in the brief's "Settled inputs, do not reopen" field (or in your decision ledger) while that ruling is in date and its pre-registered kill threshold has not fired.

**What it looks like:** Re-running the same debate every session with the same inputs and a different mood. Adversarial effort burns on decided questions instead of unverified ones.

**Defense required:** Name the pre-registered trigger that fired, or present genuinely new evidence as a delta against the ruling.

**Fix:** If neither exists, the ruling enters the brief as a fixed constraint and the pass moves on. Reopening it is a Phase A scope error.

---

## Research-integrity anti-patterns (detected in the assistant's own output)

Each of these demotes the affected claim on the spot when named. The enforcement point is in parentheses.

### R1. Source-doesn't-say-that

A real URL attached to a claim the page does not make, or a snippet paraphrased into a stronger claim than the body supports. (Phase B: verbatim-passage requirement. Phase D: citation audit re-fetches and compares.)

### R2. Single-source pyramid

A stack of conclusions resting on one source, presented with the confidence of many. (Phase B: repeated citations of one primary count as one source. Phase D: audit table exposes the pyramid.)

### R3. Citation laundering

Secondary sources paraphrasing one primary counted as independent corroboration. (Phase B: P2 must record which primary it traces to; same primary = one source. Triangulation: agreement on one source counts as one source.)

### R4. Stale-as-current

A perishable claim asserted from a source older than the freshness horizon, on a current-looking page. (Claim labeling: [PERISHABLE] + [STALE-SOURCE] demotion. Phase D: audit checks source dates against the horizon.)

### R5. Phantom precision

A number carried to more precision than its source states, or a range collapsed to a point. (Phase B: verbatim passage must contain the number as stated. Phase D: audit compares.)

### R6. Confidence inflation

Ratings drifting up because justification is only demanded below a threshold, or inference confidence exceeding its premises. (Claim labeling: every rated claim carries an evidence basis; inference confidence capped by weakest premise.)

---

## How to use this list

Before starting any research project:

1. Scan the operator patterns; note any that match your current situation
2. Either defend, revise, or change direction before starting Phase A

During a project, if the assistant names a pattern, do not push past it. For operator patterns 1, 2, 4, 5, 7, 8, 9 the assistant demands a defense; for 3 and 6 there is no defense, only the fix. Research-integrity patterns are the assistant's to name against itself, and the demotion is not optional.
