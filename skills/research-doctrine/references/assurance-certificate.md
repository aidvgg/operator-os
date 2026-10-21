# Closure Ledger

The filename is retained for package compatibility. The artifact is a fail-closed Closure Ledger, not a self-issued certificate of truth.

Append it as the last substantive section of every research-grade Phase E answer. Build it from visible artifacts, not memory. It reports what can be traced, what remains unresolved, who performed the audit, and how the answer may be used.

## Status rules

Use exactly one status:

- `INCOMPLETE`: default; one or more hard gates fail, records do not visibly reconcile, or the audit boundary is unclear
- `TRACEABLE`: a fresh record-reconciliation reviewer verified that every hard gate and referenced ID visibly resolves in the frozen packet; source entailment was not independently re-checked
- `AUDITED`: a fresh source-auditing reviewer verified the frozen packet, reopened or re-fetched load-bearing sources, and checked entailment and structural relationships
- `TRIANGULATED`: `AUDITED` plus an independent model run used the same brief and claim-and-source reconciliation is visible

Never use `PASS`. Never translate a status into a probability of truth or a claim that important error is impossible. The producing context cannot assign a positive closure status. Its ledger remains `INCOMPLETE` pending a fresh closure review even when it has L1 traceability capability. A same-context role change is not fresh review.

## Required format

```markdown
## Closure Ledger

**Closure status:** INCOMPLETE | TRACEABLE | AUDITED | TRIANGULATED
**Assurance class:** L0 UNVERIFIED | L1 TRACEABLE | L2 INDEPENDENTLY AUDITED | L3 TRIANGULATED
**As of:** YYYY-MM-DD
**Answer or decision covered:** [one sentence]
**Use limit:** [unusable, conditional use with named limits, or decision use within named bounds]
**Evidence packet:** inline below | [durable locator available to recipient]
**Audit artifact:** none | inline below | [durable locator available to recipient]

### Capability and reviewer boundary

| Capability | Available | Used | Limitation or effect |
|---|---:|---:|---|
| Live source discovery | yes/no | yes/no | ... |
| Full source-body inspection | yes/no | yes/no | ... |
| Publication/effective-date verification | yes/no | yes/no | ... |
| Fresh-context reviewer | yes/no | yes/no | ... |
| Independent second model | yes/no | yes/no | ... |

- Producing context:
- Reviewer context: none | fresh | same context
- Reviewer action: none | record reconciliation | source audit | independent-model reconciliation
- Frozen artifact identity: [hash, version, or immutable locator]
- Highest status this boundary permits:

### Atomic coverage

| Component ID | Required component | Critical | Evidence or gap record | State | Consequence of residual uncertainty |
|---|---|---:|---|---|---|
| R1.a | ... | yes/no | B1 or F1 | VERIFIED | none |

### Structural invariants

| Invariant ID | Component IDs | Dimension | Required relationship | Evidence | Verdict | Consequence |
|---|---|---|---|---|---|---|
| I1 | R1.a | denominator/unit/nesting/additivity/status/time/reporting state/other | ... | B1 | CONFIRMED | none |

### Record resolution

| Referenced ID | Record type | Included or durable locator | Resolves | Defect if unresolved |
|---|---|---|---:|---|
| B1 | claim | inline | yes | none |

### Contradiction and failure reconciliation

| ID | Component or dependency IDs | Type | Final treatment | Visible in answer | Status effect |
|---|---|---|---|---:|---|
| X1 or F1 | ... | contradiction/null/retrieval failure | ... | yes/no | ... |

### Dependency and reversal check

| Conclusion or recommendation ID | Indispensable dependencies | Weakest state | Conditional or blocked | Reversal fact |
|---|---|---|---|---|
| C1 | B1, A1 | SUPPORTED WITH LIMITATIONS | conditional | ... |

### Silence test

- Areas challenged: actors, incentives, alternatives, implementation, failure, timing, security, regulation, and base rates
- New load-bearing components found: [IDs or none]
- Every new component added to atomic coverage: yes/no

### Failed gates

| Gate | Affected IDs | Smallest repair |
|---|---|---|
| none | none | none |

### Bottom line

[One sentence stating warranted reliance and the single largest residual risk.]
```

## Reconciliation rules

- Show one row per atomic component. Do not use a compound requirement row or prose such as "all covered" as a substitute.
- Show every structural invariant that can change meaning. Two correct values do not validate a comparison with mismatched denominators, units, periods, nesting, legal status, or reporting states.
- Show every referenced claim, calculation, contradiction, failure, dependency, and artifact ID in the record-resolution table. Do not substitute an unreconciled count.
- Give each failed retrieval a row tied to the affected component IDs. A blanket gap is not resolution.
- Compare the final answer with the contradiction, failure, and dependency records before assigning status. Any disagreement forces `INCOMPLETE`.
- Treat `SUPPORTED WITH LIMITATIONS`, `CONTESTED`, `UNKNOWN`, `OUT OF SCOPE`, and `EXPERT ROUTED` as visible states, not proof of decision safety.
- Any decision-critical `NOT CHECKED` item forces `INCOMPLETE`.
- If the full evidence packet is stored elsewhere, the locator must be durable and available to the recipient. An invisible record does not resolve.
- If an output or context limit prevents printing the required rows and no recipient-accessible ledger exists elsewhere, set `INCOMPLETE`. Brevity never authorizes a positive status without visible reconciliation.
- A producer may prepare this ledger but must leave closure `INCOMPLETE`. A fresh record-reconciliation reviewer may raise it to `TRACEABLE`; only a fresh reviewer who independently inspects the sources may raise it to `AUDITED`.
- Record the frozen artifact identity and reviewer action. Any later change to a covered claim, dependency, citation, calculation, recommendation, or ledger row invalidates the assigned status and resets closure to `INCOMPLETE`.

## Silence test

Before closing, ask:

> What material fact, scope condition, relationship, alternative explanation, implementation constraint, or actor incentive could reverse this answer but is absent from the atomic coverage matrix?

Add every plausible decision-reversing item as a component, or state why it is not plausible or is out of scope. Repeat until one full pass adds no load-bearing component. The silence test is an omission search, not proof that unknown unknowns do not exist.

## Automatic `INCOMPLETE` conditions

Use `INCOMPLETE` when any of these occurs:

- a requirement, atomic component, sub-question, or applicable invariant is absent
- a critical component lacks fit inspected evidence and lacks a specific visible gap state with consequence
- a load-bearing claim relies only on a snippet, relay, training recall, or inaccessible citation
- a cited passage does not entail the claim at the same scope and relationship strength
- a material contradiction, null result, or retrieval failure is omitted from the answer or ledger
- an exact figure or named capability lacks a resolving claim or calculation record
- a denominator, unit, nesting, additivity, status, period, or reporting-state invariant is wrong or unchecked
- a recommendation depends on `UNKNOWN`, `NOT CHECKED`, stale, failed, or decision-reversing contested evidence without becoming conditional
- an expert-routed matter is presented as decision-grade advice
- the status overstates reviewer isolation or triangulation
- a positive status was assigned in the producing context, lacks a recorded fresh reviewer action, or covers an artifact changed after review
- any referenced ID does not resolve to an included record or recipient-accessible locator
- an output or context limit suppresses required ledger rows without a recipient-accessible durable packet
- the Phase B readiness label, final answer, and ledger disagree
- the silence test is missing or its new components were not incorporated

State the failed gate without euphemism. Give the smallest repair and keep the answer's use limit explicit.
