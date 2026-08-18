---
name: harvest
description: "End-of-session content harvest: mine THIS session for 1-3 content seeds that carry a receipt, and write each to outputs/content/seeds/ as an X-voice hook draft plus pillar, receipt and self-rating. Trigger on this skill by name, 'harvest this session', 'any content in this', 'pull seeds from today'. `/harvest` is the Claude Code slash alias and `$harvest` the Codex one. Never auto-posts and never manufactures a seed to fill a quota; Sam curates."
---

# Content harvest

Mine the session that just happened for content seeds. Drafts only. Sam curates and posts.

## The procedure

1. **Scan the session for seeds.** Look back over what actually happened: a build that shipped, a
   bug caught, a price held, a client move, a doctrine call, a number that came in. A seed is a
   *specific* thing that happened, not a generic take. **The bar is a receipt**: the concrete
   evidence (the file shipped, the exact number, the objection killed, the before and after) that
   makes the claim non-generic. No receipt means not a seed.

2. **Pick 1-3, no padding.** If the session produced genuinely nothing worth posting, say so
   plainly and write nothing. A false seed wastes Sam's curation. Never manufacture a seed to
   fill the quota.

3. **Write each seed** to `outputs/content/seeds/YYYY-MM-DD-<slug>.md` (date = today, slug = short
   kebab of the idea). Each file contains, in order:
   - **Hook draft** in X voice per CLAUDE.md: all lowercase, punchy short sentences, single
     quotes, `->` arrows, first person, no justifying or defensive language. State and move on.
   - **Pillar**: which content pillar this serves, per the mix owned by
     `knowledge/voice/channel-voice.md`. Read the mix there; it is deliberately not restated here.
   - **Receipt**: the concrete evidence behind the hook, the file, number, objection or
     before-and-after that makes it true. This is what stops it being generic.
   - **Self-rating**: rate the idea 1-10 (standing rule: always rate the idea) plus one specific
     improvement that would make it land harder.

4. **Never auto-post.** These are drafts for Sam to curate. Do not send, schedule, or cross-post.
   Output goes to `outputs/content/seeds/` only.

5. **Report.** Name each seed written (path plus a one-line what) and its rating, or state plainly
   that the session had no genuine seed.

## What this skill does NOT do

- It does not post, schedule, or cross-post anything.
- It does not write into `knowledge/`. Seeds are `outputs/` artifacts.
- It does not invent a receipt. A hook whose evidence you cannot name is not a seed.
