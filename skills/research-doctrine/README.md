# Research Doctrine

A Claude skill that makes Claude argue with you instead of agreeing. Refuses bad briefs. Labels every claim and grades every source. Audits its own citations against the pages they came from. Forces an adversarial pass before any recommendation.

Designed for founders, consultants, builders, and analysts who've noticed that vanilla AI output is confidently wrong more often than confidently right.

## Install (Claude)

This folder is the skill. No packaged bundle ships in this repo; the folder is always the source of truth.

**In this repo:** it already runs. `SKILL.md` is the doctrine, `OPERATOR-INTERNAL.md` is the binding to this repo's paths and stricter local defaults, and `/research-doctrine` is the invocation route. Read both before starting a run. Read `references/agentic-harness.md` too: it maps every chat-scoped rule onto agentic mechanics.

**Another Claude Code project:** copy the `research-doctrine/` folder into that project's skills directory, or into `~/.claude/skills/` for user-level use. If the project generates or manages its skill directories with tooling, follow that tooling instead of hand-placing the folder. Leave `OPERATOR-INTERNAL.md` behind, it binds to this repo only.

**Claude.ai (web/desktop/mobile):** package the folder first (the command is in `OPERATOR-INTERNAL.md`), then Settings, Capabilities, Skills, Upload Skill, select the `.skill` file. Claude installs the whole bundle (doctrine + references + templates) as one unit. It activates automatically when your prompts match the trigger conditions in the SKILL.md frontmatter.

**Anthropic API:** reference the folder in your skill configuration per the API docs.

## Install (any other LLM - system prompt drop-in)

The skill works with ChatGPT, Gemini, or any chat-based LLM that accepts a system prompt:

1. Open `SKILL.md`
2. Copy everything *below* the YAML frontmatter (the `---` block at the top)
3. Paste it into your model's system prompt or first message
4. Reference files in `references/` won't auto-load, but you can paste any of them into a chat when needed (e.g., paste a phase template to start that phase)

This drop-in is also how you equip a second model for the triangulation protocol - every participating model must run the doctrine.

## Quickstart (30 seconds)

Once installed, start a chat and declare your mode and phase:

```
MODE: Strategic
PHASE: A-Brief

I'm trying to decide whether to enter [niche X] vs. [niche Y].
```

The model will refuse to give you an answer until you've completed a proper brief. That's the point.

## What's in this skill

- **`SKILL.md`** - the doctrine itself (with skill frontmatter for Claude's skill system)
- **`OPERATOR-INTERNAL.md`** - this repo's bindings: where artifacts land, the stricter local defaults, the write-back rule. Not part of the portable doctrine, excluded from any packaged bundle.
- **`references/`** - supporting files Claude loads on demand:
  - `phase-a-brief.md` through `phase-f-market-test.md` - pre-filled phase templates
  - `phase-b-refresh.md` - the Phase B variant for re-verifying standing claims
  - `anti-patterns.md` - diagnostics for 9 operator anti-patterns and 6 research-integrity anti-patterns
  - `triangulation-protocol.md` - multi-model reconciliation at claim-and-source level
  - `agentic-harness.md` - how the doctrine runs in Claude Code and similar harnesses

## How the doctrine works

Six phases. Each happens in a fresh context. The output of one phase becomes the input to the next.

| Phase | Purpose | When to start |
|-------|---------|---------------|
| A - Brief | Define the question | Always start here |
| B - Gather | Collect sourced raw data | After brief is approved |
| C - Synthesize | Pattern-match across data | After data is gathered |
| D - Stress-test | Citation audit + adversarial critique | Mandatory for the claim classes listed in SKILL.md, recommended before any decision |
| E - Decide | Decision doc with action items | After Phase D where D is mandatory or was run; otherwise after Phase C with failure modes explored |
| F - Reality test | Plan the real-world test | After deciding, when the decision is a bet (fact-state updates end at E) |

Each phase forbids work that belongs in another phase. This is intentional. Phase mixing is the single biggest cause of bad AI research output.

## Why the friction

The doctrine refuses bad inputs, refuses to skip phases, and refuses to flatter you. If it feels like the model is being difficult, that's the skill working - not breaking.

The friction is the feature. Vanilla AI is agreeable, fast, and confidently wrong. The doctrine slows you down at the points where speed produces garbage.

## A few things you should know

- **Modes are non-negotiable.** Strategic, Research, Builder, Critique. Pick one. Switching mid-chat requires a fresh context. Builder is the declared off-switch: it stands the doctrine down for execution work.
- **Empirical claims must be labeled.** `[SOURCE]` with a P1/P2/P3 quality tier and dates, `[SNIPPET]`, `[CARRIED]`, `[RELAY]`, `[INFERENCE from: ...]`, `[TRAINING]`, `[UNKNOWN]`. Non-trivial claims (anything a decision depends on, plus every number, date, and named capability) carry an evidence-anchored 1-10 confidence rating. If the model skips this, remind it.
- **Citations get audited.** Phase D re-fetches load-bearing sources and demotes any claim whose page doesn't say what the artifact says.
- **Decisions are yours, not the model's.** The doctrine forces AI into the analyst role: gather, synthesize, counter-argue. You decide.
- **Some domains route to humans.** Legal, tax, immigration, medical, investment. The doctrine refuses to be decision-grade in these - it produces a defined draft-grade artifact (fact base + consultation question bank) you take to a real expert.

## Recommended workflow

1. Start every research project with a Phase A brief in a fresh context.
2. When the brief is approved, open a fresh context for Phase B with the brief as its only input.
3. Continue phase-by-phase, each in its own fresh context.
4. Save artifacts to your knowledge tool of choice (Notion, Obsidian, your file system) - the markdown format pastes anywhere. In this repo they go to `outputs/research/<slug>/`. If the findings supersede something you have written down, the Phase E artifact's write-back plan lists the edits; making them is your call.

## Customization

Everything in this skill is markdown. Fork it, edit it, adapt it to your domain. If you make changes, three things to keep:

1. The phase separation. This is the load-bearing structure.
2. The claim labeling with source tiers. Without it, the discipline collapses into normal AI output.
3. The Phase D citation audit. Labels that nothing ever re-checks are decoration.

If you modify the SKILL.md frontmatter, keep the `description` field detailed enough that Claude knows when to invoke the skill. The description is what triggers activation.

## Feedback

If you find a flaw, an anti-pattern this doesn't catch, or a decision class this fails for - I want to know. Built by Northwind Labs. northwindlabs.example

---

**Version 1.1** (2026-08-02) - full internal review pass. What it added: [SOURCE] now requires the page read plus a verbatim passage; source quality tiers (P1/P2/P3); perishability and freshness-horizon rules; a Phase B gather floor (decompose, disconfirm, trace to primary, stopping rule, search log); the Phase D citation audit; inference premises and confidence propagation; an N-aware triangulation rubric reconciling at claim-and-source level; a refresh template for re-verifying standing claims; the E-draft artifact for expert-routed domains; verification-test and terminal-at-E exits for non-commercial research; settled-decision protection; research-integrity anti-patterns; and the agentic-harness mapping.
