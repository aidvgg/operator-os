---
name: decision-gauntlet
description: "Adversarially test an idea, plan, price, build, or consequential choice in chat, one structured judgment question per turn. Use when Sam asks whether an idea is good, requests a stress test or devil's advocate, or wants a CHAT-ONLY SURVIVES, CHAT-ONLY DIES, or CHAT-ONLY PARKED recommendation. No files are written and no outcome authorizes action."
---

# Decision gauntlet

Pressure-test one proposed decision until its load-bearing dependencies survive, fail, or remain
unresolved. This is a chat-only advisory workflow. It writes no repository or external state,
changes no decision or initiative status, creates no task, and sends nothing.

## Preflight and routing

1. State the proposed decision, the material downside if it is wrong, and whether it is a small
   reversible choice or a consequential bet.
2. Read `knowledge/memory.md`, the current topic owner, and `ai/DECISIONS.md` before attacking the
   proposal. Read `ai/ERRORS.md` and `ai/TOMBSTONES.md` when the proposal touches money, a client
   artifact, or a superseded number.
   Apply `CLAUDE.md`'s canonical **Ask before assert, calculate before confirm** rule to every
   quantity, date, duration, motive, or derived value. This skill owns labels and question order,
   not a competing assertion rule.
3. If `ai/DECISIONS.md` already settles the choice, do not relitigate it merely because the user
   asked for a gauntlet. Report the ruling, owner, and review or reopening condition, then end with
   `CHAT-ONLY SURVIVES` when the proposal follows the ruling or `CHAT-ONLY DIES` when it conflicts.
   Reopen only when the recorded trigger or genuinely new contrary evidence exists.
4. Identify specialist ownership before interrogation when another workflow owns the necessary
   decision packet. Never invoke, hand off to, or start another workflow or subagent from inside a
   gauntlet run, including a workflow that might write only after later approval:
   - proposal, quote, SOW, or client pricing artifact: `proposal-creator`
   - invoice or agreed-work billing: `invoice-creator`
   - legal, tax, banking, entity, relocation, canonical rewrite, or irreversible client move:
     `hard-task`
   - current, disputed, multi-source, or decision-grade external evidence: `research-doctrine`
   - outbound prospect qualification: `prospect-brief`

The gauntlet may inspect an already-existing specialist-produced packet read-only after that
workflow has established its facts. If the required packet does not exist, end `CHAT-ONLY PARKED`,
name the separate workflow and exact inputs Sam may choose to invoke, and stop. Do not create a
task, message, handoff, artifact, or placeholder. A later gauntlet run may resume only after the
packet exists. The gauntlet never substitutes its own opinion for the specialist gate.

## Controlled vocabulary

Use only these labels while working:

- `FACT - VERIFIED`: directly supported by a reopened canonical owner or an inspected source.
- `FACT - OPERATOR-STATED, UNVERIFIED`: Sam supplied it, but no independent receipt was inspected.
- `FACT - UNKNOWN`: the fact is material and currently unresolved.
- `JUDGMENT - OPEN`: Sam has not chosen among the surviving tradeoffs.
- `JUDGMENT - OPERATOR-SETTLED`: Sam chose, or the decision ledger already records the choice.
- `RECOMMENDATION`: the agent's argued position, never a fact or authorization.

The agent handles facts. Retrieve, inspect, calculate, or route factual questions rather than asking
Sam to research them or choose which fact is true. When a material fact cannot be resolved, label it
`FACT - UNKNOWN` and ask only the judgment that follows, such as whether to park the decision or
proceed under an explicit condition.

## Interrogation contract

Ask exactly one structured question per turn. Each question must be a judgment call for Sam and use
this shape:

```text
Question: <one decision-bearing question>

A. <recommended option> (Recommended) - <reason tied to receipts>
B. <credible alternative> - <tradeoff>
C. <second alternative, including parking or a bounded version when appropriate> - <tradeoff>
Escape: correct the premise, supply a missing constraint, or park this branch.

Receipts: <canonical path and locator, inspected external source, or explicit UNKNOWN>
Dependency: <why this question must be resolved before the next branch>
```

Use the host's structured survey or question tool when it is available. Use single-select mode with
the recommended option first and the other two options after it. Rely on the tool's built-in Other
choice as the escape. If the host has no structured question tool in the current mode, render the
text shape above directly in chat, including the Escape line.

Put the recommended option first. Always include two credible, mutually distinct alternatives. The
escape is always real:
Sam may reject the choices, correct the premise, or park the branch without being forced into the
recommendation. Do not bundle intake questions, follow-ups, or a questionnaire into one turn.

Attack only with receipts. Every counterclaim must cite a reopened repository owner or an inspected
external source that entails it. An unsupported suspicion is not an attack and must not be phrased as
a fact. Record it as `FACT - UNKNOWN`, investigate it, or make the missing evidence the reason for a
parked outcome.

Walk dependencies in this order, skipping only branches already resolved by receipts:

1. **Demand or need:** what observed behavior proves the problem or opportunity exists.
2. **Current replacement:** what happens instead and what cost or constraint creates urgency.
3. **Economics and exposure:** real revenue, cost, capacity, downside, and reversibility at the
   evidenced volume.
4. **Smallest valid move:** the least scope that can test or deliver the claimed value.
5. **Timing and durability:** why now, what changes the answer, and what would make the move obsolete.

Do not ask a downstream question while an indispensable upstream fact or judgment remains open. A
small, cheap, reversible choice may need only the weakest one or two branches. A consequential bet
continues until every load-bearing branch is resolved or one terminal outcome is forced.

## Terminal recommendation

End with exactly one of these labels:

- `CHAT-ONLY SURVIVES`: the recommendation is to continue consideration. Name the strongest attack,
  why it failed, the conditions that must remain true, and the smallest next move Sam could
  separately authorize.
- `CHAT-ONLY DIES`: the recommendation is to stop. Name the fatal dependency, the receipts, what was
  still valuable, and the evidence that would justify reopening.
- `CHAT-ONLY PARKED`: one or more missing facts, specialist judgments, or unresolved upstream choices
  can reverse the answer. Name each missing item and the exact retrieval, specialist, or Sam choice
  needed to resume.

Every terminal response includes a compact fact and judgment register using the controlled
vocabulary. None of the three outcomes approves a build, changes scope, accepts a price, creates a
commitment, updates `ai/DECISIONS.md`, sends a client message, or authorizes any other action. State
that boundary in the terminal response.

## Completion check

The run is complete only when:

- no turn asked more than one question
- every question put the recommendation first and included alternatives plus an escape
- every asserted attack has a receipt
- facts and judgments use only the controlled labels
- dependencies were resolved in order
- settled decisions and specialist boundaries were honored
- no specialist workflow or subagent was invoked from inside the gauntlet
- the final label is exactly `CHAT-ONLY SURVIVES`, `CHAT-ONLY DIES`, or `CHAT-ONLY PARKED`
- no file or external state was written and no action was presented as authorized
