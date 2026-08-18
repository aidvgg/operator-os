# knowledge/voice

How things sound when they leave the repo. Two files, and the split between them is the point.

| File | Owns | Lifespan |
|---|---|---|
| `copy-rules.md` | The craft rules: no em dashes, dead-easy style, never justify, the value beat, no slogan copy on client documents, no call mention before the CTA, paste-ready copy carries its count. Each with a why, a one-pass test, and a bad and good example. | Permanent. These survive a rebrand, a new offer and a new market. |
| `channel-voice.md` | This operation's per-channel voice: X, LinkedIn, client and direct messages, outbound. Casing, length, pillar mix, cadence, the shape of a DM. | Replaceable. This is the worked example's voice and is meant to be rewritten. |

**Why the split matters.** A voice file that mixes the two ages badly: someone rebrands, deletes the
whole directory because "that was the old voice", and takes the em-dash ban and the value-beat rule
down with it. Keeping the craft rules in a file that never talks about Northwind Labs is what makes
them portable.

**Precedence.** Where a channel rule and a craft rule collide, the craft rule wins and the channel
rule is wrong. `CLAUDE.md` carries a compressed restatement of both; when its summary and these
files drift, fix both in the same session.

## What does not live here

- **Prices.** Not one number in this directory. `knowledge/business/outbound-offer.md` owns the
  productized offer, the client's roadmap under `knowledge/clients/` owns an engagement. A price
  restated in a voice file gets quoted from a voice file.
- **Claims about client work.** What may be said publicly about a build is owned by that client's
  own `README.md`.
- **Positioning and the brand story.** `knowledge/business/brand_foundation.md`.
- **Message skeletons.** `templates/message-templates.md` holds the fill-in-the-brackets versions.
  This directory says how they should sound; that file is what you actually paste.

## If you keep a corpus

A file of your own real posts, verbatim, is the best voice reference there is, better than any set
of rules about voice. If you keep one, put it here as `x-corpus.md` or similar, mark it as ground
truth, and never reformat it. A corpus that has been tidied to match the current rules is no longer
evidence of anything.
