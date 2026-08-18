# Copy rules: the send-ready floor

Owner of the craft rules. `CLAUDE.md` points here for the em-dash ban and every rule below it.
These are the rules that survive a rebrand: they are about how writing works, not about who
Northwind Labs is. The per-channel voice, which is very much about who Northwind Labs is, lives
next door in `knowledge/voice/channel-voice.md` and is meant to be replaced.

Seven rules. Each one gets a why, a test you can apply in a single pass, and a bad and good
example. A rule you cannot test is a preference, and preferences do not survive a deadline.

**Notation:** this file contains no em dash and no en dash anywhere, including in its own bad
examples. Where an example needs to show one, it is written `<emdash>`.

---

## 1. No em dashes, anywhere

No em dash (U+2014) in any output: client messages, proposals, invoices, drafts, `knowledge/`
files, commit messages, chat. The en dash (U+2013) is banned on the same line, because the
mechanical check treats them as one class and because nobody types one on purpose.

**Why.** Two reasons, and the second is the one that matters. First, it is the single most reliable
tell that copy came out of a language model, and a prospect who spots the tell stops reading the
argument and starts reading the tell. Second, the character buys nothing: a comma, a period or a
restructured sentence always works, so there is no cost to the ban and no case to argue.

**Test.** Search the file for the character before it ships. If the sentence collapses without it,
the sentence was carrying two ideas and wanted to be two sentences.

**Bad:** `the sync runs nightly <emdash> nobody reconciles by hand any more`
**Good:** `the sync runs nightly. nobody reconciles by hand any more.`

**Status.** House style adopted at the start, not an incident control. If it ever fails and reaches
a client, that gets a row in `ai/ERRORS.md` and the row gets named here. Until then this file is
honest about being a taste call with a mechanical floor behind it (see below).

---

## 2. Dead-easy style

Simple sentences. Plain words. One idea per sentence. If a reader has to go back and re-read a
line, the line failed, however clever it was.

**Why.** The person reading this is an ops lead on a phone, between two other problems, deciding in
about four seconds whether you understand their business. Complexity in the sentence reads as
complexity in the work. Plain language is not dumbing down, it is the fastest way to be believed.

**Test.** No word a smart twelve-year-old would have to look up. No sentence with two commas doing
structural work. Read it out loud; if you run out of breath, cut it.

**Bad:** "We architect resilient bidirectional data-synchronisation layers that eliminate manual
reconciliation overhead across disparate operational systems."
**Good:** "Your till and your warehouse do not talk. Someone counts stock by hand every week. I make
them talk overnight and send you only the mismatches."

---

## 3. Never justify, never apologize

State the work, state the price, state the change. No preemptive explanation, no defensive framing,
no apology for the fee or the timeline. Price gets defended when it is challenged, never before.

**Why.** An unasked justification tells the reader you expect an argument, so they go looking for
the argument. It converts a statement into an opening bid. The same sentence with the justification
removed is stronger and shorter, which is the whole trade.

**Test.** Delete every clause beginning with "because", "given that", "I know this might" or "just".
If the message still says what happens next, the clauses were noise.

**Bad:** "I know two weeks might seem like a lot for something like this, but there is genuinely a
lot of work in it, and I am more than happy to jump on a call to talk through the reasoning if that
would help."
**Good:** "Two weeks, fixed. One process gone, working, with a runbook. Scope and price are in the
proposal."

Cross-reference: this is also the cross-cutting rule in `CLAUDE.md`'s voice block and item 3 of the
pre-send checklist.

---

## 4. The value beat

Every post carries a mechanism, a set of steps, or a number. Diagnosis alone is not a post.

**Why.** Naming a pain proves you have seen the pain. It does not prove you can fix it, and the
reader's silent question after any "here is what is broken" post is "and?" A feed of unanswered
"and?" trains people to scroll past your name. The value beat is also what makes a post
un-plagiarisable: anyone can name the pain, only the person who built it knows which step everyone
skips.

**Test.** After the hook, can the reader do something, or check something, that they could not
before they read it? If not, it is a complaint with good formatting.

**Bad:** "most SMBs have two systems that do not talk to each other, and it is costing them far more
than they realise."
**Good:** "most smbs run two systems that do not talk. the tell -> someone exports a csv every
friday. the fix is three parts: a nightly pull, a diff, and an exception queue a human actually
reads. everyone skips the diff. the diff is the part that catches the night it failed silently."

How much of the beat renders per channel is a channel question, not a craft question, and
`knowledge/voice/channel-voice.md` owns it. The floor is the same everywhere: something the reader
can use.

---

## 5. No slogan copy on client documents

Proposals, invoices, SOWs, scoping readouts and status notes carry no tagline, no mission line, no
brand register. Sign-offs stay plain: the entity, the name, and how to reach a human.

**Why.** A client document is a document someone checks numbers on. A slogan in that context reads
as a brand asking to be liked in the same breath as it asks to be paid, and it makes every number
on the page feel like marketing. It costs credibility and buys nothing, because nobody ever chose a
vendor off an invoice footer.

**Test.** Cover the logo. Does any line exist purely to make the reader feel something about the
company rather than to tell them a fact? Delete it.

**Bad** (invoice footer): "Northwind Labs. Automation that actually ships."
**Good** (invoice footer): "Northwind Labs (operating under Rivera Holdings LLC). Questions on this
invoice: sam@northwindlabs.example"

**Scope.** Marketing surfaces, the site, posts and lead magnets, may carry a line if it earns its
place. Slogan register on a client document happens only when Sam explicitly asks for it.

---

## 6. No mention of a sales call before the CTA

In any funnel or giveaway asset, a call with Sam is mentioned exactly once, at the actual CTA, and
never before it. No disclosure lines up front, no "no call needed" reassurance, no early hint that
an ask is coming. A negated mention is still a mention.

**Why.** While the reader is receiving value, they are deciding one thing: is this person helping,
or selling. Any early mention of a call answers "selling", and every useful thing after it gets read
as bait. The help leads. The ask lands once, at the end, where it has been paid for.

**Test.** Read the asset top to bottom and mark the first place a call, a booking link or a
conversation with you appears. If it is not the CTA block, it is a violation, whatever it says.

**Bad** (page 1 of a worksheet): "By the end of this you will know whether you want a call with me.
No pressure either way."
**Good:** page 1 is the help and nothing else. The final block: "Want this built for you instead?
Here is the calendar."

**Scope.** A surface whose job *is* the CTA (the booking line, the closing block) is the CTA, not a
pre-mention. Client-side language in a scope document, a kickoff call or a weekly check-in, is not a
mention of a sales call.

---

## 7. Paste-ready copy carries its character count

Any block labeled paste-ready for an external surface states its character count in its own heading
and is checked against that surface's hard limit before it ships.

**Why.** A block that will not paste gets trimmed live in the platform's editor, and a live trim is
an unreviewed rewrite happening on a public surface with no diff and no reviewer. That is how
canonical wording forks, and it is how banned characters come back after a clean sweep.

**Test.** Count, then label. If the label and the count disagree, the label is a lie and the block
is not paste-ready.

**Bad:** `## About (paste-ready)` sitting above a block nobody counted.
**Good:** `## About (paste-ready, 2,412 chars, limit 2,600)`

No mechanical check behind this one. Counting is cheap and the failure is loud, so the control stays
procedural.

---

## The mechanical floor, and what it does not cover

`scripts/repo-doctor` ships one check for rule 1, `emdash-paste`. It is HARD in both modes: the
staged pass the pre-commit hook runs, and the full pass over the working tree.

- **Files:** `.md` under the send trees, `outputs/content/` and `outputs/outbound/`. The exact list
  lives in the script. Nothing else in the repo is scanned for dashes.
- **Lines:** only lines inside fenced blocks, because a fence is this repo's paste-block convention.
  A fence counts only at line start, so an indented fence inside an example does not flip the state.
- **Fails closed on broken fences:** an odd number of line-start fences means the file's fence
  structure cannot be trusted, so the whole file is treated as one paste block rather than letting a
  parity desync silently exempt the real blocks.
- **Posted-record exemption:** a block whose nearest preceding heading marks it as a record of what
  actually went out is skipped. Rewriting what was already sent in order to satisfy a checker
  falsifies the record, which is worse than the dash.

Three limits, stated so nobody mistakes this floor for coverage:

1. **It cannot see copy that never became a file.** A message typed into a chat window and sent is
   outside every mechanical control in this repo. The only control for that class is the one-line
   ban in `CLAUDE.md`'s voice block, which every session loads, and this file behind it.
2. **Repo-wide enforcement is not on the table.** Vendored reference material and quoted third-party
   sources are full of the character. A check that fires thousands of times on day one is a check
   that gets bypassed on day one, and a bypassed check is worse than none because it still reports
   clean. Everywhere outside the send trees, the ban is enforced by reading.
3. **Rules 2 through 7 have no mechanical check and probably never will.** Taste does not lint. They
   are enforced at review, which is exactly why each one above ships with a one-pass test instead of
   a vibe.

**Guardrail rot** (named in `ai/ERRORS.md`'s Hazards section) is the live risk here: a check that
quietly stops firing keeps buying confidence it no longer earns. If you change the send-tree list,
the fence convention or the heading exemption, re-run the fixture that proves `emdash-paste` still
fires on a planted dash. `knowledge/ops/os-roadmap.md` owns that fixture suite.

---

## What this file is not

- **Not a mandate to sweep history.** Superseded drafts and archived corpora stay exactly as
  written. A corpus is evidence of how you actually sounded, and editing evidence to match today's
  rules destroys the only thing it was good for.
- **Not a pricing file.** There is no number in here and there never will be. A price restated in a
  voice file is a price that eventually gets quoted from a voice file. `ai/ERRORS.md` 2026-07-11 is
  a dead number that lived in four files and reached a client from one of them. Pricing authority:
  `knowledge/business/outbound-offer.md` and the client's roadmap under `knowledge/clients/`.
- **Not a claims file.** What may be said publicly about a piece of client work is owned by that
  client's own `README.md`, never assumed from a case study or a post.
- **Not channel voice.** Lowercase on X, sentence case on LinkedIn, the pillar mix, the DM shape:
  all of that is `knowledge/voice/channel-voice.md`, and all of it is replaceable. The seven rules
  above are not.

*(Worked-example names and examples throughout. The rules and their reasoning are the part to keep.)*
