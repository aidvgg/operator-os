# TOMBSTONES.md - retired values `scripts/repo-doctor` greps for

## The ripple rule

When a number or a decision is superseded, the same session does three things, not one:

1. Grep the dead value across the whole repo, not just `knowledge/`. Copies rot in `templates/`,
   in `skills/`, in `.claude/agents/` and in generated documents under `outputs/`.
2. Banner or strike every current-sounding hit. A strikethrough on the value, or the exact bolded
   `**SUPERSEDED - see <path>**` line at the top of a file that died whole.
3. Add the dead string to the table below.

Step 3 is what makes steps 1 and 2 stick. Without it the ripple is a promise, and the failure this
file exists to stop is exactly that promise being kept once and forgotten after: a re-priced number
sitting un-bannered in the satellite files that quoted it, until one of them is grabbed for a client
message. That is the 2026-07-11 row in `ai/ERRORS.md`.

## Where the check is HARD and where it is soft

`scripts/repo-doctor` scans every tracked text file, plus the extracted text of generated office
documents, for each dead string in the table.

- **HARD** (blocks the commit and the push) in `knowledge/`, `.claude/`, `.agents/`, `.github/`,
  `templates/`, `skills/`, and any markdown file at the repo root, `CLAUDE.md` included. Curated
  files are the ones a future session will trust.
- **Soft** (warns, never blocks) in `outputs/` markdown and inside generated office payloads. A
  delivered artifact is a historical record, so a dead price inside one is often correct. It still
  gets named, because that is the copy a client actually reads.
- **`ai/` is skipped entirely.** That is why the dead strings can be printed in this table at all,
  and why the two other ledgers can quote them when they narrate the supersession.

Three exemptions, each judged at the occurrence and not at the line or the file:

- a `~~strikethrough~~` span that wraps that occurrence;
- historical-framing prose within about 300 characters of it (`superseded`, `re-priced`, `re-set`,
  `raise target`, `dead price`, `tombstone`, `redacted`);
- a whole file whose **first line** is the exact bolded `**SUPERSEDED ...**` banner.

Anything looser is a lie the gate tells you. Testing a whole line for `~~` anywhere is what once hid
an un-struck retired price on a line whose other copy of the same string was correctly struck.

Matching is case-insensitive with alphanumeric boundary guards, so a dead string does not fire when
a letter or a digit sits immediately against either end of it. The guard is alphanumeric only, so a
longer figure that merely starts with a dead string and continues with punctuation can still fire.
That is the intended direction of the error. A false positive gets an occurrence-scoped allow entry
in `.repo-doctor-allow`, dated and reasoned. A false negative gets a wrong number in front of a
client.

## Writing a row

Keep dead strings **specific**. A string belongs here only if every un-struck, current-sounding
occurrence of it anywhere in the repo would be wrong. Never tombstone a bare generic figure that a
future legitimate amount could hit, and never tombstone a scoped benchmark that lives correctly
inside a scoped sentence. If you find yourself reaching for an allow entry the same day you add the
row, the string was too broad.

The first column header must read exactly `Dead string`. `load_tombstones()` in
`scripts/repo-doctor` skips the header row by that literal, and any other wording is parsed as a
tombstone for the phrase you typed. If the table is missing or reshaped, the check reports
`tombstones-source` and scans nothing, loudly rather than quietly.

## Retiring a row

A tombstone is not permanent furniture. Retire it when all of these hold:

- a grep for the dead string returns only struck, bannered or `ai/` hits;
- no live artifact or generator could still reproduce it (a proposal template, a skill reference
  file, a cached data JSON);
- the change that killed the value is on the remote, so nothing unpushed still carries it.

Then **delete the row.** That is the only correct way a tombstone leaves. Never edit the dead string
to make a violation pass, and never keep a row "just in case": a table full of retired retirements
is a table nobody reads, and the next real row hides in it.

One property worth knowing before you need it: the pre-push scan reads this ledger from **the commit
being scanned**, not from the pushing checkout, which is the opposite of how every other rule is
resolved. A commit made before a value was retired was legitimately clean when it was made, and the
ripple obligation belongs to the session that retired the value. So adding a row today never
retroactively condemns yesterday's commits, and deleting one never unblocks them.

| Dead string | Retired | Live authority |
|---|---|---|
| `$3,250` | 2026-07-08 | `knowledge/business/outbound-offer.md`. The Ops Automation Sprint is one flat price now, ruled in the `ai/DECISIONS.md` 2026-07-08 row. The old two-part shape, an audit fee plus a build fee, is dead in every form, so any current-sounding occurrence of the audit-fee figure is wrong. The owner file carries it struck in place so the supersession is readable. |
| `$6,750` | 2026-07-18 | `knowledge/clients/acme-retail/roadmap.md`. Phase 2 landed higher after two additions, both agreed in writing before any code was written: the alerting layer, and a third store that opened mid-scope. The reconciliation report was in the original quote. The timing is the point of the record, so do not restate this as a mid-build re-price. The owner file keeps the figure struck in place rather than deleted, because the negotiation history is worth more than a clean file, and that struck occurrence is the only place in the repo the dead figure still appears. |
