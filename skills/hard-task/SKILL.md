---
name: hard-task
description: "Tier-2 protocol for high-stakes work no other skill covers: legal, tax, banking, entity or relocation decisions, canonical knowledge/ rewrites, repository reorganization, and irreversible client-facing moves. Trigger on this skill by name, 'run the hard-task protocol', 'this is high stakes', 'before I commit to this', or any request whose blast radius is money, legal exposure, or a canonical file. `/hard-task` is the Claude Code slash alias and `$hard-task` the Codex one. Frames the stakes, assembles canonical context, drafts, then verifies with fresh-context subagents before delivering."
---

# Hard-task protocol (Tier 2)

This OS runs two tiers of verification. **Tier 1** is carried inside a skill: proposal-creator and
invoice-creator embed their own mandatory `fact-check` (and, where a price is involved,
`price-attack`) steps. **Tier 2 is this file**, for high-stakes work no skill covers.

Run this protocol when the task is one of:

- legal, tax, banking, entity, or relocation decisions
- a canonical rewrite of `knowledge/memory.md`, or any reorganization of `knowledge/`
- repository reorganization
- an irreversible client-facing move

When genuinely unsure whether a task qualifies, a short pass of this protocol beats a confident
wrong answer.

## The protocol

1. **Frame.** Restate the task, the stakes, and the blast radius: what breaks, and what money or
   legal exposure moves, if this is wrong. If the task turns out to be routine, say so and exit
   the protocol rather than performing it. Where framing exposes open decisions, grill them before
   drafting: one question at a time, in prose, each carrying a recommended answer. Look up facts
   yourself; put only the decisions to Sam.

2. **Assemble canonical context.** List the files you will treat as authoritative *before* reading
   them: `knowledge/memory.md` plus the matching topic files per the CLAUDE.md task table. Name
   anything you are deliberately NOT trusting (auto-extracted or otherwise low-trust files,
   `outputs/` history, old call prep) and why.

3. **Draft** the answer or artifact from canonical context only.

4. **Verify with fresh context.** Spawn subagents that see the draft but not your reasoning:
   - `fact-check` always: numbers, dates, entities, file integrity.
   - `price-attack` if any price, scope, or negotiation position is involved.
   - For legal, tax, or banking claims: re-verify each load-bearing claim against a primary source
     (the official documentation, the actual statement, the actual filing). A `memory.md` line is a
     pointer, not proof, for an irreversible move.

5. **Reconcile.** Resolve verifier objections explicitly. What you overrule, you note with a reason.

6. **Deliver** with a short "verified vs assumed" split. If the work changed `knowledge/`, follow
   the write protocol in CLAUDE.md and end the session with commit + push. The pre-commit doctor
   must pass.

## What this skill does NOT do

- It does not grant send authority. Item 6 ends at a delivered artifact; nothing client-facing
  leaves without Sam's explicit go on that specific artifact.
- It does not replace a skill that already covers the work. If proposal-creator or
  invoice-creator covers it, run that skill and its embedded Tier-1 verification instead.
- It does not license a `knowledge/` write beyond what CLAUDE.md's write rule already allows.
