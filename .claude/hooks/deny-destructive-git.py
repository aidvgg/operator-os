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

Two hosts. Claude Code sends shell calls as tool_name "Bash" with the command at
tool_input.command; Codex CLI sends that same shape, so every rule below covers
both hosts unchanged, and the deny JSON on stdout with exit 0 is accepted by
both. Codex file edits arrive as tool_name "apply_patch", where the command
string is the whole patch, target paths AND new file content in one blob. Those
are exempt: the git patterns would otherwise fire on a DOCUMENT that quotes a
denied command, and this repo's prose quotes them constantly (this docstring,
CLAUDE.md's commit protocol, ai/ERRORS.md). The exemption is a named set of
patch-shaped tool names, never an allowlist of shell names, so a missing or
unrecognized tool_name is still scanned and a new shell-ish surface is denied
rather than silently exempt. A real destructive command still has to reach the
shell to run, and there it is tool_name "Bash" again.

If a denied command targets a throwaway clone, prefer re-cloning it; anything
truly requiring these commands is operator-at-the-keyboard work (a real
terminal, not the `!` prefix, which routes through this guard too).
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

# Patch-shaped surfaces carry file CONTENT in tool_input.command (Codex
# apply_patch), so the git rules must not read it as a command line. Everything
# else, including a missing tool_name, stays in scope.
PATCH_TOOLS = {"apply_patch"}
if (data.get("tool_name") or "").strip().lower() in PATCH_TOOLS:
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command")
if not isinstance(cmd, str):
    sys.exit(0)

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

# A backslash line continuation is not a segment boundary, it is whitespace the
# shell removes before it ever sees a command. Splitting on the raw newline first
# put `git reset` in one segment and `--hard` in the next, and every rule below
# tests one segment for both the verb and the flag, so the whole denied set was
# one trailing backslash away from passing. Collapse continuations before the
# split. Found by review, no incident.
cmd = re.sub(r"\\\n[ \t]*", " ", cmd)

for seg in re.split(r"&&|\|\||[;|&\n]", cmd):
    if not re.search(r"\bgit\b", seg):
        continue
    for name, hit, why in RULES:
        try:
            matched = hit(seg)
        except Exception:
            matched = False
        if matched:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "destructive-git guard: %s denied. It %s%s"
                        % (name, why, TAIL)),
                }
            }))
            sys.exit(0)

sys.exit(0)
