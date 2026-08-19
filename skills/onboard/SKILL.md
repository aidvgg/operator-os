---
name: onboard
description: "Take a fresh clone of Operator OS from the shipped demo to one person's real business: first-run setup, a plain-language interview one question at a time, the full rebrand, the demo wipe, verification with the repo's own scripts, and the first saved snapshot. Trigger on 'Set up Operator OS for me', 'make this mine', 'onboard me', 'set this up for my business', `/onboard` in Claude Code, `$onboard` in Codex, or any first session after cloning where the demo identity is still in `CLAUDE.md`. Never types bank or wire details into chat, never reads the provider key files, never pushes."
---

# Onboard: make a fresh clone theirs

You are talking to someone who is not technical. They opened this folder in an AI coding agent
and said something like "Set up Operator OS for me." Everything you say to them is plain words,
short sentences, one question at a time. Everything you do to the repo is exact, checkable, and
verified by the repo's own scripts before you call it done. The person is the operator; you are
the hands.

The procedure below is the owner. `SETUP.md` is the long-form reference it was derived from; if
the two disagree on a path or a command, check the tree, fix the wrong one, and say so.

## Hard rules

1. **Ask, never invent.** Every identity fact comes from the person's answer or from a file in
   the tree. An unanswered question becomes a `TODO(onboard): <what is missing>` line, never a
   plausible guess. Prices in particular: if they did not state one, write the TODO.
2. **Bank and wire details never enter the chat.** Do not ask for them, do not accept them if
   offered, do not write them anywhere. The person fills one named file themselves in a text
   editor (step B3). If they paste a number into chat anyway, do not repeat it, do not store it,
   and tell them to put it in the file instead.
3. **Never read the provider key files.** The two gitignored key files at the repo root (the one
   named `.env` and its `.local` sibling) are off-limits to every tool call; a guard denies the
   call. Name them, never open them. The wrapper scripts load the keys themselves.
4. **Idempotent.** Safe to re-run. Before changing anything, detect whether the rebrand already
   happened (step A4) and, if so, skip to the parts that are still missing.
5. **Stop on a real failure.** If a command exits non-zero or a file you expected is not there,
   stop, show the exact output, and ask. Do not improvise around it and do not continue to the
   next step as if it passed.
6. **Repo writes only, no sends, no push.** This skill ends with one commit on the local
   branch. It never pushes, never creates a remote, never sends anything to anyone.
7. **No em dashes** in anything you write, to the person or into a file. Comma, period, or a
   single hyphen.
8. **Do not edit these:** `SETUP.md`, `GUIDE.md`, `README.md`, `CHANGELOG.md`,
   `CONTRIBUTING.md`, `SECURITY.md` (they document the template and its demo, by design), the two
   design-standard specimen files under `skills/proposal-creator/references/` and
   `skills/invoice-creator/references/` (their `Kestrel Wholesale` client is machinery, not
   demo content), `outputs/outbound/prospect-gate.md` (machinery: the qualification ladder), and
   any generated view (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
   `.agents/skills/`, `.claude/skills/`, `.claude/commands/standup.md`, `eod.md`, `weekly.md`),
   which the generator rewrites in step D8.

## A. Preconditions and the opening message

A1. Confirm you are at the repo root: `CLAUDE.md`, `SETUP.md`, `scripts/repo-doctor` and
`knowledge/memory.md` all exist in the current directory. If not, stop and ask the person to open
the Operator OS folder itself.

A2. Tooling. Run each and record the result; do not ask the person to run anything.

| Check | Command | Needed for | If missing |
|---|---|---|---|
| git | `git --version` | everything | stop; say "this folder needs git installed" and point at `SETUP.md` section 2 |
| python3 3.9+ | `python3 --version` | every script | stop; same message |
| node | `node --version` | PDF proposals and invoices | continue; note "PDF generators will not run until node is installed" |
| Google Chrome | `ls /Applications/Google\ Chrome.app` on macOS, or `command -v google-chrome chromium` on Linux | rendering PDFs | continue; note "PDFs render once Chrome is installed or `CHROME_BIN` is set" |
| poppler | `command -v pdftotext` | `scripts/pdf-check` | continue; note it |
| rclone | `command -v rclone` | encrypted off-site backup | continue; note it |

Nothing in this skill needs node, Chrome, poppler or rclone. Their absence is reported in the
closing message (step G), not fixed here.

A3. Say this to the person first, in your own words but no longer than this:

> I will set up Operator OS for your business. First I wire the safety checks and create the
> one private file that will hold your bank details (you fill that in yourself, I never see it).
> Then I ask you about ten short questions, one at a time. Then I rewrite the demo business into
> yours, clear the demo data, run the checks, and save the first snapshot. You can stop me at
> any question.

A4. Detect a previous run. If `grep -c "Northwind Labs" CLAUDE.md` prints `0`, the rebrand has
already happened. Say so, run step F (verification) to report the state, and offer to re-open the
interview only for facts marked `TODO(onboard)` in `knowledge/memory.md`,
`knowledge/business/brand_foundation.md` and `knowledge/business/outbound-offer.md`. Do not wipe
or rewrite files that already carry the person's identity.

## B. First-run steps

These are `SETUP.md` section 2, run by you from the repo root.

B1. Wire the guardrails. Run `git config core.hooksPath .githooks`. Then `git config
core.hooksPath` must print `.githooks`.

B2. Create the private payment file if it does not exist:
`cp knowledge/business/invoices/PAYMENT-DETAILS.template.md knowledge/business/invoices/PAYMENT-DETAILS.md`.
If it already exists, leave it exactly as it is. Never edit, read aloud, or summarize this file.

B3. Tell the person, in plain words: "There is now a file called `PAYMENT-DETAILS.md` inside
`knowledge/business/invoices/`. Open it in any text editor (TextEdit on a Mac is fine) and
replace the placeholders with your real bank details whenever you like, today or later. It is
the only place those numbers live. The folder is set up so that file can never be saved into
the shared history, and I never read it. Invoices copy the bank block from there." Do not wait
for them to do it; continue.

B4. Provider keys, one sentence: "Two optional read tools (they fetch public LinkedIn and X
pages for prospect research) need paid third-party API keys; if you ever want them, you will
copy the example key file at the repo root to its `.local` sibling and paste the keys in
yourself, and I will never open that file." Do not create the key file in this skill.

B5. Run `scripts/repo-doctor`. On an untouched clone with B1 and B2 done it prints exactly
`repo-doctor: clean`. If it prints anything else, show it and stop; it is about this machine,
not the demo.

## C. The interview

One question per message. Wait for the answer. Offer the example only as an example, never as a
default. Record each answer verbatim. After the last question, read the whole list back in one
short block and ask "anything to change?" before touching a file.

| # | Question (ask in plain words) | Example answer | What it changes |
|---|---|---|---|
| 1 | What is your name, as it should appear on documents? | "Jordan Lee" | `FULL_NAME`; `FIRST_NAME` is the first word unless they say otherwise. Replaces the demo operator's name everywhere the repo names its operator (the demo's first name is `Sam`, and one validation regex reads it, step D4). |
| 2 | What is your business called? Is there a separate legal entity (an LLC or company) that bills clients, or is it just you under that name? | "Lee Bookkeeping Studio, billed through Lee Bookkeeping Studio LLC" or "just me, no company" | `BUSINESS`, `ENTITY`. If there is no separate entity, `ENTITY` equals `BUSINESS` and every "operating under" or "dba" phrase collapses to the business name alone (step D3). |
| 3 | What email should go on proposals and invoices? | "jordan@example.com" | `EMAIL`. Replaces `sam@northwindlabs.example` in both document generators and their skill docs. `DOMAIN` is the part after `@` unless they name a website. |
| 4 | In one sentence, what do you sell? | "Monthly bookkeeping and quarterly tax-ready books for small service businesses." | `WHAT_YOU_SELL`. Goes into `CLAUDE.md` Who/what, `knowledge/memory.md`, `knowledge/business/brand_foundation.md`, `knowledge/business/outbound-offer.md`, the business profile JSON. |
| 5 | Who do you sell to? | "Owner-run service businesses with 2 to 15 staff and no finance person." | `WHO_YOU_SELL_TO`. Same files, plus the ICP field of the profile. |
| 6 | How do you charge: by the hour, per project, a monthly retainer, or a mix? If you have typical numbers, say them; if not, that is fine. | "Flat monthly retainer per client; cleanups per project. Usually 400 to 900 a month." | `HOW_YOU_CHARGE` (words) and `PRICE_ROWS` (only if numbers were given; otherwise one row reading `TODO(onboard): price not given yet`). Numbers go into `knowledge/business/outbound-offer.md` only, the pricing authority, never into memory or CLAUDE.md. |
| 7 | Which channels do you actually use to find clients: X, LinkedIn, email, none yet? | "LinkedIn and email" | `CHANNELS`. Named in `CLAUDE.md` Who/what and `memory.md` Motions; sections for unused channels in `CLAUDE.md` Voice rules and `knowledge/voice/channel-voice.md` get a one-line "(not used yet)" note, not deleted. |
| 8 | How should your writing sound? Pick one from each pair: (a) sentence case everywhere, or lowercase on X; (b) plain and warm, or direct and blunt; (c) short sentences, or fuller explanations. | "sentence case, plain and warm, short" | `VOICE_SUMMARY`, one line. Rewrites the three channel bullets in `CLAUDE.md` Voice rules and adds a dated note at the top of `knowledge/voice/channel-voice.md`. Nothing else about voice is decided here. |
| 9 | What two or three letters should start your invoice numbers? They look like PREFIX-2026-001. | "LB" | `PREFIX`, uppercase letters only (the number pattern is `PREFIX-YYYY-NNN`). Replaces the demo `NL-` in the ledger, the register rules, `scripts/money` (two patterns) and `scripts/repo-doctor` (one pattern), step D5. |
| 10 | What currency do you bill in? | "USD" | `CURRENCY`. Goes into `CLAUDE.md` Pricing, `memory.md`, the ledger and register column headers, the profile. Tell them one limit honestly: the cash script reads register amounts written with a `$` sign; a non-dollar currency can appear on the invoice PDF, but the register amounts still need the `$` shape until `scripts/money` is taught otherwise. |
| 11 | What timezone are you in? | "America/Chicago" | `TIMEZONE`. Recorded in `memory.md`; used by the daily log's weekday logic and the morning brief schedule. |
| 12 | Optional tools. Which of these do you want now? I can set the ones you pick up later; none is required today. | "PDFs yes, backups later, no LinkedIn tools" | Recorded in the closing message and `knowledge/ops/tools-and-stack.md`. Plain-English cost of each, say it this way: **PDF proposals and invoices**: free, needs node and Google Chrome installed. **Encrypted off-site backup**: free software (rclone) plus a cloud drive account you already have; the weekly automatic run is macOS only and needs a one-time permission grant. **LinkedIn and X read tools**: paid third-party providers, billed by them, keys in a file I never open. **Your AI coding agent**: whatever plan you already pay for; that plus the above is the whole running cost. |

Do not ask for: bank details, the key values, a logo file (offer it in D2 as optional), or
anything the repo can read for itself.

## D. The rebrand

Work from the answers only. Every edit below is exact. When an edit says "replace", replace the
literal text; when it says "rewrite", write new prose from the answers and keep the headings.
Order matters: D1 to D7 first, the tree-wide sweep D9 second to last, the generator last.

**D1. `CLAUDE.md`** (the operating contract, highest precedence).
- Line 1: `# CLAUDE.md - Northwind Labs operating contract` -> `# CLAUDE.md - <BUSINESS> operating contract`.
- Section `## Who / what`: replace the whole section body with two or three sentences from
  answers 1, 2, 4, 5, 7: who, the business, what it sells, to whom, channels, and the line
  "Money motions: client work, outbound and content, the standard offer
  (`knowledge/business/outbound-offer.md`)." Delete the italic "worked example" note.
- Section `## Voice + format rules`: replace the italic note "*(The channel rules below are the
  worked example's voice...)*" with "*(Voice summary from the onboard interview: <VOICE_SUMMARY>.
  Per-channel detail: `knowledge/voice/channel-voice.md`.)*". Rewrite the `### X`,
  `### LinkedIn` and `### Client / direct messages` bullets to match answer 8 (casing, register,
  length); keep the "pillars ... owned by `knowledge/voice/channel-voice.md`" pointer bullet under
  X as written. Mark each channel not in answer 7 with "(not used yet)" after its heading.
- Section `### Pricing`: replace `always price in USD` and `internal pricing math in USD` with
  `<CURRENCY>`. Leave the pricing-authority bullet as written: it already points at
  `knowledge/business/outbound-offer.md` and the client roadmap files.
- Nothing else in `CLAUDE.md` carries identity except the operator's first name in prose,
  which D9 handles.

**D2. Logo and wordmark.** Ask once: "Do you have a logo as a PNG file? If yes, tell me the path
and I will put it in place; if not, your business name renders as the wordmark and that looks
fine." If yes: copy it to `skills/proposal-creator/assets/logo.png` and
`skills/invoice-creator/assets/logo.png` (both; each generator reads only its own folder). If no:
do nothing; the wordmark text is the brand string D3 sets.

**D3. Brand strings in the document generators and their docs.** In these seven files:
`skills/proposal-creator/scripts/generate-proposal-html.js`,
`skills/invoice-creator/scripts/generate-invoice-html.js`,
`skills/proposal-creator/scripts/generate-proposal.js`,
`skills/invoice-creator/scripts/generate-invoice.js`,
`skills/proposal-creator/SKILL.md`, `skills/invoice-creator/SKILL.md`,
`skills/proposal-creator/references/data-schema.md`, replace, in this order:
`Sam Rivera` -> `<FULL_NAME>`; `sam@northwindlabs.example` -> `<EMAIL>`;
`NORTHWIND LABS` -> uppercase `<BUSINESS>`; `Northwind Labs` -> `<BUSINESS>`;
`Rivera Holdings LLC` -> `<ENTITY>`. Then, only when `ENTITY` equals `BUSINESS`, collapse the
entity phrases so the footer does not read "X operating under X": replace
` · operating under <BUSINESS>` -> `` (empty), ` (operating under <BUSINESS>)` -> ``,
`<BUSINESS> · <BUSINESS>` -> `<BUSINESS>`, `<BUSINESS> &nbsp;·&nbsp; dba <BUSINESS>` ->
`<BUSINESS>`, `<BUSINESS> (dba <BUSINESS>)` -> `<BUSINESS>`, `<BUSINESS> · dba <BUSINESS>` ->
`<BUSINESS>`, `<BUSINESS>, operating under <BUSINESS>` -> `<BUSINESS>`. Also in
`skills/invoice-creator/SKILL.md`, replace the example invoice number, which is the demo ledger's
next number `NL-2026-004` (the string E2 later tombstones), with `<PREFIX>-<YEAR>-001` (three places), and the example client name `Acme Retail` with
`Example Client` where it appears in the sample JSON. Verify with
`grep -rniE 'northwind|rivera|sam@' skills/proposal-creator skills/invoice-creator`: the only
hits left are in the two design-standard specimen files, which stay.

**D4. The one place the operator's first name is functional.** In `scripts/repo-doctor`, the
`_ORIGIN_OK` regex (find it with `grep -n "_ORIGIN_OK = " scripts/repo-doctor`) carries two
`Sam` tokens: `extended by Sam` and `Sam added`. Replace both with `<FIRST_NAME>`. D3 already
changed the same vocabulary in `skills/proposal-creator/references/data-schema.md` and
`skills/proposal-creator/SKILL.md` (D9 catches any prose copy left). Prove there is no other
functional first name: `grep -rn "Sam" scripts/ | grep -E "re\.(compile|search|match|sub|findall)|r\"|r'"`
must print nothing after D9.

**D5. Invoice numbering, three patterns plus the ledger.**
- `scripts/money`: replace `r"(NL-\d{4}-\w+)"` with `r"(<PREFIX>-\d{4}-\w+)"` (the register
  parser) and `re.compile(r"NL-\d{4}-\d+[A-Za-z]?")` with
  `re.compile(r"<PREFIX>-\d{4}-\d+[A-Za-z]?")` (the record-filename pattern `INVOICE_NUM_RE`).
  Both, or the two halves disagree about what an invoice number looks like.
- `scripts/repo-doctor`: in the `summary-openbalance` check, replace
  `re.search(r"NL-\d{4}-\w+", ln)` with `re.search(r"<PREFIX>-\d{4}-\w+", ln)`. Left on the demo
  prefix it silently stops seeing any register row.
- The ledger and register themselves are replaced whole in step E3 from the templates, which
  already carry `<PREFIX>`.

**D6. Money config, in `scripts/money` near the top.**
- `FIXED_COSTS`: replace the demo rows with an empty list that keeps the comment above it and
  one line `# TODO(onboard): add your recurring costs here, one row each; owner of each number is knowledge/ops/tools-and-stack.md`.
  Never invent a cost.
- `OWNER_ALIASES`: replace the two demo pairs with an empty list and the comment
  `# TODO(onboard): (regex, owner) pairs that collapse bill-to spellings into one client.`
- `TARGET_RECURRING` and `TARGET_BUFFER`: leave the demo numbers only if the person gave none;
  if they named a monthly target or a cash buffer in answer 6, set these and say so in G.
  Otherwise add `# TODO(onboard): demo targets, set your own` above them.
- `scripts/money` must still exit 0 after this (it does on an empty list; step F proves it).

**D7. Backup and scheduled-job labels.**
- `scripts/backup-sensitive`: `KEYCHAIN_ACCOUNT = "operator-os"` -> a slug of the business
  name (lowercase, hyphens, for example `lee-bookkeeping-studio`); `KEYCHAIN_SERVICE =
  "operator-os-backup"` -> that slug plus `-backup`.
- Pick `LABEL`, a reverse-DNS identifier from the business name, for example
  `com.leebookkeeping`. Rename the two plists `scripts/com.northwindlabs.<job>.plist` for
  `<job>` in `weekly-backup` and `morning-brief` to `scripts/<LABEL>.<job>.plist` (`git mv` is
  fine), and replace `com.northwindlabs.` with `<LABEL>.` inside both plists and inside
  `scripts/weekly-backup` and `scripts/morning-brief` (their INSTALL blocks name the label in
  every `sed`, `launchctl bootstrap`, `kickstart` and `bootout` line) and in
  `knowledge/ops/tools-and-stack.md` section 6. Left undone, the doctor reports a dead pointer to
  the old plist name.

**D8. Cross-model adapter routing.**
- `scripts/sync-agent-adapters`: the brand literal is the Python string
  `"# Northwind Labs agent entrypoint"` (find it with `grep -n 'agent entrypoint"'
  scripts/sync-agent-adapters`). Replace `Northwind Labs` there with `<BUSINESS>`.
- `ai/AGENT_ROUTES.json`: the daily-log workflow description reads `Maintain Sam's daily
  operating logbook ...`; replace `Sam` with `<FIRST_NAME>`. Touch nothing else in the registry.
- Regenerate after D9: `scripts/sync-agent-adapters --write`, then
  `scripts/sync-agent-adapters --check` must print `agent-adapters: clean (N generated surfaces)`.
  Never hand-edit a generated view.

**D9. The tree-wide prose sweep.** The demo operator is named in prose across agent files,
skill files, knowledge READMEs and scripts. Over every tracked text file plus the two renamed
plists, excluding the files in hard rule 8, the generated views and this skill's own folder
`skills/onboard/` (it names the demo strings on purpose), apply in this order, whole word only
for the first name: `Sam Rivera` -> `<FULL_NAME>`; `\bSam\b` -> `<FIRST_NAME>`;
`Northwind Labs` -> `<BUSINESS>`; `Rivera Holdings LLC` -> `<ENTITY>`;
`sam@northwindlabs.example` -> `<EMAIL>`; `northwindlabs.example` -> `<DOMAIN>`; then the
entity-collapse phrases from D3 when `ENTITY` equals `BUSINESS`. Do not touch binaries, fonts or
PDFs. Afterwards `grep -rnwE 'Sam|Northwind|Rivera' --exclude-dir=node_modules --exclude-dir=.git .`
may hit only: `SETUP.md`, `README.md`, `GUIDE.md`, `CHANGELOG.md`, `skills/onboard/SKILL.md`, the
two specimen files, and the local `PAYMENT-DETAILS.md` copy (which the sweep never opens).
Anything else is a miss; fix it.

**D10. `knowledge/` identity files.** `knowledge/memory.md`, `knowledge/business/brand_foundation.md`,
`knowledge/business/outbound-offer.md`, `knowledge/business/pricing-outcomes.md` and
`knowledge/business/operator-business-profile.json` are replaced whole in step E3 from the
templates in `skills/onboard/templates/`. `knowledge/voice/copy-rules.md` survives the sweep as
is (it is craft, not identity). `knowledge/voice/channel-voice.md`: add, directly under the H1,
one line `*(Onboard note <TODAY>: voice preferences are <VOICE_SUMMARY>. The sections below are
the template's defaults, to be tuned as posts go out.)*` and mark sections for channels not in
answer 7 with "(not used yet)". `knowledge/ops/tools-and-stack.md` section 1: replace the demo
cost table rows with one row per tool the person actually pays for (answer 12) with
`TODO(onboard): your plan price` in the Monthly column, and a `**Total** | TODO(onboard)` row;
replace the "(Demo stack: ...)" parenthetical under the `Stale after` line with `(Set on <TODAY>
by the onboard skill. Replace the date with the one your statements actually rot on.)`.
`knowledge/clients/README.md`: replace the three demo references (`acme-retail/`,
`beacon-health/` in the opening line, the `beacon-health/` sentence in the "no priced work yet"
paragraph, and the roadmap path in the price-rule example) with `<client-slug>/` and
`knowledge/clients/<client>/roadmap.md`, and replace the `## Demo content` section with
`## Adding your first client` and one sentence: create `knowledge/clients/<client-slug>/README.md`
and `roadmap.md` per the sections above; the roadmap file owns every price for that engagement.

## E. The demo wipe and the rewrite queue

E1. Run the `SETUP.md` section 4 delete block, verbatim, from the repo root:

```bash
rm -rf knowledge/clients/acme-retail/ knowledge/clients/beacon-health/
rm -f  knowledge/business/invoices/NL-2026-*.md
rm -f  knowledge/ops/logbook/days/*.md knowledge/ops/logbook/reviews/*.md
rm -f  knowledge/research/smb-ops-tooling-scan-*.md
find outputs -type f ! -name README.md ! -name prospect-gate.md -delete
```

The two `find` exclusions are load-bearing: every folder README stays, and
`outputs/outbound/prospect-gate.md` stays because `skills/prospect-brief` reads it. On a fresh
clone the block removes exactly three proposal artifacts from `outputs/` and leaves the READMEs
and the gate. `knowledge/business/MONEY.md` is generated and is never hand-edited; step F
regenerates it.

E2. Clear the three ledgers in `ai/`, keeping every heading, the column documentation and the
whole `## Hazards` section of `ai/ERRORS.md` (a hazard is a licence: roughly a dozen
`repo-doctor` checks cite one). In each of `ai/DECISIONS.md`, `ai/ERRORS.md` and
`ai/TOMBSTONES.md`, delete the demo data rows under the table header and its separator row, and
nothing else. Then append one real tombstone row to `ai/TOMBSTONES.md`, because the doctor reports
`tombstones-source` as soft when the table parses to zero rows and because the demo numbering
genuinely is retired:

```
| `NL-2026-004` | <TODAY> | The template's demo invoice numbering, retired by the onboard skill. Live numbering uses the `<PREFIX>-` prefix and the next number lives in `knowledge/business/invoices/INVOICE-LEDGER.md`. Delete this row once a real retired value replaces it and the demo string is gone from the remote. |
```

That dead string is the demo ledger's next number, and after D3 it appears nowhere in a curated
file; the tombstone check stays armed on a real entry instead of an empty table.

E3. Render the templates. Each file in `skills/onboard/templates/` is a complete replacement
for one repo file; fill every `{{TOKEN}}` from the interview and write it to its destination.
A token left unfilled is a failure, not a TODO. Tokens: `FIRST_NAME`, `FULL_NAME`, `BUSINESS`,
`ENTITY`, `ENTITY_CLAUSE` (", operating under <ENTITY>" or empty when equal), `ENTITY_PHRASING`
("<BUSINESS> (operating under <ENTITY>)" or just the name), `EMAIL`, `WHAT_YOU_SELL`,
`WHO_YOU_SELL_TO`, `HOW_YOU_CHARGE`, `CHANNELS` (comma-joined), `CHANNELS_JSON` (a JSON array
of strings), `PLATFORMS_JSON` (a JSON object keyed by lowercase channel name, each value
`{"handle": "unknown", "voice": "see knowledge/voice/channel-voice.md", "status": "declared"}`),
`PREFIX`, `YEAR` (today's year), `CURRENCY`, `TIMEZONE`, `TODAY` (ISO date), `VOICE_SUMMARY`,
`MOTIONS_BLOCK` (three numbered lines: client work, outbound and content with the channels and a
pointer to `outputs/outbound/prospect-gate.md`, the standard offer pointing at
`knowledge/business/outbound-offer.md`), `PRICE_ROWS` (table rows from answer 6, or one
`TODO(onboard)` row).

| Template | Destination |
|---|---|
| `memory.md` | `knowledge/memory.md` (keeps the four anchor headings `### Motions`, `### Clients`, `### Money`, `### Open questions` that the doctor reads; no currency figure may appear between `### Clients` and `### Open questions`) |
| `invoice-ledger.md` | `knowledge/business/invoices/INVOICE-LEDGER.md` (empty Issued table, next number `<PREFIX>-<YEAR>-001`) |
| `invoice-register.md` | `knowledge/business/invoices/SUMMARY.md` (empty register, both cash-status lines `$0`) |
| `logbook.md` | `knowledge/ops/logbook/LOGBOOK.md` (no rows, cursor block says no day logged yet, opened `<TODAY>`) |
| `logbook-stats.md` | `knowledge/ops/logbook/STATS.md` (zeroed, carry-over heading dated `<TODAY>`) |
| `habits.md` | `knowledge/ops/logbook/HABITS.md` (empty registry, no marks) |
| `pain-point-bank.md` | `knowledge/pain-points/pain-point-bank.md` (schema kept, no entries) |
| `pain-point-bank.csv` | `knowledge/pain-points/pain-point-bank.csv` (header row only) |
| `brand-foundation.md` | `knowledge/business/brand_foundation.md` |
| `outbound-offer.md` | `knowledge/business/outbound-offer.md` |
| `pricing-outcomes.md` | `knowledge/business/pricing-outcomes.md` (empty ledger) |
| `business-profile.json` | `knowledge/business/operator-business-profile.json` (must parse as JSON; unanswered fields are the string `unknown`) |

E4. Rewrite queue. After E1 to E3, run `scripts/repo-doctor` and clear every remaining
`dead-pointer` line by editing the citing file to point at a real path or a `<placeholder>`;
D10 already covers `knowledge/clients/README.md` and `knowledge/ops/tools-and-stack.md`. A
`TODO(onboard): ...` line is tolerated by every check; a dangling backticked path is not. Never
clear a finding by adding an allow entry.

## F. Verification, then the first snapshot

Run all five from the repo root, in this order, and show the person the one-line result of each.
All five must pass before the commit.

| Command | Must print / exit |
|---|---|
| `scripts/money` | exit 0, ending `(register is empty, this is a zeroed rollup)`; it rewrites `knowledge/business/MONEY.md` |
| `scripts/horizon --brief` | `horizon: 0 overdue, 0 in next 14d; no verified backup recorded yet` (the demo decision's event gate is gone with its row) |
| `scripts/repo-doctor` | exactly `repo-doctor: clean`, exit 0 |
| `scripts/sync-agent-adapters --check` | `agent-adapters: clean (N generated surfaces)` |
| `scripts/test-git-guard` | last line `test-git-guard: all N assertions green (...)` |

If any line differs, stop, show it, fix the cause, rerun. Then run `git status --porcelain` and
read it: every changed, added or deleted path should be one you touched above; ask about anything
else before staging it.

Stage with an explicit path list and commit. Never `git add -A`, never `git add .`, never
`--no-verify` (the guard denies all three anyway):

```bash
git add CLAUDE.md AGENTS.md GEMINI.md .github/ .agents/ .claude/ .codex/ ai/ knowledge/ outputs/ scripts/ skills/
git commit -m "Make Operator OS mine: <BUSINESS>"
```

Directory paths stage the deletions inside them too; the gitignored payment file and key files
are never staged by this. The pre-commit hook runs `scripts/repo-doctor --staged`; if it blocks,
show the output and stop. `git log --oneline -1` then shows the new commit. Do not push.

## G. The closing message

Plain text, short, in this order:

1. What changed, in five lines or fewer: the business name is in every document and contract;
   invoice numbers start at `<PREFIX>-<YEAR>-001`; the demo clients, invoices, logbook days and
   research are gone; the first snapshot is saved as "Make Operator OS mine: <BUSINESS>"; nothing
   was pushed anywhere.
2. What they do by hand: fill `knowledge/business/invoices/PAYMENT-DETAILS.md` in a text editor
   (required before the first invoice); the optional tools they chose in answer 12 and the one
   line each needs (node and Chrome for PDFs; rclone plus `scripts/backup-sensitive --init` for
   backups; the key file for the read tools), or "none chosen, nothing to install".
3. The `TODO(onboard)` lines, by file, as a list they can answer later in one sentence each.
4. The first week, the five sentences `GUIDE.md` section 6 teaches, one per day:
   "plan my day" (morning), "log my day" (evening), "write a proposal for <client>",
   "invoice <client> for <work>", "weekly review". Add two standing ones: "add a client called
   <name>" the day real work starts, and "what does this mean?" for any warning they do not
   understand. Remind them you draft and they send.

## What this skill does not do

- It does not push, create a remote, or touch anything outside this folder.
- It does not set up rclone, launchd jobs, Chrome, node or provider keys; it names them.
- It does not grant any `knowledge/` licence beyond this one-time rebrand and wipe; after the
  commit, the normal write rules in `CLAUDE.md` apply.
- It does not relitigate template doctrine. Voice, pricing and guardrail rules transfer as they
  are; the person tunes them later with the files named above.

## Completion criteria

All true, or the run is not done:

- `grep -c "Northwind Labs" CLAUDE.md` prints `0`, and the D9 grep hits only the allowed files.
- The five F commands print the stated lines.
- `knowledge/business/invoices/PAYMENT-DETAILS.md` exists and was never opened by a tool call.
- One commit titled `Make Operator OS mine: <BUSINESS>` is at `HEAD`; `git status --porcelain`
  is empty except gitignored paths; no push happened.
- Every fact in the rewritten files came from the interview or the tree; every gap is a
  `TODO(onboard)` line.
