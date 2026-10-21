#!/usr/bin/env python3
"""PreToolUse guard for the repo-root provider-key files.

The wrappers load provider keys inside their own process. Agent tools may write
prose or code that discusses the control, but no tool may target the protected
paths directly, select them through a glob, or use the bounded direct shell
reconstruction forms the library normalizes.

Claude Code runs this hook for every tool. Known prose and code fields on its
built-ins are exempt, while unknown tools are scanned conservatively. Codex
projects shell calls to `Bash` plus a string `command`, and native edits
to `apply_patch` plus the raw patch string. Grok Build sends camelCase
`toolName` / `toolInput`, with shell as `run_terminal_command` and edits as
`search_replace` / `write`. Patch bodies are content, so only recognized target
headers are scanned. Unknown header grammar fails closed.

This command-string layer remains a floor, not a complete filesystem fence.
Nested interpreters can synthesize a path without ever placing its spelling or
a resolving glob in the hook envelope. Codex has a per-path filesystem profile,
but this repo has not adopted it. See .codex/README.md.

Fixtures: scripts/test-git-guard.

Implementation: thin stdin adapter over scripts/lib/agent_guards (shared with
the scripts/agent-guard CLI). Deny classes and reason strings live in the
library. A missing or broken library, invalid JSON or any internal error
prints a fail-closed deny, never a crash: a hook that exits without JSON
fails open on Claude Code and Grok.
"""
import json
import os
import sys

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HOOK_DIR, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "scripts", "lib"))

# Same wording as agent_guards.env.FAIL_CLOSED_REASON, held here so it still
# prints when the library itself cannot load.
FAIL_CLOSED_REASON = (
    "Blocked by the .env access guard, which failed closed: it could not "
    "confirm the tool call is safe, so it denied WITHOUT matching a protected "
    "path. This is not a detected .env access."
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
    from agent_guards.env import evaluate_env_envelope
except Exception:
    fail_closed("guard library failed to load")

try:
    data = json.load(sys.stdin)
except Exception:
    fail_closed("malformed hook input")

try:
    deny = evaluate_env_envelope(data, project_root=_ROOT)
except Exception:
    fail_closed("internal error")
if deny:
    print(json.dumps(pretooluse_deny_payload(deny.reason)))
raise SystemExit(0)
