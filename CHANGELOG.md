# Changelog

All notable changes to this template are recorded here. The format follows Keep a Changelog
(https://keepachangelog.com/en/1.1.0/); versions follow Semantic Versioning. The version of record
is the `version` field in `package.json`; `README.md` restates it and this file explains it.

## [Unreleased]

## [2.3.0] - 2026-10-21

A sync of fixes and capabilities from the operating repo this template is drawn from: a third host,
a shared guard library, new evidence tools, four first-party skills and a research doctrine rebuild.
Existing Codex clones must re-arm hook trust because `.codex/hooks.json` changed; Grok Build needs
folder trust once (`grok --trust`).

### Security

- Hardened `.claude/hooks/deny-env-access.py` across target fields, scoped glob selectors, maps,
  lists, bounded shell reconstruction and patch target headers. Malformed envelopes now fail closed,
  while known prose and code fields remain writable.
- Claude Code, Codex and Grok Build now route every tool name through the env guard.
- The env guard protects the key files in the primary checkout and in every linked worktree, and
  fails closed on malformed `.git` metadata. Dot-segment globs are normalized before matching.
  Quoted-delimiter heredoc bodies no longer false-deny, and a fail-closed deny carries a neutral
  reason that says no protected path was matched.
- Both hook adapters fail closed when the guard library cannot load, and the git guard now denies
  invalid hook JSON instead of crashing open.
- `.githooks/pre-push` sets `umask 022`, so the scan worktree's files are 0644 under any caller umask.

### Changed

- Guard logic moved to `scripts/lib/agent_guards`, with thin hook adapters under `.claude/hooks/`.
  `scripts/test-git-guard` expanded from 132 to 414 assertions, including all three host wiring
  files, malformed envelopes, near-miss false-positive controls and library-hook parity.
- `research-doctrine` rebuilt as a self-routing assurance protocol: no Mode or Phase declaration,
  atomic coverage, assurance classes L0-L3, and a Closure Ledger the producing context cannot raise
  past `INCOMPLETE`. `skills/research-doctrine/README.md` and `references/agentic-harness.md` removed.
- `scripts/repo-doctor`: a successful no-argument run is cached outside the repo, in
  `~/.cache/operator-os-repo-doctor/`, behind a fingerprint of the tree, git state, environment,
  interpreter and Codex user config. Any argument or change bypasses the cache; the new `--uncached`
  flag forces a full scan. The tombstone scan prefilters on an ASCII anchor before regex work.
- `CLAUDE.md`: required reads go through `scripts/read-context` with a context checklist; the
  decision ledger is read through `scripts/ledger-index`; new rules for grounding recommendations,
  ask before assert, verified absence and `eoc` closeout; the ratchet rule is replaced by fixing an
  error class through single-sourcing the fact; the pre-send checklist gains the approval receipt and
  the exact-bytes check.
- The generated `AGENTS.md` names Codex and Grok Build as owning `/plan`.

### Added

- Grok Build host layer (`.grok/`: config, hooks, three agent views). See `.grok/README.md`.
- `scripts/read-context`, a paged reader for tracked Markdown and text, and `scripts/ledger-index`,
  a pointer index over `ai/DECISIONS.md` and `ai/ERRORS.md`.
- `scripts/artifact-receipt-check`: approval and transition receipts that bind a send to the exact
  bytes approved.
- `scripts/agent-guard`, a CLI over the guard library.
- `scripts/extract-pdf-text`, `scripts/transcribe-media`, `scripts/scan-transcript-loops` and
  `scripts/llm-draft`.
- `scripts/x-fetch` `--article`, `--include-replies` and `--via timeline|search`; `scripts/li-fetch`
  batch requests, `--gate` and `--balance`.
- Invoice generator: exact minor-unit arithmetic and currency validation before any output, and
  `--check-data <data.json>` to validate without Chrome. Proposal data option `signatureLines: false`.
- Skills: `run-coding-session` (repo baseline, task contract, fresh-context evaluation, opt-in net
  line budget), `decision-gauntlet`, `call-debrief`, `deep-research`.
- Verified-absence record validator (`skills/research-doctrine/scripts/validate_absence_records.py`)
  and its fixture suite.
- Remote-host bookkeeping pipeline: `scripts/agent-mutate` applies a required patch to licensed
  skill paths only, from a clean listed-path start, and commits only with `core.hooksPath=.githooks`;
  judgment or owner-file proposals land in `outputs/inbox/`, and `scripts/agent-apply-inbox` applies
  them only from a TTY after an APPROVED file whose `bundle_sha256` matches. Owner:
  `knowledge/ops/remote-agent-hosts.md`.
- CI runs the new test suites.

### Fixed

- The invoice schedule now requires exactly one row flagged `current: true`.

## [2.2.0] - 2026-08-19

The first-hour pass for non-technical operators. No change to the operating contract's doctrine;
the machinery is the same, the way in is new.

### Added
- `GUIDE.md`: the front door for a solo operator who is not technical and runs the OS through an
  AI coding agent. Plain words, one action per step, the real output quoted after each step.
- `skills/onboard/`: agent-run setup. The operator says "Set up Operator OS for me."; the skill
  runs the first-run steps, interviews the operator one plain question at a time (name, business
  and billing entity, email, what you sell, who you sell to, how you charge, channels, voice,
  invoice prefix, currency, timezone, optional tools; "skip" is an allowed answer), does the rebrand and the demo
  wipe, verifies with the scripts, makes the first commit, and ends with a plain summary. Bank and
  wire details are never typed into the chat; the skill names the one local file to fill in by hand.
  Discoverable as `/onboard` in Claude Code and `$onboard` in Codex through the generated adapters.

### Changed
- `README.md` first screen rewritten for the reader: what it is in plain words, who it is for
  (now including non-technical operators, with the agent doing the technical work), `GUIDE.md`
  as the first pointer, `SETUP.md` as the long version, what you get in five bullets. The builder
  sections below keep their facts and open with a readable sentence.
- `SETUP.md` is now the reference: a banner at the top points first-time setup at `GUIDE.md`, and
  section 2 names the `onboard` skill as the supported hand-to-agent path.
- `package.json` version 2.2.0.
- After a scripted walk of `GUIDE.md` by a fictional non-technical operator: the onboard skill
  now names every demo invoice-number string in the invoice skill (the four copies of the demo
  ledger's next number and the two format strings), runs the tree-wide proof grep at E4 after the wipe and the generator pass
  instead of right after the sweep, deletes the self-describing "Template note" section in
  `ai/DECISIONS.md` with the demo rows, and tells the agent to regenerate the adapters and rerun
  `scripts/money` before the E4 doctor run. `GUIDE.md` day 1 says where the plan lands, day 3 says
  to add the client before the first proposal, and section 8 says to ignore the checker's
  "escape hatch" wording. The daily-log skill states the day-file shape, since a wiped repo
  ships no example.

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
