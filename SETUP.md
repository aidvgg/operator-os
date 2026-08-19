# SETUP - make this your business OS

> **This is the reference, the long version.** If you are setting up for the first time, start
> with [`GUIDE.md`](GUIDE.md) instead. Open the folder in your AI coding agent and say
> "Set up Operator OS for me." The agent runs sections 2 to 4 of this file for you (the `onboard`
> skill, `skills/onboard/SKILL.md`), asks you the questions only you can answer, and tells you
> what it changed. Come back here when you want the why behind a step, or want to do one by hand.

This repo is a solo-operator "business OS": a git repo that IS your business. It ships with a
fictional worked example (Sam Rivera / Northwind Labs) so you can see every part working end to end.
This guide turns the demo into your real operation.

Read it top to bottom once. Then keep it open while you rebrand, the commands are copy-paste.

---

## 1. What this is, and the philosophy

The core idea: **your business lives in version control.** Clients, decisions, pricing, invoices,
daily logs, brand voice, research, all plain markdown and JSON in one repo. Nothing lives only in
your head or in a SaaS you cannot grep.

An AI coding agent is the operator that runs on top of it. `CLAUDE.md` at the repo root is its
**operating contract**, the rules it reads first, every session. It defines:

- a **precedence order** so conflicting facts resolve deterministically
  (`CLAUDE.md` -> `knowledge/memory.md` -> topic files -> everything else),
- a **task -> context -> output** routing table (where to read, where to write, which skill to run),
- **guardrails** (no secrets in committed files, verification steps baked into money-touching skills),
- **conventions that fight rot** (status banners, expiry dates, deadline tokens, tombstoned values,
  one owner per fact).

Three directories carry the load:

- `knowledge/` - curated, authoritative truth. `knowledge/memory.md` is the canonical state snapshot;
  everything else is depth on a topic.
- `outputs/` - everything generated. Disposable relative to `knowledge/`.
- `ai/` - the three ledgers. `DECISIONS.md` holds settled rulings that are not re-argued.
  `ERRORS.md` holds every mistake that reached you or a client, with the control that now prevents
  it. `TOMBSTONES.md` holds dead values that must never reappear un-bannered.

Everything else is machinery: `skills/` (reusable generators), `scripts/` (guardrails, clock, cash
rollup, backup, agent hands), `.githooks/`, `templates/`.

**The point of this template is the machinery and the conventions.** The Northwind Labs content is a
demo you delete.

---

## 2. First-run setup

The whole of sections 2 to 4 can be handed to your agent, and that is the supported path: open
the clone in Claude Code (or Codex) and say "Set up Operator OS for me." The `onboard` skill
(`skills/onboard/SKILL.md`, reachable as `/onboard` in Claude Code and `$onboard` in Codex) runs
these sections, asks you for the values only you know (identity, prices, channels, voice), and
never asks for bank or wire details: it points you at the one local file to fill in yourself.
`GUIDE.md` is the plain-words walkthrough of that path. The manual path below is the same work
done by hand, and the reference for what the skill does. If you hand it over, read the summary
it gives you at the end and look at the diff.

**Requirements before you start:** git, Python 3.9 or newer, and node (both PDF generators are
JavaScript run by node; `npm install` is only for the legacy `.docx` path). Google Chrome or a
`CHROME_BIN` override for PDFs, poppler for `scripts/pdf-check`. macOS is the reference platform
and the only one this path has been run on end to end. On Linux, every step below that names
launchd, the Keychain, `osascript` or `qlmanage` needs a substitute, and each such step says so
where it appears. Native Windows is untested; use WSL.

From the repo root.

```bash
# 1. Wire the guardrails (pre-commit + pre-push) - one time per clone
git config core.hooksPath .githooks

# 2. Create your real payment-details file from the committed scaffold (gitignored, stays local)
cp knowledge/business/invoices/PAYMENT-DETAILS.template.md \
   knowledge/business/invoices/PAYMENT-DETAILS.md

# 3. Provider keys for the agent-hands scripts, if you use them (gitignored)
cp .env.example .env.local
```

Then open `knowledge/business/invoices/PAYMENT-DETAILS.md` and fill in your real wire details.
This file is **gitignored on purpose**. Bank and wire numbers never enter a committed file. The
invoice skill copies the wire block from here and nowhere else, and it only ever reads this file.

Sanity check the guardrail is live:

```bash
git config core.hooksPath   # prints: .githooks
scripts/repo-doctor
```

What you should see on an untouched clone with steps 1 and 2 done:

```
repo-doctor: clean
```

That is the whole output, exit 0. `scripts/horizon` on the same clone prints `OVERDUE (0)`,
`NEXT 14 DAYS (0)`, one `EVENT GATES (1)` entry (the demo decision row whose review trigger is
`Gate = 30 real conversations logged`, a valid review shape, not a warning) and a
`backup: .backup-marker absent` line that goes away after your first verified backup; its `--brief`
form, the one the session-start hooks run, is the single line
`horizon: 0 overdue, 0 in next 14d, 1 DECISIONS event gate(s); no verified backup recorded yet`.
Skip steps 1 and 2 and `repo-doctor` prints exactly two soft lines, each naming its own fix:

```
soft  payment-details-missing: knowledge/business/invoices/PAYMENT-DETAILS.md not on disk, invoicing is broken. Copy PAYMENT-DETAILS.template.md next to it and fill in the real values, which stay local-only
soft  hooks-unwired: run `git config core.hooksPath .githooks` (one-time per clone)
repo-doctor: 2 soft warning(s), no hard violations
```

Nothing else fires on an untouched clone. The demo data is dated so the clock stays quiet: the
demo `**Due:**` lines are either struck through with their outcome or rolled a year past release
in the repo's own rollover shape, the demo decision row is an explicit `Gate:` review that
`horizon` lists rather than nags, and every shipped `Stale after` page carries a date a year out.
If a run prints anything beyond the lines above, read it: it is about your machine or your edits,
not the demo. One machine-specific case: if Codex has run on your machine but you have not yet
trusted this repo's `.codex/hooks.json`, a soft `codex-hooks-untrusted` line tells you how to arm
it; it never appears where Codex has never run.

The Python floor is 3.9. Every script here parses and runs on macOS's system `python3` (3.9.6);
you do not need a newer one. The output above was measured on both 3.9.6 and a current 3.x.

**Background agents and the live tree.** `.claude/settings.json` ships
`"worktree": {"bgIsolation": "none"}`, so background agents in Claude Code run in the live working
tree rather than in a git worktree of their own. That is a deliberate default for a repo whose
sessions write into `knowledge/` and `outputs/` and expect to see each other's uncommitted work;
the containment is the "Agents and the live tree" rule in `CLAUDE.md` plus the destructive-git
guard, not isolation. If you would rather have background agents isolated, change the value to
`"worktree"` and expect their writes to land in a separate checkout you then merge.

### Optional, per capability

| You want | Install |
|---|---|
| PDF proposals and invoices | node (any current LTS; both generators are JavaScript run by node) and Google Chrome (set `CHROME_BIN` if it is not in the default location; on Linux the generators also look for `google-chrome`, `google-chrome-stable`, `chromium` and `chromium-browser` on the default paths) |
| `scripts/pdf-check` validation | poppler: `brew install poppler` on macOS, your distribution's `poppler-utils` package on Linux |
| The legacy `.docx` generators | `npm install docx` at the repo root |
| Encrypted off-site backup | `rclone`, configured with a remote (`gdrive:Backups` by default, override with `OPERATOR_OS_BACKUP_REMOTE`), then `scripts/backup-sensitive --init` once to mint the Keychain passphrase. Every other mode reads that passphrase and fails loudly if it is missing. On Linux there is no Keychain: set `OPERATOR_OS_BACKUP_PASSPHRASE_FILE` to a 0600 file outside the repo (for example `~/.config/operator-os/backup-pass`), run `scripts/backup-sensitive --init` once with it set to mint the passphrase into that file, and use a cloud remote of your own; `--ask-pass` types the passphrase instead of reading any store. |
| The unattended weekly backup | follow the INSTALL block at the top of `scripts/weekly-backup`. Step 2, the Full Disk Access grant, is not optional; the job dies without it. macOS only as shipped (launchd, Full Disk Access, `osascript`); on Linux schedule `scripts/weekly-backup --quiet` from cron with `OPERATOR_OS_BACKUP_PASSPHRASE_FILE` exported (the exact crontab line is in the NOT ON macOS block of that script's docstring), or a systemd timer running the same command. |
| The agent-hands read tools | provider API keys in `.env.local`, see `.env.example`. These are paid third-party providers, and that plus your AI coding agent (a Claude Code subscription or API budget) and the cloud remote for backup is the whole running cost of this repo; nothing else phones home. |

---

## 3. Rebrand checklist

Every spot that carries demo identity. Work down the list.

### 3a. The operating contract

`CLAUDE.md` is the highest-precedence file. Rewrite these sections to your operation:

- **Who / what** - you, your business, your money motions.
- **Voice + format rules** - the channel rules under X, LinkedIn and client messages are the demo's
  voice. Replace them. Keep the shape.
- **Pricing** - point the pricing-authority bullets at your own owner files.

Two craft rules ship as opinionated defaults, not as machinery. Keep them or drop them; the repo
does not care which, it only cares that you decide.

- **No em dashes, anywhere.** The `repo-doctor` check `emdash-paste` enforces it inside send-ready
  copy blocks: fenced blocks in `.md` files under `outputs/content/` and `outputs/outbound/`, HARD in
  both the staged and the full pass. Nothing else in the tree is scanned for dashes. If you write with
  em dashes, drop the rule from `CLAUDE.md` and `knowledge/voice/copy-rules.md` and either add a
  file-scoped allow entry for `emdash-paste` in `.repo-doctor-allow` or delete that check.
- **No call mentions before the CTA** in funnel assets. Prose only, owned by
  `knowledge/voice/copy-rules.md`; no check enforces it. Delete the line if it is not your rule.

Everything else in `CLAUDE.md` is machinery doctrine and transfers as-is.

### 3b. Logo and wordmark

Generated documents use a brand mark and a display font.

```bash
cp /path/to/your-logo.png skills/proposal-creator/assets/logo.png
cp /path/to/your-logo.png skills/invoice-creator/assets/logo.png
```

Both skills resolve `../assets/` relative to their generator script.

Three font families ship with the template, all three under the **SIL Open Font License 1.1**:
Space Grotesk (the display face, which is what the wordmark renders in), Inter Tight (body) and
JetBrains Mono (labels). The licence text is at `skills/FONT-LICENSES/OFL-1.1.txt` and the
copyright notices, versions and upstream projects are at `skills/FONT-LICENSES/NOTICE-fonts.md`.
Those files travel with the binaries because OFL condition 2 requires it. Keep them.

Swapping in a display font of your own is a four-part change, not a one-part change:

1. Drop the woff2 in **both** `skills/proposal-creator/assets/fonts/` and
   `skills/invoice-creator/assets/fonts/`. The two directories hold byte-identical copies today
   (six files, three families, two copies each), and each generator reads only its own.
2. Update the `@font-face` block in **both** generators. Each of
   `skills/proposal-creator/scripts/generate-proposal-html.js` and
   `skills/invoice-creator/scripts/generate-invoice-html.js` carries its own three blocks, and the
   font is inlined by explicit filename as a base64 data URI, so a file dropped in the directory
   with no matching edit changes nothing. Change one generator and not the other, and a proposal
   and an invoice drift apart in a way nobody notices until a client sees them side by side.
   Set each block's `font-weight` range to the weight axis your font actually has. The two
   generators do not agree with each other today, and neither exactly matches the binaries
   (measured `wght` axes: Space Grotesk 300 to 700, Inter Tight 100 to 900, JetBrains Mono 400 to
   800). Out-of-range values clamp rather than fail, so a wrong range is invisible until a weight
   you asked for renders as one you did not.
3. Update `skills/FONT-LICENSES/NOTICE-fonts.md` and the licence file next to it. A notice
   describing fonts the repo no longer ships reads as verified and is worse than no notice.
4. Check what the licence of your new font actually permits. OFL is not the only shape; some
   licences forbid embedding, and every one of these files is embedded in the PDF you send.

The shipped subsets are latin only: 229 to 231 codepoints each, covering ASCII, the common accented
latin range and a handful of punctuation and currency marks. `Á` is in. `Ł`, Cyrillic and CJK are
not. A client or project name carrying a character outside that set renders as a missing glyph in
the PDF you send. Open the rendered file before sending, which the pre-send checklist tells you to
do anyway.

### 3c. Brand strings in the document generators

Open each and change the brand name, email and entity constants:

- `skills/proposal-creator/scripts/generate-proposal-html.js`
- `skills/invoice-creator/scripts/generate-invoice-html.js`
- the legacy `generate-proposal.js` / `generate-invoice.js` if you use the docx path

Search case-insensitively and search for the brand and the entity separately. No single spelling
covers every file:

```bash
grep -rniE 'northwind|rivera|sam@northwindlabs' skills/proposal-creator skills/invoice-creator
```

The demo carries the identity in five shapes, and a case-sensitive search for one of them misses
the rest: `Northwind Labs`, the all-caps `NORTHWIND LABS` that the legacy docx generators render,
the proposal entity line `Northwind Labs (operating under Rivera Holdings LLC)`, the invoice footer
`Rivera Holdings LLC` plus `dba Northwind Labs`, and `sam@northwindlabs.example`, which does not
appear in every file.

That grep hits **nine** files, not the four generators. The other five are prose and reference
material that a rebrand has to reach too:

- `skills/proposal-creator/SKILL.md` and `skills/invoice-creator/SKILL.md` - the run instructions,
  which name the signing entity and the from-entity default.
- `skills/proposal-creator/references/data-schema.md` - the sidecar field reference.
- `skills/proposal-creator/references/design-standard-2026-08-02.dc.html` and
  `skills/invoice-creator/references/design-standard-2026-08-02.dc.html` - the design source of
  record for each document type.

The two design-standard files are specimens: real-shaped documents kept so the layout is judged as
a rendered page rather than as a spec. Their embedded numbers are deliberately dead and their
header banner says why. They are billed to `Kestrel Wholesale`, a client that appears nowhere else
in the tree, has no folder under `knowledge/clients/`, no roadmap and no ledger row. That is the
control, not an oversight: a specimen billed to a real client is a second price for an engagement
that already has an owner file. **Kestrel Wholesale is machinery, not demo content.** It stays when
you delete the demo clients in section 4. Re-rooting a specimen onto a live client removes the
control rather than editing the file.

### 3d. Invoice numbering

- `knowledge/business/invoices/INVOICE-LEDGER.md` - change the `NL-` prefix and reset
  `NEXT INVOICE NUMBER`.
- `scripts/money` - update **both** invoice-number patterns so the cash parser recognizes your
  numbers. There are two on purpose and they are not interchangeable. The register parser holds an
  inline `re.search(r"(NL-\d{4}-\w+)", inv_cell)` that reads the number out of a `SUMMARY.md` row.
  Further down, `INVOICE_NUM_RE` runs against per-invoice record filenames and is deliberately
  tighter, so a `_Project-Name` suffix on a filename is not swallowed into the number; the comment
  above it explains that split. Change one and leave the other and the two halves disagree about
  what an invoice number looks like.
- `scripts/repo-doctor` - a third copy of the shape lives in the `summary-openbalance` check
  (`re.search(r"NL-\d{4}-\w+", ln)`). This one fails silently rather than loudly: leave it on the
  demo prefix and the check stops seeing any Register row at all, so it can never warn you about a
  "nothing outstanding" claim sitting above an unpaid invoice. The comment above it says the same
  thing. Change all three in one pass and rerun `scripts/money` to prove the parser still reads
  your register.

### 3d-bis. The one place your own name is functional, not prose

`scripts/repo-doctor` bakes the operator's first name into a validation regex. The `sidecar-trace`
check's `_ORIGIN_OK` accepts exactly four `scopeTrace` origin strings, two of which name the
operator: `asked by client YYYY-MM-DD`, `asked by client YYYY-MM-DD, extended by Sam`,
`Sam added YYYY-MM-DD`, and `already live, not billable`. Leave it on the demo name and every
proposal sidecar you write with your own name in the origin cell reports `sidecar-trace` as outside
the documented vocabulary. Change the two `Sam` tokens there, and change the same vocabulary where
it is documented in `skills/proposal-creator/references/data-schema.md`, in the same pass.

Every other `Sam` in `scripts/` is prose or generated instruction text. Only these two are read by
a regex, and this grep proves it on your own tree:

```bash
grep -rn "Sam" scripts/ | grep -E "re\.(compile|search|match|sub|findall)|r\"|r'"
```

### 3e. Money config

Near the top of `scripts/money`:

- `FIXED_COSTS` - your real recurring costs and their citations. Each row cites the file that owns
  the number, so a cost change has one place to land. That owner is
  `knowledge/ops/tools-and-stack.md`, so rewrite it in the same pass. Leave it on the demo stack
  and every citation `money` prints points at a file describing somebody else's tools.
- `OWNER_ALIASES` - the alias map that collapses multiple bill-to spellings into one beneficial
  owner for concentration math. The demo collapses two spellings of the same client. Replace with
  yours.
- `TARGET_RECURRING` / `TARGET_BUFFER` - your recurring-revenue and cash-buffer targets.

### 3f. Backup and scheduled jobs

In `scripts/backup-sensitive`, rename before your first run or you will generate a passphrase under
the template's names:

```python
KEYCHAIN_ACCOUNT = "operator-os"
KEYCHAIN_SERVICE = "operator-os-backup"
```

The two launchd jobs ship as `scripts/com.northwindlabs.weekly-backup.plist` and
`scripts/com.northwindlabs.morning-brief.plist`. Rename the files and the `Label` inside each to
your own reverse-DNS identifier, then follow the INSTALL block at the top of the matching script.

Both jobs are macOS only as shipped: launchd, the Keychain, `osascript` notifications and the Full
Disk Access grant have no Linux equivalent here. On Linux skip the plist rename and use cron
instead: both `scripts/weekly-backup` and `scripts/morning-brief` carry a NOT ON macOS block in
their docstring with the crontab line, and `scripts/backup-sensitive` reads its passphrase from the
file named by `OPERATOR_OS_BACKUP_PASSPHRASE_FILE` (see its PASSPHRASE STORE paragraph); the
Keychain constants above then do not apply.

Rename the plist and the INSTALL block goes stale in the same move. Those blocks are prose inside
`scripts/weekly-backup` and `scripts/morning-brief`, and every `sed`, `launchctl bootstrap`,
`kickstart` and `bootout` line in them names the old `com.northwindlabs.*` label. Copy them out,
swap the label, and update the block in the script so the next person to install the job is not
copying a path that no longer exists.

### 3g. Cross-model adapter routing

`ai/AGENT_ROUTES.json` owns the workflow aliases and the mode-scoped action ids.
`scripts/sync-agent-adapters` owns their fixed instruction text. After any identity change that
touches them:

```bash
scripts/sync-agent-adapters --write
```

That regenerates every generated surface: the three agent entrypoints `AGENTS.md`, `GEMINI.md`
and `.github/copilot-instructions.md`, the two daily-log skill views, the three thin Claude
commands `.claude/commands/standup.md`, `eod.md` and `weekly.md`, and one thin skill adapter per
skill under both `.agents/skills/<name>/` and `.claude/skills/<name>/` (the `skill_adapters` rows in
`ai/AGENT_ROUTES.json`; 56 surfaces in total as shipped). **Never hand-edit any of them.**
`repo-doctor` blocks a commit when they drift from what the generator would produce.
`scripts/sync-agent-adapters --check` is the read-only version and prints
`agent-adapters: clean (N generated surfaces)` when nothing has drifted, where N is the count of
rows in the registry.

There is deliberately no `.claude/commands/plan.md`. Claude Code owns `/plan` as its built-in plan
mode, so the generator skips that one file and planning routes through a natural-language alias
instead. The exception is recorded in `ai/AGENT_ROUTES.json`, and the absence is enforced: create
that file and `--check` fails with `reserved platform surface must remain absent`, which
`repo-doctor` raises as a HARD violation.

**The brand name in those views is not in the registry, and grepping `ai/AGENT_ROUTES.json` for it
finds nothing.** It is a Python string literal inside `render_agent_entrypoint` in
`scripts/sync-agent-adapters`, in the list that builds the file header (do not count lines; use the
grep below):

```python
    lines = [
        HEADER,
        "# Northwind Labs agent entrypoint",
```

That one literal renders as the **first heading** of all three agent entrypoints, `AGENTS.md`,
`GEMINI.md` and `.github/copilot-instructions.md`, so it is the first line every non-Claude agent
reads about who it is working for. Find it without counting lines:

```bash
grep -n 'agent entrypoint"' scripts/sync-agent-adapters
```

Change it in the generator, never in the views, then rerun `--write`. Only the three entrypoints
change; the skill views, the skill adapters and the three Claude commands do not carry the brand
name. Editing a view directly is what `repo-doctor` blocks.

### 3h. Rewrite the canonical knowledge

These are the identity core. Rewrite them, do not find-and-replace, actually describe your operation:

- `knowledge/memory.md` - the state snapshot: who you are, active clients, money motions, live
  decisions, tools, open questions. Keep the four anchor headings (`### Motions`, `### Clients`,
  `### Money`, `### Open questions`). `repo-doctor`'s `core-restatement` check is anchored on three
  of them: it reads `### Clients` to `### Money` and `### Money` to `### Open questions` as pointer
  regions, which may name an owner file but must never restate a figure. Rename or drop one of
  those headings and the check reports itself blind rather than passing quietly.
- `knowledge/business/brand_foundation.md` - positioning, ICP, offer.
- `knowledge/business/outbound-offer.md` - your productized offer and its price. This file is the
  pricing authority for that motion.
- `knowledge/voice/copy-rules.md` - the craft rules. These mostly survive a rebrand.
- `knowledge/business/operator-business-profile.json` - regenerate cleanly with the
  `business-profile-creator` skill rather than editing the demo JSON by hand.

---

## 4. Clear the demo data

Once your identity is in, wipe the demo transactions so the numbers are yours.

```bash
# Demo clients and invoice records
rm -rf knowledge/clients/acme-retail/ knowledge/clients/beacon-health/
rm -f  knowledge/business/invoices/NL-2026-*.md

# Demo logbook (inspect first if you have already logged real days)
rm -f  knowledge/ops/logbook/days/*.md knowledge/ops/logbook/reviews/*.md

# Demo research and generated outputs (keep the directories, their READMEs, and the gate)
rm -f  knowledge/research/smb-ops-tooling-scan-*.md
find outputs -type f ! -name README.md ! -name prospect-gate.md -delete
```

Two exclusions in that `find` matter, and both are load-bearing rather than tidy.

`outputs/outbound/prospect-gate.md` sits under `outputs/` but it is **machinery, not a generated
artifact**: it is the single owner of the qualification rules that `skills/prospect-brief` applies
on every run, and `CLAUDE.md`'s routing table reads from it. Drop the `! -name prospect-gate.md`
and you delete a qualification ladder the skill depends on, then discover it on the next brief.
Tune its ladder to your own market; do not delete it.

`! -name README.md` keeps every folder's README, including the nested
`outputs/outbound/briefs/README.md`. Those READMEs document each folder's contract. `-name` matches
basenames at any depth, which is what makes one clause cover all of them.

Run verbatim on a fresh clone, that block deletes exactly the three demo proposal artifacts from
`outputs/` (`acme-phase3-ops-dashboard-data.json` and the `.html` / `.pdf` pair) and leaves seven
files: the six READMEs and the gate.

Two pages the wipe keeps carry a `**Stale after:** 2027-09-01` line: `knowledge/business/linkedin-safety-rules.md`
and the recurring-costs table in `knowledge/ops/tools-and-stack.md`, and the gate itself,
`outputs/outbound/prospect-gate.md`, carries the same date. Those dates were set a year past the
template's release so a fresh clone stays quiet, not because anything was verified on that day. When
you rewrite those pages for your own numbers, set the date your sources actually rot on; when the
date passes, `repo-doctor` prints `stale-page` and the fix is to re-verify or supersede, never to bump
the date.

Then empty the registers, leaving table headers and structure intact:

- `knowledge/business/invoices/INVOICE-LEDGER.md` - remove the demo rows, reset the next number.
- `knowledge/business/invoices/SUMMARY.md` - clear the register rows, **and reset the two
  cash-status lines to `$0` in the same edit.** These are one change, not two. `scripts/money`
  cross-checks its computed totals against those human-written lines and refuses to write when they
  disagree, so rows-removed-but-totals-left gets you `collected mismatch: computed $0 but register
  states $10,000, refusing to write wrong numbers` and a non-zero exit. That is the check working.
  Fix the lines, do not work around it.
- `knowledge/ops/logbook/LOGBOOK.md` - clear the index, reset the `LAST LOGGED` cursor.
- `knowledge/ops/logbook/STATS.md` - zero the rollup.
- `knowledge/pain-points/pain-point-bank.md` and `.csv` - clear the demo entries, keep the schema.
- `ai/DECISIONS.md`, `ai/ERRORS.md`, `ai/TOMBSTONES.md` - clear the demo rows, keep the headers and
  the format documentation. Keep the Hazards section in `ERRORS.md` if the hazards apply to you,
  and read it before deleting any of it: **a hazard is a licence.** Roughly a dozen `repo-doctor`
  checks cite a specific hazard or incident row as their justification, because `CLAUDE.md` says a
  check must trace to one. Delete a hazard bullet and you silently orphan the checks that name it.
  Drop the hazard, or drop the checks it licenses, but not one without the other.

`knowledge/business/MONEY.md` is not on that list and must not be hand-edited. It is generated, and
a hand-written figure in it is the exact failure the one-owner rule exists to stop. It is also the
one demo file that survives every delete above still holding demo cash, so **regenerating it is
part of finishing this step, not a later chore.** Run the three in this order:

```bash
scripts/money       # rewrites MONEY.md from the now-empty register
scripts/horizon     # 0 overdue, 0 upcoming
scripts/repo-doctor
```

`scripts/money` **succeeds on an empty register.** It exits 0 and writes a rollup that is zero
everywhere except fixed burn and the targets, headed by a `## Register is empty` block saying the
zero is structural. That distinction is the whole point: zero-because-nothing-was-billed and
zero-because-the-parser-broke are different facts, and the file says which one you are looking at.
An unreadable register never reaches the file at all. The moment a row exists but cannot be read,
`money` still exits 1, names the row, and writes nothing.

Order matters twice here. Run `money` **after** emptying the register, not between deleting the
`NL-2026-*.md` record files and clearing the rows: with the records gone and the open row still
there, `money` correctly refuses, because every open receivable must carry an armed `**Due:**` line
in its own record file and that file no longer exists. And run `money` **before** `repo-doctor`, or
you get a `soft money-drift` line telling you `MONEY.md` is older than `SUMMARY.md`. Running
`money` is what clears it.

### The rewrite queue

Deleting the demo client, research and invoice files leaves a `soft dead-pointer` line for every
file that still cites them. On a verbatim run of the block above that is **12 findings across
7 files**:

| File | Dead citations it still carries |
|---|---|
| `knowledge/memory.md` | the Acme roadmap, the Beacon README |
| `knowledge/business/brand_foundation.md` | the Acme roadmap, the Beacon README, the research scan |
| `knowledge/business/invoices/SUMMARY.md` | the Acme roadmap, the Beacon README |
| `knowledge/pain-points/pain-point-bank.md` | the Acme roadmap, the Beacon README |
| `knowledge/business/pricing-outcomes.md` | the Acme roadmap |
| `knowledge/clients/README.md` | the Acme roadmap |
| `ai/TOMBSTONES.md` | the Acme roadmap |

`repo-doctor` prints the first ten findings in that class and counts the rest, so the first run
shows ten lines and `dead-pointer: …and 2 more`. Rerun it as you clear them. That list is your
rewrite queue, and every entry is a real edit: these files describe the demo operation in prose,
so replacing the path alone leaves a sentence about somebody else's clients.

The finish line is exact and reachable: **`repo-doctor: clean`**, with no soft lines at all. Section 2
done, this section done, the queue worked and `scripts/money` rerun gets you there. That state means
the payment-details file exists, the registers parse, the cash rollup was regenerated from your own
numbers, and nothing points at a file that is gone. Anything still printing after that is about your
content, not about the demo, and worth reading rather than dismissing.

`scripts/horizon` clears in the same pass. Immediately after the delete block it reports 0 overdue
and 0 upcoming, because every demo `**Due:**` line lived in a file you just removed. One line
survives longer, under `EVENT GATES`: the demo decision row whose review trigger is
`Gate: 30 real conversations logged`. That is a valid review shape, not a warning, and it goes when
you clear `ai/DECISIONS.md`.

---

## 5. How the guardrails work

Small scripts, each doing one job. They are the OS's reflexes.

| Guardrail | When it runs | What it does |
|---|---|---|
| `scripts/repo-doctor --staged` | pre-commit | Blocks the commit on secrets, wire and credential shapes, protected-path writes, fake office files, expired pages, resurrected tombstoned values, stale generated views. |
| `scripts/repo-doctor` (range) | pre-push | The backstop a bypassed commit cannot outlive. Resolves what the remote actually holds with `git ls-remote`, then scans every transferred commit in a throwaway worktree. Blocks and names the offending sha. |
| `scripts/horizon` | session start, the daily-log plan and `/weekly` modes | The deadline clock. Surfaces overdue items and anything due in the next 14 days from `**Due:**` tokens across the repo. |
| `scripts/money` | after any invoice change | Cash rollup. Parses the register into `MONEY.md`: collected, outstanding, run-rate, concentration by owner. Fails loud on an unparseable row, a total that disagrees, or an open receivable with no armed `**Due:**` line. An **empty** register is not a failure: it exits 0 and writes a zeroed rollup that says so, so a `$0` here never has to be read as a broken parser. |
| `scripts/backup-sensitive` | on demand, weekly via launchd (macOS) or cron (Linux) | Encrypted archive of the gitignored local-only files. Passphrase lives only in your Keychain, or on Linux in the 0600 file named by `OPERATOR_OS_BACKUP_PASSPHRASE_FILE`. |
| `scripts/pdf-check` / `scripts/docx-check` | inside the document skills | Proves a generated file is really that format, not renamed text, before you send it. |
| `scripts/sync-agent-adapters` | after routing or contract changes | Regenerates the cross-model adapter views from one owner. |
| `.claude/hooks/deny-env-access.py` | every file-touching tool call (Read, Edit, Write, NotebookEdit, Grep, Glob, Bash) | Blocks any AI tool call that references a `.env` file. Keys are loaded by the wrapper scripts inside their own process. |
| `.claude/hooks/deny-destructive-git.py` | every Bash tool call | Denies no-verify commits and pushes, sweep staging (`add -A`, bare-dot adds, `commit -a`), hard resets, forced cleans, worktree-discarding checkout, restore and switch forms, branch force-deletes and forced or deleting pushes. Plain push stays open because the commit protocol requires it. `scripts/test-git-guard` is the fixture suite that proves both PreToolUse guards still fire; run it after any edit to either. Both are wired identically for Codex in `.codex/hooks.json`, and Codex hook trust must be armed interactively before they run there. |

Both PreToolUse guards match the text of a tool call. That is a floor, not a fence: a spelling that
never writes the matched token passes, so use filesystem-level permissions where your host offers
them and read what the agent is about to run.

The design principle across all of them: **fail loud, never silently pass.** A guardrail that is not
sure stops you. A scan that could not complete is not a scan that came back clean.

### The agent-hands failure contract

`scripts/x-fetch`, `scripts/li-fetch` and `scripts/reddit-scan` are the read tools an agent calls to
fetch outside data. They talk to providers over the network, so they fail more often than anything
else here, and an agent reading a failure as an empty result is how a live account gets written up
as a dead one. All three guarantee the same contract, and it is worth knowing because your agent
will be parsing their output:

- **Every failure is one line on stderr naming the provider, the operation and the cause. Never a
  traceback.** Exit is non-zero.
- **A missing key never touches the network.** `scripts/x-fetch` exits 1 naming both key variables;
  `scripts/li-fetch` exits 1 saying it refuses to run because an empty digest would read as a thin
  profile.
- Timeouts, dropped connections and provider 429/5xx are retried a bounded number of times with
  announced backoff. **4xx, non-JSON bodies and empty bodies are never retried**, because a decode
  fault repeats.
- An empty 200 body is reported as a provider fault, explicitly not as "nothing to report".
- A bad numeric flag is a one-line message, not a stack trace:
  `reddit-scan: --days needs a whole number, got 'abc'`, exit 1.

`scripts/reddit-scan` scans a grid, so its exit code answers "can I trust this file", not "was
everything perfect". **Exit 0 means the report stands**, with individual query failures listed under
its Query errors section. **Exit 1 means the artifact is incomplete** and says which kind at the top
of the file: `PARTIAL SCAN` (stopped early, keeps what it collected) or `FAILED SCAN` (nothing
answered, so the empty result is infrastructure, not market signal). It writes the report before it
records what it has seen, so a crash between the two can never mark candidates seen that no file
ever held.

### The escape hatch

`.repo-doctor-allow` holds narrow, dated exceptions:

```
<check-id> <path-glob>[::<token-glob>] reason=<text> expires=YYYY-MM-DD
```

`expires=` is mandatory and may not sit more than 90 days out, so an exception cannot quietly become
permanent. All three ways of getting it wrong are HARD violations that name the line number:
`allow-expired` when the date has passed, `allow-too-long` when it is more than 90 days out, and
`allow-syntax` on a malformed line. The syntax case skips only that line, so one typo cannot switch
the scanner off for everything under it.

Two more things about it that are easy to get wrong:

1. The entry is read from the **pushing checkout**, not from the commit it excuses. So an entry added
   in a later commit does clear an older commit in the same push range. That is the remedy when a
   tightened check retroactively condemns something an unpushed commit carried legitimately.
2. `git commit --no-verify` skips the staged check for one commit only. The push-time range scan is
   what catches it. `git push --no-verify` excuses nothing and skips everything, so it is strictly
   the worse tool.

---

## 6. Daily use

Read each skill's `SKILL.md` before first use.

**daily-log** - the accountability, stats and journal layer. Four modes.

| Mode | What it does | How you invoke it |
|---|---|---|
| plan | Open the day, set tasks, sync with your calendar | **Say "plan my day"**, not `/plan` |
| standup | Mid-day check-in | `/standup`, or say "standup" |
| eod | Close the day, log what shipped, recompute stats | `/eod`, or say "log my day" |
| weekly | The week's rollup | `/weekly`, or say "weekly review" |

**There is no `/plan` command and typing it will not open your day.** Claude Code owns `/plan` as
its own built-in plan mode, so `.claude/commands/plan.md` deliberately does not exist and the
generator refuses to create it. Planning routes through a natural-language alias into the generated
daily-log skill instead. `ai/AGENT_ROUTES.json` owns the alias list, and these are the exact strings
it registers for the plan mode:

```
plan my day        plan the day        let's plan my day
let's plan the day daily plan          daily planning
```

The other three modes ship as thin command files as well as aliases, which is why they work either
way. Their alias sets, also from the registry: `standup` / `daily standup`; `eod` / `log my day` /
`end of day` / `close the day`; `weekly review` / `weekly retro`.

You speak, the agent writes the row. It never seeds its own tasks; the list is yours. Close the
previous open day before planning a new one.

**proposal-creator** - branded proposal, quote or SOW as PDF. Embeds a fresh-context fact-check and
a price-attack pass. Output -> `outputs/proposals/`. The shipped demo proposal PDF under
`outputs/proposals/` is regenerated with `TZ=UTC` in front of the generator command so its
`CreationDate` carries no local timezone offset; do the same before committing any PDF you intend to
publish (a client deliverable does not need it). Both generators require node and Google Chrome or
Chromium; see the Requirements line in section 2.

**invoice-creator** - branded invoice as PDF. Always reads the next number from `INVOICE-LEDGER.md`,
never guesses. Wire block from `PAYMENT-DETAILS.md` only. Output -> `outputs/invoices/`.

**business-profile-creator** - read-and-merge update of your business profile JSON. Never blank-slate
rebuilds.

**prospect-brief** - turns a prospect URL into a decision-ready brief against your qualification
ladder in `outputs/outbound/prospect-gate.md`. No send authority.

**research-doctrine** - phase-separated research discipline for decision-grade work. Read
`skills/research-doctrine/OPERATOR-INTERNAL.md` alongside `SKILL.md` when running it in this repo.

**hard-task** - the Tier-2 protocol for high-stakes work no skill covers. `/hard-task` in Claude
Code, `$hard-task` in Codex; any other host reads `skills/hard-task/SKILL.md` and follows it.

**harvest** - end-of-session content harvest: 1-3 receipt-backed seeds to `outputs/content/seeds/`.
Never posts.

**The vendored craft library** - 17 third-party reference skills for copy, page types, CRO, SEO and
design-engineering. Reference tier: your doctrine, voice and pricing rules override anything they
model. Provenance and licences in `skills/VENDORED.md`.

---

## 7. The conventions that keep it from rotting

These are the habits that make a repo-as-business survive contact with time. They are enforced
mechanically where a check is possible.

- **Status banners.** A superseded file or number gets a bolded `SUPERSEDED - see <path>` line at
  the top, or the dead number gets struck through. A file that dies without a successor gets
  `**DEAD - <why>**`.
- **Expiry.** Anything true-today-not-forever carries `**Stale after:** YYYY-MM-DD` with a word on
  why. `repo-doctor` flags expired pages, so staleness announces itself.
- **Dated commitments.** Anything with a deadline carries `**Due:** YYYY-MM-DD - <what>` in the file
  that owns it. Resolve it by striking it through with the outcome, never by deleting it silently.
- **Tombstones.** Superseding a number means, in the same session: grep the dead value repo-wide,
  banner every hit, and add the string to `ai/TOMBSTONES.md`. `repo-doctor` then blocks it from
  coming back un-bannered.
- **One owner per state fact.** A price, deal stage or KPI lives in exactly one file. Satellites
  point at the owner. Every copy is a future stale line.
- **Error ledger.** Any mistake that reached you or a client gets one line in `ai/ERRORS.md` with
  the control that now prevents it. New rules must trace to a real entry there. No speculative
  process.
- **Ratchet rule.** A session that fixes a class of problem ends by adding the check that makes that
  class un-reintroducible. Cleanups without ratchets are rented, not owned.

### Upgrades

There is no upgrade tool yet. Your identity edits live in the files section 3 names (`CLAUDE.md`,
the generators, `scripts/money`, `scripts/repo-doctor`, `scripts/backup-sensitive`, the plists,
`scripts/sync-agent-adapters`, and the canonical knowledge files), and several of those are the same
files a later template release changes. So a new release must be merged by hand: read its
`CHANGELOG.md`, diff the machinery files against your copy, and carry the fixes across without
losing your constants. Keeping your first rebrand as one clean commit makes that diff readable
later. A config layer that separates identity from machinery is the intended fix; it is not shipped.

### Rhythm

- **Session start:** the agent reads `CLAUDE.md`, then `knowledge/memory.md`, then the topic files
  for the task, then `ai/DECISIONS.md` before anything decision-shaped. `horizon` surfaces what is due.
- **When you learn something durable** (a client, a price, a decision): it goes into `knowledge/`.
  Refine the existing line, do not append a parallel one. Let stale things die.
- **A session that wrote `knowledge/`** ends with commit and push. Git is the backup and the audit
  trail for the repo that is your business. The hooks have the last word.

That is the loop. The repo remembers so you do not have to.
