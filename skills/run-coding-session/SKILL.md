---
name: run-coding-session
description: "Run rigorous long-horizon AI coding work in a target repository. Use when starting, resuming, implementing, refactoring, debugging, or reviewing a substantial coding task against another repo, or when initializing a greenfield software project. Detect existing versus greenfield, baseline existing repos before questions, create or adapt the agent harness, freeze a task contract, and require executable gates plus fresh-context evaluation before completion."
---

# Run coding session

Turn a coding request into a bounded, observable control loop. Keep human attention on intent,
risk, and demonstrated behavior rather than file-by-file supervision.

## 1. Resolve the target

1. Resolve one absolute target path from the request and workspace evidence. If the request leaves
   multiple credible targets, ask only which path is in scope.
2. Run every target command with an explicit working directory or `git -C <target>`. Never let the
   inherited directory choose where a command lands.
3. Read the target repository's root agent instructions before other task actions, then read any
   nested instructions governing paths likely to change. Apply platform and user instructions
   first, then the target repository's instructions, then this skill.
4. Snapshot the target's git status. Treat every pre-existing change as user-owned. Work around it
   or use an isolated worktree; never discard, rewrite, or absorb it silently.
5. Classify the project:
   - **Existing:** implementation, manifests, or meaningful git history exists.
   - **Greenfield:** the target is absent or empty and the user asked to create it.
   - **Ambiguous:** documentation or scaffolding exists without clear implementation. Treat this as
     existing until evidence proves otherwise.

**Complete when:** the absolute target, instruction precedence, existing changes, and project mode
are explicit.

## 2. Establish state before intake

For an existing or ambiguous project, read
[`references/existing-repository.md`](references/existing-repository.md) and finish its baseline
procedure before asking product or implementation questions. The observation record is mandatory on
the first substantial task and must be refreshed when its recorded state is materially stale.

For a greenfield project, read
[`references/greenfield-project.md`](references/greenfield-project.md) and run its initializer
procedure.

If a prior active task contract exists, resume from its recorded state only after checking the
baseline, git history, and a smoke test against the live repository.

**Complete when:** an existing project has a commit-bound observation record, or a greenfield
project has a recorded product contract and initializer plan.

## 3. Ask only decision questions

Use the evidence already gathered. Ask no more than three questions in one round, and ask only when
the answer would change behavior, architecture, risk, or an external effect. Put the recommended
default in each question. Do not ask for facts available in the repository.

Proceed without a question when the request and repository already determine the answer. State a
reversible assumption in the task contract. Stop for authority when a choice would add production
access, a destructive migration, a new public contract, material security exposure, or an external
send or deployment outside the request.

**Complete when:** every material gap is answered, safely assumed, or named as an escalation.

## 4. Map or create the harness

Prefer an existing equivalent over a new file. Map these capabilities:

1. A short agent entry map pointing to authoritative context and commands.
2. An architecture map naming domains, dependency direction, and public boundaries.
3. Product and quality records that distinguish invariants from preferences.
4. A versioned active task contract and decision/progress log.
5. One project-native command that composes the relevant format, lint, type, test, build, and
   package checks.
6. A way for an evaluator to exercise the running system and inspect logs or other runtime evidence.

Use the files under `assets/harness/` only for missing capabilities. Adapt names and locations to
the target's conventions. Keep `AGENTS.md` a map, not a manual. Do not introduce duplicate sources
of truth.

**Complete when:** every capability has one authoritative owner and the target can tell a fresh
agent where to find it.

## 5. Freeze the task contract

Read [`references/task-contract-and-evaluation.md`](references/task-contract-and-evaluation.md).
Create or update one active task from `assets/harness/TASK.md.template`.

Before implementation:

1. Define observable outcomes, non-goals, invariants, affected public surfaces, risks, and rollback.
2. Bind every acceptance criterion to evidence such as a test, user journey, trace, metric, schema
   comparison, or artifact inspection.
3. Mark acceptance tests, public contracts, migrations, and quality gates as protected surfaces.
4. Demonstrate a red test for a bug or new behavior when the repository can express one without
   fabricating an implementation.
5. If the operator opted in to the ΔLOC budget (installed with
   `skills/run-coding-session/scripts/install_loc_budget.py`, never by default), record the budget N
   from [`references/delta-loc-budget.md`](references/delta-loc-budget.md). The default is 300 and
   only the user raises it.
6. Move the task to `READY` only when every criterion is falsifiable and no product decision is
   hiding inside implementation.

**Complete when:** the task contract is `READY` and the builder cannot redefine done while coding.

## 6. Implement one observable slice at a time

Work depth-first on one independently verifiable behavior. Keep the repository runnable between
slices. The builder may add implementation tests, but changes to protected surfaces require a
contract revision and an explicit reason before implementation continues.

After each slice, run the narrowest relevant checks. Before evaluation, run the unified task gate
and, when the ΔLOC budget is installed,
`python3 skills/run-coding-session/scripts/loc_budget.py check --repo <target>`, then inspect the
diff for scope drift, placeholders, duplicated patterns, unhandled states, public contract changes,
and unrelated edits. Fit an overrun by deleting what the change made obsolete, never by cutting
tests or required behavior.

When a failure exposes a reusable quality rule, encode the rule as a test, lint, fixture, template,
or evaluator criterion in the same task where practical. A prose reminder alone does not close the
failure class.

**Complete when:** the intended behavior works, the repository is green, ΔLOC is within budget when
the budget is installed, and the diff contains only contract-owned changes.

## 7. Evaluate with fresh context

Use a fresh evaluator for every medium- or high-risk task and for any task intended to run without
human file review. Give it the target path, frozen contract, diff, commands, and running system, but
not the builder's rationale or self-review. The evaluator must not edit code or protected tests.

Require the evaluator to try to falsify each criterion through the user-visible surface, APIs,
state transitions, logs, and architectural checks. Feed exact failures back to the builder and
repeat until the evaluator returns `ACCEPT` or a real escalation is reached.

If fresh-context execution is unavailable, label the result `SELF-VERIFIED`. Medium- and high-risk
work cannot be called independently verified or auto-merged under that label.

**Complete when:** every criterion has evidence, every evaluator objection is reconciled, and the
verdict is explicit.

## 8. Seal the checkpoint

1. Record commands, results, demonstrated behavior, evaluator verdict, residual risks, and untested
   surfaces in the task contract. Identify an atomic Git checkpoint as the commit containing the
   accepted receipt; do not write a guessed or self-referential commit hash into that same commit.
2. Update architecture, quality, or baseline records only when their owned state changed. A baseline
   remains a dated snapshot, not a live status page.
3. Leave one atomic commit or the target repository's equivalent checkpoint. Stage only task-owned
   paths. Push or deploy only when the request and target policy authorize it.
4. Leave the next session a clean start: current task state, exact next action, and no undocumented
   half-implementation.

**Session complete only when:** the task contract is `ACCEPTED`, required gates are green, fresh
evaluation passed or its honest cap is recorded, runtime evidence exists, unrelated changes remain
untouched, and the repository has a recoverable checkpoint.
