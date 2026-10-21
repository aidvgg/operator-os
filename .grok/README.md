# `.grok/` - the Grok Build host layer

Hand-maintained, the Grok counterpart of `.claude/` and `.codex/`. Not generated: only the
markdown discovery surfaces (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
`.agents/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`, and the thin `.claude/commands/`
files) come from `scripts/sync-agent-adapters`.

Grok already loads `AGENTS.md` and `CLAUDE.md` as project rules, and already scans
`.agents/skills/` plus `.claude/skills/` for skill discovery. This directory is the host
layer those generated views do not cover: hooks, permission denies, and the three subagents
(`fact-check`, `price-attack`, `client-sim`) with Grok-native tool names.

| File | What it does |
|---|---|
| `config.toml` | Project-scoped permission denies for the provider-key files. MCP and plugins would also live here. Other Grok settings load only from `~/.grok/config.toml`. |
| `hooks/guards.json` | Lifecycle hooks. Invokes the same guard scripts under `.claude/hooks/` that `.claude/settings.json` and `.codex/hooks.json` wire, so each guard has one owner. Commands locate the repo with `git rev-parse`, never `$CLAUDE_PROJECT_DIR`. |
| `agents/*.md` | Custom agents ported from `.claude/agents/*.md` with Grok tool names. Each `.claude/agents/<name>.md` has a `.codex/agents/<name>.toml` and a `.grok/agents/<name>.md`; change all three together. |

## What maps to what

| Claude Code | Codex | Grok Build | Owner |
|---|---|---|---|
| `CLAUDE.md` (auto-loaded) | `AGENTS.md` then `CLAUDE.md` | `AGENTS.md` and `CLAUDE.md` (both auto-loaded) | `CLAUDE.md` is canonical; `AGENTS.md` is generated |
| `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | both of those | generated adapters; do not copy canonical `skills/` here |
| `.claude/commands/*.md` | (no Codex equivalent) | `.claude/commands/` via Claude compatibility | generated thin commands |
| `.claude/settings.json` hooks | `.codex/hooks.json` | `.grok/hooks/guards.json` | one owner per guard: `.claude/hooks/*.py` |
| `$CLAUDE_PROJECT_DIR` in hook commands | `$(git rev-parse --show-toplevel)` | `$(git rev-parse --show-toplevel)` | never use `$CLAUDE_PROJECT_DIR` on Grok |
| `.claude/agents/*.md` (`Read`/`Bash`) | `.codex/agents/*.toml` | `.grok/agents/*.md` (`read_file`/`run_terminal_command`) | three views of the same agents |
| permissions.deny in settings.json | (hooks only; no Codex path deny adopted) | `[permission] deny` in `.grok/config.toml` plus Claude-compat rules | hooks remain the hard floor |

Grok Build Desktop uses the same `grok` binary and the same `.grok/` layer. It is not a fourth
host: trust the folder once and both the TUI and the Desktop pick it up.

## One gate: folder trust

Grok puts project hooks, project MCP, project instructions, and project skills behind one
folder trust. Until this checkout is trusted, `.grok/hooks/` and `.grok/agents/` are silently
skipped. One-time setup on a machine:

1. `git config core.hooksPath .githooks` if this clone has not already.
2. Trust the folder: `grok --trust` at the repo root, or `/hooks-trust` inside a session. The
   grant is stored in `~/.grok/trusted_folders.toml` and covers subdirectories of this
   repository.
3. Confirm with `grok inspect` that project hooks, project agents, and `AGENTS.md` /
   `CLAUDE.md` are listed.

Re-grant after cloning onto a new machine. A nested git checkout under this folder is a
separate workspace and is not covered by this grant.

## What already works without this directory

- `AGENTS.md` and `CLAUDE.md` as project rules
- `.agents/skills/` adapters (Grok scans that tree natively)
- `.claude/skills/` and `.claude/commands/` via Claude compatibility (on by default)
- Claude-style permission rules in `.claude/settings.json` (also on by default)

What does **not** work without this directory, even with Claude compatibility on:

- Claude hook commands use `$CLAUDE_PROJECT_DIR`, which Grok does not set, so the Claude
  hook block fails open. Native `.grok/hooks/` is the armed wiring.
- Claude agent frontmatter names `Read` / `Grep` / `Glob` / `Bash`. The Grok copies name
  `read_file` / `grep` / `list_dir` / `run_terminal_command`.

## What does not port

- A Codex `danger-full-access` / `approval_policy = "never"` posture. Grok's interactive
  default is ask; leave it. The PreToolUse guards still deny the protected classes.
- `$CLAUDE_PROJECT_DIR`, for the reason above.
- A generated `GROK.md`. Grok already loads `AGENTS.md` and `CLAUDE.md`; a third
  instruction file would duplicate the contract into context.
- Copying `skills/` into `.grok/skills/`. Grok already scans `.agents/skills/`; a copy would
  fork procedure.

## Guard envelope

Grok PreToolUse stdin is camelCase (`toolName`, `toolInput`) and the shell tool is
`run_terminal_command`. Claude and Codex send snake_case (`tool_name`, `tool_input`) and
`Bash`. `.claude/hooks/deny-env-access.py` and `deny-destructive-git.py` accept both.

Grok treats a crashed hook with no JSON as a miss, so the hook fails open. That is why both
scripts print an explicit `permissionDecision: deny` and exit 0, and why they print a
fail-closed deny when their shared library (`scripts/lib/agent_guards`) cannot load. Do not
"fix" them to exit 2 for Grok; exit 2 is Claude's deny, and Grok honors the JSON deny on any
exit code.

## `/plan`

Grok owns `/plan` as built-in plan mode, same as Claude Code and Codex. Daily-log planning
uses a natural planning phrase or the daily-log skill.

## Verifying the layer

```
python3 scripts/test-git-guard
python3 scripts/repo-doctor
python3 scripts/sync-agent-adapters --check
```

`scripts/test-git-guard` runs both guard scripts against Grok's camelCase envelope and checks
that `hooks/guards.json` wires each guard to the right tool surface. It proves script
behavior and file-level wiring, not that Grok invokes the hooks: only a trusted folder and
`grok inspect` can confirm that.
