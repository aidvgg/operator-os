---
name: deep-research
description: Deep-dive research executor for evidence-backed answers on a scoped question. Use when a simple quick lookup is not enough.
---

# Deep Research

Deep-research is the retrieval executor for one-off, high-integrity inquiries.

Use this skill when a question needs multiple perspectives, independent verification, and a transparent source trail.

## Activation

If the question is underspecified, ask a focused scope pass first before gathering.
Ask only what is needed for clarity:

- region or jurisdiction
- time window
- required certainty level
- budget or scale assumptions
- who will use the result

Ask at most three questions before proceeding.

## Operating constraints

- Max sources fetched: 15
- Max sourced claims to verify: 5 claims per gather cycle
- Max verification voters per claim: 3
- A claim is contested only when at least 2 of 3 voters produce a refutation.
- Every claim in the output must include a source label and confidence.

## Scope and retrieval

1. Parse the question into a single explicit scope statement.
2. Create at least 3 search angles and run parallel discovery.
3. Deduplicate URLs across angles.
4. Fetch up to 15 sources.
5. Keep only sources that are relevant, current, and readable.

Reject a source immediately if the publish date and authoring context cannot be established for a time-bound claim.

## Claim capture

For each source, extract concrete falsifiable claims only. Each claim must include:

- exact claim text
- direct supporting quote or paraphrased evidence
- a one line reason the claim is relevant
- a quality tier

Source quality tiers:

- P1: primary source, statute, regulator, vendor or origin documentation
- P2: reputable secondary citing primary
- P3: blog, forum, opinion, or unattributed media coverage

## Verification

For each claim run an adversarial verification pass with three independent votes:

- voter 1
- voter 2
- voter 3

If 2+ votes refute, mark claim status as Refuted.
If 2+ votes support with explicit citation, mark as Verified.
If votes are mixed or weak, mark as Inconclusive and continue with reduced confidence.

## Synthesis

When verification is complete:

- rank claims by direct relevance and evidence quality
- merge duplicates
- present only what was confirmed as Verified or clearly Inconclusive
- clearly separate recommendations from facts
- include open questions for any residual risk

Output format:

# Deep Research - <date>

## Scope
Short one paragraph.

## Verified Claims
- [P1|P2|P3] <claim>
  - confidence: 1-10
  - sources:
    - `<url>`

## Refuted Claims
- <claim> with refutation rationale.

## Open Questions
- what needs manual confirmation before action

## Suggested Decision Inputs
- direct bullets for what the user can act on now
- any assumptions still unverified

## Source Trail
- numbered list of fetched URLs, each with quality tier and retrieval date.

## Process note
State whether scope was clear enough on first pass and whether clarifications were required.

Do not overpromise. If the claim cannot be materially verified, state that status explicitly and do not convert it into a recommendation.
