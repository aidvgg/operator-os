#!/usr/bin/env python3
"""PreToolUse guard for the repo-root provider-key files.

The wrappers load provider keys inside their own process. Agent tools may write
prose or code that discusses the control, but no tool may target the protected
paths directly, select them through a glob, or use the bounded direct shell
reconstruction forms normalized below.

Claude Code runs this hook for every tool. Known prose and code fields on its
built-ins are exempt, while unknown tools are scanned conservatively. Codex
projects shell calls to `Bash` plus a string `command`, and native edits
to `apply_patch` plus the raw patch string. Patch bodies are content, so only
recognized target headers are scanned. Unknown header grammar fails closed.

This command-string layer remains a floor, not a complete filesystem fence.
Nested interpreters can synthesize a path without ever placing its spelling or
a resolving glob in the hook envelope. Codex has a per-path filesystem profile,
but this repo has not adopted it. See .codex/README.md.

Fixtures: scripts/test-git-guard.
"""
import codecs
import fnmatch
import json
import os
import re
import shlex
import sys
from urllib.parse import unquote


DENY_REASON = (
    ".env files hold live API keys and are off-limits to all AI tool access. "
    "Call wrapper scripts such as scripts/x-fetch or scripts/li-fetch instead; "
    "they load the keys in their own process."
)


def deny(detail=None):
    reason = DENY_REASON if detail is None else DENY_REASON + " [" + detail + "]"
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    raise SystemExit(0)


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROTECTED_BASENAMES = (
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".env.staging",
    ".env.test",
)
PATH_TOKEN = re.compile(
    r"(?<![\w.-])\.env(?:\.[\w.-]+)?\b", re.IGNORECASE)
SIMPLE_SHELL_VARIABLE = re.compile(
    r"\$(?:[A-Za-z_][A-Za-z0-9_]*|[0-9]+)")
BRACED_SHELL_VARIABLE = re.compile(r"\$\{([^{}]*)\}")
ANSI_C_QUOTE = re.compile(r"\$'((?:\\.|[^'])*)'")
LOCALE_QUOTE = re.compile(r'\$"((?:\\.|[^"])*)"')
SHELL_ASSIGNMENT = re.compile(
    r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)="
    r"(?:'([^']*)'|\"([^\"]*)\"|([^\s;&|()]*))")
PARAMETER_ALTERNATIVE = re.compile(
    r"^([A-Za-z_][A-Za-z0-9_]*)(:?[-+=?])(.*)$", re.DOTALL)
BRACE_GROUP = re.compile(r"\{([^{}]*,[^{}]*)\}")
GLOB_META = ("*", "?", "[")
POSIX_GLOB_CLASS = re.compile(r"\[\[:([a-z]+):\]\]", re.IGNORECASE)
POSIX_GLOB_RANGES = {
    "alnum": "0-9A-Za-z",
    "alpha": "A-Za-z",
    "blank": " \t",
    "digit": "0-9",
    "lower": "a-z",
    "space": " \t\r\n",
    "upper": "A-Z",
    "word": "0-9A-Za-z_",
    "xdigit": "0-9A-Fa-f",
}

PATCH_HEADER = re.compile(
    r"^\*\*\*[ \t]+(?:Add File|Update File|Delete File|Move to):"
    r"[ \t]*(\S.*?)[ \t]*$",
    re.MULTILINE | re.IGNORECASE)
PATCH_HEADERISH = re.compile(
    r"^\*\*\*[ \t]+([^:\r\n]+):[ \t]*(\S.*?)[ \t]*$",
    re.MULTILINE)
PATCH_VERBS = {"add file", "update file", "delete file", "move to"}

# These fields are content on the named built-ins, not file selectors. Inner
# Agent and Workflow tool calls still pass through PreToolUse independently.
CONTENT_FIELDS = {
    "agent": {"description", "prompt"},
    "bash": {"description"},
    "edit": {"new_string", "old_string"},
    "grep": {"pattern"},
    "notebookedit": {"new_source"},
    "powershell": {"description"},
    "task": {"description", "prompt"},
    "workflow": {"description", "script"},
    "write": {"content"},
}
GLOB_FIELDS = {
    "file_glob", "file_globs", "files_glob", "glob", "globs",
    "include", "includes", "pattern", "patterns", "selector", "selectors",
}


def path_token_hits(value):
    """Return True when a target-shaped string directly names the file class."""
    return bool(PATH_TOKEN.search(unquote(value).replace("\\", "/")))


def expand_braces(value):
    """Expand simple shell/ripgrep brace alternatives, with a hard size cap."""
    values = [value]
    for _ in range(8):
        changed = False
        expanded = []
        for item in values:
            match = BRACE_GROUP.search(item)
            if not match:
                expanded.append(item)
                continue
            changed = True
            for choice in match.group(1).split(","):
                expanded.append(item[:match.start()] + choice + item[match.end():])
        values = expanded
        if len(values) > 64:
            return None
        if not changed:
            return values
    return None


def protected_paths():
    return [os.path.join(PROJECT_ROOT, name) for name in PROTECTED_BASENAMES]


def scoped_candidates(scope, cwd, allow_parent=False):
    """Return protected path spellings reachable below a selector scope."""
    base = scope or cwd or PROJECT_ROOT
    if not os.path.isabs(base):
        base = os.path.join(cwd or PROJECT_ROOT, base)
    base = os.path.realpath(os.path.normpath(base))
    candidates = []
    for protected in protected_paths():
        protected = os.path.realpath(protected)
        base_cmp = base.casefold()
        protected_cmp = protected.casefold()
        try:
            common = os.path.commonpath((base_cmp, protected_cmp))
            inside = common == base_cmp
        except ValueError:
            inside = False
        if inside or allow_parent:
            relative = os.path.relpath(protected_cmp, base_cmp).replace(os.sep, "/")
            candidates.append(relative)
            if inside:
                candidates.extend(("./" + relative, os.path.basename(protected)))
    return candidates


def glob_hits(pattern, scope=None, cwd=None):
    """Resolve a path selector against the protected names without listing files."""
    pattern = unquote(pattern).strip().strip("'\"").replace("\\", "/")
    if not pattern or pattern.startswith("!"):
        return False
    pattern = normalize_posix_glob(pattern)
    if pattern is None:
        return True
    expansions = expand_braces(pattern)
    if expansions is None:
        return True
    allow_parent = ".." in pattern.split("/")
    candidates = ([(path.replace(os.sep, "/")) for path in protected_paths()]
                  if os.path.isabs(pattern)
                  else scoped_candidates(scope, cwd, allow_parent))
    for expanded in expansions:
        lowered = expanded.lower()
        if path_token_hits(expanded):
            return True
        if any(fnmatch.fnmatchcase(candidate.lower(), lowered)
               for candidate in candidates):
            return True
    return False


def normalize_posix_glob(pattern):
    """Translate standard named glob classes; unknown classes fail closed."""
    def replace(match):
        values = POSIX_GLOB_RANGES.get(match.group(1).lower())
        return "[" + values + "]" if values is not None else match.group(0)

    normalized = POSIX_GLOB_CLASS.sub(replace, pattern)
    return None if POSIX_GLOB_CLASS.search(normalized) else normalized


def shell_glob_forms(token):
    """Yield whole shell arguments and common option-attached selector values."""
    forms = [token]
    if "=" in token:
        forms.append(token.split("=", 1)[1])
    if token.startswith("-g") and len(token) > 2:
        forms.append(token[2:])
    return forms


def shell_selector_is_negative(token):
    """Return True for ripgrep-style selector arguments that exclude paths."""
    if token.startswith("!"):
        return True
    if token.startswith("-g") and len(token) > 2:
        return token[2:].startswith("!")
    if token.startswith("--glob="):
        return token.split("=", 1)[1].startswith("!")
    return False


def shell_assignments(command):
    """Collect literal assignments visible in the same shell envelope."""
    values = {}
    for match in SHELL_ASSIGNMENT.finditer(command):
        value = next((group for group in match.groups()[1:]
                      if group is not None), "")
        bucket = values.setdefault(match.group(1), [])
        if value not in bucket:
            bucket.append(value)
    return values


def normalize_shell_quotes(command):
    """Normalize bounded Bash dollar-quotes before token concatenation."""
    normalized = command
    for _ in range(64):
        matches = [match for match in (
            ANSI_C_QUOTE.search(normalized), LOCALE_QUOTE.search(normalized))
                   if match is not None]
        if not matches:
            return normalized
        match = min(matches, key=lambda item: item.start())
        content = match.group(1)
        try:
            replacement = content
            if match.re is ANSI_C_QUOTE and "\\" in content:
                replacement = codecs.decode(
                    content.encode("utf-8"), "unicode_escape")
        except (UnicodeDecodeError, ValueError):
            return None
        normalized = (normalized[:match.start()] + replacement
                      + normalized[match.end():])
    return None


def unique(values):
    return list(dict.fromkeys(values))


def braced_replacements(inner, assignments):
    alternative = PARAMETER_ALTERNATIVE.match(inner)
    if not alternative:
        return unique(assignments.get(inner, []) + [""])
    name, operator, fallback = alternative.groups()
    assigned = assignments.get(name, [])
    present = [value for value in assigned
               if not operator.startswith(":") or value != ""]
    if operator.endswith("+"):
        return unique(([fallback] if present else []) + [""])
    return unique(present + [fallback])


def expand_variable_matches(values, pattern, replacements):
    """Expand one variable occurrence per pass with a strict variant cap."""
    current = values
    for _ in range(16):
        changed = False
        expanded = []
        for value in current:
            match = pattern.search(value)
            if not match:
                expanded.append(value)
                continue
            changed = True
            for replacement in replacements(match):
                expanded.append(value[:match.start()] + replacement
                                + value[match.end():])
        current = unique(expanded)
        if len(current) > 64:
            return None
        if not changed:
            return current
    return None


def normalize_shell_variables(command):
    """Expand bounded assignment and parameter alternatives conservatively."""
    assignments = shell_assignments(command)
    variants = expand_variable_matches(
        [command], BRACED_SHELL_VARIABLE,
        lambda match: braced_replacements(match.group(1), assignments))
    if variants is None:
        return None
    return expand_variable_matches(
        variants, SIMPLE_SHELL_VARIABLE,
        lambda match: unique(assignments.get(match.group(0)[1:], []) + [""]))


def shell_tokens(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    return list(lexer)


def expand_shell_tilde(value, current):
    """Resolve literal home/current-directory tildes without shell execution."""
    if value == "~+" or value.startswith("~+/"):
        return current + value[2:]
    if value == "~-" or value.startswith("~-/"):
        return None
    if (value == "~" or value.startswith("~/")
            or re.match(r"^~[^/]+(?:/|$)", value)):
        expanded = os.path.expanduser(value)
        return None if expanded == value else expanded
    return value


def shell_scopes(tokens):
    """Track literal cd targets conservatively across one shell envelope."""
    scopes = [PROJECT_ROOT]
    current = PROJECT_ROOT
    for index, token in enumerate(tokens[:-1]):
        if token not in {"cd", "pushd"}:
            continue
        target_index = index + 1
        while target_index < len(tokens):
            candidate = tokens[target_index]
            if candidate == "--":
                target_index += 1
                break
            if candidate.startswith("-"):
                target_index += 1
                continue
            break
        if target_index >= len(tokens):
            continue
        target = tokens[target_index]
        if target == "-" or target in {";", "&&", "||", "|", "&"}:
            continue
        target = expand_shell_tilde(target, current)
        if target is None:
            return None
        current = os.path.realpath(
            target if os.path.isabs(target) else os.path.join(current, target))
        scopes.append(current)
    return scopes


def shell_command_hits(command):
    """Scan direct paths and globs after bounded expansion normalization."""
    quote_normalized = normalize_shell_quotes(command)
    if quote_normalized is None:
        return True
    normalized_variants = normalize_shell_variables(quote_normalized)
    if normalized_variants is None:
        return True
    for normalized in normalized_variants:
        try:
            tokens = shell_tokens(normalized)
        except ValueError:
            return True
        scopes = shell_scopes(tokens)
        if scopes is None:
            return True
        for token in tokens:
            expansions = expand_braces(token)
            if expansions is None:
                return True
            for expanded in expansions:
                if (path_token_hits(expanded)
                        and not shell_selector_is_negative(expanded)):
                    return True
                for form in shell_glob_forms(expanded):
                    if any(meta in form for meta in GLOB_META):
                        for scope in scopes:
                            tilde_form = expand_shell_tilde(form, scope)
                            if tilde_form is None or glob_hits(
                                    tilde_form, scope, scope):
                                return True
    return False


def patch_hits(command):
    """Scan target headers only, failing closed on unknown patch grammar."""
    targets = [target.strip() for target in PATCH_HEADER.findall(command)]
    headerish = PATCH_HEADERISH.findall(command)
    unknown = any(verb.strip().lower() not in PATCH_VERBS for verb, _ in headerish)
    if unknown or not targets:
        return path_token_hits(command) or shell_command_hits(command)
    return any(path_token_hits(target) for target in targets)


def field_is_glob(tool_name, key):
    return (key in GLOB_FIELDS
            or key.endswith("_glob")
            or key.endswith("_globs")
            or ("glob" in tool_name and key == "pattern"))


def field_is_path(key):
    return (key in {"path", "file_path", "notebook_path"}
            or key.endswith("_path"))


def scan(node, tool_name, scope, cwd, key=None, depth=0):
    """Scan target-shaped leaves and map keys, never known content fields."""
    if depth > 32:
        return True
    selector_field = (key == "command" or field_is_glob(tool_name, key or "")
                      or field_is_path(key or ""))
    if selector_field and not isinstance(node, (str, list, tuple)):
        return True
    if isinstance(node, dict):
        for child_key, child in node.items():
            child_key_text = str(child_key)
            if path_token_hits(child_key_text):
                return True
            if scan(child, tool_name, scope, cwd,
                    child_key_text.lower(), depth + 1):
                return True
        return False
    if isinstance(node, (list, tuple)):
        if key == "command":
            if not all(isinstance(item, str) for item in node):
                return True
            return shell_command_hits(" ".join(node))
        return any(scan(child, tool_name, scope, cwd, key, depth + 1)
                   for child in node)
    if not isinstance(node, str):
        return False
    if key in CONTENT_FIELDS.get(tool_name, set()):
        return False
    if key == "command":
        return patch_hits(node) if tool_name == "apply_patch" else shell_command_hits(node)
    if field_is_glob(tool_name, key or ""):
        return glob_hits(node, scope, cwd)
    return path_token_hits(node)


try:
    data = json.load(sys.stdin)
    if not isinstance(data, dict):
        deny("malformed hook input, failing closed")
    tool_name = data.get("tool_name") or ""
    tool_input = data.get("tool_input")
    if not isinstance(tool_name, str) or not isinstance(tool_input, dict):
        deny("malformed hook input, failing closed")
    cwd = data.get("cwd") if isinstance(data.get("cwd"), str) else PROJECT_ROOT
    scope = tool_input.get("path") if isinstance(tool_input.get("path"), str) else cwd
    if scan(tool_input, tool_name.strip().lower(), scope, cwd):
        deny()
except SystemExit:
    raise
except Exception:
    deny("internal error, failing closed")

raise SystemExit(0)
