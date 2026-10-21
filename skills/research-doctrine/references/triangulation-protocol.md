# Cross-Model Triangulation

Use this protocol to reach assurance class L3. Triangulation is independent error discovery and source reconciliation. It is not voting.

## Entry conditions

Require all of the following:

- one frozen Phase A brief
- independently executed research passes
- at least two materially different models or providers
- inspected sources and claim registers from every eligible pass
- a fresh reconciliation context that did not produce either synthesis

A same-family subagent or second context may strengthen red-teaming, but does not create cross-model independence. An output without claim IDs, evidence locators, source fitness, and terminal states is ineligible until normalized and audited.

## Independent passes

Give every model the exact same brief, scope, budgets, freshness horizons, and doctrine. Do not share another model's findings before its Phase D artifact is frozen. Record the exact model or provider identity available to the operator.

Each pass must complete A through D and report its achieved assurance class and Closure Ledger status. A model can disagree with the expected answer without being correct; preserve its evidence, not its personality.

## Normalize the artifacts

Before comparing conclusions, create a union claim table:

| Union ID | Model claim IDs | Normalized bounded claim | Source roots | Model states | Model certainty | Conflict |
|---|---|---|---|---|---|---|
| U1 | M1-B2, M2-B7 | ... | Root A, Root B | ... | ... | none |

Normalize only semantically equivalent claims. Preserve scope, date, and definition differences as distinct claims.

## Reconcile evidence roots

For each union claim:

1. inspect the strongest cited passage from every distinct root
2. collapse repeated reporting of one root
3. compare source fitness, freshness, and entailment
4. search or return to B when a disagreement turns on missing evidence
5. assign one reconciled terminal state and certainty

Use these cross-model statuses:

- `AGREED, INDEPENDENT ROOTS`: models agree and cite at least two fit distinct roots
- `AGREED, SAME ROOT`: models agree but repeat one root; no new corroboration
- `SINGLETON, STRONGER EVIDENCE`: one model differs and has the fitter evidence
- `SINGLETON, UNRESOLVED`: only one model makes the claim and evidence is insufficient
- `CONTRADICTED`: fit evidence supports incompatible claims
- `SCOPE MISMATCH`: apparent disagreement comes from different populations, dates, or definitions

At two models there is no majority. At three or more, a majority still cannot override stronger direct evidence. Source fitness adjudicates facts; model counts identify where to investigate.

## Reconcile reasoning

After evidence reconciliation, compare:

- requirements or sub-questions one model omitted
- alternative explanations unique to one pass
- assumptions and value judgments that differ
- dependency paths and weakest premises
- counter-cases and reversal conditions

Create reconciled conclusion IDs and rebuild the dependency ledger from the reconciled claim table. Do not average confidence or prose conclusions.

## Reconciliation artifact

```markdown
# [Title]: L3 Reconciliation

## Participants

| Pass | Model/provider | Brief identity | Prior class | Eligible |
|---|---|---|---|---:|
| M1 | ... | hash or exact title/date | L2 | yes |

## Union claim table

[Use the normalization schema above.]

## Source-root audit

| Union ID | Distinct roots | Strongest fit evidence | Cross-model status | Reconciled state | Certainty |
|---|---:|---|---|---|---|
| U1 | 2 | ... | AGREED, INDEPENDENT ROOTS | VERIFIED | HIGH |

## Coverage deltas

| Requirement, component, invariant, or Q ID | M1 | M2 | Reconciled treatment |
|---|---|---|---|
| Q1 | covered | omitted | restore and audit |

## Reasoning deltas

| Conclusion | Different assumptions or paths | Adjudication | Residual risk |
|---|---|---|---|
| ... | ... | ... | ... |

## Reconciled dependency ledger

[Every final conclusion linked to union claims, inferences, assumptions, and contradictions.]

## L3 gate

- Eligible independent passes: N
- Union claims not source-audited: [none required, or IDs]
- Requirements, atomic components, invariants, or sub-questions not reconciled: [none required, or IDs]
- Contradictions not resolved or carried: [none required, or IDs]
- Reconciled conclusions not dependency-traced: [none required, or IDs]
- L3 reconciliation: COMPLETE | INCOMPLETE
```

Only a complete reconciliation supports class L3 and `TRIANGULATED` status. If one model or source set is unavailable, report the strongest lower class achieved rather than treating triangulation as complete.
