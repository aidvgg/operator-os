# Operator OS

A solo-operator business OS: a git repo that **is** the business. Clients, decisions, pricing,
invoices, daily logs, brand voice, research, all as plain markdown and JSON under version control.
Nothing lives only in your head or in a SaaS you cannot grep.

An AI coding agent runs on top of it. `CLAUDE.md` is the operating contract it reads first, every
session: a precedence order so conflicting facts resolve deterministically, a task-to-context-to-output
routing table, and guardrails that fail loud.

This template ships the machinery plus a **fictional worked example** (Sam Rivera / Northwind Labs)
so every script, skill and guardrail can be run end to end on a fresh clone. The demo is deletable
scaffolding. The machinery is the point.

**Start with [`SETUP.md`](SETUP.md).** It covers first-run setup, the rebrand checklist, and how to
clear the demo data.

**Version:** 2.1.0. Changes per release: [`CHANGELOG.md`](CHANGELOG.md). The default branch is `main`.

## Who this is for

A solo operator, services or consulting shaped by default (the money model, prospect gate,
proposal and invoice skills assume you bill clients for work), who already runs an AI coding agent
and is comfortable in a terminal and git. Team or multi-operator use is not addressed: one logbook
cursor, one memory file, one operator.

## The shape

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

Small scripts, each doing one job, all of them failing loud rather than passing silently.

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

Claude Code is first-class: `CLAUDE.md` is read directly, and the `.claude/` layer wires the
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

The template is free software. Running it is not: you need an AI coding agent (a Claude Code
subscription or an API budget), and, only if you use them, paid third-party provider keys for the
LinkedIn and X fetch scripts (`scripts/li-fetch`, `scripts/x-fetch`), and an rclone-reachable cloud
remote for the backup. Nothing else phones home.

## Support

GitHub issues. Bug reports and questions have templates under `.github/ISSUE_TEMPLATE/`. Before
opening a pull request read [`CONTRIBUTING.md`](CONTRIBUTING.md). Security-relevant reports:
[`SECURITY.md`](SECURITY.md).

## Licence

- First-party code and prose: MIT, see [`LICENSE`](LICENSE).
- The three redistributed font families: SIL Open Font License 1.1, text in
  `skills/FONT-LICENSES/OFL-1.1.txt`, copyright notices and provenance in
  `skills/FONT-LICENSES/NOTICE-fonts.md`.
- Vendored third-party skills: per skill, as recorded in `skills/VENDORED.md`. Four are MIT with
  the licence text in tree (`skills/LICENSE-mengto-skills`, `skills/NOTICE-mengto.md`); the rest
  are recorded with the licence as evidenced, and where the only evidence is an upstream README
  word the row says so rather than asserting MIT.
