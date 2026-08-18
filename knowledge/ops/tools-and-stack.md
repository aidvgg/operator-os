# Tools and stack

What this file owns:

1. **The recurring cost lines.** Anything that leaves the account every month is listed once, in
   section 1 of this file. Nothing else in the repo states those numbers.
2. **The machine-side setup** a fresh clone needs to actually produce work: document pipeline,
   scheduled jobs, backup, secrets posture.
3. **Reversible tool choices**, dated, in section 10. A ruling that must not be re-argued belongs
   in `ai/DECISIONS.md` instead. The test is whether re-opening it wastes a session.

What it does not own: what the business charges (client roadmap files under `knowledge/clients/`,
and `knowledge/business/outbound-offer.md` for the productized offer), cash on hand
(`knowledge/business/invoices/SUMMARY.md`), or any live wire value.

---

## 1. Recurring costs

**Stale after:** 2027-09-01 - seat prices and plan tiers move on their own schedule. Re-verify each
line against the actual charge on the statement before this date, then move the date or cut the line.
(Demo stack: the date is set a year past the template's release so a fresh clone's clock stays
quiet. When you rewrite this table for your own stack, set the date your statements actually rot on.)

| Line | Monthly | What it buys | Kill condition |
|---|---|---|---|
| LinkedIn Sales Navigator | $100 | The sourcing seat for the manual outbound motion. Search, saved lists, profile depth. | Cut it if the outbound motion is paused, or if sourcing moves off the platform. It is the only line that is not load-bearing for delivery. |
| VPS + hosting | $20 | The always-on box: the site, and a place for a client-facing demo to sit that is not a laptop. | Cut it if nothing is deployed there for a full month. |
| AI API usage | $40 | Metered spend for the agent-hands scripts and generation work. Budget, not a contract. | Alarm, do not cut. If a month lands far over, the cause is a loop or a retry storm, not growth. |
| Accounting software | $30 | Books for the operating entity, and the export the year-end filing is built from. | Never, while the entity exists. |
| **Total** | **$190/mo** | | |

Fixed burn is deliberately tiny. That is a strategic position, not an accident: at this burn a slow
month is an inconvenience rather than an emergency, and no tool renewal ever forces a bad-fit
engagement. Every proposed subscription is judged against that, not against its own price.

**The mirror contract.** `scripts/money` hardcodes these four lines to compute burn, and each entry
there cites this file by name. The copy exists because the script must run without parsing prose.
It is still a copy, and a copy is a future stale line, so: **change the number here first, then in
`scripts/money`, in the same session.** If the two disagree, this file is right and the script is
stale.

Not on this list, on purpose:

- One-off spend (a domain renewal, a font licence, a book). Recorded at the monthly close, never
  modeled as recurring burn. A cost list that quietly absorbs one-offs stops being a burn number.
- Metered spend above the AI API budget. It gets read at the close as a signal, not smoothed into
  the fixed line.
- Anything with a free tier that is being used inside the free tier. When it starts charging it
  gets a row, on the day of the first charge.

---

## 2. The repo is the business

The whole operating system is plain files plus a handful of standard-library scripts. No database,
no dashboard, no workflow engine. Read `CLAUDE.md` for the contract these enforce.

| Script | What it does |
|---|---|
| `scripts/repo-doctor` | The gate. Secrets shapes, protected paths, fake office files, tombstoned values, expired pages, dead pointers, clock blind spots, generated-view staleness. Runs `--staged` from the pre-commit hook and full from the pre-push hook. |
| `scripts/horizon` | The clock. Reads owner-local `Due:` lines repo-wide and prints overdue plus the next 14 days. Run it at session start. |
| `scripts/money` | The metabolism. Generates the money rollup from the invoice register: collected, outstanding, run-rate, concentration by owner, burn from section 1 above. Fails loud rather than writing a guessed number. |
| `scripts/clock_grammar.py` | The single owner of the `Due:` / `Stale after:` grammar. Loaded by the three consumers above. Never re-copied into a fourth, because hand-copied grammars drift and then two scripts disagree about what "resolved" means. |
| `scripts/sync-agent-adapters` | Regenerates the cross-model views (`AGENTS.md`, `GEMINI.md`, the Copilot file, the thin command wrappers) from `ai/AGENT_ROUTES.json`. Never hand-edit a generated view. |
| `scripts/backup-sensitive` | Off-site, encrypted backup of the local-only set. See section 7. |
| `scripts/weekly-backup` | The unattended driver for the above, from a launchd agent. |
| `scripts/morning-brief` | Assembles the workday brief before the operator sits down. Read-only against `knowledge/` by construction: it holds none of the logbook write paths and cannot seed a task list. Its only write is the brief itself, into the local-only `outputs/ops/briefs/`. |
| `scripts/pdf-check` | Proves a `.pdf` is a real PDF that renders text, not a renamed file. |
| `scripts/docx-check` | Same for `.docx`: full package parse, not text extraction. |
| `scripts/x-fetch`, `scripts/li-fetch`, `scripts/reddit-scan` | Read-only agent hands. See section 5. |

---

## 3. Machine and dev stack

- **macOS**, one machine. Everything here assumes that and says so where it matters (Keychain,
  launchd, Full Disk Access).
- **python3**, system interpreter. Every repo script is standard library only, on purpose: a
  dependency install is a thing that can be missing at 9am on the day a client needs an invoice.
  The exception is the legacy document path in section 4.
- **git**, with `git config core.hooksPath .githooks` set once per clone. Without it both hooks are
  inert and the repo silently loses its gate. Setting it is step one of `SETUP.md`.
- **node**, only for the legacy `.docx` generators. `npm install docx` once at the repo root.
- **Google Chrome**, headless, for the document pipeline. `CHROME_BIN` overrides the path.
- **poppler** (`brew install poppler`), for `scripts/pdf-check`.
- **rclone**, for the backup remote and for pushing issued documents to the cloud drive archive.
  Binaries go up through rclone and are verified by checksum, never pasted through a tool that
  re-encodes them.
- **Claude Code** is the primary agent surface. Other model CLIs read the generated views produced
  by `scripts/sync-agent-adapters`, so the operating contract does not fork per model.

---

## 4. Document pipeline

Client-facing PDFs are print HTML rendered by headless Chrome. The design source of record for each
document type lives with its skill, under `skills/proposal-creator` and `skills/invoice-creator`.

The rule that matters: **a generated file is not a deliverable until a validator has opened it as
its real format.** Every PDF passes `scripts/pdf-check`, every `.docx` passes `scripts/docx-check`,
before anyone calls it done. This is not belt and braces. A generator that writes text and names it
`.docx` produces a file that passes a text-extraction sanity check and fails on the client's
machine, which is exactly how it once reached one (`ai/ERRORS.md`). Extraction cannot catch it.
Only opening the package can.

The `.docx` path is legacy and survives for one reason: a client who needs an editable file. New
work goes through the HTML-to-PDF path.

---

## 5. Agent hands, all read-only

`scripts/x-fetch`, `scripts/li-fetch` and `scripts/reddit-scan` fetch public data through paid
gateways or open APIs. They read. They do not post, follow, like, connect or message, and no script
in this repo ever will, because a send is an act of judgment and this stack drafts rather than acts.

Provider-side is the point: the vendor's infrastructure makes the request, so the operator's own
account is never the actor and cannot be rate-limited, flagged or banned for a research pull.
`x-fetch` carries a second provider on a different pipe, because the failure mode of a cheap
gateway is the vendor going dark, not the key expiring, and discovering that mid-brief is worse
than paying for redundancy.

Keys live in the gitignored env file at the repo root and are read inside each script's own
process. See section 8.

---

## 6. Scheduled jobs

Two launchd agents, both with their plist committed in `scripts/`:

- `scripts/com.northwindlabs.weekly-backup.plist` - drives `scripts/weekly-backup`.
- `scripts/com.northwindlabs.morning-brief.plist` - fires `scripts/morning-brief` on weekday
  mornings.

The committed plists carry placeholders the install step substitutes: `__REPO__` in both, plus
`__PYTHON__` and `__HOME__` in the brief job. Copy the `sed` line from the script header rather than
guessing which ones a given plist uses. Baking one machine's home directory into a committed file
makes the repo unusable
on any other machine and leaks local paths to anyone who reads it, which is why `repo-doctor` has a
check for exactly that shape.

**The Full Disk Access step is not optional.** macOS protects the desktop, documents and downloads
directories, and a launchd agent inherits none of the terminal's grants. If the repo sits in one of
those directories, the interpreter named in the plist needs Full Disk Access or the job dies before
a line of code runs, silently, forever. Install instructions and the uninstall path live in the
header of each script. Read those before installing, not after wondering why nothing has run.

---

## 7. Backup and recovery

`scripts/backup-sensitive` covers everything git deliberately does not: the wire block, the invoice
archive, personal and tax material, the quarantined inbox, and the agent auto-memory directory that
sits outside git entirely.

The flow: collect the protected set from `repo-doctor` itself (one source of truth for what is
sensitive), tar it, encrypt, HMAC the ciphertext, **decrypt it again and prove the restore**, upload
via rclone, verify the remote checksum, then write the marker file. Nothing is marked done unless
the archive decrypts and the upload verifies. Objects are named by date and content hash, and
nothing is ever deleted from the remote, so a same-day rerun cannot overwrite the object the marker
points at.

Destination: an rclone remote, `gdrive:Backups` by default, overridable per machine with the
`OPERATOR_OS_BACKUP_REMOTE` environment variable so the repo carries no one operator's storage
layout.

Passphrase: macOS Keychain, account `operator-os`, service `operator-os-backup`, minted only by
`scripts/backup-sensitive --init`. **A second copy belongs in the password manager on the day it is
minted.** A passphrase that lives only in the Keychain of the machine you are recovering from is not
a backup, it is a story about one.

`scripts/horizon` nags when the marker is more than three weeks old, and separately if the marker
predates authenticated integrity.

~~**Due:** 2026-07-30 - prove one restore from the object the marker names~~ done 2026-07-30, passphrase typed from the password manager rather than read from the Keychain, archive decrypted, members listed, canary file present, plaintext wiped.

Arm the next drill as a `**Due:**` line in this file on the day you run the current one. A backup
nobody has restored is a hope, not a control, and the only thing that turns one into the other is
someone typing the passphrase in and watching the files come back.

---

## 8. Secrets and the local-only posture

- **The wire block** lives only in `knowledge/business/invoices/PAYMENT-DETAILS.md`, gitignored.
  The committed sibling `PAYMENT-DETAILS.template.md` is the placeholder scaffold. `invoice-creator`
  reads that file and never writes it. No skill has a licence to change it; a skill that thinks it
  needs one is asking the wrong question.
- **Provider API keys** live only in the gitignored env file at the repo root. `.env.example`
  documents which keys exist without holding a value. No AI tool may read or edit those files: the
  deny rules in `.claude/settings.json` and the guard in `.claude/hooks/deny-env-access.py` enforce
  it mechanically rather than by asking nicely. Agents call the scripts, the scripts load the keys.
- **Local-only trees**: `personal/`, `outputs/ops/`, `outputs/invoices/`, and the per-research
  `local/` directories that hold unredacted contact details pulled from public sources.
- **Committed files may cite these paths, never restate their contents.** Name the fact class, not
  the counterparty, the identifier or the number. Pointers into them dangle on a fresh clone, and
  that is the designed behavior.
- `repo-doctor` blocks account-shaped, wire-shaped and credential-shaped strings on staged content,
  and the pre-push hook re-scans every commit in the range against the current checkout's rules, so
  a commit made while the gate was weaker cannot approve itself later.

---

## 9. Deliberately not in the stack

Each line is a decision, not an oversight.

- **No CRM.** Prospect state lives in the brief that produced it and in the logbook. A CRM at this
  volume is a second place for the same fact to rot.
- **No database, no dashboard.** Plain files are greppable, diffable, and readable by every model
  and every human without a client. The day a query is genuinely hard, revisit it here.
- **No outbound automation.** Sourcing and sending stay manual until the conversation gate in
  `ai/DECISIONS.md` is met. Automating a motion that has not been proven by hand scales a mistake.
- **No second capture inbox.** Tasks live in the operator's task manager. The logbook is
  accountability and stats, written by the acting agent, never a list maintained by hand in two
  places.
- **No general workflow engine.** Skills plus scripts cover the real work. An engine is a project
  that competes with client work and wins, because it is more fun.

---

## 10. Tool decision log

Append-only. Each entry: what was chosen, why, and what would reverse it. Old entries are never
rewritten, because the reason a choice looked right at the time is the useful part.

**2026-07-08 - plain files plus git over a business-management tool.** The repo already had to be
the audit trail for money and client artifacts. A second system means reconciling two truths.
Reverses if more than one person operates the business, at which point concurrent editing beats
greppability.

**2026-07-21 - one paid sourcing seat, no scraping stack.** The manual motion needs search depth,
not volume tooling. Volume tooling before the conversation gate would only produce more of an
unproven message. Reverses when the gate is met and the message is known to work.

**2026-07-23 - headless Chrome print-to-PDF as the document path, `docx` demoted to legacy.** The
docx generator produced a file that failed to open on a client machine the day before
(`ai/ERRORS.md`), and the branded design was fighting the format anyway. HTML is the design surface
the design already lives in. Reverses only for a client who needs an editable file, which is why the
old path is kept working rather than deleted.

**2026-07-27 - launchd over a hosted scheduler for the recurring jobs.** Both jobs read local files
and write local files. A hosted scheduler would need a copy of the repo and its secrets to do the
same work. Reverses if the machine stops being the single place the business runs.

**2026-08-01 - `pdf-check` and `docx-check` are mandatory rather than advised.** An advised check is
a check that gets skipped on the day it matters, which is the day something is late. Does not
reverse.
