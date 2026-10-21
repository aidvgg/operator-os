"""Shared envelope helpers and deny payload shape for agent guards."""


class GuardDeny(object):
    """A deny decision with the exact reason string surfaces should print."""

    def __init__(self, reason, rule=None):
        self.reason = reason
        self.rule = rule

    def __bool__(self):
        return True


def envelope_tool(data):
    """Read Claude/Codex snake_case or Grok camelCase tool fields.

    A missing name becomes "" so command-only fixture envelopes still scan.
    A missing input stays None/non-dict so the caller can fail closed (env)
    or treat as empty (git).
    """
    name = data.get("tool_name")
    if not isinstance(name, str) or not name.strip():
        alt = data.get("toolName")
        name = alt if isinstance(alt, str) else ""
    inp = data.get("tool_input")
    if not isinstance(inp, dict):
        alt = data.get("toolInput")
        if isinstance(alt, dict):
            inp = alt
        else:
            inp = None
    return name, inp


def pretooluse_deny_payload(reason):
    """JSON-serializable PreToolUse deny object accepted by Claude/Codex/Grok."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
