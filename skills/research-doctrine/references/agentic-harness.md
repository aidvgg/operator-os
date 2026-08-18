# Agentic Harness Mapping

The doctrine was written with chat mechanics in the foreground: fresh chats, pasted artifacts, turn counts. In an agentic harness (Claude Code and similar), those are proxies for properties the harness delivers differently. This file is the mapping. Where SKILL.md says "chat", the property below governs.

---

## Fresh chat = fresh context

The load-bearing property of "each phase happens in a fresh chat" is context isolation: the critic must not see the reasoning that produced the thing it critiques, or adversarial review degrades into rationalization.

Harness implementation: one fresh-context subagent per phase, seeded with the prior phase's artifact file path as its ONLY inherited input. The orchestrator must not pass its own reasoning, summaries, or expectations across the boundary. Never run two phases in one context.

## Artifacts are files

Artifacts live in one directory per project: `research/<slug>/` (or your project's designated output tree), named `phase-<letter>-<YYYY-MM-DD>.md`. Store fetched source bodies under `research/<slug>/sources/` so the Phase D citation audit can re-read them without re-fetching, and diff a re-fetch against what Phase B saw.

The canonical artifact closer already carries both a Chat clause and a Harness clause; in a harness the Harness clause ("hand this artifact's file path to a fresh Phase [X] run") is the operative half. Keep the closer intact, do not drop either clause.

## State lives in a file, not the session

A skill invocation is instruction text in one turn's context, not a session mode. Declared Mode, Phase, the approved brief, and the artifact chain evaporate at the first subagent boundary or context compaction, so any rule that reads chat history silently passes on an empty check.

Harness implementation: on declaration, write `research/<slug>/STATE.md` holding Mode, Phase, approved brief path, and the artifact chain. Every phase run and every subagent reads it as its first action and appends its artifact path on exit. The self-check reads from that file, not from recall, so checks fail loudly instead of passing vacuously.

## Declarations travel in task briefs

A subagent has no user to ask. Mode and Phase carried in the spawning task string count as declared; the subagent restates them as the first line of its output. A lane spawned without them halts with `ERROR: undeclared mode/phase` rather than inferring.

## Lanes are parallel subagents

A brief with independent lanes maps to parallel Phase B (and C) subagents, one per lane, each with its own fresh context and its own stopping-rule verdict. Phase D is the serialization point: one stress-test over all lanes, explicitly testing cross-lane interactions. The citation audit (Phase D step 0) runs as its own subagent seeded with the claim tables and URLs only, never the Phase C reasoning.

## The Mega-chat detector, translated

Turn counts measure nothing here; a healthy single-phase gather crosses 30 turns on tool calls alone. Harness triggers instead:

- the context holds artifacts for two different phases
- the context has been compacted or summarized since the brief was fixed
- the approved brief is no longer verbatim in context (re-read STATE.md and the brief file)

Tool-call turns never count toward any threshold. Phase A brief iteration is exempt. The fix is unchanged: fresh context, seeded with the latest artifact.

## Triangulation, translated

Same-family subagents (more contexts of the same vendor's model) never enter the agreement tally, no matter how many run; log them as extra red-team passes. True triangulation still requires a second vendor, run by the operator, with the doctrine installed via system prompt and the exact model id recorded. A non-interactive run with no second vendor reachable uses the sanctioned fallback: "TRIANGULATION: none, single-vendor" in the Phase E header plus a one-point confidence penalty on decision-critical claims.

## Landing findings

No phase writes into a curated knowledge base. The final artifact of a pass includes the write-back plan (Phase E output 8): the enumerated edits the findings imply (value changes, supersede banners, expiry updates, deadline lines) for the operator's knowledge system. Executing that plan is a separate, explicit operator decision outside the doctrine, in whatever mode and with whatever safeguards the operator's own contract requires.

## Interoperation with retrieval harnesses

A dedicated deep-research skill (fan-out search, fetch, verify, synthesize in one pass) does work this doctrine deliberately splits. When both are installed: this doctrine owns decision-grade work where a commitment follows; a retrieval harness owns bounded factual lookups with no decision attached. Used inside this doctrine, the retrieval harness runs as the Phase B executor under the approved brief and returns a Phase B artifact (claims, labels, tiers, dates, searches-run log), never conclusions.
