from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_plugin.py"


def create_minimal_plugin(root: Path, name: str = "project-delivery", version: str = "1.3.0") -> None:
    (root / ".codex-plugin").mkdir(parents=True)
    (root / "skills" / "sample").mkdir(parents=True)
    manifest = {
        "name": name,
        "version": version,
        "description": "Test plugin",
        "author": {"name": "Test Author"},
        "interface": {
            "displayName": "Test Plugin",
            "shortDescription": "Test plugin structure",
        },
    }
    (root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    (root / "skills" / "sample" / "SKILL.md").write_text(
        "---\n"
        "name: sample\n"
        "description: A sample skill used by validator tests.\n"
        "---\n\n"
        "# Sample\n\n"
        "## When to invoke\n\nFor validation.\n\n"
        "## Inputs and evidence\n\nA fixture.\n\n"
        "## Workflow\n\nValidate it.\n\n"
        "## Outputs and handoff\n\nA result.\n\n"
        "## Completion evidence\n\nThe result.\n\n"
        "## Must not\n\nInvent evidence.\n",
        encoding="utf-8",
    )
    for relative in (".codexignore", "LICENSE", "README.md", "SECURITY.md"):
        (root / relative).write_text(f"fixture: {relative}\n", encoding="utf-8")


def run_checker(root: Path, layout: str = "auto") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root), "--layout", layout],
        check=False,
        capture_output=True,
        text=True,
    )


class PluginCheckerTests(unittest.TestCase):
    def test_source_layout_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            result = run_checker(root, "source")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_versioned_cache_layout_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery" / "1.3.0+codex.test"
            create_minimal_plugin(root, version="1.3.0+codex.test")
            result = run_checker(root, "cache")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_wrong_source_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "wrong-name"
            create_minimal_plugin(root)
            result = run_checker(root, "source")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("plugin path must be", result.stdout)

    def test_malformed_manifest_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            (root / ".codex-plugin").mkdir(parents=True)
            (root / ".codex-plugin" / "plugin.json").write_text("{", encoding="utf-8")
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid manifest", result.stdout)

    def test_missing_skills_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            skill = root / "skills" / "sample" / "SKILL.md"
            skill.unlink()
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no skills found", result.stdout)

    def test_incomplete_skill_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            skill = root / "skills" / "sample" / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8").replace(
                    "## Completion evidence", "## Completion proof"
                ),
                encoding="utf-8",
            )
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing skill contract section", result.stdout)

    def test_missing_required_release_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project-delivery"
            create_minimal_plugin(root)
            (root / ".codexignore").unlink()
            result = run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required release file", result.stdout)


if __name__ == "__main__":
    unittest.main()
