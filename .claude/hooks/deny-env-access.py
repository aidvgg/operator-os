#!/usr/bin/env python3
"""PreToolUse guard: deny any AI tool call that targets the gitignored .env files.

The keys in .env/.env.local are loaded by the wrapper scripts (scripts/x-fetch,
scripts/li-fetch) inside their own process; no agent tool call may read, edit, or
reference the files directly. A key that reaches a transcript is a key that has to
be rotated, so the cheapest control is to make the file unreachable rather than to
trust every future session to leave it alone. Companion control: the
permissions.deny Read/Edit rules in .claude/settings.json. Agents call the scripts,
never the file.

Two hosts, one deny shape: the JSON below on stdout with exit 0 is what Claude
Code expects and what Codex CLI also accepts, so nothing host-specific is
emitted and Claude Code behavior is unchanged.

Claude Code surface (tool_name Read/Edit/Write/NotebookEdit/Grep/Glob/Bash).
Checked surfaces: file-path fields of file tools, and the command string of Bash.
Deliberately NOT checked: Edit old/new_string, Write content, Grep patterns, so that
docs and configs may still mention the filename in text.

Codex CLI surface. Shell calls arrive as tool_name "Bash" with the command at
tool_input.command, the same shape Claude Code sends, and are checked identically.
File edits arrive as tool_name "apply_patch", where that same command string is
the whole patch: target paths AND new file content in one blob. Scanning it raw
would invert the paragraph above and deny any doc that merely writes the
filename in prose, so for apply_patch the patch body is never scanned. Only the
paths named by envelope header lines are:

    *** Add File: <path>      *** Update File: <path>
    *** Delete File: <path>   *** Move to: <path>

The header pattern is line-anchored and patch content lines carry a "+", "-" or
" " prefix, so a body quoting a header line cannot smuggle a scan target in or
out. Fail-closed corner: an apply_patch call whose command names no header at
all is an envelope this guard cannot narrow, so it falls back to scanning the
whole string; a patch that malformed would not apply anyway.

Fixtures: scripts/test-git-guard (covers both guards).
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get("tool_name") or ""
tool_input = data.get("tool_input") or {}

# ".env" or ".env.<suffix>" appearing as a path token.
#
# Written as a NEGATIVE lookbehind, not a positive class of allowed preceding
# characters. An earlier revision enumerated `^ \ / whitespace ' " = ( :`, which
# is an allowlist of shell syntax and was therefore wrong by construction: every
# operator nobody thought of was a bypass. Measured on that pattern, all ALLOWED:
# `cat <.env.local`, `base64 <.env`, `done <.env`, `cp {.env.local,/tmp/x}`.
# Redirect is the obvious one and it is the cheapest possible exfiltration. That
# matters more than it looks on Codex, where this hook is the ENTIRE .env control
# unless the operator adopts a per-path filesystem deny profile, and where the
# sandbox may have network access, so one redirect reaches a provider.
#
# The lookbehind inverts the burden: match ".env" unless it is a continuation of
# a longer filename token. `foo.env` and `my.env` stay clear because a word
# character precedes; `/.env`, `<.env`, `{.env`, `"$X".env` and a bare `.env` all
# match, and so does any operator not invented yet. Scope is unchanged: only
# path-shaped fields and command strings are scanned, never file content, so
# prose that merely names the file is still writable.
PAT = re.compile(r"(?<![\w.-])\.env(\.[\w.-]+)?\b")

# The lookbehind above still only ever matches the LITERAL four characters ".env",
# so any spelling that never writes them is invisible to it. At a typical repo
# root `.env.local` is the only dotfile matching `.e*`, which makes `cat .e*` an
# exact, unobfuscated read of the key file, and `cat .e* | curl -d @-` one allowed
# call when the sandbox has network on. Measured allowed before this line
# existed: `.e*`, `.??v*`, `.??*`, `.[a-z]*`, `.*`.
#
# So: deny any dotfile-shaped token carrying a glob metacharacter. The token must
# START at a dot and hit `*`, `?` or `[` before any path separator, which is what
# keeps ordinary globs clear: `.github/*`, `.claude/hooks/*.py` and `find . -name
# '*.md'` all have a separator or a space first and do not match.
# Known and accepted false positive: `ls .*` is denied. Listing a name is harmless,
# but no cheap rule separates `ls .*` from `cat .*`, and this guard's documented
# posture is blunt in the safe direction. Use `ls -a`.
# This closes a spelling, not the class. A command-string matcher can never be
# complete (`python3 -c "open(chr(46)+'env.local')"` still passes). The complete
# control is the host's own per-path filesystem deny (Codex: `"**/*.env" = "deny"`
# under a `[permissions.<profile>.filesystem]` profile), enforced below the shell
# and impossible to spell around. Adopting it replaces sandbox_mode wholesale, so
# it is the operator's call; see .codex/README.md.
GLOB_TOKEN = re.compile(r"(?<![\w.-])\.[\w.-]*[*?\[]")

# Codex apply_patch envelope headers, the only lines in a patch that name a
# target path. Line-anchored on purpose: body lines are prefixed, so a document
# that quotes one of these headers is not read as a header.
PATCH_HEADER = re.compile(
    r"^\*\*\*[ \t]+(?:Add File|Update File|Delete File|Move to):[ \t]*(\S.*?)[ \t]*$",
    re.MULTILINE | re.IGNORECASE)

haystack = []
for key in ("file_path", "path", "notebook_path"):
    value = tool_input.get(key)
    if isinstance(value, str):
        haystack.append(value)

command = tool_input.get("command")
# Globs are a shell notion, so GLOB_TOKEN applies only to a shell command string,
# never to apply_patch header paths or to a file-tool path field.
shell_text = ""
if isinstance(command, str):
    if tool_name.strip().lower() == "apply_patch":
        targets = [t.strip() for t in PATCH_HEADER.findall(command)]
        haystack.extend(targets or [command])
    else:
        haystack.append(command)
        shell_text = command

if PAT.search("\n".join(haystack)) or GLOB_TOKEN.search(shell_text):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                ".env files hold live API keys and are off-limits to all AI tool "
                "access. Call scripts/x-fetch or scripts/li-fetch instead; they "
                "load the keys in their own process."
            ),
        }
    }))
sys.exit(0)
