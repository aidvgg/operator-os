"""Destructive-git / sweep-staging deny logic shared by hooks and remotes.

Denied classes (same as deny-destructive-git.py docstring):
  worktree destruction, history/remote force, --no-verify, sweep staging.
"""
import re

from .common import GuardDeny, envelope_tool, pretooluse_deny_payload

TAIL = (" Denied mechanically by .claude/hooks/deny-destructive-git.py, trace "
        "ai/ERRORS.md. Targeting a throwaway clone? Re-clone it instead. "
        "Otherwise this is operator-at-the-keyboard work in a real terminal.")


def flag_cluster(letter):
    """Single-dash short-flag cluster containing <letter>, e.g. -fd for f."""
    return re.compile(r"(^|\s)-[a-zA-Z]*" + letter + r"[a-zA-Z]*\b")


# Whole-token bare-dot pathspec: " . ", " .. ", " ./ ", " ../ " (not ./path).
DOT_TOKEN = re.compile(r"(^|\s)\.\.?/?(\s|$)")
DASH_SEP = re.compile(r"\s--(\s|$)")

WT = ("overwrites working-tree changes; parallel per-engagement sessions mean "
      "uncommitted cross-lane work is the EXPECTED state here.")


def sub(word):
    return re.compile(r"\b" + word + r"\b")


RULES = [
    ("reset --hard", lambda s: sub("reset").search(s) and "--hard" in s,
     "discards uncommitted work in the index and working tree irrecoverably. "
     "reset --soft / --mixed stay available."),
    ("forced clean", lambda s: sub("clean").search(s) and (
        "--force" in s or flag_cluster("f").search(s)),
     "deletes untracked files; in this repo that includes gitignored "
     "local-only business files (wire details, issued invoices). "
     "clean -n (dry run) stays available."),
    ("pathspec/forced checkout", lambda s: sub("checkout").search(s) and (
        DASH_SEP.search(s) or DOT_TOKEN.search(s) or "--force" in s or
        flag_cluster("f").search(s) or re.search(r"(^|\s)-B\b", s)),
     WT + " Branch switching (checkout <branch>, checkout -b) stays available."),
    ("worktree restore", lambda s: sub("restore").search(s) and not (
        "--staged" in s and "--worktree" not in s and
        not flag_cluster("W").search(s)),
     WT + " restore --staged (unstage only) stays available."),
    ("forced switch", lambda s: sub("switch").search(s) and (
        "--force" in s or "--discard-changes" in s or
        re.search(r"(^|\s)-[a-zA-Z]*f\b", s) or re.search(r"(^|\s)-C\b", s)),
     WT + " switch <branch> / switch -c stay available."),
    ("branch force-delete", lambda s: sub("branch").search(s) and (
        flag_cluster("D").search(s) or
        ("--force" in s and ("--delete" in s or re.search(r"(^|\s)-d\b", s)))),
     "force-deletes a branch regardless of merge state. branch -d stays "
     "available."),
    ("forced/deleting push", lambda s: sub("push").search(s) and (
        "--force" in s or "--mirror" in s or "--delete" in s or
        re.search(r"(^|\s)-f\b", s) or
        re.search(r"\bpush\b[^\n]*\s[+:]\S", s)),
     "rewrites or deletes remote history; the remote is the backup and audit "
     "trail for the repo that IS the business. Plain push stays available."),
    ("push --no-verify", lambda s: sub("push").search(s) and "--no-verify" in s,
     "skips the pre-push range scan, the backstop a bypassed commit cannot "
     "outlive (CLAUDE.md commit protocol)."),
    ("sweep staging", lambda s: sub("add").search(s) and (
        flag_cluster("A").search(s) or re.search(r"--all\b", s) or
        DOT_TOKEN.search(s)),
     "sweep staging; a parallel session's uncommitted work gets swept into a "
     "foreign commit. Stage explicit paths."),
    ("commit -a sweep", lambda s: sub("commit").search(s) and
     flag_cluster("a").search(s),
     "implicit sweep staging of every tracked change. Stage explicit paths, "
     "then commit."),
    ("commit --no-verify", lambda s: sub("commit").search(s) and (
        "--no-verify" in s or flag_cluster("n").search(s)),
     "skips the staged doctor scan. The sanctioned unblock for a doctor block "
     "is a scoped allow entry, not a bypass."),
]

# Patch-shaped surfaces carry file CONTENT in tool_input.command (Codex
# apply_patch), so the git rules must not read it as a command line.
PATCH_TOOLS = {"apply_patch"}


def check_git_command(command):
    """Return GuardDeny if command hits a denied git class, else None."""
    if not isinstance(command, str):
        return None
    # A backslash line continuation is shell whitespace, not a segment boundary.
    cmd = re.sub(r"\\\n[ \t]*", " ", command)
    for seg in re.split(r"&&|\|\||[;|&\n]", cmd):
        if not re.search(r"\bgit\b", seg):
            continue
        for name, hit, why in RULES:
            try:
                matched = hit(seg)
            except Exception:
                matched = False
            if matched:
                reason = ("destructive-git guard: %s denied. It %s%s"
                          % (name, why, TAIL))
                return GuardDeny(reason, rule=name)
    return None


def evaluate_git_envelope(data):
    """Evaluate a PreToolUse envelope; return GuardDeny or None.

    Missing/non-dict input or non-string command allows (same as the hook).
    Patch-shaped tool names are exempt.
    """
    if not isinstance(data, dict):
        return None
    tool_name, tool_input = envelope_tool(data)
    if tool_input is None:
        tool_input = {}
    if not isinstance(tool_input, dict):
        return None
    if tool_name.strip().lower() in PATCH_TOOLS:
        return None
    cmd = tool_input.get("command")
    return check_git_command(cmd)


def deny_payload_for(deny):
    return pretooluse_deny_payload(deny.reason)
