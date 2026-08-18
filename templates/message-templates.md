# Message templates

Plain-text skeletons for client and outbound messages. Fill the `[brackets]`, delete the
guidance, send.

**Rules that apply to all of them:**

- Plain text, no markdown. These get pasted into DMs, email and chat, where markdown renders
  as literal asterisks and reads like a bot.
- Every number comes from its owner, never from recall: the productized offer from
  `knowledge/business/outbound-offer.md`, an engagement price from
  `knowledge/clients/<client>/roadmap.md`, anything invoice-shaped from
  `knowledge/business/invoices/INVOICE-LEDGER.md`.
- All numbers in USD.
- No price in the first-touch message. Phase-and-price framing once there is real interest.
- No timeline you have not personally verified. A date you guessed becomes a date they planned
  around.
- Never justify the work or the price unasked. State it and move on.
- A filled template is a draft, not a send. Nothing client-facing leaves without an explicit go
  on that specific message, however clean it looks.

---

## 1. Outbound first-touch (X or LinkedIn DM)

Curiosity-led. No pitch, no price, no mention of a call. The goal is a reply, not a sale.

    hey [name], thanks for connecting. saw you run [company]. are you
    mostly on [manual ops / spreadsheets / a patchwork of tools] for
    [the workflow you automate] right now?

    trying to get a clearer picture of how [businesses in their space]
    actually handle it vs how it gets talked about.

Guidance: lowercase and low-friction on X, sentence case on LinkedIn or email. One real
question, then stop typing and let them answer. If you cannot name their specific workflow,
you have not done the research and the message will read as a mail merge. Qualify first against
`outputs/outbound/prospect-gate.md`.

---

## 2. Second touch after silence

One follow-up, and only if you have something to add. A bare "just bumping this" is a message
that asks for attention without paying for any.

    [name], one more thought and then I will leave it alone.

    [one specific, useful observation about their setup or their space,
    something they could act on without hiring anyone.]

    if [the pain] is not actually a problem for you, say so and I will
    stop.

Guidance: the exit line is not politeness, it is a filter. A no is a usable answer and silence
is not. Never send a third.

---

## 3. Referral ask (warm contact)

For a happy client or someone who already knows the work.

    Hey [name], quick one. I am taking on more [automation / build] work
    alongside what we have been doing together. If you know anyone
    drowning in [manual reporting / data entry / repetitive ops], an
    intro would be welcome. No pressure either way, you just know the
    space better than most.

Guidance: name the exact pain you solve, not "clients in general". A vague ask gets a vague
nod. One ask, no follow-up, no guilt.

---

## 4. Scoped-work follow-up (phase-and-price)

Once there is verbal interest. Anchors the first phase only. The client never sees a full
programme number in a DM.

    [name], happy to build this. The cleanest way in is to phase it.

    Phase 1: [smallest slice that delivers real value on its own, for
    example sync the two systems and put a status view on top]. Fixed
    scope, fixed price, [$X,000]. [50% to start, 50% on delivery.]

    Once Phase 1 is live and you have used it, we scope Phase 2
    ([the next slice]) as its own piece. You always know exactly what
    you are buying before you commit to it.

    Want the formal scope for Phase 1?

Guidance: one number, one phase. If they push for a total, say the total depends on how far
they want to take it and offer a phased proposal that splits the phases cleanly. If the slice
looks underpriced for the complexity, flag it to yourself before you send. Rounding down
quietly is how a build turns into unpaid weeks.

---

## 5. Sending the proposal

Short. The document does the work. A cover note that re-argues the proposal signals you do not
trust it.

    [name], scope for Phase 1 attached.

    [One line naming what it covers and what it deliberately does not.]

    Anything in there you want moved, tell me and I will re-cut it.

Guidance: send the PDF that passed `scripts/pdf-check`, not a renamed draft. Re-derive every
number in the document from its owning file before it goes.

---

## 6. Sending the invoice

    [name], invoice [NUMBER] attached for [what it covers], [$X,000],
    due [date].

    Payment details are on the invoice. Shout if anything on it needs
    changing.

Guidance: the number comes from the ledger, never from counting. The wire block comes from the
local payment-details file, never from memory. Issued invoices are gitignored on purpose,
because they carry that block.

---

## 7. Moving a date

Send it the day you know, not the day it slips.

    [name], [deliverable] is moving to [new date]. [One sentence on
    what changed.] Nothing else in the phase shifts.

    [What you need from them, if anything.]

Guidance: no apology paragraph, no explanation nobody asked for. The date, the cause in one
line, and what happens next. Then update the Due line in the file that owns the commitment so
`scripts/horizon` stops reporting the old one.
