# Existing repository branch

Establish what is true before proposing what should change. The baseline is an observation record,
not an architecture rewrite and not a claim that undocumented behavior is intentional.

## Baseline sequence

1. Read the target's agent instructions, contributor guide, primary README, manifests, lockfiles,
   CI definitions, architecture records, and advertised project commands.
2. Run the observer without writing into the target:

   ```text
   python3 <skill-dir>/scripts/observe_repo.py --target <absolute-target> --output <temporary-json>
   ```

3. Treat the observer output as an inventory lead. Resolve every load-bearing point against the
   actual target file or command before writing it into the baseline.
4. Identify the existing equivalents for agent context, architecture, product intent, quality
   rules, active plans, decision history, tests, CI, and runtime inspection.
5. Run the documented validation commands that are available without installing dependencies or
   reaching production. Record each command, exit status, and the first actionable failure. Record
   `NOT RUN` with the exact missing prerequisite when a command cannot run.
6. Compare git status before and after observation. Account for every new change. Baseline commands
   must not leave unexplained target modifications.
7. Write the result to the target's existing engineering-doc location, or default to
   `docs/agentic/BASELINE.md` using `assets/harness/BASELINE.md.template`.

## Evidence labels

Use one of these labels for every material statement:

- **OBSERVED:** supported by a named file, command, or runtime result.
- **INFERRED:** the evidence supports the interpretation but the repository does not declare it.
- **UNKNOWN:** the evidence is absent, contradictory, inaccessible, or not safely testable.

An inference cannot become an invariant merely because it looks sensible. Carry it into the
questions or task contract.

## Required coverage

The baseline is complete only when it accounts for:

- capture time, absolute target, git root, branch, commit, and pre-existing worktree changes
- governing instructions and their path scope
- project purpose as declared, plus product unknowns
- source topology, domain boundaries, entrypoints, and external integrations
- languages, runtime, package manager, manifests, generated code, and deployment surfaces
- advertised format, lint, type, unit, integration, end-to-end, build, and security checks
- CI jobs and the local command that most closely reproduces them
- the observed pass, fail, or not-run state of each available baseline command
- existing observability, fixtures, seed data, preview environments, and rollback mechanisms
- architectural risks, quality debt, contradictions, and unknowns relevant to the requested task
- existing harness capabilities and the missing capabilities the session may add

## Staleness

Put the captured commit and timestamp in the header and state that the file is a snapshot. Refresh
the baseline before planning when it is absent, when the recorded commit is not an ancestor of the
current work, or when manifests, architecture, CI, public contracts, or validation commands changed
materially. For ordinary feature commits, record the delta in the active task instead of rewriting
the whole baseline.

## Existing-project questions

Ask after the baseline, and only for unresolved decisions:

1. Which observable outcome decides that this task worked?
2. Which compatibility, architecture, or non-goal constraint is fixed but absent from the repo?
3. May the task add dependencies, migrations, public interfaces, or deployment changes?

Collapse answered questions. If none remains, begin the task contract without an intake round.
