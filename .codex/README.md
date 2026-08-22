# `.codex/` - the Codex host layer

Hand-maintained, the Codex counterpart of `.claude/`. Not generated: only the markdown discovery
surfaces (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.agents/skills/*/SKILL.md`,
`.claude/skills/*/SKILL.md`, and the thin `.claude/commands/` files) come from
`scripts/sync-agent-adapters`.

| File | What it does |
|---|---|
| `config.toml` | Project-scoped Codex config: sandbox mode, approval policy, subagent defaults. |
| `hooks.json` | Lifecycle hooks. Invokes the same guard scripts under `.claude/hooks/` that `.claude/settings.json` wires, so each guard has one owner. |
| `agents/*.toml` | Custom agents ported from `.claude/agents/*.md`. The fresh-context verifiers the skills treat as mandatory. Each `.claude/agents/<name>.md` has a `.codex/agents/<name>.toml`; change them together. |

## Two gates, and they are independent

**Project trust** makes `config.toml` and `agents/` live. Codex asks for it the first time you open
the repo; until you grant it, this whole directory is silently ignored and the repo runs under your
global Codex defaults with none of its guards. Custom agents auto-discover from `agents/` with no
`[agents.<name>] config_file` rows, so do not add those rows.

**Hook trust is separate**, keyed on a hash of `hooks.json`, and granted interactively. Wiring a
guard is not arming it. Until it is armed, `codex exec` runs this repo with the sandbox in
`config.toml`, and neither `deny-env-access.py` nor `deny-destructive-git.py` fires, and Codex says
nothing about it: no prompt, no startup warning, no stderr line.

Arm it once: run `codex` at the repo root interactively and answer the hook-review prompt with
"Trust all and continue". **Re-arm after any edit to `hooks.json`**, because trust is a hash of the
file: an edited file is an untrusted file until you accept it again.

## The default posture, and how to loosen it

`config.toml` ships `sandbox_mode = "workspace-write"` and `approval_policy = "on-request"`: the
sandbox may write inside the workspace and Codex asks before anything outside it. Operators who
trust this repo's own guard hooks and git hooks as the safety layer may loosen it to
`danger-full-access` plus `approval_policy = "never"`; that is a machine-wide sandbox boundary,
not a repo-only grant, and it only makes sense once hook trust is armed.

The env guard scans target-shaped fields recursively, resolves scoped selectors against the
protected repo-root names, normalizes bounded direct shell forms, checks every patch target header,
and fails closed on malformed envelopes. Both host files wire it with a match-all selector so new or
unknown tool names still reach the scanner. It remains a command-envelope floor: a nested
interpreter can synthesize a path without placing a detectable spelling or resolving selector in
the envelope. The complete control on Codex is its own per-path filesystem deny
(`"**/*.env" = "deny"` under a `[permissions.<profile>.filesystem]` profile selected by
`default_permissions`), enforced below the shell. Adopting it replaces `sandbox_mode` wholesale,
so it is your call; this template does not ship it. Treat the hooks as the floor, not the fence.

## Verifying the layer

`scripts/test-git-guard` runs both guard scripts against 196 assertions and checks both host wiring
files. It proves script behavior and file-level wiring, not that a host invokes the hooks: Codex-side
registration is this directory plus the trust prompt above, and only an interactive Codex session
can confirm the hooks are armed.
