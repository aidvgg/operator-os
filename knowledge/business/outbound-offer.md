# The outbound offer: Ops Automation Sprint

**This file is the pricing authority for the productized outbound motion.** It owns the sprint
price, the care-retainer price, the raise rule, the qualification bar and the gate. Any price for
this offer found in any other file, in an old proposal, in a call note, in `outputs/`, in a
harness memory, or in a model's recollection, is **historical. Do not quote it.** Named as the
authority by `CLAUDE.md`'s pricing-authority line and by `ai/TOMBSTONES.md`.

Client engagement prices are NOT here. Those live in `knowledge/clients/<client>/roadmap.md`,
one file per client, same rule.

**The satellite duplicate is closed.** `knowledge/business/brand_foundation.md` used to state the
offer price on its own positioning line. It now carries a pointer here and no figure, so a
re-price is written once, in this file, and rippled through `ai/TOMBSTONES.md`. That is the whole
reason this file exists as a separate page instead of a section inside the brand doc.

---

## 1. What the offer is

**Ops Automation Sprint.** Two weeks. One integration built, or one manual process removed,
delivered running in production, with a runbook the client's own people can follow.

Not an audit. Not a strategy deck. Not a discovery phase that ends in a bigger proposal. The
deliverable is a thing that runs on Monday morning without Sam in the room.

Optional follow-on: **Care retainer.** Monitoring, failure alerts, and a fixed small amount of
change work per month on what the sprint delivered.

## 2. Price

| Line | Price | Terms |
|---|---|---|
| Ops Automation Sprint | **$4,000** | Flat. One invoice, issued on handover, net 14. |
| Care retainer (optional) | **$1,200/mo** | Month to month, cancel any time, starts the month after handover. |

Both in USD. Both are the whole number. There is no audit fee, no discovery fee, no setup fee,
no hourly fallback.

**Flat, never hourly, never split.** Ruled 2026-07-08, `ai/DECISIONS.md`. Hourly invites scope
haggling on every line and caps the upside on work that gets faster with every rep. The ruling
owns its own review date; do not re-argue it here and do not restate the date here either.

**Price history.** The offer used to be sold in two parts, an audit fee then a build fee. The audit
half was ~~$3,250~~, and the whole two-part shape was retired on 2026-07-08 in favour of the flat
$4,000 above. It went because the audit half was doing sales work rather than delivery work, and
because two numbers give a buyer two places to negotiate. The retired string is recorded in
`ai/TOMBSTONES.md`, and `repo-doctor` blocks it from reappearing un-struck anywhere under
`knowledge/`, `.claude/`, `templates/` or `skills/`. It survives on this line, struck, because the
owner file is the one place a dead number is allowed to show its own supersession.

## 3. The raise rule (pre-registered, so it is not a mood)

Registered in advance so a raise is a trigger being hit, not a good week being over-read.

- **No price edits mid-batch.** A batch is one full run of the gate in section 6. Changing the
  number halfway means the reply rate is measuring two offers and neither result is usable.
- **Trigger to raise:** the first full batch closes above 50 percent of the sprints quoted, OR
  no prospect in the batch pushes back on the number at all. Either one means the price is under
  what the market will carry.
- **The new number is decided at that review and written here**, in this file, in that session,
  with the old one struck and tombstoned. It is deliberately not pre-committed: picking a raise
  target today from zero closes is guessing dressed as policy.
- **Trigger to hold and change the offer instead:** the batch stalls at the price with the scope
  intact. That is an offer problem, not a price problem, and dropping the number would hide it.

Underpricing is the standing bias, stated in `CLAUDE.md` and recorded case by case in
`knowledge/business/pricing-outcomes.md`. `.claude/agents/price-attack.md` reads both before it
attacks any draft. If a scope looks bigger than a two-week sprint, that is not a discount
conversation, it is a phased engagement and it belongs in a client roadmap file.

## 4. Scope boundary

**In scope, always:**

- One integration, or one manual process, chosen and named before the sprint starts.
- Access and credentials handled in week one, or the clock does not start.
- Error handling, retries, and an alert when the job fails. An automation that fails silently is
  worse than the manual step it replaced, because nobody is watching the manual step's absence.
- A runbook: what it does, where it runs, how to see it worked, what to do when it did not.
- One handover walkthrough with whoever will own it.

**Out of scope, always, and stated in writing before the invoice:**

- A second integration. That is a second sprint.
- Data cleanup of historical records. Priced separately if they want it.
- Replacing either system. We sync what they have. See
  `knowledge/business/brand_foundation.md` on why.
- UI, dashboards or reporting surfaces. Those are build work, not sprint work, and they get a
  phased engagement with a roadmap file.
- Ongoing operation. That is the care retainer.
- Anything discovered mid-sprint that was not named at the start. It goes on the list, it does
  not go in the sprint.

**Scope changes are re-quoted before the build starts, never absorbed.** The record on this is in
`knowledge/business/pricing-outcomes.md`: the one engagement where scope grew got re-quoted before
any code was written, the client agreed, and the original number is now a tombstone rather than a
loss. A price that moves after work has started is a different and far worse conversation.

## 5. Qualification bar

This is the **offer-level** bar: is this business a fit for a two-week fixed-price sprint at all.
The connect-stage and pre-send ladder is a different thing and it is owned by
`outputs/outbound/prospect-gate.md`, which `skills/prospect-brief` applies as written. Do not
restate that ladder here and do not invent a rule that contradicts it.

**Must be true, all of them:**

1. Two or more systems of record in daily use that do not talk to each other.
2. A named human doing the workaround by hand, on a schedule. If nobody can name who does it, the
   pain is theoretical.
3. Someone in the conversation can say yes to a four-figure spend without a committee.
4. The systems have an API, an export, or a database we can reach. "It is on a PC in the back
   office" is a different, longer project.

**Hard no:**

- Pre-revenue, or no process yet. There is nothing to automate, only something to invent.
- An in-house engineering team that already owns integrations. The pain has an owner and we would
  be a third opinion.
- Anyone who opens with wanting "AI" rather than wanting a specific thing to stop being manual.
  The offer is plumbing. AI shows up only where judgment is genuinely needed.
- Anyone asking for a free proof of concept before a paid anything. The paid diagnostic exists
  for exactly this and it filters better than a free call.

**Never a disqualifier:** already paying for a tool in the category, or having built their own
janky internal script. Both mean they priced the pain already.

## 6. The gate (kill-or-go), and the copy freeze

This is the threshold `skills/daily-log` reads at `/weekly` and never restates in its own file.

**Gate:** 30 logged real conversations. A conversation is a two-way exchange with a qualified
person, not a connect, not an accept, not a like.

**Measured at 30, one of three verdicts.** These are motion-level verdicts and they are a
different vocabulary from the per-prospect verdicts in `outputs/outbound/prospect-gate.md`. A KILL
here retires a channel; a KILL there declines one person.

- **GO** if at least 2 sprints are sold, or at least 20 percent of conversations reached a
  priced proposal. The motion works; scale the input and open the raise review in section 3.
- **CHANGE THE OFFER** if conversations happen but nothing prices. The message is landing and
  the offer is not. Rewrite the offer, keep the channel, reset the count.
- **KILL** if 30 conversations cannot be had at all. The channel is wrong for this buyer.

Sending more messages before 30 is not a fix for either failing verdict. That is the trap this
gate exists to close.

**Manual only until the gate resolves.** No sequencer, no automation tool, no scheduler on the
sends. Ruled 2026-07-26, `ai/DECISIONS.md`: automating a motion that has not been proven by hand
scales a mistake and buys a platform restriction on top. The volume envelope for manual sending
is `knowledge/business/linkedin-safety-rules.md`.

**Copy freeze: IN EFFECT.** Declared with the gate, 2026-07-26.

This file owns **whether** a freeze is running and **when it lifts**. It does not own what a freeze
means or what it forbids: that is `outputs/outbound/prospect-gate.md`, and `skills/prospect-brief`
reads both. Do not restate the mechanics here, because two copies of a rule is one copy that goes
stale.

- **Release condition:** the gate above resolves, whatever the verdict. Not "when a message feels
  stale", not "when a prospect seems different", not "when a prospect looks unusual enough to
  deserve a custom opener".
- **On release:** if the verdict is CHANGE THE OFFER, the copy is rewritten once, the freeze is
  re-declared here, and the count resets. A partial thaw is the same as no freeze.

## 7. What this file does not decide

- Whether a specific prospect is worth writing to -> `outputs/outbound/prospect-gate.md`.
- What the message says -> `templates/message-templates.md`, frozen per section 6.
- Which pain to lead with -> `knowledge/pain-points/pain-point-bank.md`.
- Whether the number was right in hindsight -> `knowledge/business/pricing-outcomes.md`.
- Anything about a live client engagement -> that client's roadmap file.
- Whether to send -> the operator, per the `CLAUDE.md` pre-send checklist, item 7.
