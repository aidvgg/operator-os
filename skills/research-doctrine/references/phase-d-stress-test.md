# Phase D: Audit and Challenge

Freeze the Phase C or C-Merge artifact. When a fresh context is available, give the reviewer only the approved brief, source register, claim register, evidence passages, search log, contradiction log, dependency ledger, and frozen synthesis. Do not pass the producing rationale.

When no fresh context is available, apply the same audit packet as a context firewall and cap assurance at L1.

## Attack 1: Citation audit

For every load-bearing empirical claim:

1. inspect the cited passage and locator
2. judge entailment as `CONFIRMS`, `PARTIAL`, `CONTRADICTS`, or `DEAD`
3. recheck source fitness and freshness
4. resolve `[RELAY]` and `[SNIPPET]` to inspected evidence or `UNVERIFIED`
5. identify every dependent inference, conclusion, and recommendation
6. demote all dependents when the claim fails or narrows

## Attack 2: Coverage audit

Reconstruct the A atomic coverage map. Give every requirement, component, and sub-question one terminal state. Flag anything present in A but absent from B or C as `SILENT OMISSION`. A missing item automatically fails D until restored or explicitly excluded. Do not accept a compound requirement row as proof that each named component was covered.

## Attack 3: Relationship audit

Rebuild the structural invariant checklist. For every material figure, comparison, policy, legal statement, and reporting claim, retest the applicable denominator, unit, nesting, additivity, status, effective period, and reporting-state transition. Compare the claim wording with the evidence at the same relationship strength.

An accurate value attached to the wrong denominator, period, status, or state fails. A repeated source does not repair the relationship. Demote every affected component and dependent conclusion.

## Attack 4: Dependency audit

Trace each conclusion backward to evidence. Check that:

- every dependency ID exists
- indispensable assumptions are visible
- certainty does not exceed the weakest indispensable premise
- no conclusion rests on an unresolved relay, snippet, training claim, stale claim, or missing premise
- cross-lane conclusions came through C-Merge

Audit every exact Phase E figure and named capability. Reproduce calculations from their inputs, units, method, rounding, and sensitivity. Recheck sourced figures and capabilities against inspected evidence. Demote the item and its dependents when the audit fails. Remove any untraced incidental figure.

## Attack 5: Adversarial audit

For every material conclusion:

- write the strongest evidence-grounded counter-case
- test the most plausible alternative explanation
- run or inspect the disconfirming search
- state what evidence would reverse the conclusion
- write a pre-mortem with an observable failure signal

Search for direct counter-evidence to an existing claim. Record new counter-evidence in a D claim register with full evidence records. Open no unrelated research branch.

## Phase D artifact

```markdown
# [Title]: Phase D Audit

## Citation audit

| Claim ID | Entailment | Fitness | Freshness | Audit verdict | Demoted dependents | Repair |
|---|---|---|---|---|---|---|
| B1 | CONFIRMS | FIT | current | SURVIVES | none | none |

## Coverage audit

| R, component, or Q ID | Present in A | Evidence in B | Treatment in C | Terminal state | Omission verdict |
|---|---:|---|---|---|---|
| R1.a | yes | B1 | C1 | VERIFIED | present |

## Relationship audit

| Invariant ID | Component IDs | Dimension | Evidence | B verdict | D verdict | Demoted dependents | Repair |
|---|---|---|---|---|---|---|---|
| I1 | R1.a | denominator/unit/nesting/additivity/status/time/reporting state/other | B1 | CONFIRMED | SURVIVES | none | none |

## Dependency audit

| Conclusion ID | Path complete | Weakest dependency | Post-audit state | Post-audit certainty | Blocker |
|---|---:|---|---|---|---|
| C1 | yes | B4 | SUPPORTED WITH LIMITATIONS | MODERATE | ... |

## Calculation audit

| Calculation ID | Inputs resolve | Method reproducible | Result matches | Sensitivity adequate | Audit verdict | Demoted dependents |
|---|---:|---:|---:|---:|---|---|
| K1 | yes | yes | yes | yes | SURVIVES | none |

## Adversarial findings

| Conclusion ID | Strongest counter-case | Alternative explanation | Reversal evidence | Pre-mortem signal | Verdict |
|---|---|---|---|---|---|
| C1 | ... | ... | ... | ... | SURVIVES / NARROW / FAIL |

## Contradiction register

| Conflict ID | Evidence on each side | Resolution or bound | Final state | Required final-answer disclosure |
|---|---|---|---|---|
| X1 | ... | ... | CONTESTED | ... |

## D findings created from counter-evidence

[Full source and claim records for any new counter-evidence, or none.]

## Phase D gate

- Load-bearing empirical claims not audited: [none required, or IDs]
- Requirements, atomic components, or sub-questions not accounted for: [none required, or IDs]
- Structural invariants not audited: [none required, or IDs]
- Conclusions not dependency-traced: [none required, or IDs]
- Phase E exact figures or named capabilities not audited: [none required, or IDs]
- Parallel lanes absent from C-Merge: [none required, not applicable, or IDs]
- Material contradictions not resolved or carried: [none required, or IDs]
- Phase B readiness reconciles to visible rows: yes/no
- Proposed closure status: INCOMPLETE | TRACEABLE | AUDITED
- Silent omissions: [none required, or IDs]
- Unsupported conclusion dependencies: [none required, or IDs]
- Reviewer isolation: same context | fresh context
- Phase D: COMPLETE | INCOMPLETE
```

If D is not a fresh context, it must propose `INCOMPLETE`. A fresh D reviewer may propose `TRACEABLE` after record reconciliation, or `AUDITED` only after reopening or re-fetching load-bearing sources and checking entailment and structural relationships. Record the frozen artifact identity and reviewer action. If any component, invariant, citation, contradiction, dependency, or readiness label fails, propose `INCOMPLETE` and name the affected IDs.

Advance only surviving or explicitly conditional conclusions. When D is incomplete, return the affected IDs to B or C rather than patching them invisibly inside E.
