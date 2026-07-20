from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PROTOCOL_SCRIPT = REPOSITORY_ROOT / "scripts" / "route_canary_protocol.py"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from route_canary_protocol import COORDINATOR_ATTESTATION  # noqa: E402
from route_canary_protocol import PRIVATE_BINDING_PROTOCOL  # noqa: E402


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_plugin(root: Path, version: str) -> None:
    manifest = {
        "name": "project-delivery",
        "version": version,
        "description": "Fixture plugin for sealed coordinator tests.",
        "skills": "./skills",
        "interface": {
            "displayName": "Project Delivery",
            "category": "Developer Tools",
        },
    }
    write_json(root / ".codex-plugin" / "plugin.json", manifest)
    (root / "skills" / "delivery-orchestrator").mkdir(parents=True)
    (root / "skills" / "delivery-orchestrator" / "SKILL.md").write_text(
        """---
name: delivery-orchestrator
description: Route fixture delivery work.
---

## When to invoke

Use for fixture routes.

## Inputs and evidence

Read fixture facts.

## Workflow

Route fixture work.

## Outputs and handoff

Return fixture route.

## Completion evidence

Record fixture evidence.

## Must not

Do not fabricate fixture results.
""",
        encoding="utf-8",
    )
    (root / ".codexignore").write_text(".git\n.venv\n", encoding="utf-8")
    (root / "LICENSE").write_text("fixture license\n", encoding="utf-8")
    (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
    (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")


class CanaryFixture:
    def __init__(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repository = self.root / "source-repository"
        self.source = self.repository / "plugins" / "project-delivery"
        self.personal_root = self.root / "personal-marketplace"
        self.prepared = self.personal_root / "plugins" / "project-delivery"
        self.marketplace = self.personal_root / "marketplace.json"
        self.control = self.root / "control"
        self.prompt_manifest = self.control / "route-prompts.json"
        self.instruction_file = self.control / "AGENTS.md"
        self.task_prompt = self.control / "task-prompt.txt"
        self.launch = self.control / "launch.json"
        self.binding = self.control / "task-binding.json"
        self.observation = self.control / "raw-observation.bin"
        self.capture_output = self.control / "capture.json"
        self.source_version = "1.4.0-rc.1"
        self.prepared_version = "1.4.0-rc.1+codex.test-20260720"
        self.installed = (
            self.root
            / ".codex"
            / "plugins"
            / "cache"
            / "personal"
            / "project-delivery"
            / self.prepared_version
        )
        self.internal_task_id = "019f7fff-1111-7222-8333-123456789abc"
        self._build()

    def __enter__(self) -> CanaryFixture:
        return self

    def __exit__(self, *unused: object) -> None:
        self.temporary.cleanup()

    def _git(self, *arguments: str) -> None:
        subprocess.run(
            ["git", "-C", str(self.repository), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _build(self) -> None:
        self.repository.mkdir()
        self._git("init", "-b", "main")
        self._git("config", "user.name", "Canary Test")
        self._git("config", "user.email", "canary@example.invalid")
        make_plugin(self.source, self.source_version)
        self._git("add", ".")
        self._git("commit", "-m", "test: create canary fixture")

        shutil.copytree(self.source, self.prepared)
        prepared_manifest_path = self.prepared / ".codex-plugin" / "plugin.json"
        prepared_manifest = json.loads(prepared_manifest_path.read_text(encoding="utf-8"))
        prepared_manifest["version"] = self.prepared_version
        write_json(prepared_manifest_path, prepared_manifest)
        shutil.copytree(self.prepared, self.installed)

        write_json(
            self.marketplace,
            {
                "name": "personal",
                "interface": {"displayName": "Personal"},
                "plugins": [
                    {
                        "name": "project-delivery",
                        "source": {
                            "source": "local",
                            "path": "./plugins/project-delivery",
                        },
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Developer Tools",
                    }
                ],
            },
        )
        self.control.mkdir()
        self.prompt_manifest.write_bytes(
            b'{"schema_version":1,"source_contract_schema_version":3,'
            b'"evidence_class":"prompt-only blind canary input",'
            b'"scenarios":[{"id":"ROUTE-X","prompt":"Blind"}]}\n'
        )
        self.instruction_file.write_text(
            "# Projectless canary instructions\nUse only installed plugin skills.\n",
            encoding="utf-8",
        )
        self.observation.write_bytes(
            b"not JSON; intentionally opaque to coordinator\x00route decisions remain ungraded\n"
        )

    def command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(PROTOCOL_SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )

    def prepare(
        self,
        installed: Path | None = None,
        prepared: Path | None = None,
        marketplace: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return self.command(
            "prepare",
            "--repository-root",
            str(self.repository),
            "--prompt-manifest",
            str(self.prompt_manifest),
            "--source-package",
            str(self.source),
            "--prepared-source",
            str(prepared or self.prepared),
            "--installed-cache",
            str(installed or self.installed),
            "--marketplace",
            str(marketplace or self.marketplace),
            "--task-prompt-output",
            str(self.task_prompt),
            "--observation-mode",
            "projectless",
            "--instruction-file",
            str(self.instruction_file),
            "--output",
            str(self.launch),
        )

    def write_binding(self, **overrides: object) -> bytes:
        launch = json.loads(self.launch.read_text(encoding="utf-8"))
        binding = {
            "schema_version": 1,
            "protocol": PRIVATE_BINDING_PROTOCOL,
            "public_run_nonce": launch["public_run_nonce"],
            "public_receipt_slug": launch["public_receipt_slug"],
            "launch_state_sha256": sha256(self.launch.read_bytes()),
            "internal_task_id": self.internal_task_id,
            "task_created_at_utc": launch["launch_time_utc"],
            "task_prompt_sha256": launch["task_prompt"]["sha256"],
        }
        binding.update(overrides)
        write_json(self.binding, binding)
        self.binding.chmod(0o600)
        return self.binding.read_bytes()

    def capture(self) -> subprocess.CompletedProcess[str]:
        return self.command(
            "capture",
            "--launch-state",
            str(self.launch),
            "--expected-launch-sha256",
            sha256(self.launch.read_bytes()),
            "--observation",
            str(self.observation),
            "--task-binding",
            str(self.binding),
            "--output",
            str(self.capture_output),
        )


class RouteCanaryProtocolTests(unittest.TestCase):
    def test_prepare_and_capture_bind_exact_bytes_without_grading_semantics(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            launch = json.loads(fixture.launch.read_text(encoding="utf-8"))
            binding_bytes = fixture.write_binding()
            captured = fixture.capture()
            self.assertEqual(captured.returncode, 0, captured.stdout + captured.stderr)
            result = json.loads(fixture.capture_output.read_text(encoding="utf-8"))

            self.assertEqual(
                launch["prompt_manifest"]["sha256"],
                sha256(fixture.prompt_manifest.read_bytes()),
            )
            self.assertTrue(launch["source_git"]["clean"])
            self.assertEqual(launch["source_git"]["status_byte_count"], 0)
            self.assertEqual(
                launch["parity"]["source_to_prepared"]["mode"],
                "manifest-version-cachebuster-only",
            )
            self.assertEqual(
                launch["parity"]["prepared_to_installed"]["mode"],
                "exact-byte-parity",
            )
            self.assertEqual(
                launch["parity"]["source_to_installed"]["mode"],
                "manifest-version-cachebuster-only",
            )
            self.assertEqual(
                launch["plugin_identities"]["installed_cache"]["cache_relative_path"],
                f"plugins/cache/personal/project-delivery/{fixture.prepared_version}",
            )
            self.assertEqual(
                result["raw_observation"]["sha256"],
                sha256(fixture.observation.read_bytes()),
            )
            self.assertEqual(
                result["task_prompt"]["sha256"],
                sha256(fixture.task_prompt.read_bytes()),
            )
            self.assertIn(
                "project-delivery canonical blind route task prompt v1",
                fixture.task_prompt.read_text(encoding="utf-8"),
            )
            task_prompt_text = fixture.task_prompt.read_text(encoding="utf-8")
            for hidden_contract_field in (
                '"required_capabilities"',
                '"conditional_capabilities"',
                '"forbidden_capabilities"',
                '"precedence"',
                '"artifacts"',
            ):
                self.assertNotIn(hidden_contract_field, task_prompt_text)
            self.assertEqual(result["private_task_binding_sha256"], sha256(binding_bytes))
            self.assertEqual(result["coordinator_attestation"], COORDINATOR_ATTESTATION)
            rendered = fixture.capture_output.read_text(encoding="utf-8")
            self.assertNotIn(fixture.internal_task_id, rendered)
            self.assertNotIn(str(fixture.root), rendered)
            self.assertNotIn("task_binding", rendered.replace("private_task_binding_sha256", ""))
            self.assertEqual(
                result["observation_boundary"]["mode"], "projectless"
            )
            self.assertEqual(
                result["observation_boundary"]["instruction_files"][0]["sha256"],
                sha256(fixture.instruction_file.read_bytes()),
            )
            self.assertEqual(fixture.launch.stat().st_mode & 0o777, 0o600)
            self.assertIn(
                "Capture did not inspect or grade expected route semantics.",
                result["coordinator_attestation"]["bounded_limitations"],
            )

    def test_capture_rejects_prompt_manifest_changed_after_launch(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()
            fixture.prompt_manifest.write_bytes(b"changed prompt bytes\n")

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("launch state changed since prepare", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_capture_rejects_task_prompt_changed_after_launch(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()
            fixture.task_prompt.write_text(
                fixture.task_prompt.read_text(encoding="utf-8")
                + "\nHidden expected route.\n",
                encoding="utf-8",
            )

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("launch state changed since prepare: task_prompt", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_capture_rejects_wrong_externally_retained_launch_seal(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()

            captured = fixture.command(
                "capture",
                "--launch-state",
                str(fixture.launch),
                "--expected-launch-sha256",
                "0" * 64,
                "--observation",
                str(fixture.observation),
                "--task-binding",
                str(fixture.binding),
                "--output",
                str(fixture.capture_output),
            )

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("externally retained prepare seal", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_capture_rejects_dirty_source_git_state(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()
            (fixture.repository / "untracked-after-launch.txt").write_text(
                "dirty\n", encoding="utf-8"
            )

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("source Git worktree must be clean", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_capture_rejects_installed_payload_changed_after_launch(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()
            (fixture.installed / "README.md").write_text("tampered\n", encoding="utf-8")

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("prepared/installed parity failed", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_capture_rejects_nonprivate_or_mismatched_task_binding(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding(public_run_nonce="canary-" + "0" * 32)
            fixture.binding.chmod(0o644)

            exposed = fixture.capture()

            self.assertNotEqual(exposed.returncode, 0)
            self.assertIn("permissions must be owner-only", exposed.stderr)
            fixture.binding.chmod(0o600)
            mismatched = fixture.capture()
            self.assertNotEqual(mismatched.returncode, 0)
            self.assertIn("public_run_nonce does not match launch", mismatched.stderr)
            self.assertNotIn(fixture.internal_task_id, mismatched.stderr)
            fixture.binding.unlink()
            fixture.write_binding(task_prompt_sha256="0" * 64)
            wrong_prompt = fixture.capture()
            self.assertNotEqual(wrong_prompt.returncode, 0)
            self.assertIn("task prompt SHA-256 does not match", wrong_prompt.stderr)

    def test_prepare_rejects_non_cache_shaped_installed_tree(self) -> None:
        with CanaryFixture() as fixture:
            invalid_installed = (
                fixture.root / "cache" / "project-delivery" / fixture.prepared_version
            )
            shutil.copytree(fixture.prepared, invalid_installed)

            prepared = fixture.prepare(installed=invalid_installed)

            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("installed plugin path must end in plugins/cache", prepared.stderr)
            self.assertFalse(fixture.launch.exists())

    def test_prepare_rejects_noncanonical_cachebuster_manifest_serialization(self) -> None:
        with CanaryFixture() as fixture:
            manifest_path = fixture.prepared / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_path.write_text(
                json.dumps(manifest, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            shutil.rmtree(fixture.installed)
            shutil.copytree(fixture.prepared, fixture.installed)

            prepared = fixture.prepare()

            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn(
                "exact Plugin Creator cachebuster serialization", prepared.stderr
            )
            self.assertFalse(fixture.launch.exists())

    def test_capture_rejects_marketplace_entry_changed_after_launch(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()
            marketplace = json.loads(fixture.marketplace.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["category"] = "Changed"
            write_json(fixture.marketplace, marketplace)

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("launch state changed since prepare", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_prepare_resolves_plugin_creator_personal_marketplace_layout(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.root / "plugins" / "project-delivery"
            marketplace = fixture.root / ".agents" / "plugins" / "marketplace.json"
            shutil.copytree(fixture.prepared, prepared)
            marketplace.parent.mkdir(parents=True)
            shutil.copy2(fixture.marketplace, marketplace)

            result = fixture.prepare(prepared=prepared, marketplace=marketplace)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_capture_rejects_launch_older_than_six_hours(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            launch = json.loads(fixture.launch.read_text(encoding="utf-8"))
            launch["launch_time_utc"] = "2000-01-01T00:00:00Z"
            fixture.launch.unlink()
            write_json(fixture.launch, launch)
            fixture.launch.chmod(0o600)
            fixture.write_binding()

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("six-hour launch window", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_prepare_rejects_duplicate_prompt_manifest_key(self) -> None:
        with CanaryFixture() as fixture:
            fixture.prompt_manifest.write_bytes(
                b'{"schema_version":1,"source_contract_schema_version":3,'
                b'"evidence_class":"prompt-only blind canary input",'
                b'"scenarios":[{"id":"ROUTE-X","prompt":"Blind",'
                b'"prompt":"Shadowed"}]}\n'
            )

            prepared = fixture.prepare()

            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("prompt manifest contains duplicate JSON object key", prepared.stderr)
            self.assertIn("'prompt'", prepared.stderr)
            self.assertFalse(fixture.launch.exists())

    def test_prepare_rejects_duplicate_plugin_manifest_key(self) -> None:
        with CanaryFixture() as fixture:
            manifest_path = fixture.prepared / ".codex-plugin" / "plugin.json"
            original = manifest_path.read_text(encoding="utf-8")
            duplicate = original.replace(
                f'"version": "{fixture.prepared_version}"',
                f'"version": "{fixture.prepared_version}",\n'
                f'  "version": "{fixture.prepared_version}-shadow"',
                1,
            )
            self.assertNotEqual(original, duplicate)
            manifest_path.write_text(duplicate, encoding="utf-8")

            prepared = fixture.prepare()

            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("plugin manifest contains duplicate JSON object key", prepared.stderr)
            self.assertIn("'version'", prepared.stderr)
            self.assertFalse(fixture.launch.exists())

    def test_prepare_rejects_nested_duplicate_marketplace_key(self) -> None:
        with CanaryFixture() as fixture:
            original = fixture.marketplace.read_text(encoding="utf-8")
            duplicate = original.replace(
                '"path": "./plugins/project-delivery"',
                '"path": "./plugins/project-delivery",\n'
                '          "path": "./plugins/shadow"',
                1,
            )
            self.assertNotEqual(original, duplicate)
            fixture.marketplace.write_text(duplicate, encoding="utf-8")

            prepared = fixture.prepare()

            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("marketplace contains duplicate JSON object key", prepared.stderr)
            self.assertIn("'path'", prepared.stderr)
            self.assertFalse(fixture.launch.exists())

    def test_capture_rejects_duplicate_launch_state_key(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            original = fixture.launch.read_bytes()
            fixture.launch.write_bytes(
                b'{"schema_version":1,' + original.removeprefix(b"{")
            )

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn("launch state contains duplicate JSON object key", captured.stderr)
            self.assertIn("'schema_version'", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_capture_rejects_duplicate_private_binding_key(self) -> None:
        with CanaryFixture() as fixture:
            prepared = fixture.prepare()
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            fixture.write_binding()
            original = fixture.binding.read_bytes()
            fixture.binding.write_bytes(
                b'{"schema_version":1,' + original.removeprefix(b"{")
            )

            captured = fixture.capture()

            self.assertNotEqual(captured.returncode, 0)
            self.assertIn(
                "private task-binding contains duplicate JSON object key",
                captured.stderr,
            )
            self.assertIn("'schema_version'", captured.stderr)
            self.assertFalse(fixture.capture_output.exists())

    def test_prepare_rejects_final_symlink_control_inputs(self) -> None:
        for attribute in ("prompt_manifest", "marketplace", "instruction_file"):
            with self.subTest(attribute=attribute), CanaryFixture() as fixture:
                control_path = getattr(fixture, attribute)
                target = control_path.with_name(control_path.name + ".target")
                control_path.rename(target)
                control_path.symlink_to(target)

                prepared = fixture.prepare()

                self.assertNotEqual(prepared.returncode, 0)
                self.assertIn("regular non-symlink file", prepared.stderr)
                self.assertFalse(fixture.launch.exists())

    def test_capture_rejects_final_symlink_control_inputs(self) -> None:
        for attribute in ("launch", "binding", "observation"):
            with self.subTest(attribute=attribute), CanaryFixture() as fixture:
                prepared = fixture.prepare()
                self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
                fixture.write_binding()
                control_path = getattr(fixture, attribute)
                target = control_path.with_name(control_path.name + ".target")
                control_path.rename(target)
                control_path.symlink_to(target)

                captured = fixture.capture()

                self.assertNotEqual(captured.returncode, 0)
                self.assertIn("regular non-symlink file", captured.stderr)
                self.assertFalse(fixture.capture_output.exists())

    def test_prepare_rejects_nonregular_control_input(self) -> None:
        with CanaryFixture() as fixture:
            fixture.prompt_manifest.unlink()
            fixture.prompt_manifest.mkdir()

            prepared = fixture.prepare()

            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("prompt manifest must be a regular non-symlink file", prepared.stderr)
            self.assertFalse(fixture.launch.exists())


if __name__ == "__main__":
    unittest.main()
