# LinkedIn safety rules

**Stale after:** 2027-09-01 - platform limits and enforcement behaviour change without notice and
without announcement. Nothing below is a published limit. Re-verify against the platform's current
help pages before relying on any number here, and supersede this page rather than bumping the date.
(Template page: the date is set a year past the template's release so a fresh clone's clock stays
quiet. Re-verify the numbers before you rely on them, whatever the date says.)

**Verify before relying on.** Every figure on this page is an operating heuristic assembled from
public guidance and observed behaviour. Treat them as a conservative envelope, not as a threshold
you are entitled to run at.

**Authority note.** This file owns the **safety envelope**: the band a send volume must stay
inside, and the signals that force a stop. It does not own how many messages actually go out on a
given day. That is a motion decision, recorded in `knowledge/memory.md` and counted in
`knowledge/ops/logbook/STATS.md`. If the operating number ever sits outside the band below, the
band wins and the motion changes, not this page.

The offer, the gate and the copy freeze that govern what gets sent:
`knowledge/business/outbound-offer.md`.

---

## Safe daily volume

Round numbers on purpose. Precision here would be false confidence.

| Action | Envelope | Note |
|---|---|---|
| Connection requests | 15 to 25 per day, about 5 days a week | Roughly 100 to 125 a week. Risk climbs steeply past 50 a day, and faster still with any automation attached. |
| Messages to existing connections | up to about 50 per day | Spread across the day. Never in one burst. |
| Profile views | browse normally | Do not speed-click through hundreds in an hour. There is no useful number here, only a pattern that looks like a script. |
| InMail or paid-seat messaging | not used | Assumes a seat this operation does not run. If that changes, this row needs its own verified envelope before the first send. |

A weekly invitation ceiling also exists and is enforced separately from any daily pattern. It is
not restated here as a number, because it is exactly the kind of figure that moves. Assume it
exists, stay well under it, and treat the platform's own warning banner as the real boundary.

## Rules to follow

1. **Batch, do not blast.** Two batches a day, morning and afternoon. Never the day's whole
   allocation in one sitting.
2. **Vary the timing and the count.** Not 9:00 sharp, not exactly 20 every day. A fixed clock and
   a fixed count is the single most script-shaped pattern available to a human.
3. **Personalise anything with a message body.** No identical text sent to many people in a short
   window. A no-note connection request sidesteps this on the invite itself; it still binds on
   every follow-up.
4. **Zero third-party automation.** No sequencer, no scheduler, no browser extension that clicks
   for you. This is the fastest route to a restriction, and it is also a standing ruling, not a
   preference: manual sourcing and manual sends until the gate resolves, `ai/DECISIONS.md`,
   2026-07-26.
5. **Request hygiene.** If requests are ignored 5 times in a row, stop and review the targeting.
   A growing pile of ignored and pending invites is what produces "I do not know this person"
   reports, and those compound into restrictions.
6. **One account, one machine, one network.** Do not log in from several networks in the same day.

## What gets an account restricted

Detection signals, in rough order of how reliably they fire:

- any third-party automation tool touching the account
- identical message text to many people in a short window
- several "I do not know this person" reports from rejected requests
- logging in from multiple locations or IPs on the same day
- a very high total action count in a single day
- perfectly regular cadence: same time, same count, every day

Note that four of the six are pattern signals rather than volume signals. Staying under a number
while behaving like a script is not safety.

## Warning banner protocol

If the platform shows **any** warning banner (a weekly invitation limit notice, a "you are
connecting too quickly" prompt, or any similar restriction notice):

1. **Stop all outreach for 7 days.** All of it, including messages to existing connections.
2. Write down which pattern most likely triggered it, in the day's logbook entry.
3. Restart at the bottom of the band, around 10 a day, and ramp back over two weeks.

A banner is the cheap warning. It is the last free lesson before the expensive one.

## Restriction protocol (break glass)

A different tier from a warning banner. This is for an account that is actually restricted or
locked out. The envelope above exists so this section never fires.

1. **Try the app first.** If the platform asks for identity verification and the in-app flow
   works, complete it there and follow its instructions. Everything below is only for when the
   in-app flow fails.
2. **File one support ticket** through the account-access form in the platform's own help centre.
   Describe what actually happened, plainly, in two or three sentences.
3. **Truth gate.** Never send a canned description of a failure that did not happen. An identity
   or trust-and-safety matter is the one place a copied template can turn a temporary restriction
   into a permanent one. Describe the real failure or say nothing.
4. **Phishing gate.** A restricted account is a prime phishing target. Upload identity documents
   only through the platform's own app or its own domain, reached by typing the address yourself.
   Never through a link in an email, however official it looks. The platform never needs your
   password.
5. **If the appeal is rejected, wait 14 days and do not touch the account at all.** No logins, no
   second ticket. Let the rejected ticket age out, then file a new one saying the same true thing.
   The lever is patience, not escalation. This can take several rounds.
6. **Confirm receipt.** After submitting, check that the automated acknowledgement email arrived.
   No acknowledgement means the submission probably did not land; resubmit.

## Other channels

The same envelope shape applies to X and to email, with different numbers and different
enforcement. Do not copy the figures above across platforms. If a second channel goes live, it
gets its own verified envelope on its own page before the first send, and this page's authority
note pattern is the one to copy.

## Maintenance

Re-verification is not a date bump. When the expiry above arrives:

1. Re-read the platform's current published guidance on invitation limits and automation.
2. Check the logbook for any warning banner or unusual rejection rate since the last check.
3. Either move the numbers and the date together with a note on what changed, or supersede this
   page with a banner pointing at its replacement.
