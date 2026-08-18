# skills/

One folder per skill, each with a `SKILL.md` (the instructions) plus any `scripts/`, `assets/`, `references/` it needs. **Read the `SKILL.md` before running the skill**, every time. The folder is the unit: a new skill always gets its own `skills/<name>/`, never a loose file at this level.

`CLAUDE.md` ("Skills" section) is the authoritative inventory: invocation rules, write licences, verification gates, local-run notes. This file lists what exists and points there for policy, so the two cannot drift into a fight. Provider discovery wrappers (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, the generated skill views) come from `ai/AGENT_ROUTES.json`; they point here and never own workflow policy.

## First-party (8)

Written for this operation. These are the ones that carry write licences and verification gates, all defined in `CLAUDE.md`.

- `proposal-creator` - client-facing proposals, quotes and SOWs, print HTML rendered to PDF. Carries two mandatory fresh-context verification gates.
- `invoice-creator` - branded invoices, print HTML to PDF. Takes the invoice number from the ledger, never from recall, and reads the wire block from the local-only payment-details file.
- `daily-log` - the daily operating logbook: plan, standup, end of day, weekly review. Accountability and stats, not a capture inbox.
- `business-profile-creator` - read-and-merge update of the business profile JSON. Never a blank-slate rebuild.
- `prospect-brief` - turns a prospect URL into a decision-ready brief: qualification ladder applied as written, pain-bank match, opener prep. No send authority.
- `research-doctrine` - phase-separated, source-tiered, adversarially audited research for decision-grade work. Its `OPERATOR-INTERNAL.md` binds the generic doctrine to this repo's paths; read it alongside `SKILL.md` when running it here.
- `hard-task` - the Tier-2 protocol for high-stakes work no skill covers; `/hard-task` in Claude Code, `$hard-task` in Codex, read directly on any other host.
- `harvest` - end-of-session content harvest: 1-3 receipt-backed seeds to `outputs/content/seeds/`. Never posts.

## Vendored reference library (17)

Third-party craft skills for copy, page types, CRO and SEO, design and build. Provenance and licence, one row per vendored item, plus the deliberately-skipped list: `VENDORED.md`. Licence and attribution files in tree: `LICENSE-mengto-skills` and `NOTICE-mengto.md` (the four MengTo-origin skills). Ten of the seventeen carry no licence text in tree; `VENDORED.md` records their licence as evidenced rather than asserting one.

They are reference-tier. First-party doctrine wins every conflict (precedence, voice, pricing policy, send authority), none of them carries a `knowledge/` write licence, and none of them can authorize a send.

## Packaging

No packaged `.skill` bundles live in this repo. The extracted folders are what run locally and are always authoritative; a bundle is a build product that goes stale the moment the folder moves, so build one only when you need to import a skill into claude.ai, and rebuild it every time.

Generic command: `cd skills && rm -f <name>.skill && zip -r <name>.skill <name> -x "*.DS_Store"`

A skill folder may carry internal-only files that need extra exclusions. The authoritative per-skill command then lives inside that skill's folder: `research-doctrine` excludes `OPERATOR-INTERNAL.md`, which must never ship.
