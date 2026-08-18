# knowledge/pain-points

The raw material for outbound copy, offers and content. Every entry is one thing an operator
said is broken in their own back office, with enough evidence attached that you can quote it,
price against it, or write a post about it without going back to the source.

Two files, one bank:

| File | What it is |
|---|---|
| `pain-point-bank.md` | the readable bank. Full entries, quotes, curation notes. What a human reads before writing anything. |
| `pain-point-bank.csv` | the machine mirror. Same entries, same ids, same values. What `scripts/reddit-scan --append-bank` appends to and what any script or agent parses. |

They are edited in the same pass. A change in one and not the other is a silent lie the next
session inherits, and the CSV is the copy that scripts trust.

This folder holds no prices. A cost figure in an entry is what the *prospect's problem* costs
them, always marked as an estimate. What Northwind Labs charges lives in exactly one owner file
per motion: `knowledge/business/outbound-offer.md` for the productized offer, the client's
roadmap file under `knowledge/clients/` for an engagement. Restating a sell-side number here is
how a dead price ends up in a client message.

---

## Schema

The CSV header is a contract. `scripts/reddit-scan` reads it and fills the columns it can honestly
fill, leaving the rest blank for the human pass. Matching is case-insensitive and ignores stray
whitespace, so changing capitalisation is safe. Renaming is not: a header the scanner does not
recognise is a column it fills with nothing, quietly. The names it looks for are
`CANDIDATE_COLUMNS` in that script, and `COLUMN_ALIASES` maps the common variants onto them, so a
rename means adding the new name to that map in the same pass. To check a rename for real, run
`--append-bank` once and read `git diff` on this file. The append is append-only, so a bad result
is one `git checkout --` away. Do not check it with `--dry-run`: that flag returns before the
append runs, so it reports a clean scan and tells you nothing about which cells got filled.

| Column | Filled by | Value |
|---|---|---|
| `ID` | human | `PP-NNN`, assigned once and never reused. Stable, because copy and briefs cite it. A scanner-appended row arrives with a blank id; stamping it is the first step of the human pass. |
| `Status` | human, or `CANDIDATE - not promoted` by the scanner | `CANDIDATE - not promoted`, `PROMOTED <YYYY-MM-DD>`, or `RETIRED <YYYY-MM-DD>`. See the promotion rule below. |
| `Theme` | human | one slug from the theme list below. Controlled vocabulary, so clusters are countable. |
| `Short Pain Summary` | scanner writes the post title, human rewrites it | 1 to 3 sentences, dense with specifics. No filler. |
| `Raw Quote` | scanner or human | verbatim. Never paraphrased, never cleaned up. If you tidied it, it is not a quote. |
| `Who Feels It` | human | the role and the size of business. Not the company, the seat. |
| `Observable Symptom` | human | what someone standing in that office would actually see. The test below. |
| `Estimated Cost` | human | time or money, ranged, and explicitly labelled as an estimate and whose estimate it is. |
| `Pain Intensity` | human | 1 to 5. Calibration below. |
| `Willingness to Pay` | human | `Yes - explicit`, `Yes - implied`, `Unclear`, `No`. The scanner writes `tell present` or `not stated` until a human re-judges it. |
| `Source Type` | human | `discovery call`, `client delivery`, `forum scan`, `peer conversation`, `inbound DM`. |
| `Source Platform` | scanner or human | where it came from, for example `Reddit r/smallbusiness`. |
| `Source URL` | scanner | link, when there is one. Blank for calls and DMs, and that is fine. |
| `Date Added` | scanner or human | ISO date the entry entered the bank. |
| `Signals` | scanner only | which tells fired, using the scanner's own names. Blank on hand-captured entries, and blank is correct there. |
| `Prefilter Score` | scanner only | the mechanical score. Not a quality judgment, it is a reading queue. |
| `Offer Angle` | human | what you would build against it. Never what it costs to buy. |

Two columns are deliberately machine-only. A hand-captured entry has no `Signals` and no
`Prefilter Score`, and filling them by hand would make an entry look scanner-validated when it
was one conversation. A blank cell is an honest prompt to do the work. A guessed cell is a lie
the bank then carries forever.

**Themes** (extend deliberately, not per entry): `inventory-reconciliation`, `double-entry`,
`month-end-reporting`, `silent-failure`, `location-onboarding`, `data-drift`,
`knowledge-in-inbox`.

---

## What makes an entry good

Five tells. An entry with four of them is worth writing up. An entry with one is a note, not a
pain point.

1. **First-person and active.** They have the problem now. Not "a friend of mine", not "we might
   one day". Second-hand pain is the single most common way a bank fills up with nothing.
2. **Quantified.** Hours, records, locations, incidents, a percentage. A number they said out
   loud beats a number you inferred, and the entry should say which it is.
3. **Named stack.** The actual tools. "Two systems" is a category, "the till system and the
   warehouse system" is a build.
4. **Tried and failed.** What they already attempted and why it broke. The strongest buying
   signal there is, because it prices the alternatives for you.
5. **Willingness to pay.** A budget, current tool spend, or hiring intent. Not a dollar figure
   appearing somewhere in the text, which is usually their own pricing, not their demand.

**The observable-symptom test.** If you cannot name something a visitor would physically notice,
you have a theme and not a pain point. "Reporting is hard" fails. "A workbook with a tab per
source and a summary tab of formulas nobody else can follow" passes. The symptom is also what you
open a conversation with, because naming it proves you have seen the problem before.

**Intensity calibration.** 5 is a quantified catastrophe or visible first-person desperation. 4 is
strong active pain with specifics. 3 is real but milder, or second-hand. 2 or below is
hypothetical and does not belong in the bank. If everything in your bank is a 4 or 5, the scale
has stopped doing work and so has your judgment.

**Intake is deliberately looser than the bar above.** A candidate is worth capturing when it shows
strong signal **or** a willingness-to-pay tell. Either alone is enough. Quality is enforced at
promotion, not at capture, because a high intake bar means you only ever record what you already
believed. `scripts/reddit-scan` implements exactly this gate. If you move it, record the ruling in
`ai/DECISIONS.md` so it is not re-argued every run.

---

## Candidate vs promoted

Two states with a one-way door between them.

- **CANDIDATE** - captured, curated, not yet believed. Usable for content and for research. Never
  cited as evidence in a proposal, an offer, or a pricing argument.
- **PROMOTED** - the operator has read the entry and said so. Usable everywhere.
- **RETIRED** - looked real, was not. Keep the row, set the status, and write one line saying what
  killed it. A miss is evidence too, and a deleted row teaches nobody.

**Promotion is the operator's explicit verdict, always.** No agent promotes an entry. No script
promotes an entry. No amount of corroboration promotes an entry on its own. The reason is narrow
and worth stating: the bank is the input to what gets built and what gets charged for, so a bank
that can promote its own finds turns a scraper's taste into an offer. Once that happens the bank
stops being evidence about the market and starts being a mirror.

What an agent may do without asking: capture a candidate, curate it, write the cost estimate,
propose an offer angle, and say plainly that it looks promotable and why. Then stop.

`scripts/reddit-scan --append-bank` is bound by the same rule mechanically. It appends only, never
edits or deletes an existing row, and stamps every row it writes `CANDIDATE - not promoted`. If
the header ever loses its status-shaped column the mark gets pushed onto the front of the first
cell instead, because the one failure that actually costs something is a scraped row that reads
like a curated one.

---

## Where entries come from

| Source type | How it lands |
|---|---|
| `discovery call` | you heard it. Write it up the same day, while the wording is still theirs. |
| `client delivery` | you found it while building something else. The highest-trust source in the bank and the most often skipped. |
| `forum scan` | `scripts/reddit-scan` writes ranked candidates to `outputs/research/pain-signals/<YYYY-MM-DD>.md`, and with `--append-bank` also into the CSV. Everything it writes is a candidate. |
| `peer conversation` | another operator's pain, or their client's. Useful, one voice, treat accordingly. |
| `inbound DM` | someone replied to a post with their own version of it. Weak on evidence, strong on wording, because it is written in the language your content already reached. |

A scanner run is a reading queue, not research. The judgment (how bad it really is, what you would
sell against it, whether it is the same pain as one already in the bank) is a human pass, and the
gap between a scored row and a curated entry is where all the value sits.

---

## How the bank feeds the rest of the OS

- **Outbound** (`outputs/outbound/`). An opener quotes the observable symptom, not the solution.
  `skills/prospect-brief` matches a prospect against the bank and names the entry id it matched,
  so a brief carries its evidence. Qualification rules stay in `outputs/outbound/prospect-gate.md`,
  which owns them. The bank supplies the pain, not the verdict.
- **Content** (`outputs/content/`). The best posts are one entry, rendered. The symptom is the
  hook, the cost estimate is the substance, the offer angle is the mechanism. Voice rules bind:
  `knowledge/voice/copy-rules.md`.
- **Offers** (`knowledge/business/outbound-offer.md`). An offer that does not trace to at least
  two promoted entries in the same theme is a guess. That traceability is the whole point of the
  promoted state.
- **Proposals** (`outputs/proposals/`). Use an entry to check that the scope you are pricing
  addresses the symptom the client actually described. Never quote another client's entry in a
  proposal.
- **Templates** (`templates/message-templates.md`). Message skeletons leave a slot for the
  symptom line. The bank fills the slot.

---

## Housekeeping

This file and the bank carry no `**Stale after:**` line, on purpose. A perishable page makes a
claim that is true today and false later, so it must expire. The bank is a growing corpus of dated
observations, and an old entry is not wrong, it is old. Each entry carries its own `Date Added`,
and an entry whose world has changed gets `RETIRED` with a reason rather than a bumped date.

Re-read the promoted entries when a motion stops converting. If the copy that used to work has
stopped, one of these entries has quietly become false, and finding which one is faster than
rewriting the copy.
