# Security

This repository is a template for a git repo that holds a business. The interesting security
surface is therefore what an AI coding agent can do inside it, and what can leak through a commit.

## What the guards do

- `scripts/repo-doctor` (pre-commit on the staged set, pre-push on every transferred commit) blocks
  provider-prefixed key shapes (`sk-`, `gh*_`, `github_pat_`, `re_`, `xox*-`, `AKIA`), JWTs, PEM
  private-key blocks, banking shapes (SWIFT/BIC, IBAN, ABA/routing and account digit runs) and
  phone-number shapes, plus writes to protected paths and fake office files. Its exact pattern list
  is `SECRET_PATTERNS` in the script.
- `.claude/hooks/deny-env-access.py` scans target fields, scoped selectors, lists, maps, bounded
  direct shell forms and patch target headers for the gitignored key files. Malformed envelopes fail
  closed. The wrapper scripts load keys in their own process; agents call the scripts.
- `.claude/hooks/deny-destructive-git.py` denies no-verify commits and pushes, sweep staging, hard
  resets, forced cleans, worktree-discarding checkout, restore and switch forms, branch
  force-deletes and forced or deleting pushes from agent tool calls.
- The pre-push hook resolves what the remote holds with `git ls-remote`, scans every transferred
  commit in a throwaway worktree, and blocks on the first offending sha; a range it cannot fully
  scan is blocked, not sampled.
- Both PreToolUse guards are wired for Codex in `.codex/hooks.json`; the env guard uses a match-all
  selector on both hosts so new tools still reach it. The doctor's `codex-parity` check blocks a
  drift between the two host layers.

## What the guards do not do

- The secrets scanner is shape-based. A bare hex or base64 token with no recognisable prefix
  commits clean. Generic `password=` / `api_key=` assignments are deliberately not matched.
- The env guard reads only a tool-call envelope. Nested interpreters and external state can still
  synthesize a path without placing a detectable spelling or resolving selector in that envelope.
  It is a floor, not a fence: use filesystem-level permissions where your host offers them (Codex
  has a per-path filesystem permission profile; Claude Code has `permissions.deny`) and read what
  your agent is about to run.
- On Codex, hook trust is separate from project trust and is granted interactively per content
  hash. Until you arm it, Codex runs this repo with neither guard and prints no warning.
- Nothing here protects a machine that is already compromised, a leaked git remote credential, or
  a cloud remote you configured for the backup.

## Reporting

Open a GitHub issue for anything that is not itself a secret. If your report contains a live
credential or a real person's private data, do not put it in an issue: open an issue that says
only "security report, need a private channel" and the maintainer will reply with one. Do not
paste the payload anywhere public.

Please include: the file or script, the command or tool call, what you expected the guard to do,
and what it did.
