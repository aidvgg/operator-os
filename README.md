# Operator OS

Operator OS is a folder that holds your whole business: your clients, your prices, your
decisions, your invoices, your daily log, your brand voice. Everything is a plain text file you
can open, read and search. An AI coding agent (Claude Code, Codex, or a similar tool) reads the
rules in this folder and does the work with you: it writes the proposal, issues the invoice, logs
the day, and refuses to do the few things that must never happen by accident.

**New here? Start with [`GUIDE.md`](GUIDE.md).** It walks you through the first hour in plain
words. Once the folder is open in your agent, you say one sentence: "Set up Operator OS for me."
The agent asks you a few questions and does the rest.

[`SETUP.md`](SETUP.md) is the long version: the same setup, with every command spelled out and the
reasons behind each step. Read it when you want to know why, or when you would rather do a step
by hand.

## Who this is for

A solo operator who bills clients for work: a consultant, a coach, a freelancer, a one-person
agency, a small shop. You do not need to be technical. The agent does the technical work
(the commands, the file edits, the saved snapshots) and tells you what it did in plain words.
Builders who already use a terminal (the text window where you type commands) get the same
machinery, plus the reference sections below. Team or multi-operator use is not addressed: one logbook, one memory file, one operator.

## What you get

- One place for the truth about your business, in files you own and can read without any app.
- A branded proposal and a branded invoice you can generate as a PDF, with the invoice number
  taken from a register so it is never guessed.
- A daily log with a plan in the morning and a close at night, and a weekly review.
- A clock that surfaces anything with a deadline before it is late.
- Guardrails that stop bank details and keys from ever landing in a saved snapshot, and stop the
  agent from running the few commands that destroy history.

The template ships with a **fictional worked example** (Sam Rivera / Northwind Labs) so every
part of it can be run end to end on day one. The setup clears that demo and puts your
business in its place.

**Version:** 2.2.0. Changes per release: [`CHANGELOG.md`](CHANGELOG.md). The default branch is `main`.

---

The rest of this page is the reference for builders and the curious. You can skip it on day one.

## The shape

How the folder is laid out. Each row is one top-level folder and the one job it has.

| Directory | What it is |
|---|---|
| `knowledge/` | Curated, authoritative truth. `knowledge/memory.md` is the canonical state snapshot. |
| `outputs/` | Everything generated: proposals, invoices, content, research. Disposable relative to `knowledge/`. |
| `ai/` | The three ledgers: settled decisions, the error log, and tombstoned values that must not come back. Plus `AGENT_ROUTES.json`, the routing registry the adapter views are generated from. |
| `skills/` | Reusable generators, one folder per skill, each with a `SKILL.md` read before running. Provenance and licences for the vendored ones: `skills/VENDORED.md`. |
| `scripts/` | The guardrails, the deadline clock, the cash rollup, the backup, the agent-hands tools. |
| `templates/` | Message and document skeletons. |
| `.githooks/` | Pre-commit and pre-push enforcement. |
| `.claude/` | Claude Code host layer: settings, the PreToolUse guards, subagents, commands, workflows, and `product-marketing-context.md`, the router the vendored copy/SEO skills read before asking questions. |
| `.codex/` | Codex host layer: config, hook wiring for the same guard scripts, agent mirrors. |
| `raw/` | Quarantined dumps. Never truth until distilled. Gitignored, so it is absent on a fresh clone; make it when you have something to quarantine. |

## The guardrails

The checks that keep mistakes from reaching a client or a saved snapshot. Each is a small script
with one job, and each complains out loud rather than passing quietly.

- `scripts/repo-doctor` blocks secrets, protected-path writes, fake office files, expired pages,
  resurrected dead values, and stale generated views. Its secrets scanner is shape-based: it
  catches provider-prefixed key shapes (`sk-`, `gh*_`, `github_pat_`, `re_`, `xox*-`, `AKIA`),
  JWTs, PEM private-key blocks, and banking shapes (SWIFT/BIC, IBAN, ABA/routing and account
  numbers, plus phone-number shapes). It does **not** catch a bare hex or base64 token with no
  prefix, and it deliberately skips generic `password=` / `api_key=` assignment shapes because
  they fire on prose. Know the scope; do not read a clean scan as "no secret is possible here."
- `scripts/horizon` is the deadline clock, surfacing overdue and next-14-days commitments.
- `scripts/money` recomputes the cash rollup from the invoice register and fails on any
  disagreement. An empty register is not a disagreement: it writes a zeroed rollup that says the
  zero is structural, so `$0` is never ambiguous between a quiet month and a broken parser.
- `scripts/backup-sensitive` makes an encrypted archive of the local-only files.
- `scripts/pdf-check` and `scripts/docx-check` prove a generated document is really that format and
  not renamed text.
- `scripts/sync-agent-adapters` regenerates the cross-model adapter views and the per-skill discovery
  adapters from one routing registry, so Claude Code, Codex, Gemini CLI and GitHub Copilot get the
  same instructions from a single owner.
- `.claude/hooks/deny-env-access.py` and `.claude/hooks/deny-destructive-git.py` are PreToolUse
  guards: the first denies any agent tool call that references the gitignored key files, the second
  denies no-verify commits and pushes, sweep staging, hard resets, forced cleans and forced or
  deleting pushes. `scripts/test-git-guard` is the fixture suite that proves both still fire.

Command-string guards are a floor, not a fence. A guard that matches the text of a command can be
spelled around by a command that never writes the matched token. They stop the accidental and the
lazy; they do not replace filesystem-level permissions where a host offers them, and they do not
replace reading what your agent is about to run.

## Hosts

Which AI coding agents this works with, and how each one finds the rules. Claude Code is first-class: `CLAUDE.md` is read directly, and the `.claude/` layer wires the
guards, the subagents (`fact-check`, `price-attack`, `client-sim`), the commands and the workflows.
Codex runs the same contract through `.codex/` (config, hook wiring for the same guard scripts,
agent mirrors) plus `$skill` adapters generated under `.agents/skills/`. Codex gates that layer
twice: project trust makes `.codex/config.toml` and the agents live, and hook trust is a separate,
per-content-hash grant you make interactively by running `codex` at the repo root and accepting the
hook-review prompt; until you do, neither guard fires under Codex and Codex does not say so. Re-arm
after any edit to `.codex/hooks.json`. Details: `.codex/README.md`. Gemini CLI and GitHub Copilot get
generated instruction views (`GEMINI.md`, `.github/copilot-instructions.md`) that point back at the
canonical files. `ai/AGENT_ROUTES.json` owns the routing; `scripts/sync-agent-adapters --write`
generates `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, the daily-log workflow views,
and one discovery adapter per skill under `.agents/skills/` and `.claude/skills/`; none of them is
hand-edited, and `repo-doctor` blocks the commit if one drifts. Discovery is separate from
ownership: a skill is owned by `skills/<name>/SKILL.md`, and the per-host adapters only point there.

## Requirements

What has to be installed on your computer. If you are following `GUIDE.md`, your agent checks
these for you and tells you what is missing.

- **git**, and **Python 3.9 or newer**. Every script parses and runs on macOS's system `python3`
  (3.9.6); the floor is stated as a version so the claim is testable.
- **node** (any current LTS). Both PDF generators (`skills/proposal-creator` and
  `skills/invoice-creator`) are JavaScript run by node. `npm install` is needed only for the legacy
  `.docx` path.
- **Google Chrome** or Chromium for the PDF generators. Both generators search the default macOS
  and Linux install paths (`google-chrome`, `google-chrome-stable`, `chromium`, `chromium-browser`);
  set `CHROME_BIN` when yours lives elsewhere. Both generators are run by **node** and need no
  `npm install`.
- **poppler** (`pdfinfo`, `pdftotext`, `pdffonts`) for `scripts/pdf-check`.
- **rclone** plus a configured cloud remote, only if you use the encrypted off-site backup.

**Platform.** macOS is the reference platform and the only one the demo path has been run on end to
end. On Linux the launchd plists become cron lines (each scheduled script's docstring carries one), the
backup passphrase comes from a file named by `OPERATOR_OS_BACKUP_PASSPHRASE_FILE` instead of the
Keychain, and the `osascript` and `qlmanage` steps skip themselves with a one-line note; `SETUP.md`
notes each. Native Windows is untested; use WSL.

## Running cost

What this costs to run. The template is free software. Running it is not: you need an AI coding agent (a Claude Code
subscription or an API budget), and, only if you use them, paid third-party provider keys for the
LinkedIn and X fetch scripts (`scripts/li-fetch`, `scripts/x-fetch`), and an rclone-reachable cloud
remote for the backup. Nothing else phones home.

## Support

Where to ask for help or report a problem: GitHub issues. Bug reports and questions have templates under `.github/ISSUE_TEMPLATE/`. Before
opening a pull request read [`CONTRIBUTING.md`](CONTRIBUTING.md). Security-relevant reports:
[`SECURITY.md`](SECURITY.md).

## Licence

What you are allowed to do with this code and these files.

- First-party code and prose: MIT, see [`LICENSE`](LICENSE).
- The three redistributed font families: SIL Open Font License 1.1, text in
  `skills/FONT-LICENSES/OFL-1.1.txt`, copyright notices and provenance in
  `skills/FONT-LICENSES/NOTICE-fonts.md`.
- Vendored third-party skills: per skill, as recorded in `skills/VENDORED.md`. Four are MIT with
  the licence text in tree (`skills/LICENSE-mengto-skills`, `skills/NOTICE-mengto.md`); the rest
  are recorded with the licence as evidenced, and where the only evidence is an upstream README
  word the row says so rather than asserting MIT.
