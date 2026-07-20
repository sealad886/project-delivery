from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
CHECKER = REPOSITORY_ROOT / "scripts" / "check_installed_parity.py"


def make_installed_cache(temporary: str) -> Path:
    version = json.loads(
        (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )["version"]
    installed = Path(temporary) / "cache" / "project-delivery" / version
    shutil.copytree(PLUGIN_ROOT, installed)
    return installed


def run_checker(installed: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(PLUGIN_ROOT), str(installed)],
        check=False,
        capture_output=True,
        text=True,
    )


class InstalledParityTests(unittest.TestCase):
    def test_exact_copy_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installed = make_installed_cache(temporary)
            result = run_checker(installed)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("exact_source_cache_parity=true", result.stdout)

    def test_extra_installed_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installed = make_installed_cache(temporary)
            (installed / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
            result = run_checker(installed)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("installed cache contains extra file", result.stdout)

    def test_extra_empty_installed_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installed = make_installed_cache(temporary)
            (installed / "scratch").mkdir()

            result = run_checker(installed)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("installed cache contains extra directory: scratch", result.stdout)

    def test_empty_forbidden_installed_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installed = make_installed_cache(temporary)
            (installed / "tests").mkdir()

            result = run_checker(installed)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("installed contains forbidden path: tests", result.stdout)


if __name__ == "__main__":
    unittest.main()
