"""Shared remote-write pipeline for agent-mutate and agent-apply-inbox.

Fail closed. Never git add -A. Never --no-verify. Restore listed files on
any failure before commit. Callers authorize paths before run_pipeline.
"""
from __future__ import annotations

import re
import shlex
import subprocess
import sys
from pathlib import Path


class MutateError(Exception):
    def __init__(self, cls, detail):
        self.cls = cls
        self.detail = detail
        super().__init__("%s: %s" % (cls, detail))


def normalize_path(p):
    p = (p or "").strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    if not p or p.startswith("/") or p == ".." or p.startswith("../") or "/../" in ("/%s/" % p):
        raise MutateError("path-escape", "refusing non-repo-relative path %r" % p)
    return p


def agent_guard(cwd, *args):
    return subprocess.run(
        [sys.executable, str(cwd / "scripts" / "agent-guard"), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def guarded_run(cwd, cmd, check=True):
    """Scan the rendered command with env+git guards, then run argv (no shell)."""
    rendered = " ".join(shlex.quote(str(c)) for c in cmd)
    env = agent_guard(cwd, "env", "--command", rendered, "--root", str(cwd))
    if env.returncode != 0:
        raise MutateError(
            "env-deny",
            (env.stderr or env.stdout or "env guard denied").strip(),
        )
    if Path(str(cmd[0])).name == "git":
        git = agent_guard(cwd, "git", "--command", rendered)
        if git.returncode != 0:
            raise MutateError(
                "git-deny",
                (git.stderr or git.stdout or "git guard denied").strip(),
            )
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if check and r.returncode != 0:
        err = ((r.stderr or "") + (r.stdout or "")).strip()
        raise MutateError(
            "command-failed",
            "%s exited %s: %s" % (cmd[0], r.returncode, err[:800]),
        )
    return r


def hooks_path_ok(cwd):
    r = subprocess.run(
        ["git", "-C", str(cwd), "config", "--get", "core.hooksPath"],
        capture_output=True,
        text=True,
    )
    val = (r.stdout or "").strip()
    if val != ".githooks":
        raise MutateError(
            "hooksPath",
            "core.hooksPath must be .githooks (got %r); refuse remote commit" % val,
        )


def doctor_staged(cwd):
    r = subprocess.run(
        [sys.executable, str(cwd / "scripts" / "repo-doctor"), "--staged"],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    if r.returncode != 0:
        raise MutateError("doctor-hard", out[:800] or "repo-doctor --staged failed")
    if re.search(r"repo-doctor:.*\b(\d+)\s+hard violation", out, re.I):
        m = re.search(r"repo-doctor:.*\b(\d+)\s+hard violation", out, re.I)
        if m and int(m.group(1)) > 0:
            raise MutateError("doctor-hard", out[:800])
    elif re.search(r"(?m)^hard\s+", out):
        raise MutateError("doctor-hard", out[:800])
    return out


def env_scan_path(cwd, path):
    scan = agent_guard(cwd, "env", "--path", path, "--root", str(cwd))
    if scan.returncode != 0:
        raise MutateError("env-deny", (scan.stderr or path).strip())


def porcelain_sets(cwd):
    """Return (tracked_dirty, untracked) path sets from git status -z."""
    r = subprocess.run(
        ["git", "-C", str(cwd), "status", "--porcelain", "-z"],
        capture_output=True,
        check=True,
    )
    tracked = set()
    untracked = set()
    parts = r.stdout.split(b"\0")
    i = 0
    while i < len(parts):
        item = parts[i]
        if not item:
            i += 1
            continue
        status = item[:2]
        path = item[3:].decode("utf-8", "replace") if len(item) > 3 else ""
        kind = status[:1]
        if kind in (b"R", b"C"):
            if path:
                tracked.add(normalize_path(path))
            i += 1
            if i < len(parts) and parts[i]:
                tracked.add(normalize_path(parts[i].decode("utf-8", "replace")))
        elif status == b"??":
            if path:
                untracked.add(normalize_path(path))
        else:
            if path:
                tracked.add(normalize_path(path))
        i += 1
    return tracked, untracked


def require_clean_start(cwd, paths):
    tracked, untracked = porcelain_sets(cwd)
    listed = set(paths)
    blocked = sorted((tracked | untracked) & listed)
    if blocked:
        raise MutateError(
            "dirty-path",
            "listed paths must be clean before the patch: %s" % blocked,
        )
    extra = sorted(tracked - listed)
    if extra:
        raise MutateError(
            "dirty-tree",
            "unrelated dirty tracked paths block remote write: %s" % extra,
        )


def snapshot_files(cwd, paths):
    snap = {}
    for p in paths:
        fp = cwd / p
        if fp.is_file():
            snap[p] = fp.read_bytes()
        else:
            snap[p] = None
    return snap


def restore_snapshot(cwd, snap, extras):
    for p, content in snap.items():
        fp = cwd / p
        if content is None:
            if fp.is_file():
                fp.unlink()
        else:
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_bytes(content)
    for p in extras:
        fp = cwd / p
        if fp.is_file():
            fp.unlink()
    all_paths = sorted(set(snap) | set(extras))
    if all_paths:
        subprocess.run(
            ["git", "-C", str(cwd), "reset", "HEAD", "--", *all_paths],
            capture_output=True,
            text=True,
        )


def patch_named_paths(cwd, patch_file):
    r = subprocess.run(
        ["git", "-C", str(cwd), "apply", "--numstat", "--unidiff-zero", str(patch_file)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise MutateError(
            "patch-parse",
            (r.stderr or r.stdout or "git apply --numstat failed").strip()[:800],
        )
    named = []
    for line in (r.stdout or "").splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        raw = parts[2].strip()
        if " => " in raw:
            raw = raw.split(" => ", 1)[1].strip()
        if raw.startswith("{") and "}" in raw:
            # numstat rename form: prefix/{old => new}
            raw = raw.split(" => ", 1)[-1].rstrip("}").strip()
        named.append(normalize_path(raw))
    if not named:
        raise MutateError("patch-parse", "patch names no files")
    return named


def apply_patch(cwd, patch_file):
    # Remotes often emit zero-context unified diffs (@@ -N,1 +N,1 @@). Plain
    # git apply rejects those; --unidiff-zero accepts them and still applies
    # normal context patches.
    flags = ["--unidiff-zero"]
    guarded_run(cwd, ["git", "-C", str(cwd), "apply", *flags, "--check", str(patch_file)])
    guarded_run(cwd, ["git", "-C", str(cwd), "apply", *flags, str(patch_file)])


def run_pipeline(
    cwd,
    paths,
    patch_file,
    message,
    host,
    skill,
    mode,
    no_pull=False,
    no_push=False,
    dry_run=False,
):
    """Apply patch, stage exactly paths, doctor, commit, push.

    Caller has already env-scanned and authorized every path. Worktree must
    start clean. On any failure before commit, restore snapshotted files.
    """
    if not patch_file or not Path(patch_file).is_file():
        raise MutateError("missing-patch", "remote writes require --patch / patch.diff")
    patch_file = Path(patch_file).resolve()
    paths = [normalize_path(p) for p in paths]
    if not paths:
        raise MutateError("usage", "require at least one path")
    if len(set(paths)) != len(paths):
        raise MutateError("usage", "duplicate --paths entries")

    for p in paths:
        env_scan_path(cwd, p)

    hooks_path_ok(cwd)
    require_clean_start(cwd, paths)

    if not no_pull:
        guarded_run(cwd, ["git", "-C", str(cwd), "pull", "--ff-only"])
        require_clean_start(cwd, paths)

    named = patch_named_paths(cwd, patch_file)
    extra_named = sorted(set(named) - set(paths))
    if extra_named:
        raise MutateError(
            "unlicensed-path",
            "patch touches paths outside the authorized set: %s" % extra_named,
        )
    missing_named = sorted(set(paths) - set(named))
    if missing_named:
        raise MutateError(
            "stage-mismatch",
            "authorized paths missing from patch: %s" % missing_named,
        )

    snap = snapshot_files(cwd, paths)
    _before_tracked, before_untracked = porcelain_sets(cwd)
    extras_created = []
    try:
        apply_patch(cwd, patch_file)
        tracked, untracked = porcelain_sets(cwd)
        listed = set(paths)
        extras_created = sorted(
            (tracked - listed) | ((untracked - before_untracked) - listed)
        )
        if extras_created:
            raise MutateError(
                "unlicensed-path",
                "apply dirtied paths outside the authorized set: %s" % extras_created,
            )
        missing_dirty = sorted(listed - tracked - untracked)
        if missing_dirty:
            raise MutateError(
                "stage-mismatch",
                "authorized paths unchanged after patch: %s" % missing_dirty,
            )
        guarded_run(cwd, ["git", "-C", str(cwd), "add", "--", *paths])
        staged = subprocess.run(
            ["git", "-C", str(cwd), "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        staged_set = {normalize_path(s) for s in staged if s.strip()}
        if staged_set != set(paths):
            raise MutateError(
                "stage-mismatch",
                "staged set must equal authorized paths; extra=%s missing=%s"
                % (sorted(staged_set - set(paths)), sorted(set(paths) - staged_set)),
            )
        doctor_staged(cwd)
        if dry_run:
            restore_snapshot(cwd, snap, extras_created)
            print("agent-mutate: dry-run OK")
            print("paths: %s" % ", ".join(paths))
            print("doctor: clean")
            return 0

        body = (
            "%s\n\n"
            "agent-mutate host=%s skill=%s mode=%s\n"
            "paths: %s\n" % (message, host, skill, mode, ", ".join(paths))
        )
        guarded_run(cwd, ["git", "-C", str(cwd), "commit", "-m", body])
    except Exception:
        restore_snapshot(cwd, snap, extras_created)
        raise

    sha = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if not no_push:
        guarded_run(cwd, ["git", "-C", str(cwd), "push"])
    print("agent-mutate: receipt")
    print("sha: %s" % sha)
    print("paths: %s" % ", ".join(paths))
    print("doctor: clean")
    print("host: %s" % host)
    print("skill: %s" % skill)
    print("mode: %s" % mode)
    return 0
