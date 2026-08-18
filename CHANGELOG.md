# Changelog

All notable changes to this template are recorded here. The format follows Keep a Changelog
(https://keepachangelog.com/en/1.1.0/); versions follow Semantic Versioning. The version of record
is the `version` field in `package.json`; `README.md` restates it and this file explains it.

## [2.1.0] - 2026-08-19

Public-release hardening pass. No change to the operating contract's doctrine; every item is a
guard, a host layer, a notice or a doc made true.

### Added
- `LICENSE` (MIT) for the first-party code and prose; `package.json` gains `version` and `license`.
- `.claude/hooks/deny-destructive-git.py`: PreToolUse guard denying no-verify commits and pushes,
  sweep staging, hard resets, forced cleans, worktree-discarding checkout, restore and switch forms,
  branch force-deletes and forced or deleting pushes.
- `scripts/test-git-guard`: the fixture suite that proves both PreToolUse guards still fire.
- `.codex/` host layer: config, hook wiring for the same guard scripts, agent mirrors, plus the
  `codex-parity` doctor check that keeps the two host layers wired identically.
- Skill adapters for every skill (`.agents/skills/`, `.claude/skills/`) generated from a
  `skill_adapters` registry in `ai/AGENT_ROUTES.json`; the generator refuses an adapter whose
  canonical `SKILL.md` lacks `name` and `description` frontmatter.
- `skills/hard-task/` and `skills/harvest/` as skills both hosts can run; the Claude command files
  are now thin pointers.
- `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE/`.
- A non-Keychain passphrase path for `scripts/backup-sensitive`, so the backup runs off macOS.

### Changed
- `.claude/hooks/deny-env-access.py` updated to the current regex set (redirects, brace expansion
  and dot-glob spellings are now denied).
- `skills/prospect-brief/SKILL.md` gains `name` and `description` frontmatter so skills hosts can
  discover it.
- `skills/NOTICE-mengto.md` rewritten to describe only the four MengTo-origin skills that ship.
- `skills/VENDORED.md` rewritten as a per-item provenance and licence table; the ten skills whose
  only licence evidence is an upstream README word are recorded as exactly that.
- `README.md`, `SETUP.md`, `CLAUDE.md`: node named as a requirement (both PDF generators are
  JavaScript); platform statement made honest (macOS reference, Linux substitutes noted, Windows
  via WSL); secrets-scanner scope and the floor-not-fence nature of command-string guards stated;
  hosts paragraph rewritten (Claude Code first-class, Codex via `.codex/` plus `$skill` adapters,
  Gemini and Copilot instruction views); default branch `main`; version, support, running-cost and
  who-this-is-for lines added.
- The PDF generators look for Chrome or Chromium on the default Linux paths as well as macOS, and
  honour `CHROME_BIN`.
- The pre-push hook no longer hardcodes a macOS temp directory.
- `scripts/reddit-scan --help` prints help instead of starting a live scan.

### Fixed
- First-run false alarms on a fresh clone: `money-drift` no longer fires from checkout mtime order,
  and the demo's `**Due:**` lines no longer trip `clock-chronic` on day one.
- Demo `Stale after` dates handled so the demo does not rot in an adopter's clone.

## [2.0.0] - 2026-08-04

The v2 template: the machinery of a solo-operator business OS (operating contract, precedence
order, routing table, guardrail scripts, git hooks, document generators, daily-log, prospect-brief,
research-doctrine, business-profile-creator, the vendored craft library, the font licences) plus a
fictional worked example (Sam Rivera / Northwind Labs) so every path runs end to end on a fresh
clone.
