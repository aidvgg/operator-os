# Phase A: Frame

Infer a first draft from the user's request. Ask only for a missing choice that could materially change the result. Record all other reasonable defaults as assumptions.

## Brief artifact

```markdown
# [Title]: Phase A Brief

## Research contract

- Question:
- Deliverable:
- Decision or use:
- Stakes and reversibility:
- Decision deadline:
- Source, time, and tool budget:
- Output budget and evidence-first allocation:
- Required assurance class, if specified:

## Scope

- Geography or jurisdiction:
- Population, customer, product, or system:
- Comparison set:
- Time window:
- Definitions:
- Canonical inputs supplied by the user:

## Freshness horizons

| Claim class | Stale after | Reason |
|---|---|---|
| prices, rules, capabilities, market facts, other | ... | ... |

## Requirements

| ID | Required output or condition | Why decision-relevant | Critical | Mapped sub-question | Terminal state |
|---|---|---|---:|---|---|
| R1 | ... | ... | yes/no | Q1 | pending |

## Atomic coverage matrix

Split each requirement into the smallest components whose omission or misstatement could change the answer. Do not treat a compound prompt clause as one row.

| Component ID | Requirement | Exact component to establish | Critical | Evidence needed | Q ID | Terminal state |
|---|---|---|---:|---|---|---|
| R1.a | R1 | ... | yes/no | ... | Q1 | pending |

## Structural invariant checklist

List only relationship dimensions that could change meaning. Mark non-applicable dimensions explicitly.

| Invariant ID | Component IDs | Dimension | Exact relationship to preserve | Failure trap | Verdict |
|---|---|---|---|---|---|
| I1 | R1.a | denominator/unit/nesting/additivity/status/time/reporting state/other | ... | ... | pending |

## Sub-questions

| ID | Question | Component IDs | Evidence needed | Disconfirmation target | Lane |
|---|---|---|---|---|---|
| Q1 | ... | R1.a | ... | What result would reverse the expected answer? | core |

## Success and failure criteria

- Success criteria: [observable pass/fail conditions]
- Failure criteria: [named defects that invalidate the output]

## Settled inputs

| Input | Basis | Review date | Reopen only if |
|---|---|---|---|
| ... | ... | ... | ... |

## Exclusions

| Excluded item | Reason | Consequence if material |
|---|---|---|
| ... | ... | ... |

## Assumptions

| ID | Assumption | Why needed | What changes if false |
|---|---|---|---|
| A1 | ... | ... | ... |

## Scope challenge

- Omitted actor or incentive that could reverse the answer:
- Omitted alternative or base rate:
- Omitted implementation or operational constraint:
- Omitted security, legal, or regulatory constraint:
- Omitted timing or freshness risk:
- New requirements added from this challenge:

## Gate

- Requirements not mapped to sub-questions or exclusions: [none required, or IDs]
- Atomic components not mapped to sub-questions or exclusions: [none required, or IDs]
- Critical components: [IDs]
- Structural invariants without a row or explicit not-applicable verdict: [none required, or IDs]
- Explicit exclusions: [IDs or none]
- Material ambiguity remaining: none | [IDs]
- Phase A: COMPLETE | INCOMPLETE
```

Complete Phase A only when each atomic component maps to a sub-question or a reasoned exclusion, every critical component is identified, every foreseeable relationship trap has an invariant row, and each sub-question names the evidence and disconfirmation needed. Protect evidence work in the output budget. Do not spend the budget on explanatory process prose that can be represented by one table row.
