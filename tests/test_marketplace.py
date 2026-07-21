from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_marketplace.py"


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


class MarketplaceTests(unittest.TestCase):
    def test_repository_marketplace_and_license_parity_pass(self) -> None:
        result = run_checker(REPOSITORY_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("license_parity=true", result.stdout)

    def test_marketplace_path_escape_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            (root / ".agents" / "plugins").mkdir(parents=True)
            shutil.copytree(
                REPOSITORY_ROOT / "plugins" / "project-delivery",
                root / "plugins" / "project-delivery",
            )
            shutil.copy2(REPOSITORY_ROOT / "LICENSE", root / "LICENSE")
            marketplace = json.loads(
                (REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                    encoding="utf-8"
                )
            )
            marketplace["plugins"][0]["source"]["path"] = "../../outside"
            (root / ".agents" / "plugins" / "marketplace.json").write_text(
                json.dumps(marketplace),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("escapes the repository", result.stdout)

    def test_mutable_marketplace_ref_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            (root / ".agents" / "plugins").mkdir(parents=True)
            shutil.copytree(
                REPOSITORY_ROOT / "plugins" / "project-delivery",
                root / "plugins" / "project-delivery",
            )
            shutil.copy2(REPOSITORY_ROOT / "LICENSE", root / "LICENSE")
            marketplace = json.loads(
                (REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                    encoding="utf-8"
                )
            )
            marketplace["plugins"][0]["source"]["ref"] = "main"
            (root / ".agents" / "plugins" / "marketplace.json").write_text(
                json.dumps(marketplace),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be immutable release 'v1.4.0'", result.stdout)

    def test_wrong_marketplace_repository_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            (root / ".agents" / "plugins").mkdir(parents=True)
            shutil.copytree(
                REPOSITORY_ROOT / "plugins" / "project-delivery",
                root / "plugins" / "project-delivery",
            )
            shutil.copy2(REPOSITORY_ROOT / "LICENSE", root / "LICENSE")
            marketplace = json.loads(
                (REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                    encoding="utf-8"
                )
            )
            marketplace["plugins"][0]["source"]["url"] = (
                "https://github.com/example/project-delivery.git"
            )
            (root / ".agents" / "plugins" / "marketplace.json").write_text(
                json.dumps(marketplace),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source.url must be", result.stdout)

    def test_additional_marketplace_entry_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            (root / ".agents" / "plugins").mkdir(parents=True)
            shutil.copytree(
                REPOSITORY_ROOT / "plugins" / "project-delivery",
                root / "plugins" / "project-delivery",
            )
            shutil.copy2(REPOSITORY_ROOT / "LICENSE", root / "LICENSE")
            marketplace = json.loads(
                (REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                    encoding="utf-8"
                )
            )
            marketplace["plugins"].append(
                {
                    "name": "unexpected",
                    "source": {"source": "local", "path": "./plugins/unexpected"},
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Developer Tools",
                }
            )
            (root / ".agents" / "plugins" / "marketplace.json").write_text(
                json.dumps(marketplace),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must contain exactly one entry", result.stdout)


if __name__ == "__main__":
    unittest.main()
