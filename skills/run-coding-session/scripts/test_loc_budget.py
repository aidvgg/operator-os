#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("loc_budget.py")


def lines(count: int, prefix: str = "value") -> str:
    return "".join(f"{prefix}_{index} = {index}\n" for index in range(count))


class LocBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        self.repo.mkdir()
        self.env = {**os.environ, "LOC_BUDGET_STATE": str(Path(self.temporary.name) / "state"), "LOC_BUDGET": "300"}
        for args in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            self.git(*args)
        self.write("src/old.py", lines(150, "old"))
        self.git("add", "src/old.py")
        self.git("commit", "-qm", "base")
        self.write("scratch.py", lines(500, "preexisting"))  # user-owned dirt before the session

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)

    def write(self, rel: str, text: str) -> None:
        (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / rel).write_text(text)

    def run_script(self, *args: str, event: dict | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            input=json.dumps(event) if event else None,
            capture_output=True, text=True, env=self.env, cwd=self.repo, check=False,
        )

    def hook(self, name: str, host: str = "claude", **fields) -> dict:
        event = {"session_id": "s1", "hook_event_name": name, "cwd": str(self.repo), **fields}
        result = self.run_script("hook", host, event=event)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def edit(self, rel: str, text: str) -> None:
        self.hook("PreToolUse", tool_name="Write", tool_input={"file_path": str(self.repo / rel)})
        self.write(rel, text)

    def test_net_growth_blocks_until_deletion_pays_for_it(self) -> None:
        self.hook("SessionStart", source="startup")
        self.edit("src/feature.py", lines(350))
        blocked = self.hook("Stop")
        self.assertEqual(blocked["decision"], "block")
        self.assertIn("ΔLOC +350", blocked["reason"])
        self.assertNotIn("scratch.py", blocked["reason"])
        self.git("add", "src/feature.py")
        self.git("commit", "-qm", "mid-session commit does not reset the budget")
        self.assertEqual(self.hook("Stop")["decision"], "block")
        self.edit("src/old.py", lines(90, "old"))
        self.assertEqual(self.hook("Stop"), {})

    def test_forced_passes_are_capped_then_handed_to_user(self) -> None:
        self.hook("SessionStart", source="startup")
        self.edit("src/feature.py", lines(400))
        self.assertEqual(self.hook("Stop")["decision"], "block")
        self.assertEqual(self.hook("Stop", stop_hook_active=True)["decision"], "block")
        self.assertIn("systemMessage", self.hook("Stop", stop_hook_active=True))
        self.assertEqual(self.run_script("set", "500").returncode, 0)
        self.assertEqual(self.hook("Stop"), {})

    def test_untouched_repo_tests_and_markers(self) -> None:
        self.hook("SessionStart", source="startup")
        self.write("src/parallel_session.py", lines(400))
        self.assertEqual(self.hook("Stop"), {})  # a Claude session that edited nothing here
        self.assertEqual(self.hook("Stop", host="codex")["decision"], "block")
        self.hook("SessionStart", source="clear")
        self.edit("tests/test_feature.py", lines(400))
        self.assertEqual(self.hook("Stop"), {})
        self.edit("src/old.py", lines(150, "old") + "# TO" + "DO finish later\n")
        self.assertIn("placeholder markers +1", self.hook("Stop")["reason"])

    def test_check_against_head_without_session(self) -> None:
        self.assertEqual(self.run_script("check").returncode, 1)  # the 500-line untracked file
        (self.repo / "scratch.py").unlink()
        self.git("mv", "src/old.py", "src/moved.py")  # a staged rename is not growth
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("ΔLOC +0", result.stdout)
        self.assertIn("measured against HEAD", result.stdout)


if __name__ == "__main__":
    unittest.main()
