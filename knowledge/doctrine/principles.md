# Operating principles

First-party. Written here, not inherited from anyone. Nine of them, and none is here on taste alone. Where a principle came out of a specific ruling in `ai/DECISIONS.md`, an incident row in `ai/ERRORS.md`, or a hazard named there, it cites it.

They are deliberately few. Thirty principles is the same as zero principles, because you cannot hold thirty things in your head at the moment you are about to do the wrong thing.

If you are adopting this template: read these as a worked example of the format, then delete the ones you do not actually believe and replace them with the ones that have already cost you money. A borrowed principle does not fire under pressure.

---

## 1. Verify before you promise

Nothing leaves with a date, a number or a capability claim that has not been checked against the file that owns it, in this session.

**Why.** An estimate given from optimism becomes a commitment the moment the other side hears it, and the walk-back costs more than the delay would have. (`ai/DECISIONS.md`, ruling of 2026-07-19.)

**Rules out.** Timelines from memory. Prices recalled instead of re-read. "Should be straightforward" said before opening the system. Any client-facing number that did not come out of its owner file minutes ago.

---

## 2. One owner per fact

Every price, status, deadline and KPI lives in exactly one file. Everything else links to it.

**Why.** A number copied into a second file is a number that will be wrong in one of them, and you will not know which. A superseded price sat in four files, one got updated, and the dead one reached a client. (`ai/ERRORS.md`, 2026-07-11.)

**Rules out.** Restating a figure "for convenience". Summary docs that quote numbers rather than paths. A deal stage recorded in both a client file and a rollup. When you catch yourself typing a value you read somewhere else, type the path instead.

---

## 3. If the rule is not mechanical, it will rot

A rule you have to remember is a rule you will forget on the day it matters. Any rule that can become a check becomes a check, in the session it is written.

**Why.** Conventions decay silently and nobody notices until the thing they prevented happens again. The failure mode above that is worse: a check that stops firing still looks like protection, so it buys false confidence for free. Guardrail rot is a named hazard in `ai/ERRORS.md`, and the fixture suite that tests the checks themselves is specified in `knowledge/ops/os-roadmap.md`.

**Rules out.** Cleanups that end with "be careful next time". Adding a convention without adding the grep that enforces it. Assuming a check still works because it was working when it was written.

---

## 4. Price the outcome, not the hours

Scope is fixed and priced as a phase. Speed is yours to keep.

**Why.** Hourly billing caps the upside on exactly the work that gets faster with reps, and it moves the conversation onto the hours instead of the result. (`ai/DECISIONS.md`, ruling of 2026-07-08.) The live numbers sit in `knowledge/business/outbound-offer.md` and the client's file under `knowledge/clients/`. They are never restated here.

**Rules out.** Hourly rates. Splitting an engagement into an "audit fee" that pre-negotiates the real work downward. Quoting a range to seem reasonable. Justifying a price before anyone has asked about it.

---

## 5. Do the manual version first

No automating a motion that has not been run by hand enough times to know what it actually is.

**Why.** Automating an unproven motion scales a mistake and then hides it behind a dashboard. Outbound stays manual sourcing and manual sends until 30 real conversations are logged, for exactly this reason. (`ai/DECISIONS.md`, ruling of 2026-07-26.)

**Rules out.** Buying tooling to avoid the uncomfortable part of the motion. Building the pipeline before there is anything in the pipeline. Counting "the system is built" as progress while the count of real conversations has not moved. Building is the comfortable failure mode for a technical operator, which is precisely why it needs a written rule and not good intentions.

---

## 6. Let stale things die

When a fact is superseded, the old version is bannered or struck in the same session, and the dead value goes into `ai/TOMBSTONES.md`. A file with no job left gets killed, not archived.

**Why.** Stale content does not sit quietly, it competes. Any current-sounding line will be read as current by a future session, by an agent, or by you at speed on a Friday.

**Rules out.** Appending a new section instead of fixing the old one. "Keeping it around for reference" with no banner on it. Deleting a resolved commitment silently, which destroys the record that it ever existed. Strike it through with the outcome instead.

---

## 7. Write the ruling down with a review date

Any decision that carries a prediction gets a row in `ai/DECISIONS.md` with a date to check it. Settled rulings are not re-argued.

**Why.** Without the row you relitigate the same question every few weeks and call it thinking. With the row but no date you never find out whether you were right, which is the whole point of writing it down.

**Rules out.** Re-opening a settled pricing or scope question because it has started to feel uncomfortable again. Decisions that exist only as prose in a chat log. A review cell that says "later".

---

## 8. Concentration is a risk you are carrying, not a compliment

Know what share of collected revenue comes from one client, and say the number out loud rather than round it away.

**Why.** A client who is all of your revenue is not a strong relationship, it is a single point of failure with a friendly face, and the day it ends is the day you start selling from zero with no warm pipeline. `scripts/money` computes the share on every run so it cannot be quietly avoided.

**Rules out.** Pausing outbound because delivery is full. Reading a large invoice as evidence of pipeline health. Finding out how concentrated you were at the moment it stops being true.

---

## 9. Nothing ships until it opens

A generated file is not a deliverable until it has been opened and validated as its real format. A `.pdf` passes `scripts/pdf-check`, a `.docx` passes `scripts/docx-check`.

**Why.** A generator that writes text and names it `.docx` produces a file that looks right in every way except the one that matters, and the client is the person who discovers it. (`ai/ERRORS.md`, 2026-07-22.)

**Rules out.** Shipping on "the generator exited clean". Treating successful text extraction as proof of validity, which passes happily on a malformed file. Any send where step 6 of the pre-send checklist got skipped because the artifact looked small.

---

## Adding a principle

One test: name the specific thing it would have prevented. If the answer is hypothetical, it is a preference, and preferences do not belong in this file. Preferences about how things read go in `knowledge/voice/copy-rules.md`. Preferences about everything else go nowhere.

Removing one has the same bar in reverse. A principle you have quietly stopped following is worse than no principle, because it makes the whole list read as decoration.
