# Phase B: Refresh Standing Claims

Use this branch when Phase A includes prior claims that may have changed. Load `evidence-standard.md`. Treat each prior claim, mapped atomic component, and structural invariant as a unit of work.

## Refresh verdicts

Assign exactly one verdict to every prior claim:

- `CONFIRMED`: current fit evidence supports the same bounded claim
- `CHANGED`: current evidence establishes a different value or rule
- `SUPERSEDED`: a newer identified claim replaces it
- `NOW UNVERIFIABLE`: the former support cannot be re-established
- `CONTESTED`: current fit evidence conflicts
- `NOT CHECKED`: the pass did not inspect the claim

Do not call a claim unchanged without fresh evidence. Preserve the prior evidence tier and date beside the new result so downgrades remain visible.

## Refresh artifact

```markdown
# [Title]: Phase B Refresh

## Prior-claim coverage

| Prior ID | Exact prior claim | Prior source/tier | Prior verified | Current verdict | Current claim ID | State | Decision effect |
|---|---|---|---|---|---|---|---|
| P1 | ... | ... | ... | CHANGED | B1 | VERIFIED | ... |

## Atomic component coverage

[Use the atomic coverage schema from phase-b-gather.md. Map every refreshed claim to its Phase A component IDs.]

## Structural invariant verdicts

[Use the invariant schema from phase-b-gather.md. Recheck any denominator, unit, nesting, additivity, status, period, or reporting-state relationship that may have changed.]

## Current source register

[Use the source-register schema from phase-b-gather.md.]

## Current claim register

[Use the claim-register schema from phase-b-gather.md.]

## Delta ledger

| Prior ID | Old bounded value | New bounded value | Effective date | Evidence | Dependents to revisit |
|---|---|---|---|---|---|
| P1 | ... | ... | ... | B1 | C2, recommendation D1 |

## Search and contradiction logs

[Use the search, contradiction, null-result, retrieval-failure, and stopping schemas from phase-b-gather.md, including one disconfirming search per sub-question.]

## Phase B refresh gate

- Prior claims without a verdict: [none required, or IDs]
- Atomic components without a state: [none required, or IDs]
- Structural invariants without a verdict: [none required, or IDs]
- Current load-bearing claims without inspected evidence: [none required, or IDs]
- Downgrades or supersessions not exposed: [none required, or IDs]
- NOT CHECKED prior claims: [IDs or none]
- Readiness: READY | READY FOR CONDITIONAL SYNTHESIS | NOT READY
- Phase B refresh: COMPLETE | INCOMPLETE
```

Complete the refresh only when every prior claim has a verdict, every mapped component and invariant has an explicit state, and the readiness label reconciles to the rows. A missing row is a failure, not an unchanged claim. A failed refresh attempt creates a component-specific gap; it never proves that the prior value still holds.
