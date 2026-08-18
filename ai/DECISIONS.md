# DECISIONS.md - the judgment ledger

One row per decision that has actually been settled. Read this file before any decision-shaped
move: pricing, scope, a gate, a commitment, a client send.

**A settled ruling is not re-argued.** If a row covers the question in front of you, execute it and
move on. That is the whole point of the ledger: a decision costs its argument once. Re-opening a
row is itself a decision and gets its own row, dated the day it was re-opened.

## The columns

**Ruling** is what was decided, stated so a stranger could execute it without the conversation that
produced it. Write the boundary too, because most re-argument is really a scope question wearing a
disagreement costume: say what the ruling does not cover.

**Why** is the reasoning in a sentence or two, plus the falsifier. A ruling with no falsifier is a
preference, and preferences do not need a ledger. Name the observation that would prove the ruling
wrong, so the review has something to read instead of a mood to consult.

**Review on** is what keeps a row honest. A ruling made today is a bet, and the review date is when
the bet gets scored. Three consumers read this column:

- `scripts/horizon` surfaces a review as its date comes up, and prints any open row whose cell is
  not a date under its REVIEW-DATE PARSE block rather than dropping it silently.
- full-mode `scripts/repo-doctor` emits a soft `decision-undated` line for every open row whose
  cell holds no `YYYY-MM-DD`.
- `/weekly` re-reads every row past its date whose Outcome is still blank.

The file's own rule is **no review date, no row.** A row leaves the nag exactly two honest ways:
Sam sets a real date, or the row closes with a verdict mark in Outcome. Never by silencing the
check, never by deleting the row.

**Outcome** stays blank while the question is live. At review it gets one line: what was predicted,
what actually happened, and whether the ruling holds. Both `horizon` and `repo-doctor` skip a row
once its Outcome cell opens with a verdict mark, so a blank cell or an hourglass keeps nagging on
purpose. A miss that cost real money or real time gets promoted to a row in `ai/ERRORS.md`.

## Superseding a row

Do not edit a ruling in place and do not delete it. Instead:

1. Strike the dead ruling with `~~...~~` and close its Outcome with the verdict plus a pointer to
   the row that replaces it.
2. Add a new row dated the day the decision was actually made, not the day it got written down.
3. If a number died with the ruling, the ripple rule fires in the same session: add the dead string
   to `ai/TOMBSTONES.md`, then grep the tree and banner or strike every current-sounding copy.

A ruling that quietly changes shape is worse than no ledger at all, because every satellite file
and every future session still believes the old one.

## Template note, and this one is deliberate

The third row's Review-on cell holds an event gate instead of a date, in the form
`Gate: <condition>`. That is the ledger's second valid review shape: a date creates a calendar
review that `scripts/horizon` nags when it passes, and a `Gate:` cell creates a review that fires
when the condition is met, which the clock cannot judge, so horizon lists it under EVENT GATES
every run instead of inventing a date for it. Any other non-date cell (an empty one, or a bare
"after 30 conversations") is a broken row: `scripts/repo-doctor` names it as `decision-undated`
and horizon lists it under REVIEW-DATE PARSE, because a review that can never fire is not a
control. Try it: strip the `Gate:` prefix from the third row and run both scripts. Delete this
section along with the demo rows when you make the repo yours.

| Date | Ruling | Why | Review on | Outcome |
|---|---|---|---|---|
| 2026-07-08 | **The Ops Automation Sprint is priced at one flat $4,000, never hourly and never split into an "audit fee" plus a build fee.** Owner of the number is `knowledge/business/outbound-offer.md`, and outside this ruling no other file restates it. What this does not cover: client build phases, which are priced per engagement in that client's roadmap file. | Hourly invites scope haggling and caps the upside on work that gets faster with reps. Falsifier: the flat price meets zero resistance across the next batch of sprint conversations, which means it was set too low and the number should move rather than the model; or every sprint needs a change order to land, which means one flat price cannot hold the scope and the answer is a narrower boundary, not an hourly fallback. | 2026-10-08 | |
| 2026-07-19 | **Every client message uses phase-and-price framing, and no timeline is given until Sam has personally verified it.** Applies to the whole client surface: proposals, invoices, direct messages, call follow-ups. A date taken from a tool, a calendar guess, or somebody else's estimate is not verified. | A timeline given from optimism became a missed date and an apology. Falsifier: a personally verified timeline still slips, which would mean the verification step is checking the wrong thing, and the fix is to commit to a dependency ("starts when the API credentials land") rather than to a calendar date. | 2026-10-19 | |
| 2026-07-26 | **Outbound stays manual sourcing and manual sends until 30 real conversations are logged.** No sequencer, no scraper, no automation tooling before then. A real conversation is a two-way exchange, not a send. | Automating a motion that has not been proven by hand scales a mistake, and buys tooling for a bottleneck nobody has identified yet. Falsifier: manual volume stalls well short of 30 for reasons that are capacity rather than fit, in which case the constraint is Sam's hours, the gate is protecting nothing, and tooling was the right question all along. *(The Review-on cell is an event gate, not a date, on purpose. See the template note above.)* | Gate: 30 real conversations logged | |
