# Operator-internal execution notes

Exclude this repo-specific binding from the shipped skill. The product remains portable markdown instructions and requires no runtime system. If this file conflicts with `CLAUDE.md`, follow `CLAUDE.md`.

## Precedence and context

- Let the skill self-route. Do not require the operator to declare a mode or phase.
- Treat the repository reads required by `CLAUDE.md` as Phase A inputs. Read `knowledge/memory.md`, relevant topic files, and `ai/DECISIONS.md` before decision-shaped work. Read `ai/ERRORS.md` and `ai/TOMBSTONES.md` when the contract requires them.
- Populate settled inputs from `ai/DECISIONS.md`. Reopen one only when its recorded trigger fires or new evidence materially changes it.
- Apply the repo's expert, pricing, client-send, safety, and write rules in addition to the portable doctrine.
- Invocation route: `/research-doctrine` in Claude Code (the hand-written wrapper `.claude/commands/research-doctrine.md` reads `SKILL.md` plus this file), or the generated skill adapters on other hosts. Reading `SKILL.md` plus this file is the load step.

## Local artifacts

The doctrine does not require files. Inside this repo, use files for durable traceability:

- Artifacts: `outputs/research/<slug>/phase-<stage>-<YYYY-MM-DD>.md`
- Optional source snapshots: `outputs/research/<slug>/sources/`
- Optional run index: `outputs/research/<slug>/STATE.md`, containing the approved brief, artifact chain, capability profile, and achieved assurance class

These paths implement the instruction locally; they are not part of the public method. Write them with absolute paths and stage them by explicit path, never `git add -A`.

Apply repo artifact conventions:

- use `**Stale after:** YYYY-MM-DD - why` for web-sourced or perishable work
- use `**Due:** YYYY-MM-DD - consequence` for dated commitments, so `scripts/horizon` sees them
- preserve superseded artifacts with a banner
- cite canonical `knowledge/` owners instead of restating their values
- redact public phone numbers from committed source snapshots as `[REDACTED-PUBLIC-PHONE]`; keep unredacted contact data only in the gitignored `outputs/research/<slug>/local/` subtree. repo-doctor's phone-shape check blocks the commit otherwise.

This skill has no write license into `knowledge/`. Phase E may produce a write-back plan. Execute that plan only through a separately authorized repository step, under the "Writing `knowledge/`" rule in `CLAUDE.md`, in the parent session.

## Local execution shape

Use the strongest available implementation without turning it into a user-operated workflow:

1. Run A in the main session and create the coverage map.
2. Run B lanes in parallel fresh contexts when independent lanes exist. The local `deep-research` skill or workflow (`skills/deep-research/SKILL.md`, `.claude/workflows/deep-research.js`) may execute a B lane if it returns the doctrine's evidence artifact, not conclusions.
3. Run C per lane, then run C-Merge over every lane before D.
4. Run the citation audit in a fresh context seeded only with the audit packet. Run the adversarial audit after it. Record L2 only when reviewer isolation is real.
5. Run E in the main session. Append the complete Closure Ledger and keep it `INCOMPLETE` until a fresh reviewer reconciles the frozen packet. Same-context work may have L1 traceability capability but cannot award positive closure.
6. Run F only for a real-world bet. Give its owner and deadline a visible `**Due:**` line.

Use a different model/provider and the portable triangulation protocol only when L3 is required. Same-vendor subagents count as independent audit passes, not cross-model triangulation.

## Local strictness

- Run D before every E.
- Treat any missing atomic component, unchecked structural invariant, uninspected load-bearing citation, untraced exact Phase E figure or named capability, blanket retrieval gap, orphan record ID, unsupported recommendation dependency, skipped C-Merge, missing silence test, false capability claim, or overstated reviewer boundary as `INCOMPLETE`.
- Use `hard-task` alongside the doctrine for high-consequence expert-routed work. The doctrine owns evidence and assurance; `hard-task` owns the repo's framing and delivery safeguards.
- Use no em dashes in artifacts (`knowledge/voice/copy-rules.md`).
- When a return-to-B route is cheap and operator-unlockable (a gated PDF behind an email form, a free API key), Phase E labels every finding that route could move as provisional and names the route, instead of presenting it as a correction to an earlier record. A full report fetched later can reverse a finding drawn from its summary.

## Using the doctrine outside this repo

- Another Claude Code project: copy the `research-doctrine/` folder into that project's skills directory, or into `~/.claude/skills/` for user-level use. Leave this file behind.
- Claude.ai: build a bundle with the command below, then upload the `.skill` file as a skill.
- Any other chat model: paste `SKILL.md` below its frontmatter into the system prompt, and paste a reference file into the chat when a stage needs it. Every model in a triangulation run must carry the doctrine this way.

## Packaging the skill for export

Run from `skills/`:

```bash
rm -f research-doctrine.skill
zip -r research-doctrine.skill research-doctrine -x "*.DS_Store" -x "research-doctrine/OPERATOR-INTERNAL.md"
```

The folder is authoritative and the `.skill` file is a build product (`skills/README.md`). Inspect the archive listing after building. `OPERATOR-INTERNAL.md` must not ship.
