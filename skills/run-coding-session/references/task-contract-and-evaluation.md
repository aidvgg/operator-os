# Task contract and evaluation

The task contract is the state machine for one independently verifiable change. Its template is
`assets/harness/TASK.md.template`. Keep the contract stable while implementation changes beneath it.

## States

- `DRAFT`: discovery or a product decision is incomplete.
- `READY`: outcomes, protected surfaces, risk, and evidence are frozen.
- `IMPLEMENTING`: the builder is changing contract-owned surfaces.
- `VERIFYING`: implementation stopped and the evaluator owns the verdict.
- `ACCEPTED`: every required gate and criterion passed with recorded evidence.
- `BLOCKED`: a named external dependency or authority prevents progress.

Only evidence moves a task forward. A builder's confidence does not.

## Protected surfaces

Freeze the parts that define success before implementation:

- acceptance and regression tests created from the contract
- public API, event, schema, and migration expectations
- architectural dependency rules and security boundaries
- quality-gate configuration and evaluator rubric

The builder may propose a revision, but must stop, record the reason, and move the task back to
`DRAFT`. A test change that only makes the implementation pass is a rejection.

## Risk routing

- **Low:** local, reversible behavior inside an established pattern. Unified gates and a fresh
  general evaluator are sufficient for unattended completion.
- **Medium:** new feature path, dependency, background job, integration, persistent state, or public
  behavior. Require a fresh evaluator and runtime evidence.
- **High:** identity, authorization, money, destructive migration, cryptography, secrets, personal
  data, production infrastructure, irreversible external effect, or a new public contract. Require
  a fresh evaluator plus the relevant specialist and human judgment at the boundary decision.

## Evaluator packet

Give a fresh evaluator only:

- absolute target and governing instruction paths
- baseline and frozen task contract
- base and head commits or the exact diff
- documented commands and how to start the system
- fixtures or test identities that are safe to use

Do not include the builder's rationale, self-rating, or claim that the task is complete.

## Evaluator mandate

Use this mandate verbatim when dispatching a fresh evaluator:

```text
Act as a skeptical, read-only evaluator. Treat the task contract as authoritative and the builder's
work as an untrusted candidate. Do not edit code, tests, configuration, or task records. Reproduce
the baseline, inspect the diff, and try to falsify every acceptance criterion through the closest
user-visible surface. Exercise negative paths and state transitions. Check architectural boundaries,
public contracts, security-sensitive behavior, logs, and regressions proportional to risk. Return
ACCEPT only when every required criterion has concrete evidence. Otherwise return REJECT with exact
reproduction steps, expected versus observed behavior, affected paths, and severity. List anything
you could not test as UNVERIFIED.
```

## Reconciliation

The builder fixes `REJECT` findings, then a fresh evaluator reruns the affected criteria and the
full required gate. Record every finding as fixed, overruled with evidence, or still open. An
unexplained overrule blocks `ACCEPTED`.

## Review packet

The final task record must let a human judge outcomes without reading each file:

- what behavior changed and what remained out of scope
- which public interfaces, schemas, dependencies, or architecture edges changed
- commands and results, including the evaluator verdict
- user-level demonstration or artifact evidence
- residual risk, untested surfaces, rollback, and follow-up tasks

Track escaped defects, reopened tasks, evaluator disagreement, architectural violations, and
regression recurrence. Do not use generated lines, test count, or green-CI rate as quality proxies.
