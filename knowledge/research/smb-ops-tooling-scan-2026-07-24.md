# SMB ops tooling scan - what they already run

**Stale after:** 2027-09-01 - connector-platform plan tiers and per-operation pricing move every
quarter, and the whole conclusion turns on what those platforms still do not cover. (Demo page: the
date is set a year past the template's release so a fresh clone's clock stays quiet; the setup wipe
removes this file. A real scan of yours carries the date its sources actually rot on.)

**Decision this feeds:** is the Ops Automation Sprint sold as a *replacement* for the tools an SMB
already owns, or as the *glue* between them. Secondary question on the same run: keep selling
one-off glue per client, or build a connector product.

**Run:** slug `smb-ops-tooling-scan`, phases A to E, 2026-07-21 to 2026-07-24. Full claim table with
URLs and verbatim passages lives in the run directory under `outputs/research/`. This page carries
tier, as-of date and basis only, per `knowledge/research/README.md`.

**Triangulation:** same brief run through a second vendor's model. Two deltas, both reconciled
below.

**Prices:** none in this file. The offer's price is owned by
`knowledge/business/outbound-offer.md`; an engagement price is owned by that client's roadmap.

---

## Bottom line

1. **Sell glue, not replacement.** The tools are already bought, already trained on, already load
   bearing. Nobody buys a rip-and-replace from a solo operator. (C1, C2, C4)
2. **The wedge is the pair with no prebuilt connector.** Qualify on which two systems do not talk,
   and disqualify the moment a maintained connector exists for exactly that pair. (C3)
3. **Silent failure is the retainer hook, not the build.** The build is the sale. The night the
   sync dies quietly is what keeps the retainer alive. (C4, weakly C7)
4. **Do not build a connector product.** It would compete on the pairs the platforms already own
   and inherit the long tail that makes one-off work worth paying for. (C3, C5)

---

## Claims

Labels follow `skills/research-doctrine`. Tier, as-of date and basis here; URLs and the verbatim
passage behind each one stay in the run artifact.

**C1. Mid-market point-of-sale and warehouse systems document an export or webhook path, but gate it
behind an upper plan tier.**
`[SOURCE:P1, vendor documentation, as of 2026-07-22]` `[PERISHABLE: plan-tier feature gating]`
Confidence **7**. Four vendors' own documentation pages, two of them dated inside 90 days.

**C2. Small-business accounting and CRM packages publish read and write APIs with per-minute caps
well below a full-catalogue nightly push.**
`[SOURCE:P1, vendor API documentation, as of 2026-07-22]` `[PERISHABLE: rate limits]`
Confidence **7**. Three vendors' own rate-limit pages. Shapes the build (batch and backfill windows),
not the positioning.

**C3. The no-code connector category covers the popular pairs deeply and the long tail not at all.
Warehouse, clinic intake, dispatch and route planning have no maintained prebuilt connector.**
`[SOURCE:P2, two platform directories plus their own community request threads, as of 2026-07-23]`
Confidence **8**. Two independent directories agreeing, each tracing to a platform's own catalogue.
This is the load-bearing claim for the wedge.

**C4. In every operation looked at, the integration that matters is not run by a tool. It is run by a
person with a spreadsheet, on a weekly cadence.**
`[SOURCE:P1, own discovery notes, 5 calls, 2026-07-06 to 2026-07-21]`
Confidence **8**. First-party primary. Small n, stated in Limits.

**C5. Connector platforms price per task or per operation, so a row-level nightly sync costs more
than the same work batched.**
`[SOURCE:P2, pricing explainers, no vendor pricing page was read]` `[PERISHABLE: vendor pricing]`
Confidence **5**, **capped**. Pricing may only be asserted on P1, so this is stated as unverified and
is deliberately not load-bearing anywhere below.

**C6. The buyer is not comparing this to a connector platform. They are comparing it to hiring
another part-time ops person, or to leaving it alone.**
`[INFERENCE from: C3, C4]`
Confidence **6**, held below both premises on purpose: C4's n is 5 and this is the claim the pitch
leans on hardest.

**C7. Nothing in the category markets alerting on a sync that fails silently. Monitoring ships as a
dashboard the customer has to remember to open.**
`[SOURCE:P3, vendor marketing pages and two forum threads, as of 2026-07-23]`
Confidence **3**. Suggestive, not evidence. Nothing below rests on it.

**C8. SMB month-end reporting is assembled by hand from exports in most of the operations looked at.**
`[CARRIED: Phase B]`
Confidence **7**, carrying its Phase B tier unchanged. The matching entries in
`knowledge/pain-points/pain-point-bank.md` were collected independently, which is corroboration, not
a second source.

---

## What this means for the offer

**Positioning.** "I make what you already own talk to each other" beats "I build you a system".
C1 and C2 say the door is open (there is an export path, there is an API), C4 says the door is not
being used. A 40-person business will not re-train everyone on a Tuesday, and asking them to is how
a good build loses to no build.

**Qualification.** The question on a first call is which two systems do not talk, not what industry
they are in. The disqualifier is a maintained connector for that exact pair: if one exists, the job
is a configuration afternoon and the price collapses to what an afternoon is worth. C3 is what makes
the long tail defensible work. This belongs in the ladder, so `outputs/outbound/prospect-gate.md`
owns the applied version of it and this page owns the reasoning.

**Where the recurring revenue lives.** The build is the sale, and the build ends. What does not end
is the risk that the sync fails at 02:00 on a Sunday and nobody notices until the stock count is
wrong on Friday. C4 says that failure mode is exactly what the manual weekly process was
accidentally covering, because a human doing it by hand notices when it does not happen. Automating
it removes the human and the alarm at the same time. C7 hints that nobody in the category sells the
alarm back, but C7 is a 3 and carries no weight; the case rests on C4.

**No connector product.** C3 says the valuable pairs are the ones the platforms have declined to
maintain, and C5 hints that platform economics punish exactly the high-frequency shape this work
needs. Building a product means maintaining that long tail as a vendor, which is the cost the
platforms already chose not to carry. The asymmetry runs the right way today: one-off glue, priced
as a build.

---

## Deltas from the second-vendor run

1. **It put replacement above glue for businesses under about ten people**, on the argument that a
   very small operation has nothing worth preserving. Reconciled: not the buyer. A Sprint buyer is
   already paying for two systems, and that is what makes the pair exist at all. Glue stands.
2. **It rated C3 higher on directory counts alone.** Reconciled downward: a directory listing is a
   marketing surface, and two of the listed long-tail connectors resolved to community templates
   with no support commitment behind them. Directory presence is not coverage. C3 stayed at 8.

---

## What would change this conclusion

Observables, worst first.

1. **A connector platform ships long-tail connector authoring that a non-technical ops lead can
   actually finish.** Not a developer SDK; those exist and change nothing. The signal is a template
   gallery covering warehouse, intake and dispatch with a support commitment attached. That closes
   the C3 wedge, and the offer has to move up the stack to the exception queue and the alerting.
2. **Discovery calls stop naming the pair.** If two consecutive calls say the sync already works and
   the real pain is reporting, the wedge has moved to reporting. This shows up in
   `knowledge/pain-points/pain-point-bank.md` before it shows up in revenue, because every call's
   named pain lands there with its source type.
3. **More than half of the next ten logged outbound conversations open with "we are replacing X".**
   That is the market saying replacement, and the positioning line in
   `knowledge/business/outbound-offer.md` is then wrong rather than early.
4. **A prospect declines on per-operation cost grounds.** C5 is capped at 5 and is not load-bearing
   precisely so this does not quietly become an argument in copy. If it ever matters, re-run it as a
   P1 claim off the vendor's own pricing page first.

Nothing above turns on C7. If C7 collapses entirely, the alerting hook survives on C4 and the pain
bank; what dies is the market-gap framing around it, which was never load-bearing.

---

## Limits, stated plainly

- **n is 5.** Five discovery calls, all inbound or referred, all in retail and allied health. A
  biased sample, and it is the sample this conclusion rests on.
- **No enterprise.** Everything here breaks at the point a business has an IT function with an
  opinion and a procurement process.
- **No regulated-data pass.** Anything touching patient or payment data needs its own run.
  The allied-health engagement tracked in `knowledge/clients/beacon-health/README.md` sits in that
  class and this scan was not used to scope it.
- **No vendor names and no vendor prices in this file, on purpose.** Named-vendor pricing is the
  fastest-rotting claim there is, and a curated page carrying it reads as current for a full quarter
  after it stops being true. Categories age slower, which is why the Stale-after line is four months
  out rather than one.

---

## Write-back executed 2026-07-24

- `knowledge/business/outbound-offer.md`: the scope boundary now says plainly that replacing either
  system is out of scope and that we sync what they already have. No price touched. That file owns
  the number and the number did not change.
- `knowledge/business/brand_foundation.md`: the buyable-problem section now points here as the market
  read behind the glue framing, rather than repeating the reasoning.
- `knowledge/pain-points/pain-point-bank.md`: **no change.** The entries that corroborate C4 and C8
  were already promoted on their own call and forum evidence, before and after this run. Promoting
  them again on a scan that cites them would have turned one body of evidence into two.
- **Nothing written to `ai/DECISIONS.md`.** This is a fact-state update, not a ruling. If the glue
  framing gets challenged again, that is when it earns a row with a review date.

**Terminal at the decide phase. No market-test phase.** Re-verify on or before the Stale-after date
at the top, or the first time an observable above fires.
