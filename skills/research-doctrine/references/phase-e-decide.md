# Phase E: Answer or Decide

Load `assurance-certificate.md`. Use only the Phase D survivors and declared user preferences. Make the final output readable while preserving full traceability in the registers.

Resolve every exact number, date, threshold, rate, limit, price, sample size, and named capability in this artifact to an inspected claim, supplied-evidence record, or calculation ID. Cite the ID inline or include it in the evidence table. Remove untraced incidental figures.

## Research-answer variant

Use when the deliverable is an answer, comparison, explanation, or finding rather than a choice.

```markdown
# [Answer title]

## Answer

[Direct answer first. Distinguish established facts, bounded findings, and analysis.]

## What the evidence establishes

- [Conclusion ID]: [finding] ([state], [certainty], as of [date])

## Limits and contradictions

- [IDs, consequence, and whether the answer remains usable]

## What would change the answer

- [Reversal fact, threshold, or date]

## Load-bearing evidence and calculations

| ID | Bounded claim or value | Source passage and locator, or calculation method | Fitness or inputs | Freshness | Audit verdict | State and certainty |
|---|---|---|---|---|---|---|
| B1 or K1 | ... | ... | ... | ... | ... | ... |

## Traceability

| Output statement | Conclusion IDs | Load-bearing claim IDs | State |
|---|---|---|---|
| ... | C1 | B1, B4 | SUPPORTED WITH LIMITATIONS |

[Append the complete Closure Ledger.]
```

## Decision variant

Use when the deliverable is a recommendation or choice.

```markdown
# [Decision title]

## Recommendation

[One direct sentence, or a conditional decision when a reversal dependency is unresolved.]

## Why

| Reason | Conclusion IDs | Load-bearing claims | Post-audit state | Decision effect |
|---|---|---|---|---|
| ... | C1 | B1, B4 | VERIFIED | ... |

## Load-bearing evidence and calculations

| ID | Bounded claim or value | Source passage and locator, or calculation method | Fitness or inputs | Freshness | Audit verdict | State and certainty |
|---|---|---|---|---|---|---|
| B1 or K1 | ... | ... | ... | ... | ... | ... |

## Options considered

| Option | Evidence-backed advantage | Evidence-backed cost | Key assumption | Why selected or rejected |
|---|---|---|---|---|
| ... | ... | ... | A1 | ... |

## Risks accepted

- [Contradictions, weak dependencies, and residual uncertainty carried from D]

## Kill thresholds

| Signal | Threshold | Detection method | Action if crossed |
|---|---|---|---|
| ... | ... | ... | ... |

## Action plan

| Action | Owner | Due or sequence | Dependency | Evidence it worked |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Write-back plan

[Enumerate any state updates, supersessions, refresh dates, or decision records. Do not execute writes without the authority required by the host environment.]

[Append the complete Closure Ledger.]
```

Withhold an unconditional recommendation when any indispensable dependency is `UNKNOWN`, `NOT CHECKED`, stale, `CONTESTED` in a decision-reversing way, or `EXPERT ROUTED`. State the condition that would unlock it.

## Expert-routed E-draft

Use for decision-grade legal, tax, immigration, medical, or individualized investment matters.

```markdown
# [Title]: Draft-Grade Research for Expert Review

## Verified fact base

| Claim or calculation ID | Bounded claim or value | Source passage and locator, or calculation method | Fitness or inputs | Audit verdict | State and certainty | As of |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

## Options and what each turns on

[No go or no-go recommendation.]

## Consultation questions

| Question | Dependency resolved | What changes by answer |
|---|---|---|
| ... | ... | ... |

## Action boundary

- Required expert:
- Items marked EXPERT ROUTED:
- Do not act on:

## Not-advice statement

Draft-grade research for preparation only. Decision-grade output requires [qualified professional].

[Append the complete Closure Ledger. Expert-routed items may be accounted for, but the ledger covers research preparation only.]
```
