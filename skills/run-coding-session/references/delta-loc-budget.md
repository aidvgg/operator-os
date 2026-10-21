# ΔLOC budget

Opt-in. The rule binds only after the operator installs it with
`skills/run-coding-session/scripts/install_loc_budget.py` (see Enforcement below). Once installed, it
applies to every coding task, in every repository, on every host. A task may grow the codebase by at
most N net non-blank source lines:

    ΔLOC = LOC(added) - LOC(removed) <= N

- **N defaults to 300.** Only the user sets or raises N. When a task contract exists, record N in it.
- **Counted:** code files and extensionless shebang scripts, including untracked files and commits
  made during the session. **Not counted:** tests (reported, not budgeted), HTML, CSS, docs, data,
  config, and dependency, build, vendor or tmp directories.
- **Finish the work.** Implement end to end. Any new TODO, FIXME, XXX, HACK or not-implemented marker
  fails the check.
- **Growth is not free.** Before adding a helper, abstraction, adapter, compatibility layer or
  special-case branch, look for the smaller design.
- **Pay for growth with deletion.** When the change cannot fit, remove what it made obsolete: old
  paths, duplicated logic, superseded abstractions, compatibility code, dead branches. Replace the old
  behavior instead of wrapping it in a new condition.
- **No gaming.** Never fit the budget by cutting tests, error handling or required behavior, or by
  squeezing code onto fewer lines.
- **Measure before ending a turn:** run
  `python3 skills/run-coding-session/scripts/loc_budget.py check --repo <target>`, the script path
  relative to the operator repository root and `<target>` the absolute path of the repo under work
  (exit 1 means over budget).
- **If it truly cannot fit,** stop and give the user the measured ΔLOC and the N you need. Run
  `loc_budget.py set N` only after the user names N. Run `loc_budget.py reset` only after a task is
  accepted and committed, to start the next task's budget.

Enforcement: nothing is wired by default. The operator opts in by running
`python3 skills/run-coding-session/scripts/install_loc_budget.py` (`--check` reports what is missing
and changes nothing). Only that operator-run install writes outside the repository: it wires this
file into `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, and the checker into
`~/.claude/settings.json` (SessionStart, PreToolUse on edit tools, Stop) and `~/.codex/hooks.json`
(SessionStart, Stop; they run only after the user trusts them in `/hooks`), backing each changed file
up as `<file>.bak-loc-budget`. Agents and the onboarding flow never run it. The Stop hook blocks the
turn up to twice per overrun, then hands the overrun to the user. A Claude session is judged only in
repos where it used an edit tool. The rationale: agents grow codebases by default, so an explicit
net-growth ceiling forces the smaller design and makes deletion the way to pay for new code.
