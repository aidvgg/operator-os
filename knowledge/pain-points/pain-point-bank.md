# Pain point bank

The readable bank. Seven entries: what small and mid-size operators say is broken in their own
back office, who feels it, what it costs, and what Northwind Labs would build against it.

`pain-point-bank.csv` in this folder is the machine-readable mirror of this file. Same entries,
same ids, same values. Edit both in the same pass or the mirror is a lie. Schema, the quality
bar, and the promotion rule live in `knowledge/pain-points/README.md`.

**No prices in this file.** Offer angles describe what gets built, never what it costs to buy.
Sell-side pricing has exactly one owner per motion: `knowledge/business/outbound-offer.md` for
the productized offer, the client's roadmap file in `knowledge/clients/` for an engagement. The
dollar figures below are the *prospect's* cost of the problem, which is a different fact and is
always marked as an estimate.

*(Everything below is the template's worked example. Delete all seven rows, keep the shape.)*

---

## Index

| ID | Theme | Status | Intensity | WTP | Source type | Added |
|---|---|---|---|---|---|---|
| PP-001 | inventory-reconciliation | PROMOTED 2026-07-09 | 5/5 | Yes - explicit | discovery call | 2026-07-06 |
| PP-002 | double-entry | PROMOTED 2026-07-28 | 4/5 | Yes - implied | discovery call | 2026-07-23 |
| PP-003 | month-end-reporting | PROMOTED 2026-07-21 | 4/5 | Yes - implied | forum scan | 2026-07-14 |
| PP-004 | silent-failure | PROMOTED 2026-07-21 | 5/5 | Yes - implied | forum scan | 2026-07-16 |
| PP-005 | location-onboarding | CANDIDATE - not promoted | 3/5 | Unclear | peer conversation | 2026-07-27 |
| PP-006 | data-drift | CANDIDATE - not promoted | 3/5 | Unclear | forum scan | 2026-08-01 |
| PP-007 | knowledge-in-inbox | CANDIDATE - not promoted | 3/5 | Unclear | inbound DM | 2026-08-03 |

Spread: 4 promoted, 3 candidates. Intensity 5/5 x2, 4/5 x2, 3/5 x3. Sources: 2 calls, 3 forum
scans, 1 peer conversation, 1 inbound DM. A bank where everything scores 5/5 is a bank that has
stopped judging, so the spread is the health check, not the count.

---

## PP-001 - Weekly stock count reconciled by hand between two systems

**Status** PROMOTED 2026-07-09 · **Theme** inventory-reconciliation · **Intensity** 5/5 · **WTP** Yes - explicit
**Added** 2026-07-06 · **Source** discovery call, retail prospect

**Summary**: Multi-location retailer whose point-of-sale and warehouse system do not talk. One
person exports both every Monday and hunts for the rows that disagree. The count is stale again
by midweek.

**Who feels it**: ops lead at a 20 to 60 person multi-location retailer. Reports to the owner,
has no engineer.

**Observable symptom**: a shared spreadsheet with a version number in its filename, updated every
Monday morning. Store managers phone the office to ask what stock actually is rather than trust
the screen.

**In their words**:
> Every Monday I export from the till system, export from the warehouse system, and sit there
> with two tabs open looking for the rows that disagree. It takes most of the day and by
> Wednesday it is wrong again.

**What it costs**: 5 to 8 hours a week of the ops lead, roughly $1,100 to $2,300 a month in
loaded time, before any sale lost to a location showing stock it does not have. Estimated from
the call, not measured.

**Offer angle**: nightly two-way sync plus a reconciliation report listing only the disagreeing
rows, and an alert when the disagreement count jumps. Scoped and priced per engagement in the
client roadmap file.

**Curation note**: the entry that produced the first paid build, see
`knowledge/clients/acme-retail/roadmap.md`. Quantified, first person, active now, and the buyer
asked what a fix would cost before we raised it. That last tell is why this is the only
Yes - explicit row in the bank.

---

## PP-002 - The same intake form typed into two systems

**Status** PROMOTED 2026-07-28 · **Theme** double-entry · **Intensity** 4/5 · **WTP** Yes - implied
**Added** 2026-07-23 · **Source** discovery call, clinic group prospect

**Summary**: intake form is completed once and typed into two systems that do not integrate.
Mismatches are invisible until a downstream bill or claim bounces.

**Who feels it**: front-desk admin at a 5 to 20 person appointment-based business, plus the
practice manager who fields the fallout.

**Observable symptom**: a tray of completed forms beside the keyboard, and the habit of opening
one system to check the spelling of a name in the other.

**In their words**:
> The form gets filled in once and typed in twice. When the two do not match nobody finds out
> until billing bounces, and then it is my problem and the patient's problem.

**What it costs**: 10 to 14 minutes per new record. At 60 to 90 new records a month that is 10 to
20 hours, plus rework on the mismatches. Roughly $700 to $1,600 a month. Estimated from the call.

**Offer angle**: one intake form as the single entry point, writing to both systems, with a
mismatch queue for records that fail validation instead of a silent overwrite.

**Curation note**: sat as a candidate for five days on one voice alone. Promoted once a paid
scoping engagement confirmed the record volume, see `knowledge/clients/beacon-health/README.md`.
The generalizable part is not the sector, it is the shape: one form, two destinations, no
reconciliation, and the error surfacing at the money end.

---

## PP-003 - Month-end reporting assembled by hand from four exports

**Status** PROMOTED 2026-07-21 · **Theme** month-end-reporting · **Intensity** 4/5 · **WTP** Yes - implied
**Added** 2026-07-14 · **Source** forum scan, Reddit r/smallbusiness
**Prefilter** score 4 · signals: first_person_pain, quantified, named_stack, asking_how

**Summary**: the first week of every month goes to building a workbook with a tab per source
system. The bottom-line number is still not trusted, and prior months get restated when an error
surfaces.

**Who feels it**: owner-operator of a 10 to 50 person business, or the bookkeeper who builds it
and the owner who does not trust it.

**Observable symptom**: a workbook with a tab per source and a summary tab of formulas nobody
else can follow. Decisions wait for it, then get made on it anyway.

**In their words**:
> the first five days of the month i am not running the business, i am building the report about
> the business. four exports, one workbook, and i still do not trust the number at the bottom.

**What it costs**: 15 to 25 hours per month-end for one person, roughly $900 to $1,900 a month.
The larger cost is a week of decisions made on last month's guess. Estimated, the poster gave
hours but no rate.

**Offer angle**: scheduled pulls into one table, one reviewed report, human step reduced to
sign-off. Anomaly flags on any figure that moves more than a set threshold.

**Curation note**: found by `scripts/reddit-scan`, curated by hand. Two more posts in the same
week described the same first-week pattern, which is the corroboration the bar asks for. The
buying trigger is calendar-driven, so this one lands in the last week of a month and dies in the
second.

---

## PP-004 - The nightly job that had been dead for nine days

**Status** PROMOTED 2026-07-21 · **Theme** silent-failure · **Intensity** 5/5 · **WTP** Yes - implied
**Added** 2026-07-16 · **Source** forum scan, Reddit r/msp
**Prefilter** score 4 · signals: first_person_pain, quantified, tried_failed

**Summary**: a scheduled sync ran cleanly for months, so nobody watched it. It failed silently
and the failure was found by a customer, days later, with a manual backfill to follow.

**Who feels it**: the one semi-technical person in the business, or the owner where there is no
technical person at all.

**Observable symptom**: no dashboard and no alert, just a habit of opening the tool to check it
ran. The failure is found downstream, by a customer or an accountant.

**In their words**:
> it ran fine for months so we stopped looking at it. it had been dead nine days before anyone
> noticed and then we lost two days backfilling. no error, no email, nothing.

**What it costs**: one to three incidents a quarter, 6 to 16 hours of backfill each, roughly $600
to $1,800 an incident, plus the credibility hit with whoever found it first. Estimated.

**Offer angle**: a heartbeat on every scheduled job and an alert when a job does not report in,
not only when it errors. Ships with a runbook naming who gets called and what they do.

**Curation note**: the strongest entry in the bank that is not about labor hours, and the one
that reframes reliability work as insurance rather than efficiency. Timing-sensitive in the
opposite direction to PP-003: it converts in the fortnight after an incident and reads as
theoretical in a quiet quarter. Worth pairing with PP-001 or PP-003 in any pitch, because a sync
nobody monitors is the same failure waiting on a longer fuse.

---

## PP-005 - Opening a new location is two weeks of manual setup

**Status** CANDIDATE - not promoted · **Theme** location-onboarding · **Intensity** 3/5 · **WTP** Unclear
**Added** 2026-07-27 · **Source** peer conversation, operator in the same market

**Summary**: every new site is provisioned by hand from a checklist, and every site ends up
configured slightly differently from the last one.

**Who feels it**: operations director at a business opening its fourth site or later.

**Observable symptom**: a checklist document of 40 to 60 line items, copied and renamed per
opening, with someone's initials against half the rows.

**In their words**:
> Opening a site is a two week admin job before anyone sells anything, and every site ends up
> slightly different because whoever set it up made their own calls.

**What it costs**: 60 to 100 hours per opening, roughly $3,000 to $5,000 of internal time, plus
config drift that later shows up as reporting that does not compare like for like. Our estimate,
not theirs.

**Offer angle**: provisioning driven from one config file per location, so a new site is a form
submission and a review rather than a fortnight. Drift report naming where a site diverges from
the standard.

**Why still a candidate**: one voice, no second source, and the cost figure is ours rather than
anything the operator stated. It also only bites a business that opens sites often enough to
care, which narrows the buyer more than the other six. Promote it when a second operator
describes the same shape unprompted.

---

## PP-006 - The CRM and the billing system disagree on the customer count

**Status** CANDIDATE - not promoted · **Theme** data-drift · **Intensity** 3/5 · **WTP** Unclear
**Added** 2026-08-01 · **Source** forum scan, Reddit r/SaaS
**Prefilter** score 3 · signals: first_person_pain, named_stack, asking_how

**Summary**: sales maintains the CRM, finance maintains billing, neither is wrong, and the
business has two answers to how many customers it has.

**Who feels it**: whoever has to defend the revenue number out loud, usually the founder.

**Observable symptom**: a recurring email thread asking which record is right, and a monthly
ritual of picking the number that looks more defensible.

**In their words**:
> sales updates the crm, finance updates the billing system, and neither one is wrong. we just
> have two answers to how many customers we have and i pick one before the monthly review.

**What it costs**: 3 to 6 hours a week chasing which record is right, roughly $500 to $1,300 a
month. The real cost is a headline number the owner cannot defend. Our estimate, no figure was
stated.

**Offer angle**: one system named as the source of truth per field, a one-way sync in the
direction that follows from it, and a weekly drift report on the fields that still diverge.

**Why still a candidate**: real and common, but the poster stated no hours and no money, so the
whole cost line is inference. The prefilter kept it on signal alone. One call that puts a number
on it moves it to promoted, and if the number comes back small it gets retired instead.

---

## PP-007 - What was promised lives in one person's inbox

**Status** CANDIDATE - not promoted · **Theme** knowledge-in-inbox · **Intensity** 3/5 · **WTP** Unclear
**Added** 2026-08-03 · **Source** inbound DM, reply to a post

**Summary**: the quote, the exception granted and the date agreed all live in one person's email.
When that person is away nobody can answer a customer.

**Who feels it**: owner of a 5 to 15 person services business who still sells every job
personally.

**Observable symptom**: the team messages the owner on holiday to ask what was agreed. Jobs get
re-done because the agreed scope was reconstructed from memory.

**In their words**:
> If I am off for a week the team cannot tell a customer what we agreed, because what we agreed
> is in my inbox.

**What it costs**: 2 to 4 hours a week of interrupted owner time, plus at least one re-done job a
quarter. Roughly $400 to $900 a month of owner time. Softest estimate in the bank.

**Offer angle**: a job record created at quote time that carries the agreed scope and the thread
with it, so the answer sits in the same place for everyone.

**Why still a candidate**: genuine, and the weakest of the seven on evidence. The cost is soft,
and the buyer is the same person who would have to change their own habit, which is the hardest
sale in the bank. Kept because it converts well as *content* even if it never converts as an
offer, and the bank feeds both.
