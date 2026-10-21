# Phase C: Synthesize

Use only the Phase B evidence artifact and canonical inputs named in the brief. Introduce no new empirical claim. Send missing premises back to B. Do not synthesize an artifact labeled `NOT READY`; return it to B. For `READY FOR CONDITIONAL SYNTHESIS`, preserve every named condition in each affected conclusion.

## Synthesis procedure

1. Group claims by atomic component and sub-question without dropping zero-evidence components.
2. Separate empirical claims, assumptions, inferences, predictions, and preferences.
3. Create inference IDs `I1...In`; name every premise by claim ID.
4. Create calculation IDs `K1...Kn` for every derived value intended for Phase E; preserve inputs, units, method, rounding, and sensitivity.
5. Create conclusion IDs `C1...Cn`; name every indispensable claim, inference, calculation, and assumption.
6. Propagate the weakest indispensable dependency into the conclusion state and certainty.
7. Preserve contradictions and alternative explanations.
8. Mark any missing premise as `RETURN TO B`, never fill it from model recall.

## Phase C artifact

```markdown
# [Title]: Phase C Synthesis

## Coverage carry-forward

| Component ID | Q ID | Critical | B status | Claims or gap records used | C treatment | State |
|---|---|---:|---|---|---|---|
| R1.a | Q1 | yes/no | ... | B1, B4 | I1, C1 | SUPPORTED WITH LIMITATIONS |

## Invariant carry-forward

| Invariant ID | Component IDs | B verdict | C treatment | State effect |
|---|---|---|---|---|
| I1 | R1.a | CONFIRMED | preserved | none |

## Inference register

| Inference ID | Inference | Premise IDs | Alternative explanation | State | Certainty and basis |
|---|---|---|---|---|---|
| I1 | ... | B1, B4 | ... | SUPPORTED WITH LIMITATIONS | MODERATE: ... |

## Conclusion register

| Conclusion ID | Draft conclusion | Claim dependencies | Inference dependencies | Assumptions | Contradictions | State | Certainty |
|---|---|---|---|---|---|---|---|
| C1 | ... | B1, B4 | I1 | A1 | X1 | CONTESTED | LOW |

## Calculation register

| Calculation ID | Derived value | Input IDs and units | Method | Rounding | Sensitivity | State and certainty |
|---|---|---|---|---|---|---|
| K1 | ... | B1, B4 | ... | ... | ... | ... |

## Dependency ledger

| Output ID | Depends on | Weakest indispensable dependency | What would reverse it |
|---|---|---|---|
| C1 | B1, B4, I1, A1 | B4 | ... |

## Return-to-B register

| Missing premise | Needed by | Why material | Required evidence |
|---|---|---|---|
| ... | C1 | ... | ... |

## Phase C gate

- B atomic components or sub-questions not carried forward: [none required, or IDs]
- Structural invariants not carried forward: [none required, or IDs]
- Phase B readiness respected: yes/no
- Conclusions without complete dependency paths: [none required, or IDs]
- Phase E derived figures not reproducible: [none required, or IDs]
- Missing premises not exposed: [none required, or IDs]
- Unlabeled new empirical claims: 0
- Phase C: COMPLETE | INCOMPLETE
```

## C-Merge for parallel lanes

Synthesize each lane separately first. Then merge the lane artifacts before D:

1. map duplicate claims to common evidentiary roots
2. identify cross-lane dependencies and incompatible definitions
3. reconcile or preserve contradictions
4. create merged conclusion and dependency registers
5. map every original requirement, atomic component, invariant, and sub-question into the merged artifact

Call the result `Phase C-Merge`. Complete it only when every lane and every original component and invariant appears in the merged coverage table. Phase D receives C-Merge, not an unmerged stack of lane reports.
