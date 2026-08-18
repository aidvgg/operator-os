# Channel voice

**This file is the worked example's voice. It is meant to be replaced.** Lowercase on X, a
50/30/20 pillar mix, a particular DM shape: none of that is universal, and copying another
operator's voice is how you end up sounding like a person who copied someone's voice. Keep the
*shape* of this file (a section per channel, each with rules, a mix or a cadence, and a bad and
good example) and rewrite the content in your own.

The craft rules in `knowledge/voice/copy-rules.md` are the opposite: they survive a rebrand and
they are not up for a rewrite. Everything here sits on top of them. Where a channel rule below
seems to conflict with a craft rule, the craft rule wins and the channel rule is wrong.

`CLAUDE.md` carries a compressed version of this file in its voice block. That summary and this
file must agree; when they drift, fix both in the same session, because a stale summary in the
highest-precedence file is worse than no summary.

---

## X

**Form.**

- All lowercase. Including the first word, including proper nouns you are not quoting.
- Short sentences, one idea each. A line break beats a comma.
- Single quotes, never double.
- `->` for arrows. Never an arrow glyph.
- First person, always. No "we". There is no we.
- No hashtags, no emoji, no engagement bait ("thoughts?", "who else has seen this?").
- No thread unless the idea genuinely has parts. A padded thread is four posts of filler
  protecting one good line.

**Pillars and mix.**

| Pillar | Share | What it is | The bar |
|---|---|---|---|
| Build notes | 45% | How a thing was actually built. The mechanism, the tradeoff, the part that broke. | A builder could steal something from it. |
| Teardowns | 35% | A tool, a claim or a pattern meeting a real workload. | Name the claim, never the person. Show the mechanism that settles it. |
| Operator log | 20% | What actually happened in the business. | A number, or it is not a log, it is a mood. |

The mix is measured over a rolling 20 posts, not per week. Weekly mix arithmetic on a base of three
posts is theatre.

**Bad:** "Excited to share some thoughts on why data integration is such a challenge for SMBs
today! 🚀 What's been your experience? #automation #AI"
**Good:** "spent two days on a sync that already worked. the bug was that nobody knew when it
didn't. added one alert -> the client found a broken feed the same week. the build was never the
hard part."

---

## LinkedIn

**Form.**

- Sentence case. Lowercase reads as sloppy to this audience, not as voice.
- One idea per line, blank line between. No wall of text, no single-sentence-paragraph parody
  either. Roughly one to three lines per block.
- This is where the value beat gets its full render. X can compress the mechanism to one line;
  here it gets the steps, in order, with the one everybody skips called out.
- Lead-magnet posts use a comment-keyword CTA: one keyword, stated once, at the end. Never a
  keyword plus a link plus a DM ask, which is three steps and loses most of the people who wanted
  the thing.
- No pods, no "agree?", no reposting your own post with "in case you missed it".
- Any block labeled paste-ready carries its character count (`copy-rules.md` rule 7).

**Bad:** "Agree? 👇 Most businesses are sitting on a goldmine of data they simply aren't using.
Comment DATA below and let's connect to discuss how I can help you unlock it. Happy to jump on a
quick call!"
**Good:** a post that walks the three parts of a nightly sync, says which part fails silently, shows
the exception queue, and ends with: "I wrote the runbook I use for this. Comment SYNC and I will
send it over."

Note what the good version does not do: it does not mention a call anywhere before that final line,
and the final line offers the document, not a meeting. That is `copy-rules.md` rule 6, and it is the
rule most often broken on this channel.

---

## Client and direct messages

**Form.**

- Plain text. No markdown. Bold and bullets in a chat window read as a document someone generated
  rather than a person typing.
- Phase-and-price framing: what the phase is, what it costs, what it produces. Never a scope without
  a price boundary, never a price without a scope boundary.
- **No timeline that Sam has not personally verified.** This is a settled ruling, not a preference:
  `ai/DECISIONS.md`, 2026-07-19. A date offered from optimism becomes a date the client plans
  around, and then an apology.
- Every number re-derived from its owner before it is typed: the ledger for anything invoice-shaped,
  the client's roadmap for an engagement price, `knowledge/business/outbound-offer.md` for the
  productized offer. Never from memory, never from an old message thread.
- No apology openers. "Sorry for the slow reply" spends the first line of the message on the least
  interesting fact in it.
- Bad news travels first and travels short: the change, the cause in one line, what happens next.

**Send authority.** The pre-send checklist in `CLAUDE.md` is a quality gate, not permission. Nothing
client-facing leaves without Sam's explicit go on that specific artifact, however clean the checks
came back. Repo work is autonomous. Sends are not.

**Bad:** "Hey! So sorry for the delay on this 🙏 I've been absolutely swamped. I *think* we should
be able to have the dashboard done by end of next week, maybe the week after depending on how the
API stuff goes, but I'll definitely keep you posted!"
**Good:** "The dashboard is moving to the following Tuesday. The warehouse API caps how fast we can
backfill history, so the backfill runs over a weekend. Nothing else in the phase shifts. I need the
second location's credentials before Friday to keep that date."

---

## Outbound (cold and semi-cold)

**Form.**

- Sentence case, not the X lowercase. Lowercase in a cold DM reads as careless rather than casual.
- Messy human, not SDR. No "I hope this finds you well", no "quick question", no "just circling
  back", no "as per my last message". Those phrases are a uniform, and the uniform is what gets
  filtered.
- One observation, one question. No pitch, no deck, no price in a first touch.
- The observation is about their *operation*, not their profile. If the sentence could be pasted to
  a hundred people, it is not an observation, it is a mail merge with extra steps.
- Under 90 words. If it needs more than that, it is a call, not a message.
- No mention of a call before the ask, and the ask arrives once (`copy-rules.md` rule 6).
- A second touch only if you have something new to add, and never a third. The exit line ("if this
  is not actually a problem for you, say so and I will stop") is a filter, not politeness: a no is
  usable and silence is not.

**Boundaries.** This file owns only how outbound *sounds*. Who is worth writing to is owned by
`outputs/outbound/prospect-gate.md`. What the offer is and what it costs is owned by
`knowledge/business/outbound-offer.md`. The fill-in skeletons are in `templates/message-templates.md`.

**Bad:** "Hi [name], I hope this finds you well! I came across your profile and was really impressed
by your background. I help companies like yours leverage AI to drive efficiency and unlock growth.
Would you be open to a quick 15-minute call this week to explore synergies?"
**Good:** "Hey, saw you run three locations off one warehouse system. Are the stock counts still
being reconciled by hand each week, or did you get the till talking to it? Asking because everyone I
speak to in that setup has a person doing it on a Friday and nobody puts it on the org chart."

---

## What this file does not own

- The craft rules: `knowledge/voice/copy-rules.md`.
- Pricing and the offer: `knowledge/business/outbound-offer.md`, plus the client's roadmap under
  `knowledge/clients/`.
- Who to contact and when to disqualify: `outputs/outbound/prospect-gate.md`.
- What may be claimed publicly about a client's work: that client's own `README.md`.
- The brand's positioning and story: `knowledge/business/brand_foundation.md`.

---

## Rewriting this file for your own operation

1. Pick your channels. Two is plenty. A channel you post to once a month is not a channel.
2. For each one, write the form rules as *observable* constraints (casing, length, punctuation,
   what is banned) rather than adjectives. "Punchy" is not a rule. "Under 90 words, one question"
   is.
3. Write your own pillar mix and say how you measure it. A mix with no measurement window is a
   wish.
4. Give every channel a bad example and a good example. The bad example does more work than the
   rules above it, because it is the one people recognise themselves in.
5. Leave the "what this file does not own" section pointing at your owners. It is what stops this
   file slowly absorbing your prices.
