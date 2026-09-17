# Contributing

Issues are welcome: bugs, questions, a notice or attribution you want corrected. Use the templates
under `.github/ISSUE_TEMPLATE/`. Pull requests are welcome for machinery (scripts, hooks, skills,
docs); the fictional worked example is deliberately small and does not need more demo content.

Before you open a pull request:

1. Run `scripts/repo-doctor` from the repo root and get it clean, or explain every line it prints.
   The pre-commit and pre-push hooks run the same checks; wire them once with
   `git config core.hooksPath .githooks`.
2. If you touched a guard (`.claude/hooks/*.py`), run `scripts/test-git-guard` and add a fixture
   for the shape you changed.
3. If you touched routing or a `SKILL.md`, run `scripts/sync-agent-adapters --write` and commit the
   regenerated views with the change. Never hand-edit a generated view.
4. Keep one owner per state fact. A number, path or rule lives in one file; other files point at
   it. A second copy is a stale line waiting to happen and the review will ask you to remove it.
5. No em dashes anywhere in what you write, including commit messages. Comma, period, or a single
   hyphen. Vendored third-party skill files (see `skills/VENDORED.md`) are kept verbatim and are
   exempt from this rule.
6. A new check must trace to a real failure: an `ai/ERRORS.md` row or a hazard named there. No
   speculative process.

Stage explicit paths, never a sweep. Keep the pull request to one change; a doc fix and a guard
change are two pull requests.

By contributing you agree that your contribution is licensed under the MIT licence in `LICENSE`.
