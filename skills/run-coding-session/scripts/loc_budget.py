#!/usr/bin/env python3
"""Delta-LOC budget: the net non-blank source lines a coding task may add.

Rule and rationale: ../references/delta-loc-budget.md

  loc_budget.py hook claude|codex   hook entrypoint (SessionStart, PreToolUse, Stop) on stdin
  loc_budget.py check [--repo P]    measure P against a live session baseline, else against HEAD
  loc_budget.py set N [--repo P]    set the budget for live sessions tracking P (the user's call only)
  loc_budget.py reset [--repo P]    re-baseline live sessions tracking P after a committed task

Exit status of check: 0 inside the budget, 1 over it.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from observe_repo import CODE_EXTENSIONS, SKIP_DIRS, is_test  # one owner for source/test classes

DEFAULT_BUDGET = int(os.environ.get("LOC_BUDGET", "300"))
MAX_BLOCKS = 2  # forced passes per overrun before it is handed to the user
LIVE_SECONDS = 24 * 3600
STATE = Path(os.environ.get("LOC_BUDGET_STATE", Path.home() / ".claude" / "loc-budget"))
# Markup is excluded so generated documents (proposal HTML, styled reports) never spend a budget.
EXTENSIONS = (CODE_EXTENSIONS - {".html", ".css"}) | {".mjs", ".cjs", ".astro"}
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
# Bracketed letters keep this line from matching itself.
MARKER = re.compile(rb"\b(?:TO[D]O|FIX[M]E|XX[X]|HAC[K])\b|NotImplemented[E]rror|\b(?:todo|unimplemented)!\(")
RULE = Path(__file__).resolve().parent.parent / "references" / "delta-loc-budget.md"
FIX = (
    "Do not end the turn yet: the budget is a hard invariant. Look for the smaller design first. "
    "Then delete what this change made obsolete: old paths, duplicated logic, superseded "
    "abstractions, compatibility code, dead branches. Replace behavior instead of wrapping the old "
    "path in a new condition. Never fit the budget by cutting tests, error handling or required "
    "behavior, by squeezing code onto fewer lines, or with TODOs and placeholders. If the task truly "
    "cannot fit, stop and ask the user for a larger budget with the measured number; only the user "
    f"sets it. Rule: {RULE}"
)


def git(repo: str | Path, *args: str) -> bytes | None:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def repo_root(path: str | None) -> str | None:
    if not path:
        return None
    directory = Path(path).expanduser()
    while not directory.is_dir():
        directory = directory.parent
    out = git(directory, "rev-parse", "--show-toplevel")
    return out.decode().strip() if out else None


def eligible(rel: str) -> bool:
    """Source by path alone; an extensionless path still needs a shebang to count."""
    parts = rel.split("/")
    if SKIP_DIRS.intersection(parts[:-1]) or ".min." in parts[-1]:
        return False
    extension = os.path.splitext(parts[-1])[1].lower()
    return not extension or extension in EXTENSIONS


def counts(data: bytes | None) -> tuple[int, int]:
    if data is None or b"\0" in data[:8000]:
        return (0, 0)
    return (sum(1 for line in data.splitlines() if line.strip()), len(MARKER.findall(data)))


def read(root: str, rel: str) -> bytes | None:
    try:
        return (Path(root) / rel).read_bytes()
    except OSError:
        return None


def is_source(root: str, base: str, rel: str, data: bytes | None) -> bool:
    if os.path.splitext(rel)[1]:
        return True
    sniff = data if data is not None else git(root, "cat-file", "blob", f"{base}:{rel}")
    return (sniff or b"").startswith(b"#!")


def changed(root: str, base: str) -> set[str]:
    out = (git(root, "diff", "--name-only", "--no-renames", "-z", base) or b"") + (
        git(root, "ls-files", "-o", "--exclude-standard", "-z") or b""
    )
    paths = {p.decode(errors="surrogateescape") for p in out.split(b"\0") if p}
    return {p for p in paths if eligible(p)}


def baseline(root: str) -> dict:
    head = git(root, "rev-parse", "-q", "--verify", "HEAD^{commit}")
    base = head.decode().strip() if head else EMPTY_TREE
    dirty = {}
    for rel in changed(root, base):
        data = read(root, rel)
        if is_source(root, base, rel, data):
            dirty[rel] = counts(data)
    return {"base": base, "dirty": dirty, "budget": DEFAULT_BUDGET, "touched": False}


def measure(root: str, repo: dict) -> dict:
    rows = []
    for rel in changed(root, repo["base"]) | set(repo["dirty"]):
        data = read(root, rel)
        if rel in repo["dirty"]:
            before = tuple(repo["dirty"][rel])
        elif is_source(root, repo["base"], rel, data):
            before = counts(git(root, "cat-file", "blob", f"{repo['base']}:{rel}"))
        else:
            continue
        now = counts(data)
        if now != before:
            rows.append((now[0] - before[0], now[1] - before[1], rel))
    source = [row for row in rows if not is_test(Path(row[2]))]
    loc, markers = sum(row[0] for row in source), sum(row[1] for row in source)
    tests = sum(row[0] for row in rows) - loc
    lines = [
        f"{root}: ΔLOC {loc:+d} net non-blank source lines, budget {repo['budget']}; "
        f"tests {tests:+d} (not budgeted); new placeholder markers {markers:+d}"
    ]
    lines += [f"  {d:+d} {rel}" for d, _, rel in sorted(rows, key=lambda r: -abs(r[0]))[:8]]
    return {"loc": loc, "markers": markers, "over": loc > repo["budget"] or markers > 0, "text": "\n".join(lines)}


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def save(path: Path, state: dict) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(state))
    temporary.replace(path)


def track(repos: dict, path: str | None, touched: bool = False) -> None:
    root = repo_root(path)
    if not root:
        return
    if root not in repos:
        repos[root] = baseline(root)
    if touched:
        repos[root]["touched"] = True


def hook(host: str) -> int:
    event = json.load(sys.stdin)
    session = re.sub(r"[^\w.-]", "_", str(event.get("session_id") or ""))
    if not session:
        return 0
    path = STATE / f"{session}.json"
    name = event.get("hook_event_name")
    fresh = name == "SessionStart" and event.get("source") in ("startup", "clear")
    state = {} if fresh else load(path)
    repos = state.setdefault("repos", {})
    if name == "SessionStart":
        for old in STATE.glob("*.json"):
            if time.time() - old.stat().st_mtime > 14 * 24 * 3600:
                old.unlink(missing_ok=True)
        track(repos, event.get("cwd"))
    elif name == "PreToolUse":
        target = (event.get("tool_input") or {}).get("file_path") or (event.get("tool_input") or {}).get("notebook_path")
        if not target or not eligible(Path(target).name):
            return 0
        track(repos, target, touched=True)
    elif name == "Stop":
        # Claude sessions are judged only in repos they edited, so a parallel session's code never
        # blocks a documents-only session. Codex exposes no edit envelope here, so it is judged on all.
        reports = [
            measure(root, repo)
            for root, repo in repos.items()
            if Path(root).is_dir() and (host == "codex" or repo.get("touched"))
        ]
        over = "\n\n".join(r["text"] for r in reports if r["over"])
        # Forced passes are counted per overrun episode, not per stop chain, so no host can loop.
        if not over:
            state["blocks"] = 0
        elif state.get("blocks", 0) < MAX_BLOCKS:
            state["blocks"] = state.get("blocks", 0) + 1
            print(json.dumps({"decision": "block", "reason": f"{over}\n\n{FIX}"}))
        else:
            print(json.dumps({"systemMessage": f"ΔLOC budget still exceeded after {MAX_BLOCKS} forced passes:\n{over}"}))
    save(path, state)
    return 0


def live_sessions(root: str):
    for path in STATE.glob("*.json"):
        if time.time() - path.stat().st_mtime < LIVE_SECONDS:
            state = load(path)
            if root in state.get("repos", {}):
                yield path, state


def main(argv: list[str]) -> int:
    if argv[:1] == ["hook"]:
        return hook(argv[1] if len(argv) > 1 else "claude")
    repo_arg = argv[argv.index("--repo") + 1] if "--repo" in argv else os.getcwd()
    root = repo_root(repo_arg)
    if not root or not argv or argv[0] not in ("check", "set", "reset"):
        print(__doc__ if root else f"not a git repository: {repo_arg}", file=sys.stderr)
        return 2
    sessions = sorted(live_sessions(root), key=lambda item: item[0].stat().st_mtime)
    if argv[0] == "check":
        repo = sessions[-1][1]["repos"][root] if sessions else {**baseline(root), "dirty": {}}
        report = measure(root, repo)
        print(report["text"] + ("" if sessions else "\n  (no live session baseline: measured against HEAD)"))
        return 1 if report["over"] else 0
    for path, state in sessions:
        if argv[0] == "set":
            state["repos"][root]["budget"] = int(argv[1])
        else:
            state["repos"][root] = {**baseline(root), "budget": state["repos"][root]["budget"], "touched": state["repos"][root]["touched"]}
        save(path, state)
    print(f"{argv[0]}: {len(sessions)} live session(s) tracking {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))  # a crash exits 1, never 2, so it cannot block a Stop
