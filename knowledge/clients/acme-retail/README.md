# Acme Retail - client front page

**Scope, phases and prices are owned by `knowledge/clients/acme-retail/roadmap.md`.** This file
carries no figures. It holds what is true across the whole relationship: who they are, how they
behave, what may and may not be said about them, and where everything else lives.

**Last updated:** 2026-08-04.

## Who they are

Specialty retailer, roughly 40 staff. Three stores plus a small warehouse that supplies all three.
Family-owned, no IT function, no in-house developer. One person runs operations for the whole
group and that person is our contact.

Their point-of-sale and their warehouse system have never talked to each other. Until 2026-07-18
someone reconciled stock counts by hand every week, in a spreadsheet, and the numbers were wrong by
the time the reconciliation finished. That is the entire origin of this engagement.

## Status today

- Phase 1 (discovery) and Phase 2 (the nightly sync) are delivered, signed off and paid in full.
- The sync has been in production since 2026-07-18. Two incidents since, both handled, both logged
  in the roadmap.
- Phase 3 (ops dashboard) was proposed 2026-08-01 and is undecided. The decision date and the chase
  rule are armed as a `**Due:**` line in the roadmap, which owns them.
- Nothing is currently blocked on us.

## Contact and cadence

- **One contact: the ops lead.** They own the weekly reconciliation, so they felt the pain directly
  and they are the internal champion for everything we have built. Treat them as the buyer for
  practical purposes.
- **The owner signs.** The ops lead recommends, the owner approves. That is one extra hop on every
  decision and it is the main reason a decision date is a week out rather than a day.
- **Venue:** chat for day-to-day, email for anything carrying a number. Sending a price over chat
  invites a chat-speed answer, which with this client means the ops lead answering for the owner.
- **Reply pattern:** same day on chat, a day or two on email, and effectively silent during
  stocktake week. Silence has twice turned out to be workload, never a no. Chase once, in one line,
  and do not attach a new number to the chase.

## Relationship read

- **Trust: high, and earned recently rather than assumed.** Two phases delivered on what was
  promised, both invoices paid without a reminder.
- **Price posture: not hostile, and not a haggler.** They have never asked for a phase price to come
  down. They did ask for scope to go up mid-Phase-2 and accepted the re-price in writing without
  argument. The lesson to carry: with this client the negotiation is about scope, not about the
  number, so protect the scope line and the number takes care of itself.
- **Cadence: one phase, one invoice, paid on receipt.** They have not asked for instalments and have
  not been offered any. Proposing a milestone split here would create a problem that does not exist.
- **Technical depth: operational, not architectural.** The ops lead reads the reconciliation report
  every morning and will spot a variance before we do. They will not evaluate the stack and do not
  want to. Frame everything in what a store manager sees, never in what the job does.
- **Who they protect:** their store managers. Any change that makes a store manager look wrong in
  front of head office is the change they will push back on, whatever it costs.

## Standing rules

- **No public reference.** No case study, no logo, no named testimonial, no "we built X for Y".
  Consent has never been asked for. Public copy says "a multi-location retailer" and nothing more
  specific until they say otherwise in writing, at which point that permission is recorded here and
  this bullet is rewritten. `.claude/product-marketing-context.md` routes any proof claim back to
  this file, so this bullet is the actual gate.
- **Two names, one client.** The trading name is Acme Retail. The paying entity is Acme Retail
  Group. The first invoice went out to the trading name before their finance side corrected it;
  everything since bills the Group entity, and that is the default going forward. `scripts/money`
  collapses both spellings onto one owner, so the concentration math counts them once instead of
  showing two half-sized clients.
- **No client credentials in this repo.** The SFTP key and the point-of-sale API secret live in the
  password manager under named entries. The roadmap names the entries. It never holds the values.
- **No timeline they have not been given deliberately.** Nothing has been promised on a date for
  Phase 3. Keep it that way until there is a verified date to give.

## Concentration

Every dollar collected to date came from this client. That is a real single-point risk on the
revenue side, not a footnote: one relationship holds the entire cash base, and the same person is
the champion, the reporter of bugs and the route to the signer.

The number itself is generated, not written by hand. `scripts/money` recomputes concentration into
`knowledge/business/MONEY.md` on every run; read it there. The mitigation lane is the outbound
motion in `knowledge/business/outbound-offer.md`, not anything done inside this engagement.

## Where everything lives

| Thing | File |
|---|---|
| Phases, scope, prices, technical state, open risks, live commitments | `knowledge/clients/acme-retail/roadmap.md` |
| What was billed and what was paid | `knowledge/business/invoices/SUMMARY.md` |
| Per-invoice records | `knowledge/business/invoices/NL-2026-001.md`, `knowledge/business/invoices/NL-2026-002.md` |
| Cash position and concentration | `knowledge/business/MONEY.md` (generated by `scripts/money`) |
| Retired figures from this engagement | `ai/TOMBSTONES.md` |
| Rehearsal before a call or a send | `.claude/agents/client-sim.md`, grounded on this folder |
