# Beacon Health - client front page

**Stage: scoping.** A paid diagnostic is delivered and invoiced. The readout has not happened yet.
**There is no build scope and no build price. None may be quoted, in any form, until the readout.**

**Last updated:** 2026-08-04.

There is no `roadmap.md` in this folder on purpose. A roadmap exists once there are phases and a
number. Until then this page is the whole client, and it owns the one price that does exist: the
diagnostic fee below.

## Who they are

Allied-health clinic group. 12 staff across three sites, physiotherapy and podiatry with a
part-time dietitian. Owner-operated by two clinicians who both still see patients. No IT function.
The practice manager runs everything operational across all three sites.

## The problem in their words

Every new patient's intake is typed twice. Once into the practice-management system, where the
clinical record lives, and once into the billing system, because the two do not integrate and never
have. The front desk does both. Appointment changes are entered twice as well, which nobody
mentioned until the diagnostic went looking.

The cost is not the typing. It is that a transcription error surfaces weeks later as a rejected
claim, at which point someone has to reconstruct what the correct detail was, resubmit, and chase.
Group-wide they take roughly 60 new intakes a week.

## Engagement to date

- **2026-07-27: paid scoping diagnostic agreed. Price: $1,500.** This file is the owner of that
  figure.
- **2026-07-31: diagnostic delivered and invoiced as NL-2026-003.** Currently outstanding. The
  register entry and the cash position live in `knowledge/business/invoices/SUMMARY.md`; the armed
  chase line lives in `knowledge/business/invoices/NL-2026-003.md`, which owns it. Do not restate
  either here.

**Why the diagnostic was paid rather than free.** A free scope is a free consulting engagement, and
it ends in a proposal nobody has committed anything to. Charging for it filters for intent, pays for
the week, and makes the output theirs whether or not a build follows. It also means the first
conversation about money already happened and went fine, which is a real signal about the second.

## What the diagnostic covered

The two systems and what each one is actually authoritative for. The intake path end to end at one
site, watched rather than described. Field-level mapping between the two systems. Where in that path
re-typing introduces error. What an integration would fix and, more usefully, what it would not.

## Hard rule for this client: no patient data

No patient data leaves their environment and none enters this repo, at any stage, including a build.

The diagnostic worked from field-level schema, record counts, and a redacted sample the practice
manager prepared themselves. That boundary is not negotiable on our side and it is not a technical
judgement to be made mid-build. If a future scope genuinely needs real records to be correct, that
is a conversation with them about their obligations, raised in advance, in writing, before any code
assumes access.

Practical consequence for anything generated here: a proposal, a brief or an agent run for this
client is grounded on schema and counts. If a draft contains a patient detail, something has gone
wrong upstream and the draft is discarded rather than edited.

## Findings so far

Headline only. The delivered document holds the detail.

1. **The integration has a licence cost that is theirs, not ours.** Their practice-management system
   can emit an outbound webhook on the plan they are already on. Their billing system exposes an
   import API only on a higher tier than the one they hold. So the cheapest technical path carries a
   recurring subscription increase they have not budgeted for and did not know about. This is the
   single biggest open question and it is the reason no build number exists yet.
2. **The duplication is wider than intake.** Appointment reschedules and cancellations are entered
   twice too. Any integration that only covers intake leaves the second-largest source of the same
   error class untouched, and would be sold as fixing a problem it half fixes.
3. **Nobody owns the reconciliation.** Rejected claims come back to whoever is on the desk that day.
   There is no queue and no record of how often it happens, so the cost is felt but not measured.
   The measurement is worth doing before the build, not after, or there is no way to show the build
   worked.

## The readout

~~**Due:** 2026-08-08~~ **Due:** 2027-09-08 - Beacon Health scoping readout call (demo commitment, re-dated a year
out so a fresh clone's clock stays quiet; the setup wipe removes this file). Walk the three findings, put the licence
tier question to them directly, and leave the call with either a decision to scope a build or a
clean no. Both are good outcomes. A vague third answer is not.

**No build number in that call.** Not a range, not "roughly", not a comparison to another client's
engagement. The tier question changes the shape of the work, so any number given before it is
answered is a guess that becomes an anchor. If pressed: phase and price come after the tier answer,
and that is the entire reply. No explanation offered, none needed.

## Contact and cadence

- **The practice manager** is the day-to-day contact and the person who feels the pain. Everything
  has gone through them.
- **The two owners sign.** They meet weekly and decide things there, so anything sent late in a week
  gets an answer early in the next one. Build that into any date rather than being surprised by it.
- **Email only.** No chat channel, and they have not offered one.
- **Reply pattern: prompt and detailed.** They answer with more information than was asked for,
  which is the pattern of a client who wants to be understood correctly rather than one who is
  stalling.
- **They asked about privacy before they asked about price.** That is where the first real objection
  will come from, and it is the reason the data boundary above is written as a rule rather than a
  preference.

## Trust and price posture

New relationship. One paid transaction, invoiced and not yet cleared. No history of chasing, no
history of a negotiation, no observed reaction to a number larger than they expected.

That last one is genuinely unknown and it should be said out loud rather than assumed in either
direction. Anything simulating this client should return `not in the files` on price posture instead
of inventing a haggler or a pushover.

## Standing rules

- **No public reference of any kind.** No case study, no logo, no sector name attached to a
  testimonial. Health sector, new relationship, consent never asked for. If public proof is ever
  wanted here, it is asked for explicitly and the answer is recorded in this file.
- **No patient data.** See the hard rule above.
- **Bill-to** is copied exactly as it stands on the invoice record, never retyped from memory.
  There is one spelling here, unlike Acme, so there is nothing for `scripts/money` to collapse.
- **No timeline.** Nothing has been promised on a date beyond the readout, and nothing should be
  until there is a scope to hang a date on.

## What is genuinely undecided

Whether there is a build at all. The honest read is that the licence-tier answer decides it: if the
higher tier is affordable to them the integration is straightforward and worth doing, and if it is
not, the realistic options are a thinner manual-assist scope or nothing. Both of those are fine
outcomes for a diagnostic that has already been paid for.

## Where everything lives

| Thing | File |
|---|---|
| What was billed and what is outstanding | `knowledge/business/invoices/SUMMARY.md` |
| The invoice record, and the armed chase tripwire | `knowledge/business/invoices/NL-2026-003.md` |
| Cash position | `knowledge/business/MONEY.md` (generated by `scripts/money`) |
| The productized offer, if the answer turns out to be a small one | `knowledge/business/outbound-offer.md` |
| Rehearsal before the readout call | `.claude/agents/client-sim.md`, grounded on this folder |
| Folder conventions and the price rule | `knowledge/clients/README.md` |
