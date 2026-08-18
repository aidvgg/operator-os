# Operator-internal execution notes (NOT shipped - excluded from any packaged bundle)

Repo-specific bindings for running the doctrine inside this Operator OS. `SKILL.md` and `references/` stay generic so the doctrine is portable; this file owns everything that names this repo. If a rule here conflicts with `CLAUDE.md`, CLAUDE.md wins.

## Precedence

- CLAUDE.md's operating contract overrides the ask ceremony only, and what it licenses is a declared default, not silent inference: open with "Proceeding under MODE: [X], PHASE: [Y]; correct me if wrong" and continue (the doctrine's own Activation section grants exactly this). Phase separation, claim labeling, source tiering, and expert routing are never overridden.
- `ai/DECISIONS.md` rows populate the brief's "Settled inputs, do not reopen" field. They enter Phase A as settled inputs with their decision date, review date, and pre-registered kill threshold, not as positions to re-argue. Pull `ai/ERRORS.md` and `ai/TOMBSTONES.md` in the same read when the topic touches money, a client-facing artifact, or a superseded number.
- Repo reads that CLAUDE.md mandates before decision-shaped moves (`knowledge/memory.md`, the matching topic files, DECISIONS / ERRORS / TOMBSTONES) are a precondition of Phase A, not research: do them while building the brief. Reading canonical files is allowed in every Mode, because they are the brief's ground truth rather than new retrieval.

## Where things land

- Invocation route: `/research-doctrine` via the thin hand-written wrapper `.claude/commands/research-doctrine.md`. The wrapper points here: reading `SKILL.md` plus this file IS the load step. Without the wrapper the skill is readable by path only.
- Artifacts: `outputs/research/<slug>/phase-<letter>-<YYYY-MM-DD>.md`, plus `STATE.md` and `sources/` in the same directory. Absolute paths, explicit-path staging, never `git add -A`. An agent that trusts an inherited working directory eventually writes into the wrong tree; this is the control that stops it.
- Fetched source bodies routinely contain public contact phone numbers, which trip repo-doctor's phone-shape secrets check and block the commit. That is the check working, not a false positive. Redact them in the committed copy with a `[REDACTED-PUBLIC-PHONE]` marker and keep the unredacted contact points in `outputs/research/<slug>/local/` (gitignored). Committed files cite that path; the live URL stays the authority.
- **This skill holds no write licence into `knowledge/`.** The Phase E (or E-draft) artifact carries the write-back plan: enumerated edits, supersede banners, tombstone entries, Due lines, Stale-after updates. Executing that plan is a separate explicit step the operator sanctions per run, under the "Writing `knowledge/`" rule in CLAUDE.md, in the parent session (a subagent's `knowledge/` write is committed by the parent).
- Repo artifact conventions apply to every artifact: `**Stale after:** YYYY-MM-DD - why` on anything web-sourced or perishable (the doctrine's generic "Review by" line maps to this, use the repo's Stale-after form here), `**Due:** YYYY-MM-DD - what/what happens` on any dated commitment so `scripts/horizon` sees it, SUPERSEDED banners over deletion, one owner per state fact (cite `knowledge/` paths, never restate their values).

## Local defaults (stricter than the shipped product)

- Phase D is mandatory before every Phase E, not just the listed claim classes. The stress test always precedes the decide phase here, with no exceptions for small or obvious-looking passes.
- Expert-routed domains (legal, tax, immigration, medical, investment) run A through D in full, produce the E-draft artifact, and compose with `/hard-task`: the doctrine supplies B through D, hard-task owns framing, fresh-context verification, and delivery.
- The `deep-research` workflow (`.claude/workflows/deep-research.js`) is the sanctioned Phase B executor: hand it the approved brief (or one lane of it) and require the Phase B artifact shape back (claim table with IDs, tiers, dates, verbatim passages, searches-run log), never conclusions.
- Subagent model tiering: tier up by default. Anything carrying judgment or review weight gets the strong model; only mechanical grep-and-report steps get the cheap one. A citation audit is not a mechanical step.
- Triangulation: a second vendor is reachable here (the operator can run the same brief through another model in a browser), so the single-vendor fallback is for unattended runs only.
- No em dashes in any artifact, ever (`knowledge/voice/copy-rules.md`).

## Execution shape in this harness (the efficient run)

One doctrine pass maps onto this harness like this; deviate only with a reason:

1. **Phase A** runs in the main session, interactively with the operator. Building the brief IS the CLAUDE.md pre-decision read: `knowledge/memory.md`, topic files, DECISIONS / ERRORS / TOMBSTONES feed Settled inputs and Prior state under test. Write the brief to `outputs/research/<slug>/phase-a-<date>.md` and create `STATE.md`.
2. **Phase B** fans out: one fresh-context subagent per lane, in parallel. Read-only stages always run concurrently; serialize only when two stages write the same tree. Refresh lanes use the phase-b-refresh verdict table. Each lane writes its own artifact and fetched source bodies to `sources/`.
3. **Phase C** is one subagent per lane, seeded only with that lane's B artifact path.
4. **Phase D** is two stages: the citation-audit subagent (claim tables and URLs only, never C reasoning), then the stress-test subagent over all lanes' C artifacts plus the audit table. This is the serialization point.
5. **Phase E / E-draft** back in the main session, where the operator is. The artifact carries the write-back plan; the operator sanctions the `knowledge/` writes, then the session executes them, ripples tombstones, and commits.
6. Fact-state refreshes end at E ("Terminal - no Phase F"). A verification-test Phase F (a booked consult, an official enquiry, a filed pre-application) gets a `**Due:**` line so horizon tracks it.

## Packaging the skill for export

The folder is authoritative. If you want a `.skill` bundle to import into claude.ai, build it from the folder and exclude this file:

`cd skills && rm -f research-doctrine.skill && zip -r research-doctrine.skill research-doctrine -x "*.DS_Store" -x "research-doctrine/OPERATOR-INTERNAL.md"`

A bundle is a build product, never the source of truth (`skills/README.md`). This file must never ship: check the zip listing after building.
