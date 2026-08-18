# Multi-Model Triangulation Protocol

Some decisions are too high-stakes to trust to a single model's output, no matter how disciplined the doctrine. Triangulation is the procedure for running the same brief through multiple models and reconciling the deltas.

One warning before the procedure: models trained on overlapping web text make correlated errors, and the errors that correlate most are widely-republished stale numbers. Cross-model agreement is therefore NOT evidence that a published fact is current. Triangulation earns its keep on judgment-bearing claims (is this niche viable, is this positioning defensible), and on surfacing deltas worth investigating. For any factual claim with a publisher, the arbiter is the source, never the vote.

---

## When triangulation is required

The doctrine flags these decision classes as requiring triangulation before Phase E:

- Revenue strategy decisions
- Niche or vertical choice
- Pricing changes
- Build or scope decisions with material cost (per the brief's Stakes field)
- Pivots away from current focus

If your decision is in this class and you have not triangulated, the doctrine refuses to produce a Phase E artifact. One carve-out: in a non-interactive run where no second vendor is reachable, the run may proceed with the header line "TRIANGULATION: none, single-vendor" in the Phase E artifact and a one-point confidence penalty on every decision-critical claim. Everywhere a human can open a second model, the refusal stands.

---

## The procedure

### Step 1: Approved brief

Take the Phase A artifact (the approved brief). Do not modify it. The same brief must go to every model. Modifying the brief between models invalidates the comparison.

### Step 2: Run the brief through each model independently

Open separate chats in:

- Claude (with the doctrine installed)
- A second model, different vendor (with the doctrine installed via the README's system-prompt drop-in)
- Optionally a third model for higher-stakes decisions (doctrine installed, same way)

The doctrine must be installed in EVERY participating model. A vanilla model has never seen the phase definitions, the label set, or the confidence scale, and cannot produce a conformant artifact; its fluent, unlabeled output would otherwise be counted as an equal vote against disciplined output.

Record each participant's exact model id. A same-family run (another instance, context, or subagent of the same vendor's model) never enters the agreement tally; log it as an extra red-team pass instead.

Run each independently through Phases B, C, and D. Save each Phase D artifact.

### Step 3: Open a reconciliation context

In a fresh context with the doctrine installed:

```
MODE: Critique
PHASE: D-Stress-test (reconciliation)

## Inputs
[Each model's Phase D artifact, labeled by source and exact model id.]

## Gate
An input artifact lacking claim labels, source URLs, and confidence ratings is rejected from reconciliation, not reconciled. An unlabeled claim cannot count as agreement or dissent.

## Reconciliation instructions

Reconcile at claim-plus-source granularity. Each artifact's claim table (claim, label, tier, source URL, dates, confidence) is the input, not its prose conclusions.

For N participating models, sort claims into:
1. Unanimous (N of N), citing DIFFERENT independently verifiable sources - treat as corroborated
2. Unanimous or majority, citing the SAME source - one source, not corroboration; verify that source
3. Majority (only meaningful when N is 3 or more) - investigate the dissent before scoring it
4. Singleton (one model only) - "uncorroborated, investigate": open the cited source and adjudicate on evidence
5. Contradicted across models - unresolved; adjudicate at the source, never by averaging

At N=2 the tiers are: agreed / singleton / contradicted. There is no majority tier; do not manufacture one.

A singleton backed by a verifiable P1 source outranks a unanimous claim with no primary. Agreement is never evidence of currency for a published fact: check the source's own date against the freshness horizon regardless of the vote.

Output a reconciled claim table where every claim carries its cross-model status AND its strongest source with tier and date.
```

### Step 4: Use the reconciled synthesis as Phase D input for Phase E

The decision in Phase E rests on the reconciled output, not any single model's view.

---

## Why this matters

Different models have different sycophancy patterns and different default biases, and when they search they sometimes reach different sources. That last part is the real value: a second vendor adds evidence mainly by reaching pages the first one didn't, not by holding a different opinion.

Disagreement between models is not a problem to resolve by averaging - it is a signal to investigate. The disagreement often points at exactly the area where the underlying question is genuinely uncertain.

---

## What this is not

Triangulation is not "use the model that agrees with you most." It is not "average the outputs." It is not "pick the cleanest answer." And agreement is not verification: two models repeating the same stale figure from the same training corpus is one error with two voices.

It is structured cross-model adversarial review at the claim-and-source level. The protocol exists because no single model - including the one running this doctrine - is reliable enough on its own for high-stakes decisions.
