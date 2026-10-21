"""Fail-closed memo for a successful local, no-argument repo-doctor run.

OPERATOR_OS_DOCTOR_DATE may pin the cache clock to YYYY-MM-DD for reproducible
runs and tests. Normal operation uses the current local datetime.
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


SCHEMA = 2
SKIP_ROOT_DIRS = {".git", "node_modules", ".worktrees"}
# Live key files are never statted or hashed. The tracked placeholder is ordinary config.
KEY_FILE_PREFIX, KEY_TEMPLATE = ".env", ".env.example"


def cache_now(env):
    """Return the cache clock, honoring the documented YYYY-MM-DD override."""
    pinned = env.get("OPERATOR_OS_DOCTOR_DATE")
    if pinned:
        return datetime.strptime(pinned, "%Y-%m-%d").replace(hour=12)
    return datetime.now()


def _key_file(name):
    return name.startswith(KEY_FILE_PREFIX) and name != KEY_TEMPLATE


def cache_path(root, env):
    home = Path(env.get("HOME") or Path.home()).resolve()
    path = home / ".cache" / "operator-os-repo-doctor" / hashlib.sha256(
        os.fsencode(str(root.resolve()))).hexdigest() / "result.json"
    if (home / ".cache").is_symlink() or path.parent.resolve().is_relative_to(root.resolve()):
        return None
    return path


def _git(root, env, *args, absent_ok=False):
    result = subprocess.run(["git", *args], cwd=root, env=env, capture_output=True, timeout=5)
    if result.returncode == 0 or (absent_ok and result.returncode == 1):
        return result.stdout
    raise OSError("git fingerprint input unavailable")


def fingerprint(root, env, now):
    """Hash metadata, including ctime for same-size edits whose mtime was restored."""
    try:
        root = Path(root).resolve(strict=True)
        tracked = _git(root, env, "ls-files", "--stage", "-z")
        for entry in filter(None, tracked.split(b"\0")):
            path = Path(os.fsdecode(entry.split(b"\t", 1)[-1]))
            if _key_file(path.name) or path.parts[0] in SKIP_ROOT_DIRS:
                return None
        environment = sorted((key, value) for key, value in env.items()
                             if key in {"HOME", "PATH", "TZ", "LANG", "CODEX_HOME", "XDG_CONFIG_HOME"}
                             or key in {"OPERATOR_OS_DOCTOR_DATE"}
                             or key.startswith(("GIT_", "PYTHON", "LC_")))
        inputs = [SCHEMA, str(root), now.date().isoformat(), sys.version, sys.executable, environment, tracked]
        for args in (("rev-parse", "--verify", "HEAD"), ("status", "--porcelain=v1", "-z", "-uall"),
                     ("config", "--list", "--show-origin", "-z")):
            inputs.append(_git(root, env, *args))
        names = ("MERGE_HEAD", "info/exclude", "info/sparse-checkout", "info/grafts", "shallow",
                 "objects/info/alternates", "packed-refs", "refs/replace")
        args = [argument for name in names for argument in ("--git-path", name)]
        git_paths = _git(root, env, "rev-parse", "--path-format=absolute", *args).splitlines()
        if len(git_paths) != len(names) or any(not Path(os.fsdecode(p)).is_absolute() for p in git_paths):
            return None
        home = Path(env.get("HOME") or Path.home())
        excludes = _git(root, env, "config", "--path", "--get", "core.excludesFile", absent_ok=True).strip()
        excludes = Path(os.fsdecode(excludes)) if excludes else \
            Path(env.get("XDG_CONFIG_HOME") or home / ".config") / "git" / "ignore"
        if not excludes.is_absolute():
            return None
        pending = [(root, True), (Path(os.fsdecode(git_paths[-1])), True)]
        pending.extend((path, False) for path in [Path(sys.executable).resolve(strict=True), excludes,
                       Path(env.get("CODEX_HOME") or home / ".codex") / "config.toml",
                       *(Path(os.fsdecode(path)) for path in git_paths[:-1])])
        digest = hashlib.sha256(repr(inputs).encode(errors="surrogateescape"))
        for path, recursive in pending:
            try:
                item = path.lstat()
            except FileNotFoundError:
                digest.update(os.fsencode(str(path)) + b"\0missing\0")
                continue
            directory = stat.S_ISDIR(item.st_mode)
            if not (directory or stat.S_ISREG(item.st_mode)) or not item.st_mode & stat.S_IRUSR:
                return None
            if directory and recursive:
                pending.extend((child, True) for child in sorted(path.iterdir())
                               if not (path == root and child.name in SKIP_ROOT_DIRS and child.is_dir())
                               and (child.is_dir() or not _key_file(child.name)))
            old = not directory and path.is_relative_to(root / "knowledge") \
                and item.st_mtime < now.timestamp() - 7 * 86400
            digest.update(repr((str(path), item.st_dev, item.st_ino, item.st_mode, item.st_size,
                                item.st_mtime_ns, item.st_ctime_ns, old)).encode(errors="surrogateescape"))
        return digest.hexdigest()
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def _private(path, kind):
    info = path.lstat()
    if not kind(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise OSError("unsafe cache permissions")
    return info


def _record(key, output):
    return {"schema": SCHEMA, "key": key, "rc": 0, "stdout": output,
            "digest": hashlib.sha256(output.encode()).hexdigest()}


def read_cache(path, key):
    if path is None or key is None:
        return None
    try:
        _private(path.parent, stat.S_ISDIR)
        if _private(path, stat.S_ISREG).st_size > 2_000_000:
            return None
        data = json.loads(path.read_text())
        output = data["stdout"]
        if isinstance(output, str) and output.endswith("\n") \
                and "repo-doctor: " in output.splitlines()[-1] and data == _record(key, output):
            return output
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return None


def write_cache(path, key, output):
    if path is None or key is None:
        return
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        _private(path.parent, stat.S_ISDIR)
        with tempfile.TemporaryDirectory(dir=path.parent, prefix=".doctor-") as directory:
            staged = Path(directory) / path.name
            with staged.open("w", encoding="utf-8") as file:
                os.fchmod(file.fileno(), 0o600)
                json.dump(_record(key, output), file)
                file.flush()
                os.fsync(file.fileno())
            staged.replace(path)
    except OSError:
        pass
