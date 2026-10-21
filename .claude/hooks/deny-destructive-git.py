#!/usr/bin/env python3
"""PreToolUse guard: deny destructive git and sweep staging in agent tool calls.

Trace: the hazards named in ai/ERRORS.md (an agent that ran `git add -A` plus
`git commit --no-verify` from an inherited cwd and committed to main, sweeping in
a parallel session's uncommitted work) and the explicit-path-staging rule it
re-breached. CLAUDE.md's "Agents and the live tree" bullet is the prose
containment; this hook is its mechanical floor, adapted from the blocklist idea
in mattpocock-skills' git-guardrails. Fixtures: scripts/test-git-guard.

Denied classes, each with its reason at the match site:
  worktree destruction   reset --hard / forced clean / pathspec checkout /
                         worktree restore / forced switch or checkout
  history & remote       branch -D, forced or mirror or deleting push
  scan bypass            push --no-verify, commit --no-verify (-n)
  sweep staging          add -A / --all / bare-dot pathspec, commit -a
Plain `git push` stays allowed: the commit protocol requires it and the
pre-push doctor scans the range. `git commit --amend`, `reset --soft/--mixed`,
`restore --staged`, `branch -d`, `clean -n` stay allowed.

Blunt by design, same posture as deny-env-access.py: patterns run over each
shell segment of the raw command string, so in a SHELL call a commit message or
grep pattern QUOTING a denied shape is also denied. Safe direction; rephrase or
use -F. Known limit: `git checkout <dir>/` with a bare path (no `--`, no dot
token) is not recognized as a pathspec checkout. Not an adversarial control, an
accident control: an alias or obfuscation walks past it.

Three hosts. Claude Code and Codex CLI send shell calls as tool_name "Bash"
with the command at tool_input.command. Grok Build sends camelCase toolName
"run_terminal_command" with the command at toolInput.command. Every rule
covers all three once the envelope is normalized, and the deny JSON on stdout
with exit 0 is accepted by all three. Codex file edits arrive as tool_name
"apply_patch", where the command string is the whole patch, target paths AND
new file content in one blob. Those are exempt: the git patterns would
otherwise fire on a DOCUMENT that quotes a denied command, and this repo's
prose quotes them constantly (this docstring, CLAUDE.md's commit protocol,
ai/ERRORS.md). The exemption is a named set of patch-shaped tool names, never
an allowlist of shell names, so a missing or unrecognized tool_name is still
scanned and a new shell-ish surface is denied rather than silently exempt. A
real destructive command still has to reach the shell to run, and there it is
tool_name "Bash" or "run_terminal_command".

If a denied command targets a throwaway clone, prefer re-cloning it; anything
truly requiring these commands is operator-at-the-keyboard work (a real
terminal, not the `!` prefix, which routes through this guard too).

Implementation: thin stdin adapter over scripts/lib/agent_guards.git (shared
with the scripts/agent-guard CLI). Denied classes and reason strings live
there. A missing or broken library, invalid JSON or any internal error prints
a fail-closed deny, never a crash: a hook that exits without JSON fails open
on Claude Code and Grok.
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HOOK_DIR, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "scripts", "lib"))

FAIL_CLOSED_REASON = (
    "Blocked by the destructive-git guard, which failed closed: it could not "
    "confirm the tool call is safe, so it denied WITHOUT matching a denied git "
    "command."
)


def fail_closed(detail):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "%s [%s, failing closed]" % (
            FAIL_CLOSED_REASON, detail),
    }}))
    raise SystemExit(0)


try:
    from agent_guards.common import pretooluse_deny_payload
    from agent_guards.git import evaluate_git_envelope
except Exception:
    fail_closed("guard library failed to load")

try:
    data = json.load(sys.stdin)
except Exception:
    fail_closed("malformed hook input")

try:
    deny = evaluate_git_envelope(data)
except Exception:
    fail_closed("internal error")
if deny:
    print(json.dumps(pretooluse_deny_payload(deny.reason)))
raise SystemExit(0)
