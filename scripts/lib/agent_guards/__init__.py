"""Shared agent deny guards for PreToolUse hooks and remote CLIs.

One owner for env-path and destructive-git deny classes. Hooks stay thin
stdin adapters; the scripts/agent-guard CLI calls the same functions.
"""
from .common import GuardDeny, envelope_tool, pretooluse_deny_payload
from .git import check_git_command, evaluate_git_envelope
from .env import check_env_command, check_env_tool, evaluate_env_envelope

__all__ = [
    "GuardDeny",
    "envelope_tool",
    "pretooluse_deny_payload",
    "check_git_command",
    "evaluate_git_envelope",
    "check_env_command",
    "check_env_tool",
    "evaluate_env_envelope",
]
