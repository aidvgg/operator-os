#!/usr/bin/env python3
"""Produce a read-only structural inventory for a coding-session baseline."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


OBSERVER_VERSION = 1
MAX_FILES = 100_000
MAX_REPORTED_PATHS = 100
MAX_LARGEST_FILES = 20
MAX_JSON_BYTES = 1_000_000

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".output",
    "target",
    "out",
    "tmp",
    "temp",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".turbo",
}

ALLOWED_HIDDEN_DIRS = {".github", ".circleci"}
ALLOWED_HIDDEN_FILES = {".gitlab-ci.yml"}

MANIFEST_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "Gemfile",
    "Gemfile.lock",
    "composer.json",
    "composer.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "gradlew",
    "Makefile",
    "justfile",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}

INSTRUCTION_NAMES = {"AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "SECURITY.md", "CODEOWNERS"}
INSTRUCTION_PREFIXES = ("README", "ARCHITECTURE")

CI_NAMES = {"Jenkinsfile", "azure-pipelines.yml", ".gitlab-ci.yml", "buildkite.yml"}
TEST_CONFIG_PATTERNS = (
    "pytest.ini",
    "tox.ini",
    "playwright.config",
    "cypress.config",
    "vitest.config",
    "jest.config",
    "karma.conf",
)

CODE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".ex",
    ".exs",
    ".go",
    ".h",
    ".hpp",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".lua",
    ".m",
    ".mm",
    ".php",
    ".pl",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sh",
    ".sol",
    ".sql",
    ".svelte",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
    ".zig",
}

LANGUAGE_BY_EXTENSION = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".css": "CSS",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".go": "Go",
    ".h": "C/C++ headers",
    ".hpp": "C++ headers",
    ".html": "HTML",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript JSX",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".lua": "Lua",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    ".php": "PHP",
    ".pl": "Perl",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scala": "Scala",
    ".sh": "Shell",
    ".sol": "Solidity",
    ".sql": "SQL",
    ".svelte": "Svelte",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript JSX",
    ".vue": "Vue",
    ".zig": "Zig",
}

FRAMEWORK_PACKAGES = {
    "@angular/core",
    "@nestjs/core",
    "@playwright/test",
    "@remix-run/react",
    "@sveltejs/kit",
    "astro",
    "cypress",
    "django",
    "electron",
    "expo",
    "express",
    "fastapi",
    "flask",
    "jest",
    "next",
    "nuxt",
    "prisma",
    "react",
    "react-native",
    "remix",
    "svelte",
    "vite",
    "vitest",
    "vue",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Absolute or relative repository path")
    parser.add_argument("--output", help="Write JSON to this path instead of stdout")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    return parser.parse_args()


def visible_relative_path(relative: Path) -> bool:
    for part in relative.parts:
        if part in ALLOWED_HIDDEN_DIRS or part in ALLOWED_HIDDEN_FILES:
            continue
        if part.startswith("."):
            return False
    return True


def run_command(args: list[str], cwd: Path, timeout: int = 8) -> tuple[int, str]:
    try:
        result = subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode, output


def git_value(target: Path, *args: str) -> str | None:
    code, output = run_command(["git", "-C", str(target), *args], target)
    return output if code == 0 else None


def sanitized_git_status(target: Path) -> dict[str, Any]:
    raw = git_value(target, "status", "--short")
    if raw is None:
        return {"available": False, "count": 0, "paths": [], "truncated": False}

    paths: list[str] = []
    for line in raw.splitlines():
        payload = line[3:] if len(line) > 3 else ""
        candidates = [item.strip().strip('"') for item in payload.split(" -> ")]
        if not candidates:
            continue
        if all(visible_relative_path(Path(candidate)) for candidate in candidates):
            paths.append(payload)

    return {
        "available": True,
        "count": len(paths),
        "paths": paths[:MAX_REPORTED_PATHS],
        "truncated": len(paths) > MAX_REPORTED_PATHS,
    }


def git_observation(target: Path) -> dict[str, Any]:
    root = git_value(target, "rev-parse", "--show-toplevel")
    if root is None:
        return {"present": False}

    branch = git_value(target, "branch", "--show-current") or "DETACHED"
    head = git_value(target, "rev-parse", "HEAD")
    commit_count_raw = git_value(target, "rev-list", "--count", "HEAD")
    try:
        commit_count = int(commit_count_raw) if commit_count_raw is not None else 0
    except ValueError:
        commit_count = 0

    return {
        "present": True,
        "root": str(Path(root).resolve()),
        "branch": branch,
        "head": head,
        "commit_count": commit_count,
        "status": sanitized_git_status(target),
    }


def is_manifest(path: Path) -> bool:
    return path.name in MANIFEST_NAMES or path.suffix.lower() in {".csproj", ".sln"}


def is_instruction(path: Path) -> bool:
    return path.name in INSTRUCTION_NAMES or path.name.startswith(INSTRUCTION_PREFIXES)


def is_ci(path: Path) -> bool:
    parts = path.parts
    return (
        path.name in CI_NAMES
        or (len(parts) >= 3 and parts[0] == ".github" and parts[1] == "workflows")
        or (len(parts) >= 2 and parts[0] == ".circleci")
    )


def is_test(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts[:-1]}
    stem = path.stem.lower()
    return bool(
        lowered_parts.intersection({"test", "tests", "spec", "specs", "__tests__", "e2e"})
        or stem.startswith(("test_", "test-"))
        or stem.endswith(("_test", ".test", "_spec", ".spec", ".e2e"))
    )


def is_test_config(path: Path) -> bool:
    name = path.name.lower()
    return any(name == pattern or name.startswith(pattern + ".") for pattern in TEST_CONFIG_PATTERNS)


def safe_read_json(path: Path) -> dict[str, Any] | None:
    try:
        if path.stat().st_size > MAX_JSON_BYTES:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def package_observation(target: Path, file_paths: list[Path]) -> dict[str, Any]:
    package_files = [path for path in file_paths if path.name == "package.json"]
    root_package = next((path for path in package_files if path.parent == target), None)
    if root_package is None:
        return {"present": False}

    data = safe_read_json(root_package)
    if data is None:
        return {"present": True, "readable": False, "path": "package.json"}

    scripts = data.get("scripts") if isinstance(data.get("scripts"), dict) else {}
    dependencies: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = data.get(key)
        if isinstance(value, dict):
            dependencies.update(item for item in value if isinstance(item, str))

    return {
        "present": True,
        "readable": True,
        "path": "package.json",
        "name": data.get("name") if isinstance(data.get("name"), str) else None,
        "scripts": sorted(item for item in scripts if isinstance(item, str)),
        "framework_signals": sorted(dependencies.intersection(FRAMEWORK_PACKAGES)),
        "workspace": "workspaces" in data,
    }


def scan_files(target: Path) -> dict[str, Any]:
    extension_counts: Counter[str] = Counter()
    language_counts: Counter[str] = Counter()
    top_level: set[str] = set()
    manifests: list[str] = []
    instructions: list[str] = []
    ci_files: list[str] = []
    test_configs: list[str] = []
    test_files: list[str] = []
    code_files = 0
    docs_files = 0
    all_files: list[Path] = []
    largest: list[tuple[int, str]] = []
    truncated = False

    for current, directories, files in os.walk(target, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in SKIP_DIRS
            and (
                not directory.startswith(".")
                or directory in ALLOWED_HIDDEN_DIRS
            )
        )

        for filename in sorted(files):
            path = current_path / filename
            try:
                relative = path.relative_to(target)
            except ValueError:
                continue
            if not visible_relative_path(relative) or path.is_symlink():
                continue
            if len(all_files) >= MAX_FILES:
                truncated = True
                break

            all_files.append(path)
            top_level.add(relative.parts[0])
            suffix = path.suffix.lower() or "[none]"
            extension_counts[suffix] += 1

            if path.suffix.lower() in CODE_EXTENSIONS:
                code_files += 1
                language = LANGUAGE_BY_EXTENSION.get(path.suffix.lower())
                if language:
                    language_counts[language] += 1
            if path.suffix.lower() in {".md", ".mdx", ".rst", ".txt"} or "docs" in relative.parts:
                docs_files += 1
            if is_manifest(relative):
                manifests.append(relative.as_posix())
            if is_instruction(relative):
                instructions.append(relative.as_posix())
            if is_ci(relative):
                ci_files.append(relative.as_posix())
            if is_test_config(relative):
                test_configs.append(relative.as_posix())
            if is_test(relative):
                test_files.append(relative.as_posix())

            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            largest.append((size, relative.as_posix()))

        if truncated:
            break

    largest.sort(key=lambda item: (-item[0], item[1]))
    package = package_observation(target, all_files)

    return {
        "total_files": len(all_files),
        "scan_truncated": truncated,
        "code_files": code_files,
        "test_file_count": len(test_files),
        "docs_files": docs_files,
        "top_level_entries": sorted(top_level)[:MAX_REPORTED_PATHS],
        "manifests": sorted(manifests)[:MAX_REPORTED_PATHS],
        "instruction_files": sorted(instructions)[:MAX_REPORTED_PATHS],
        "ci_files": sorted(ci_files)[:MAX_REPORTED_PATHS],
        "test_configs": sorted(test_configs)[:MAX_REPORTED_PATHS],
        "sample_test_files": sorted(test_files)[:25],
        "languages": [
            {"name": name, "files": count}
            for name, count in language_counts.most_common(20)
        ],
        "extensions": [
            {"extension": extension, "files": count}
            for extension, count in extension_counts.most_common(25)
        ],
        "largest_files": [
            {"path": path, "bytes": size}
            for size, path in largest[:MAX_LARGEST_FILES]
        ],
        "package": package,
    }


def classify_project(scan: dict[str, Any], git: dict[str, Any]) -> tuple[str, list[str]]:
    evidence: list[str] = []
    total_files = int(scan["total_files"])
    code_files = int(scan["code_files"])
    manifests = scan["manifests"]
    commit_count = int(git.get("commit_count", 0)) if git.get("present") else 0

    if total_files == 0:
        return "greenfield", ["No visible files were found."]
    if code_files > 0:
        evidence.append(f"Found {code_files} code files.")
    if manifests:
        evidence.append(f"Found {len(manifests)} project manifests or lockfiles.")
    if commit_count > 0:
        evidence.append(f"Git history contains {commit_count} commits.")
    if code_files > 0 or manifests or commit_count > 1:
        return "existing", evidence
    return "ambiguous", ["Visible files exist, but implementation evidence is limited."]


def observe(target: Path) -> dict[str, Any]:
    scan = scan_files(target)
    git = git_observation(target)
    mode, mode_evidence = classify_project(scan, git)
    return {
        "observer_version": OBSERVER_VERSION,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "target": str(target),
        "mode_hint": mode,
        "mode_evidence": mode_evidence,
        "git": git,
        "inventory": scan,
        "limitations": [
            "Inventory only: no build, test, lint, type, security, or runtime command was executed.",
            "Hidden files are excluded except known continuous-integration paths.",
            "Dependency, cache, generated-output, and vendor directories are excluded.",
            "Detected commands and frameworks are leads that must be verified against target files.",
        ],
    }


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"observe_repo: target is not a directory: {target}", file=sys.stderr)
        return 2

    result = observe(target)
    indent = None if args.compact else 2
    payload = json.dumps(result, indent=indent, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
