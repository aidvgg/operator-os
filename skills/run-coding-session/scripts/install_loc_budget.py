#!/usr/bin/env python3
"""Opt in to the ΔLOC budget for every Claude Code and Codex session on this machine. Idempotent.

  install_loc_budget.py          install; each changed file is first copied to <file>.bak-loc-budget
  install_loc_budget.py --check  change nothing; exit 1 if any wiring is missing

The budget is off until the operator runs this. Only a run without --check writes, and it writes
only the user-level files under ~/.claude and ~/.codex named below. Run it yourself; an agent or
the onboarding flow never runs it, since these files sit outside the repository.
"""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOK = f"{shlex.quote(str(HERE / 'loc_budget.py'))} hook"
RULE = HERE.parent / "references" / "delta-loc-budget.md"
HOME = Path.home()
HOOKS = {
    HOME / ".claude" / "settings.json": (
        "claude",
        [("SessionStart", None), ("PreToolUse", "Edit|Write|MultiEdit|NotebookEdit"), ("Stop", None)],
    ),
    HOME / ".codex" / "hooks.json": ("codex", [("SessionStart", "startup|resume|clear|compact"), ("Stop", None)]),
}
INSTRUCTIONS = {
    HOME / ".claude" / "CLAUDE.md": f"@{RULE}",
    HOME / ".codex" / "AGENTS.md": f"Before any coding task, read {RULE} and follow it.",
}


def write(path: Path, text: str) -> None:
    if path.exists():
        shutil.copy2(path, path.with_name(path.name + ".bak-loc-budget"))
    path.write_text(text)


def main(check: bool) -> int:
    missing = []
    for path, (host, events) in HOOKS.items():
        if not path.parent.is_dir():
            continue
        data = json.loads(path.read_text()) if path.exists() else {}
        hooks = data.setdefault("hooks", {})
        added = False
        for event, matcher in events:
            groups = hooks.setdefault(event, [])
            if any(HOOK in hook.get("command", "") for group in groups for hook in group.get("hooks", [])):
                continue
            missing.append(f"{path}: {event} hook")
            group = {"hooks": [{"type": "command", "command": f"{HOOK} {host}", "timeout": 60}]}
            groups.append({"matcher": matcher, **group} if matcher else group)
            added = True
        if added and not check:
            write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    for path, line in INSTRUCTIONS.items():
        if not path.parent.is_dir():
            continue
        text = path.read_text() if path.exists() else ""
        if str(RULE) in text:
            continue
        missing.append(f"{path}: rule pointer")
        if not check:
            write(path, text + ("\n" if text.strip() else "") + f"# Coding tasks\n\n{line}\n")
    verb = "missing" if check else "installed"
    print("\n".join(f"{verb}: {item}" for item in missing) or "ΔLOC budget already wired everywhere")
    if missing and not check and any("codex" in item for item in missing):
        print("Codex runs new hooks only after you trust them: open `codex`, run /hooks, trust both entries.")
    return 1 if missing and check else 0


if __name__ == "__main__":
    raise SystemExit(main("--check" in sys.argv[1:]))
