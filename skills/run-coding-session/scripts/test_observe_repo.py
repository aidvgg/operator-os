#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("observe_repo.py")


class ObserveRepoTests(unittest.TestCase):
    def run_observer(self, target: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--target", str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        payload = json.loads(result.stdout) if result.stdout else {}
        return result, payload

    def test_existing_typescript_project_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            (target / "src").mkdir()
            (target / "tests").mkdir()
            (target / ".github" / "workflows").mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
            (target / "src" / "index.ts").write_text("export const answer = 42;\n", encoding="utf-8")
            (target / "tests" / "index.test.ts").write_text("// fixture\n", encoding="utf-8")
            (target / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            (target / "package.json").write_text(
                json.dumps(
                    {
                        "name": "fixture",
                        "scripts": {"test": "vitest", "check": "tsc --noEmit"},
                        "devDependencies": {"vitest": "1.0.0"},
                    }
                ),
                encoding="utf-8",
            )

            result, payload = self.run_observer(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(payload["mode_hint"], "existing")
            self.assertIn("AGENTS.md", payload["inventory"]["instruction_files"])
            self.assertIn("package.json", payload["inventory"]["manifests"])
            self.assertIn(".github/workflows/ci.yml", payload["inventory"]["ci_files"])
            self.assertEqual(payload["inventory"]["package"]["scripts"], ["check", "test"])
            self.assertIn("vitest", payload["inventory"]["package"]["framework_signals"])
            self.assertEqual(payload["inventory"]["test_file_count"], 1)

    def test_empty_directory_is_greenfield(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, payload = self.run_observer(Path(temporary))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(payload["mode_hint"], "greenfield")
            self.assertEqual(payload["inventory"]["total_files"], 0)

    def test_hidden_file_is_not_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            (target / ".private").write_text("secret\n", encoding="utf-8")
            (target / "README.md").write_text("# Fixture\n", encoding="utf-8")

            result, payload = self.run_observer(target)
            serialized = json.dumps(payload)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(".private", serialized)
            self.assertEqual(payload["mode_hint"], "ambiguous")

    def test_missing_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing"
            result = subprocess.run(
                ["python3", str(SCRIPT), "--target", str(missing)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("target is not a directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
