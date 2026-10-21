# Remote agent hosts

**Owner of this doc:** this file. The generated agent entrypoints point here through
`ai/AGENT_ROUTES.json` `host_classes.remote.ops_doc`.

## Why

Local hosts (Claude Code, Codex, Grok Build) load PreToolUse guards. A remote agent host that
cannot load PreToolUse hooks, such as an always-on chat service or a scheduled cloud worker, gets no
such guard. Safety must not depend on a host that is absent, so remote writes use **the same deny
logic and the same doctor path** as local sessions, not a softer parallel policy.

## Host classes

| Class | Examples | Reads | Writes |
|---|---|---|---|
| Local interactive | Claude Code, Codex, Grok Build | Working tree | Direct edits, PreToolUse guards, `.githooks` |
| Remote agent | Any host that cannot load PreToolUse hooks | Clone or hosting API | Bookkeeping: `scripts/agent-mutate`. Owner files: inbox only, the operator applies |

## Shared enforcement core

One library: `scripts/lib/agent_guards/` (the write pipeline is `mutate_pipeline.py`).

- PreToolUse adapters: `.claude/hooks/deny-env-access.py` and `.claude/hooks/deny-destructive-git.py`, wired on every local host.
- Remote CLI: `scripts/agent-guard env --command/--path` and `scripts/agent-guard git --command`.
- Same deny classes and reason strings on both surfaces. Never fork a second regex set.
- Doctor: `scripts/repo-doctor --staged` before commit, and the pre-push range scan via `.githooks` when `core.hooksPath=.githooks`.
- A failed mutate restores the snapshotted files and unstages them. It never runs `reset --hard`.

Fixtures: `scripts/test-git-guard` (library and hook parity) and `scripts/test-agent-mutate` (env
deny, dirty tree, doctor HARD restore, licensed commit, TTY inbox, hash bind).

## Write pipelines

### Bookkeeping mutate (licensed paths)

A remote host, against a clone whose listed paths are clean:

```
scripts/agent-mutate \
  --host <name> \
  --skill daily-log \
  --mode <mode> \
  --paths <explicit file> \
  --patch <unified.diff> \
  --message <subject>
```

`--patch` is required, and the files the patch names must equal `--paths`. Zero-context patches
are accepted. Unrelated dirty tracked files refuse. Listed paths that are already dirty refuse, so
a live checkout cannot launder the operator's uncommitted edits.

Licences: `daily-log` (the five logbook paths in `skills/daily-log/SKILL.md` hard rule 3) and
`prospect-brief` (`outputs/outbound/briefs/**`). Staging is explicit `git add --` only, never
`git add -A`, never `--no-verify`. The pipeline refuses unless `core.hooksPath=.githooks`. The env
scan runs before the licence check, so a `.env` path reports `env-deny`, not `unlicensed-path`.

### Judgment or owner-file proposal (inbox)

A remote host writes under `outputs/inbox/<host>/<UTC-stamp>/` and **stops**. It never runs
`scripts/agent-apply-inbox`.

The operator inspects the bundle, then:

```
scripts/agent-apply-inbox outputs/inbox/<host>/<UTC-stamp> --print-hash
# write APPROVED containing: bundle_sha256: <hex>
scripts/agent-apply-inbox outputs/inbox/<host>/<UTC-stamp>
```

Apply requires a TTY, an `APPROVED` file whose `bundle_sha256` matches `PROPOSAL.md`,
`MANIFEST.json` and `patch.diff`, and the inbox path `outputs/inbox/<host>/<stamp>/`. Changing the
patch after approval is a hash mismatch. Owner-file paths are allowed on this path; env deny, the
protected-path doctor and the hooksPath check still apply. There is no `--approved` flag.

## Skills

Canonical skills stay in `skills/<name>/SKILL.md`. Remote hosts read those files from their clone
or the hosting API. The generated adapters under `.agents/skills/` and `.claude/skills/` are
discovery only.

## Out of scope

Deploying the script pack to a remote host, any UI for inbox approval, and bookkeeping licences
beyond `daily-log` and `prospect-brief`.
