# Phase B: Gather

Load `evidence-standard.md`. Use the approved Phase A brief as the research contract. Gather evidence without recommendations.

## Gather procedure

For each sub-question in order:

1. Confirm every mapped atomic component, its criticality, and its invariant rows.
2. Search for the most direct primary evidence for each component.
3. Inspect the source body and preserve a supporting passage and locator.
4. Trace secondary evidence to its original evidentiary root.
5. Add an independent root for load-bearing or contested claims.
6. Run and record at least one disconfirming search.
7. Record negative results, contradictions, scope mismatches, and source failures against specific component IDs.
8. Test every applicable denominator, unit, nesting, additivity, legal or policy status, time period, and reporting-state relationship.
9. Apply the stopping rule separately to that sub-question.

Stop discovery when two consecutive fit, independent sources add no material claim or contradiction, or when the declared budget is exhausted. Record which condition stopped the work. Saturation never closes a component that lacks evidence or a gap state. Budget exhaustion leaves explicit component-level `NOT CHECKED` items.

Give evidence work priority over visible method narration. Preserve claims, passages, locators, component states, invariant verdicts, and failures first. Compress repeated search commentary into table rows. If a context or output limit threatens, reduce prose and source-list duplication before reducing evidence coverage.

## Phase B artifact

```markdown
# [Title]: Phase B Evidence

## Capability record

- Discovery available:
- Source-body inspection available:
- Date verification available:
- Material limitations:

## Atomic coverage status

| Component ID | Q ID | Critical | Status | Evidence IDs | Gap or consequence |
|---|---|---:|---|---|---|
| R1.a | Q1 | yes/no | VERIFIED | B1, B2 | none |

## Structural invariant verdicts

| Invariant ID | Component IDs | Dimension | Required relationship | Evidence IDs | Verdict | Consequence if failed |
|---|---|---|---|---|---|---|
| I1 | R1.a | denominator/unit/nesting/additivity/status/time/reporting state/other | ... | B1 | CONFIRMED | none |

## Source register

| Source ID | Title and publisher | URL or locator | Published/effective | Accessed | Tier | Evidence root | Scope |
|---|---|---|---|---|---|---|---|
| S1 | ... | ... | ... | ... | P1 | ... | ... |

## Claim register

| Claim ID | Exact claim | Q IDs | Type | Evidence | Fitness summary | Entailment | Freshness | State | Certainty and basis |
|---|---|---|---|---|---|---|---|---|---|
| B1 | ... | Q1 | empirical | [SOURCE:P1] S1 | direct; independent; current; scope fit; method transparent; incentive noted | CONFIRMS | as of ... | VERIFIED | HIGH: ... |

## Evidence passages

### B1 / S1

- Passage, 25 words or fewer:
- Locator:
- Material qualifier preserved:

## Search log

| Q ID | Query or method | Date | Purpose | Result and new evidence |
|---|---|---|---|---|
| Q1 | ... | ... | support/disconfirm | ... |

## Contradiction and null-result log

| ID | Q or claim IDs | Conflict or null result | Material effect | Next treatment |
|---|---|---|---|---|
| X1 | ... | ... | ... | carry to C / return to B |

## Retrieval-failure log

| Failure ID | Component IDs | Source or method attempted | Failure | Alternative checked | Component state | Consequence |
|---|---|---|---|---|---|---|
| F1 | R1.b | ... | blocked/dead/dynamic/missing cell/no result | ... | UNKNOWN | ... |

A failure row never supports a claim that the underlying fact, rule, event, or value does not exist. Give each affected component its own `UNKNOWN` state unless it was identified but not examined, in which case use `NOT CHECKED`.

## Verified-absence records

Use a verified-absence record only when a completed, bounded search establishes that a defined item was not found inside the inspected boundary. This is a search-method record, not a universal fact claim and not a new terminal state.

~~~json
{
  "absence_id": "A1",
  "q_ids": ["Q1"],
  "component_ids": ["R1.b"],
  "corpus_or_paths": ["policy/current/", "policy/archive/2025/"],
  "terms_and_synonyms": {
    "terms": ["automatic renewal"],
    "synonyms": ["auto-renewal", "renews automatically"]
  },
  "search_date": "2026-08-30",
  "tool_or_method": {
    "tool": {
      "kind": "EXECUTABLE",
      "identity": "ripgrep 14.1.1"
    },
    "procedure": "SEARCH_THEN_INSPECT_ALL_MATCHES",
    "parameters": {
      "terms_and_synonyms": {
        "terms": ["automatic renewal"],
        "synonyms": ["auto-renewal", "renews automatically"]
      },
      "corpus_or_paths": ["policy/current/", "policy/archive/2025/"],
      "options": ["CASE_INSENSITIVE", "FIXED_STRING", "RECURSIVE"]
    },
    "completion": {
      "declared_count": 42,
      "inspected_count": 42,
      "blocked_count": 0,
      "match_count": 0
    }
  },
  "inspected_count": 42,
  "retrieval_status": "COMPLETE",
  "scoped_result": {
    "outcome": "NOT_FOUND",
    "inspected_count": 42,
    "corpus_or_paths": ["policy/current/", "policy/archive/2025/"]
  },
  "consequence": {
    "mode": "BOUNDED_ABSENCE",
    "component_ids": ["R1.b"],
    "corpus_or_paths": ["policy/current/", "policy/archive/2025/"]
  }
}
~~~

The listed top-level fields are all required and are the only permitted top-level fields. Use a stable `A` ID, at least one Q ID and component ID, explicit corpus paths or corpus names, the exact terms and recorded synonyms, a real ISO calendar date, and a positive inspected-item count.

Every top-level corpus boundary must be unique and must be a specific name or path. Root paths and root file URIs, including drive-designator-only file URIs, any all-dot path segment, bare generic labels such as corpus or file, glob metacharacters, and unqualified totality labels such as all websites, everything, everywhere, whole, entire, global, universal, world, internet, web, company-wide, org-wide, organization-wide, or enterprise-wide are invalid. File URIs are parsed structurally: query and fragment data do not count toward boundary depth, percent-encoded paths are decoded before dot-segment checks, and authority or UNC-like forms require a resource or share segment beyond the host. Normal relative and absolute paths, specific file URIs, and bounded proper names such as `World Bank policy archive 2025` remain valid. The method, result, and consequence inherit the same boundary by exact mirroring.

`tool_or_method` is a closed object with exactly four fields:

- `tool`: exactly `kind` and `identity`. Kind is `EXECUTABLE` or `MANUAL`. Manual identity is exact `manual review`. Executable identity is a simple tool identifier plus semantic version, or a path or filename ending in `.py`, `.sh`, `.js`, `.exe`, or `.bin`. Narrative and non-executable paths such as `/tmp/report.txt` are invalid.
- `procedure`: `SEARCH_THEN_INSPECT_ALL_MATCHES` for `EXECUTABLE`, or `MANUAL_REVIEW_ALL_DECLARED_ITEMS` for `MANUAL`.
- `parameters`: exactly `terms_and_synonyms`, `corpus_or_paths`, and `options`. The first two mirror the top-level fields. Options are a unique nonempty list drawn from `CASE_INSENSITIVE`, `CASE_SENSITIVE`, `FIXED_STRING`, `REGEX`, `RECURSIVE`, and `LINE_BY_LINE`. Manual review uses exactly `LINE_BY_LINE`. Executable search uses exactly one case mode, exactly one match mode, optional `RECURSIVE`, and never `LINE_BY_LINE`.
- `completion`: exactly `declared_count`, `inspected_count`, `blocked_count`, and `match_count`. Every value is a non-boolean nonnegative integer. Both declared and inspected counts must equal the top-level `inspected_count`; blocked and match counts must both be zero.

`retrieval_status` must be `COMPLETE`. The closed completion record, not prose classification, makes blocked, partial, and positive searches incompatible with verified absence.

`scoped_result` is deliberately structural. It must contain exactly `outcome`, `inspected_count`, and `corpus_or_paths`. The outcome must be `NOT_FOUND`; its count and corpus must exactly equal the top-level values. This mirrored representation binds the result to the inspected count and boundary without trusting prose. It rejects positive findings, retrieval-failure narratives, hidden universal claims, and inconsistent counts. Put a positive finding in the claim register instead.

`consequence` is also a closed object. It contains exactly `mode`, `component_ids`, and `corpus_or_paths`. The mode is one of `BOUNDED_ABSENCE`, `UNKNOWN`, `NO_DURABLE_CLAIM`, or `QUESTION_OPEN`. Its ID and corpus arrays must exactly mirror the top-level arrays. No consequence prose is accepted.

A retrieval with any blocked item, uninspected declared item, or positive match cannot satisfy this schema. Log blocked or partial work under retrieval failures and positive findings in the claim register. The structural record validates internal consistency only; it does not inspect the corpus or prove that the recorded search occurred.

The optional standard-library checker accepts one JSON record or a JSON array. Use explicit absolute paths so the command does not depend on the caller's working directory.

~~~bash
# Repository checkout
python3 /absolute/path/to/repository/skills/research-doctrine/scripts/validate_absence_records.py /absolute/path/to/absence-records.json

# Extracted or installed package
python3 /absolute/path/to/research-doctrine/scripts/validate_absence_records.py /absolute/path/to/absence-records.json
~~~

The checker validates the closed record and its mirrored counts, IDs, corpus, result, and consequence. It does not inspect the corpus or independently prove that the recorded search occurred.

## Stopping verdicts

| Q ID | Stop condition | Last two independent sources | Unchecked work | Decision consequence |
|---|---|---|---|---|
| Q1 | saturation/budget | S4, S5 | none | none |

## Phase B gate

- Atomic components without explicit status: [none required, or IDs]
- Critical components without fit inspected evidence or a specific gap state: [none required, or IDs]
- Structural invariants without verdicts: [none required, or IDs]
- Sub-questions without a recorded disconfirming search: [none required, or IDs]
- Load-bearing claims without inspected source bodies: [none required, or IDs]
- Budget-exhausted or not-checked items: [IDs or none]
- Retrieval failures not mapped to component states: [none required, or IDs]
- Invalid, incomplete, or unbounded verified-absence records: [zero required, or IDs]
- Blanket absence conclusions from failed retrievals: zero required
- Silent critical omissions: zero required
- Readiness: READY | READY FOR CONDITIONAL SYNTHESIS | NOT READY
- Phase B: COMPLETE | INCOMPLETE
```

Use `READY` only when every critical component has fit inspected evidence and every invariant is confirmed. Use `READY FOR CONDITIONAL SYNTHESIS` when every component is explicit but one or more critical components are `UNKNOWN`, `CONTESTED`, or `SUPPORTED WITH LIMITATIONS`; name the required conditions. Use `NOT READY` when any component is missing, any critical relationship is unchecked, a blanket gap hides affected facts, a scoped absence lacks a valid verified-absence record, or a critical claim relies only on snippets, relays, or training recall.

Complete B only when every atomic component has a state, every invariant has a verdict, every sub-question has a disconfirming search and stopping verdict, and the readiness label reconciles to the visible rows. Do not let a strong search log compensate for missing or incorrect evidence.
