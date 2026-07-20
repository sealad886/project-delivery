from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from check_distribution_bundle import payload_sha256, select_paths  # noqa: E402
from check_route_receipts import fresh_observation_sha256  # noqa: E402
from route_canary_protocol import CAPTURE_EVIDENCE_CLASS  # noqa: E402
from route_canary_protocol import COORDINATOR_ATTESTATION  # noqa: E402
from route_canary_protocol import PROTOCOL as COORDINATOR_PROTOCOL  # noqa: E402
from route_canary_protocol import RAW_HASH_METHOD  # noqa: E402
from route_canary_protocol import TASK_PROMPT_PROTOCOL  # noqa: E402
from route_canary_protocol import render_task_prompt  # noqa: E402


CHECKER = SCRIPTS_ROOT / "check_route_receipts.py"
SOURCE_REVISION = "0123456789abcdef0123456789abcdef01234567"
SHARED_REFERENCE = re.compile(r"`(\.\./\.shared/[a-z0-9._-]+\.(?:json|md))`")


def load_contracts() -> dict[str, object]:
    return json.loads(
        (REPOSITORY_ROOT / "tests" / "route-contracts.json").read_text(
            encoding="utf-8"
        )
    )


def contract_by_id(scenario_id: str) -> dict[str, object]:
    return next(
        item for item in load_contracts()["scenarios"] if item["id"] == scenario_id
    )


def synthetic_route(contract: dict[str, object]) -> list[str]:
    required = list(contract["required_capabilities"])
    edges = [
        (before, after)
        for before, after in contract["precedence"]
        if before in required and after in required
    ]
    remaining = list(required)
    route: list[str] = []
    while remaining:
        eligible = [
            skill
            for skill in remaining
            if all(before in route for before, after in edges if after == skill)
        ]
        assert eligible, f"cyclic synthetic route: {contract['id']}"
        selected = eligible[0]
        remaining.remove(selected)
        route.append(selected)
    for controller in contract.get("required_reentry", []):
        owners = contract.get("required_reentry_after", {}).get(controller, [])
        if any(owner in route for owner in owners):
            route.append(controller)
    for controller, owners in contract.get("required_final_after", {}).items():
        selected_owners = [owner for owner in owners if owner in route]
        if controller in route and selected_owners:
            controller_last = max(
                index for index, skill in enumerate(route) if skill == controller
            )
            owner_last = max(
                max(index for index, skill in enumerate(route) if skill == owner)
                for owner in selected_owners
            )
            if controller_last <= owner_last:
                route.append(controller)
    return route


def synthetic_scenario(contract: dict[str, object]) -> dict[str, object]:
    scenario_id = contract["id"]
    meaningful_outcome = scenario_id in {"ROUTE-010", "ROUTE-015", "ROUTE-018"}
    route = synthetic_route(contract)
    dispositions: dict[str, dict[str, object]] = {}
    for conditional in contract["conditional_capabilities"]:
        skill = conditional["skill"]
        if skill == "retrospective-improvement":
            if meaningful_outcome:
                state = "activated"
                trigger_result = "met"
                route.append(skill)
            else:
                state = "planned-future"
                trigger_result = "future-pending"
        else:
            state = "not-applicable"
            trigger_result = "not-met"
        dispositions[skill] = {
            "state": state,
            "trigger_evaluation": {
                "trigger_statement": conditional["when"],
                "source": "installed-runtime",
                "result": trigger_result,
            },
            "rationale": (
                "The structured synthetic evidence records this exact trigger disposition."
            ),
            "evidence": ["Synthetic prompt and installed-runtime observation evidence."],
        }
    return {
        "id": scenario_id,
        "prompt": contract["prompt"],
        "scale": contract["scale"],
        "risk": contract["risk"],
        "authority": contract["authority"],
        "taxonomy_rationale": (
            "Synthetic classification evidence exercises the sealed schema without "
            "claiming fresh model behavior."
        ),
        "taxonomy_evidence": ["Synthetic prompt taxonomy evidence."],
        "actual_route": route,
        "conditional_dispositions": dispositions,
        "extra_capability_justifications": {},
        "delivery_result": "not-run",
        "evidence": ["Synthetic route-only observation; no delivery work was run."],
        "gaps": [],
        "outcome_observation": {
            "state": (
                "meaningful-outcome-observed"
                if meaningful_outcome
                else "no-meaningful-outcome-observed"
            ),
            "evidence": [
                (
                    (
                        "The prompt explicitly identifies a completed delivery outcome."
                        if scenario_id == "ROUTE-018"
                        else "The prompt identifies an incident or failed staged deployment."
                    )
                    if meaningful_outcome
                    else "The prompt does not establish a completed delivery outcome."
                )
            ],
        },
        "scenario_observation": {
            "observation_scope": "route-only-no-effects",
            "effects_performed": [],
            "legacy_administrative_visibility": [],
            "legacy_invocations": [],
            "legacy_runtime_events": [],
            "legacy_branded_state_created": [],
        },
    }


def instruction_closure(installed_root: Path, skill: str) -> dict[str, object]:
    skill_relative = Path("skills") / skill / "SKILL.md"
    skill_path = installed_root / skill_relative
    references = {
        (skill_path.parent / reference).resolve().relative_to(
            installed_root.resolve()
        ).as_posix()
        for reference in SHARED_REFERENCE.findall(
            skill_path.read_text(encoding="utf-8")
        )
    }
    paths = {skill_relative.as_posix(), *references}
    files = []
    for relative in sorted(paths):
        files.append(
            {
                "relative_path": relative,
                "role": (
                    "skill-root"
                    if relative == skill_relative.as_posix()
                    else "required-reference"
                ),
                "sha256": hashlib.sha256(
                    (installed_root / relative).read_bytes()
                ).hexdigest(),
                "state": "read-completely-before-route-freeze",
            }
        )
    skill_sha = hashlib.sha256(skill_path.read_bytes()).hexdigest()
    return {
        "skill": skill,
        "relative_path": skill_relative.as_posix(),
        "state": "loaded",
        "skill_sha256": skill_sha,
        "instruction_closure": {
            "state": "complete",
            "files": files,
            "unresolved_references": [],
        },
    }


def make_receipt(installed_root: Path) -> dict[str, object]:
    contracts = load_contracts()
    scenarios = [synthetic_scenario(contract) for contract in contracts["scenarios"]]
    selected_skills = sorted(
        {
            skill
            for scenario in scenarios
            for skill in scenario["actual_route"]
        }
    )
    manifest_path = installed_root / ".codex-plugin" / "plugin.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    receipt: dict[str, object] = {
        "schema_version": 3,
        "contract_schema_version": contracts["schema_version"],
        "evidence_class": "fresh-task semantic route observation",
        "semantic_fields_were_frozen_before_contract_comparison": True,
        "semantic_freeze_scope": [
            "actual_route",
            "authority",
            "conditional_dispositions",
            "evidence",
            "extra_capability_justifications",
            "gaps",
            "outcome_observation",
            "risk",
            "scale",
            "scenario_observation",
            "taxonomy_evidence",
            "taxonomy_rationale",
        ],
        "semantic_freeze_evidence": [
            "Synthetic sealed-schema fixture fixes the full semantic record before comparison."
        ],
        "annotation_provenance": {
            "semantic_fields_origin": "blind-before-contract-comparison",
            "contract_access": "after-capture-only",
            "post_freeze_enrichment_fields": [
                "plugin_identity",
                "repository_identity",
                "task_identity.public_receipt_id",
                "task_identity.selected_at",
                "task_identity.source_observation_sha256",
            ],
            "semantic_fields_revised_after_comparison": False,
        },
        "plugin_identity": {
            "name": manifest["name"],
            "installed_version": manifest["version"],
            "source_revision": SOURCE_REVISION,
            "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "payload_sha256": payload_sha256(
                installed_root, sorted(select_paths(installed_root))
            ),
            "payload_hash_method": (
                "project-delivery length-prefixed path-and-content sha256 v1"
            ),
            "cache_relative_path": (
                "plugins/cache/test/project-delivery/" + manifest["version"]
            ),
        },
        "task_identity": {
            "public_receipt_id": "route-canary-20260720t120000z-0123456789ab",
            "selected_at": "2026-07-20T12:00:00Z",
            "source_observation_sha256": "0" * 64,
        },
        "repository_identity": {
            "name": "projectless-canary",
            "revision": "not-applicable",
            "working_tree_state": "no-repository",
            "instructions_evidence": (
                "Synthetic fixture uses only the installed plugin instruction closure."
            ),
        },
        "observation_scope": "route-only-no-effects",
        "effects_performed": [],
        "legacy_administrative_visibility": [],
        "legacy_invocations": [],
        "legacy_runtime_events": [],
        "legacy_branded_state_created": [],
        "loaded_specialists": [
            instruction_closure(installed_root, skill) for skill in selected_skills
        ],
        "scenarios": scenarios,
    }
    receipt["task_identity"]["source_observation_sha256"] = (
        fresh_observation_sha256(receipt)
    )
    return receipt


def refresh_digest(receipt: dict[str, object]) -> None:
    receipt["task_identity"]["source_observation_sha256"] = (
        fresh_observation_sha256(receipt)
    )


def find_scenario(receipt: dict[str, object], scenario_id: str) -> dict[str, object]:
    return next(item for item in receipt["scenarios"] if item["id"] == scenario_id)


def assert_safe_failure_grade(
    testcase: unittest.TestCase,
    grade: dict[str, object],
) -> None:
    testcase.assertEqual(grade["verdict"], "FAIL")
    testcase.assertEqual(grade["candidate_proof"], "not-established")
    testcase.assertIsInstance(grade["error_count"], int)
    testcase.assertGreater(grade["error_count"], 0)
    testcase.assertEqual(len(grade["errors"]), grade["error_count"])
    testcase.assertRegex(grade["error_set_sha256"], r"^[0-9a-f]{64}$")
    for index, error in enumerate(grade["errors"], 1):
        testcase.assertRegex(
            error,
            rf"^validation-error-{index:03d} sha256=[0-9a-f]{{64}}$",
        )


def run_checker(
    receipt: dict[str, object],
    installed_root: Path,
    *,
    refresh: bool = True,
) -> subprocess.CompletedProcess[str]:
    if refresh:
        refresh_digest(receipt)
    receipt_path = installed_root.parents[4] / "receipt.json"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            str(receipt_path),
            "--root",
            str(REPOSITORY_ROOT),
            "--installed-plugin-root",
            str(installed_root),
            "--expected-source-revision",
            SOURCE_REVISION,
            "--allow-unattested-v3",
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def directory_count(selected: list[Path]) -> int:
    directories: set[Path] = set()
    for relative in selected:
        parent = relative.parent
        while parent != Path("."):
            directories.add(parent)
            parent = parent.parent
    return len(directories)


def package_identity(plugin_root: Path) -> dict[str, object]:
    selected = sorted(select_paths(plugin_root))
    manifest_raw = (plugin_root / ".codex-plugin" / "plugin.json").read_bytes()
    manifest = json.loads(manifest_raw.decode("utf-8"))
    return {
        "name": manifest["name"],
        "version": manifest["version"],
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "file_count": len(selected),
        "directory_count": directory_count(selected),
        "payload_sha256": payload_sha256(plugin_root, selected),
        "payload_hash_method": (
            "project-delivery length-prefixed path-and-content sha256 v1"
        ),
    }


def run_attested_checker(
    receipt: dict[str, object],
    installed_root: Path,
    *,
    mutate_attestation: object | None = None,
    mutate_attestation_bytes: object | None = None,
    mutate_prompt_bytes: object | None = None,
    mutate_receipt_bytes: object | None = None,
    expected_attestation_sha256: str | None = None,
    expected_source_revision: str | None = None,
    receipt_symlink: bool = False,
    attestation_symlink: bool = False,
    grade_parent_symlink: bool = False,
    task_prompt_suffix: bytes = b"",
) -> tuple[subprocess.CompletedProcess[str], Path, Path, Path]:
    refresh_digest(receipt)
    control_root = installed_root.parents[4]
    grader_root = control_root / "grader-source"
    source_revision = subprocess.run(
        ["git", "-C", str(grader_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    claimed_revision = expected_source_revision or source_revision
    receipt["plugin_identity"]["source_revision"] = claimed_revision
    refresh_digest(receipt)
    receipt_path = control_root / "attested-receipt.json"
    prompt_path = control_root / "attested-prompts.json"
    attestation_path = control_root / "attestation.json"
    task_prompt_path = control_root / "task-prompt.txt"
    grade_path = control_root / "grade.json"
    for path in (
        receipt_path,
        prompt_path,
        attestation_path,
        task_prompt_path,
        grade_path,
    ):
        if path.exists() or path.is_symlink():
            path.unlink()
    receipt_bytes = (json.dumps(receipt, indent=2) + "\n").encode("utf-8")
    if callable(mutate_receipt_bytes):
        receipt_bytes = mutate_receipt_bytes(receipt_bytes)
    if receipt_symlink:
        receipt_target = control_root / "attested-receipt-target.json"
        receipt_target.write_bytes(receipt_bytes)
        receipt_path.symlink_to(receipt_target)
    else:
        receipt_path.write_bytes(receipt_bytes)
    prompt = {
        "schema_version": 1,
        "source_contract_schema_version": 3,
        "evidence_class": "prompt-only blind canary input",
        "scenarios": [
            {"id": item["id"], "prompt": item["prompt"]}
            for item in receipt["scenarios"]
        ],
    }
    prompt_bytes = (json.dumps(prompt, indent=2) + "\n").encode("utf-8")
    task_prompt_source_bytes = prompt_bytes
    if callable(mutate_prompt_bytes):
        prompt_bytes = mutate_prompt_bytes(prompt_bytes)
    prompt_path.write_bytes(prompt_bytes)

    plugin_identity = receipt["plugin_identity"]
    source_identity = package_identity(grader_root / "plugins" / "project-delivery")
    installed_package_identity = package_identity(installed_root)
    relation_mode = (
        "exact-byte-parity"
        if source_identity["payload_sha256"]
        == installed_package_identity["payload_sha256"]
        else "manifest-version-cachebuster-only"
    )
    identities = {
        "source_package": copy.deepcopy(source_identity),
        "prepared_personal_source": copy.deepcopy(installed_package_identity),
        "installed_cache": {
            **copy.deepcopy(installed_package_identity),
            "marketplace": "test",
            "cache_relative_path": plugin_identity["cache_relative_path"],
        },
    }
    source_to_prepared = {
        "mode": relation_mode,
        "file_count": source_identity["file_count"],
        "source_payload_sha256": source_identity["payload_sha256"],
        "prepared_payload_sha256": installed_package_identity["payload_sha256"],
    }
    source_to_installed = {
        "mode": relation_mode,
        "file_count": source_identity["file_count"],
        "source_payload_sha256": source_identity["payload_sha256"],
        "installed_payload_sha256": installed_package_identity["payload_sha256"],
    }
    if relation_mode == "manifest-version-cachebuster-only":
        source_to_prepared.update(
            {
                "source_version": source_identity["version"],
                "prepared_version": installed_package_identity["version"],
            }
        )
        source_to_installed.update(
            {
                "source_version": source_identity["version"],
                "installed_version": installed_package_identity["version"],
            }
        )
    capture: dict[str, object] = {
        "schema_version": 1,
        "protocol": COORDINATOR_PROTOCOL,
        "evidence_class": CAPTURE_EVIDENCE_CLASS,
        "launch_time_utc": "2026-07-20T12:00:00Z",
        "captured_at_utc": "2026-07-20T12:05:00Z",
        "public_run_nonce": "canary-0123456789abcdef0123456789abcdef",
        "public_receipt_slug": "route-canary-20260720t120000z-0123456789ab",
        "launch_state_sha256": "1" * 64,
        "prompt_manifest": {
            "sha256": hashlib.sha256(prompt_bytes).hexdigest(),
            "byte_count": len(prompt_bytes),
            "hash_method": RAW_HASH_METHOD,
        },
        "source_git": {
            "head": source_revision,
            "status_format": (
                "git status --porcelain=v1 -z --untracked-files=all "
                "--ignore-submodules=none"
            ),
            "status_sha256": hashlib.sha256(b"").hexdigest(),
            "status_byte_count": 0,
            "clean": True,
        },
        "plugin_identities": identities,
        "parity": {
            "source_to_prepared": {
                **source_to_prepared,
            },
            "prepared_to_installed": {
                "mode": "exact-byte-parity",
                "file_count": installed_package_identity["file_count"],
                "payload_sha256": installed_package_identity["payload_sha256"],
            },
            "source_to_installed": {
                **source_to_installed,
            },
        },
        "marketplace_entry": {
            "file_sha256": "2" * 64,
            "marketplace_name": "test",
            "plugin_name": "project-delivery",
            "entry_sha256": "3" * 64,
            "entry_hash_method": "sha256 of canonical sorted compact JSON",
            "source_type": "local",
            "source_path": "./plugins/project-delivery",
            "target_payload_sha256": installed_package_identity["payload_sha256"],
        },
        "observation_boundary": {
            "mode": "projectless",
            "repository_name": "not-applicable",
            "revision": "not-applicable",
            "working_tree_state": "no-repository",
            "instruction_files": [
                {
                    "label": "instruction-1-AGENTS.md",
                    "sha256": "4" * 64,
                    "byte_count": 128,
                    "hash_method": RAW_HASH_METHOD,
                }
            ],
        },
        "private_task_binding_sha256": "5" * 64,
        "raw_observation": {
            "sha256": hashlib.sha256(receipt_bytes).hexdigest(),
            "byte_count": len(receipt_bytes),
            "hash_method": RAW_HASH_METHOD,
        },
        "coordinator_attestation": COORDINATOR_ATTESTATION,
    }
    task_prompt_bytes = render_task_prompt(
        task_prompt_source_bytes,
        capture["public_run_nonce"],
        capture["public_receipt_slug"],
        capture["source_git"],
        identities["installed_cache"],
    ) + task_prompt_suffix
    task_prompt_path.write_bytes(task_prompt_bytes)
    capture["task_prompt"] = {
        "sha256": hashlib.sha256(task_prompt_bytes).hexdigest(),
        "byte_count": len(task_prompt_bytes),
        "hash_method": RAW_HASH_METHOD,
        "prompt_protocol": TASK_PROMPT_PROTOCOL,
    }
    if callable(mutate_attestation):
        mutate_attestation(capture)
    attestation_bytes = (json.dumps(capture, indent=2) + "\n").encode("utf-8")
    if callable(mutate_attestation_bytes):
        attestation_bytes = mutate_attestation_bytes(attestation_bytes)
    if attestation_symlink:
        attestation_target = control_root / "attestation-target.json"
        attestation_target.write_bytes(attestation_bytes)
        attestation_path.symlink_to(attestation_target)
    else:
        attestation_path.write_bytes(attestation_bytes)
    expected_sha = expected_attestation_sha256 or hashlib.sha256(
        attestation_bytes
    ).hexdigest()
    if grade_parent_symlink:
        grade_real_parent = control_root / "grade-real-parent"
        grade_real_parent.mkdir(exist_ok=True)
        grade_link_parent = control_root / "grade-link-parent"
        if grade_link_parent.exists() or grade_link_parent.is_symlink():
            grade_link_parent.unlink()
        grade_link_parent.symlink_to(grade_real_parent, target_is_directory=True)
        grade_path = grade_link_parent / "grade.json"
    result = subprocess.run(
        [
            sys.executable,
            str(grader_root / "scripts" / "check_route_receipts.py"),
            str(receipt_path),
            "--root",
            str(grader_root),
            "--installed-plugin-root",
            str(installed_root),
            "--expected-source-revision",
            claimed_revision,
            "--coordinator-attestation",
            str(attestation_path),
            "--expected-attestation-sha256",
            expected_sha,
            "--prompt-manifest",
            str(prompt_path),
            "--task-prompt",
            str(task_prompt_path),
            "--grade-output",
            str(grade_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return result, receipt_path, attestation_path, grade_path


class SealedRouteSemanticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        temporary_root = Path(self.temporary.name)
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.installed_root = (
            temporary_root
            / "plugins"
            / "cache"
            / "test"
            / "project-delivery"
            / manifest["version"]
        )
        shutil.copytree(PLUGIN_ROOT, self.installed_root)
        self.grader_root = temporary_root / "grader-source"
        shutil.copytree(
            SCRIPTS_ROOT,
            self.grader_root / "scripts",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        (self.grader_root / "tests" / "fixtures").mkdir(parents=True)
        shutil.copy2(
            REPOSITORY_ROOT / "tests" / "route-contracts.json",
            self.grader_root / "tests" / "route-contracts.json",
        )
        shutil.copy2(
            REPOSITORY_ROOT
            / "tests"
            / "fixtures"
            / "route-contracts-v2.legacy.json",
            self.grader_root
            / "tests"
            / "fixtures"
            / "route-contracts-v2.legacy.json",
        )
        shutil.copytree(
            PLUGIN_ROOT,
            self.grader_root / "plugins" / "project-delivery",
        )
        shutil.copy2(
            REPOSITORY_ROOT / ".gitignore",
            self.grader_root / ".gitignore",
        )
        for command in (
            ["git", "init", "-q"],
            ["git", "config", "user.name", "Project Delivery Tests"],
            ["git", "config", "user.email", "tests@example.invalid"],
            [
                "git",
                "add",
                "-f",
                "--",
                ".gitignore",
                "plugins",
                "scripts",
                "tests",
            ],
            ["git", "commit", "-q", "-m", "test: freeze grader source"],
        ):
            subprocess.run(
                command,
                cwd=self.grader_root,
                check=True,
                capture_output=True,
            )
        self.receipt = make_receipt(self.installed_root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_schema_v3_route_matrix_passes_as_structured_but_unattested(self) -> None:
        result = run_checker(self.receipt, self.installed_root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            f"route_policy_records={len(load_contracts()['scenarios'])}", result.stdout
        )
        self.assertIn("candidate_proof=requires-coordinator-attestation", result.stdout)

    def test_three_record_binding_establishes_bounded_candidate_proof(self) -> None:
        result, receipt_path, attestation_path, grade_path = run_attested_checker(
            self.receipt, self.installed_root
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("candidate_proof=established-for-route-policy-only", result.stdout)
        self.assertIn("evidence_profile=sealed-three-record", result.stdout)
        grade = json.loads(grade_path.read_text(encoding="utf-8"))
        self.assertEqual(grade["verdict"], "PASS")
        self.assertEqual(grade["scenario_count"], len(load_contracts()["scenarios"]))
        self.assertEqual(
            grade["raw_observation_sha256"],
            hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            grade["coordinator_attestation_sha256"],
            hashlib.sha256(attestation_path.read_bytes()).hexdigest(),
        )

    def test_three_record_binding_rejects_receipt_byte_mismatch(self) -> None:
        def mutate(capture: dict[str, object]) -> None:
            capture["raw_observation"]["sha256"] = "0" * 64

        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt,
            self.installed_root,
            mutate_attestation=mutate,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("raw observation SHA-256 does not match", result.stdout)
        grade = json.loads(grade_path.read_text(encoding="utf-8"))
        assert_safe_failure_grade(self, grade)
        self.assertNotIn("raw observation", " ".join(grade["errors"]))

    def test_three_record_binding_rejects_unretained_attestation_bytes(self) -> None:
        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt,
            self.installed_root,
            expected_attestation_sha256="0" * 64,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("externally retained SHA-256", result.stdout)
        grade = json.loads(grade_path.read_text(encoding="utf-8"))
        assert_safe_failure_grade(self, grade)
        self.assertNotIn("externally retained", " ".join(grade["errors"]))

    def test_three_record_binding_rejects_noncanonical_task_wrapper(self) -> None:
        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt,
            self.installed_root,
            task_prompt_suffix=b"\nHidden expected route: implementation-execution\n",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("do not match the canonical blind prompt", result.stdout)
        grade = json.loads(grade_path.read_text(encoding="utf-8"))
        assert_safe_failure_grade(self, grade)
        self.assertNotIn("canonical blind prompt", " ".join(grade["errors"]))

    def test_expected_commit_bytes_are_bound_to_installed_payload(self) -> None:
        license_path = self.installed_root / "LICENSE"
        license_path.write_bytes(license_path.read_bytes() + b"\nsynthetic mutation\n")
        mutated_identity = package_identity(self.installed_root)
        self.receipt["plugin_identity"]["payload_sha256"] = mutated_identity[
            "payload_sha256"
        ]

        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt, self.installed_root
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("differs from the expected source commit outside", result.stdout)
        assert_safe_failure_grade(
            self, json.loads(grade_path.read_text(encoding="utf-8"))
        )

    def test_canonical_plugin_creator_cachebuster_is_the_only_allowed_transform(
        self,
    ) -> None:
        manifest_path = self.installed_root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = manifest["version"] + "+codex.20260720123456"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        cachebusted_root = self.installed_root.parent / manifest["version"]
        self.installed_root.rename(cachebusted_root)
        self.installed_root = cachebusted_root
        self.receipt = make_receipt(self.installed_root)

        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt, self.installed_root
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            json.loads(grade_path.read_text(encoding="utf-8"))["verdict"], "PASS"
        )

    def test_cachebuster_cannot_hide_an_additional_manifest_change(self) -> None:
        manifest_path = self.installed_root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = manifest["version"] + "+codex.20260720123456"
        manifest["description"] = "synthetically altered after the source commit"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        altered_root = self.installed_root.parent / manifest["version"]
        self.installed_root.rename(altered_root)
        self.installed_root = altered_root
        self.receipt = make_receipt(self.installed_root)

        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt, self.installed_root
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("changes beyond the canonical cachebuster", result.stdout)
        assert_safe_failure_grade(
            self, json.loads(grade_path.read_text(encoding="utf-8"))
        )

    def test_dirty_grader_source_cannot_establish_candidate_proof(self) -> None:
        dirty_path = self.grader_root / "untracked-during-grade.txt"
        dirty_path.write_text("synthetic dirty state", encoding="utf-8")
        try:
            result, _receipt_path, _attestation_path, grade_path = (
                run_attested_checker(self.receipt, self.installed_root)
            )
        finally:
            dirty_path.unlink()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("grading source must be clean", result.stdout)
        assert_safe_failure_grade(
            self, json.loads(grade_path.read_text(encoding="utf-8"))
        )

    def test_unresolvable_expected_revision_cannot_establish_candidate_proof(self) -> None:
        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt,
            self.installed_root,
            expected_source_revision="f" * 40,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source revision cannot be resolved", result.stdout)
        assert_safe_failure_grade(
            self, json.loads(grade_path.read_text(encoding="utf-8"))
        )

    def test_duplicate_keys_are_rejected_in_receipt_attestation_and_prompt(self) -> None:
        cases = {
            "receipt": {
                "mutate_receipt_bytes": lambda raw: raw.replace(
                    b'{\n  "schema_version": 3,',
                    b'{\n  "schema_version": 3,\n  "schema_version": 3,',
                    1,
                )
            },
            "attestation": {
                "mutate_attestation_bytes": lambda raw: raw.replace(
                    b'{\n  "schema_version": 1,',
                    b'{\n  "schema_version": 1,\n  "schema_version": 1,',
                    1,
                )
            },
            "prompt": {
                "mutate_prompt_bytes": lambda raw: raw.replace(
                    b'{\n  "schema_version": 1,',
                    b'{\n  "schema_version": 1,\n  "schema_version": 1,',
                    1,
                )
            },
        }
        for label, options in cases.items():
            with self.subTest(label=label):
                result, _receipt_path, _attestation_path, _grade_path = (
                    run_attested_checker(
                        copy.deepcopy(self.receipt),
                        self.installed_root,
                        **options,
                    )
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("duplicate object key", result.stdout)

    def test_final_symlinks_are_rejected_for_receipt_and_attestation(self) -> None:
        for label, options in (
            ("receipt", {"receipt_symlink": True}),
            ("attestation", {"attestation_symlink": True}),
        ):
            with self.subTest(label=label):
                result, _receipt_path, _attestation_path, _grade_path = (
                    run_attested_checker(
                        copy.deepcopy(self.receipt),
                        self.installed_root,
                        **options,
                    )
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("regular non-symlink file", result.stdout)

    def test_contract_control_file_final_symlink_is_rejected(self) -> None:
        contract_path = self.grader_root / "tests" / "route-contracts.json"
        contract_target = self.grader_root.parent / "route-contracts-target.json"
        contract_target.write_bytes(contract_path.read_bytes())
        contract_path.unlink()
        contract_path.symlink_to(contract_target)

        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt, self.installed_root
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("route contracts must be a regular non-symlink file", result.stdout)
        self.assertFalse(grade_path.exists())

    def test_grade_output_parent_symlink_is_rejected(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-003")
        item["actual_route"].remove("project-context")

        result, _receipt_path, _attestation_path, grade_path = run_attested_checker(
            self.receipt,
            self.installed_root,
            grade_parent_symlink=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(grade_path.exists())
        self.assertIn("failure grade could not be written", result.stdout)

    def test_error_output_escapes_injected_newlines_and_success_tokens(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-003")
        item["id"] = "ROUTE-003\nPASS candidate_proof=established"

        result = run_checker(self.receipt, self.installed_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(
            any(line.startswith("PASS ") for line in result.stdout.splitlines())
        )
        self.assertIn(r"\nPASS candidate_proof=established", result.stdout)

    def test_failed_semantic_check_persists_independent_fail_grade(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-003")
        item["actual_route"].remove("project-context")

        result, receipt_path, attestation_path, grade_path = run_attested_checker(
            self.receipt,
            self.installed_root,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("misses required capabilities: project-context", result.stdout)
        grade = json.loads(grade_path.read_text(encoding="utf-8"))
        assert_safe_failure_grade(self, grade)
        self.assertEqual(grade["scenario_count"], len(load_contracts()["scenarios"]))
        self.assertNotIn("ROUTE-003", " ".join(grade["errors"]))
        self.assertEqual(
            grade["raw_observation_sha256"],
            hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            grade["coordinator_attestation_sha256"],
            hashlib.sha256(attestation_path.read_bytes()).hexdigest(),
        )

    def test_instruction_closure_must_be_exact_complete_and_hash_bound(self) -> None:
        loaded = self.receipt["loaded_specialists"][0]
        closure = loaded["instruction_closure"]
        closure["files"][0]["state"] = "skipped"
        closure["files"].pop()
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("was not declared completely read", result.stdout)
        self.assertIn("instruction closure omits files", result.stdout)

    def test_trigger_state_contradiction_and_invalid_source_fail(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-014")
        disposition = item["conditional_dispositions"]["delivery-coordination"]
        disposition["state"] = "activated"
        disposition["trigger_evaluation"]["result"] = "not-met"
        disposition["trigger_evaluation"]["trigger_statement"] = "fabricated"
        disposition["trigger_evaluation"]["source"] = "expected-contract"
        item["actual_route"].append("delivery-coordination")
        self.receipt["loaded_specialists"].append(
            instruction_closure(self.installed_root, "delivery-coordination")
        )
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contradicts trigger result", result.stdout)
        self.assertIn("lacks a substantive blind trigger statement", result.stdout)
        self.assertIn("trigger source must be installed-runtime", result.stdout)

    def test_retrospective_uses_preexisting_outcome_not_canary_delivery(self) -> None:
        failed_deployment = find_scenario(self.receipt, "ROUTE-015")
        result = run_checker(self.receipt, self.installed_root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(failed_deployment["delivery_result"], "not-run")
        self.assertEqual(
            failed_deployment["outcome_observation"]["state"],
            "meaningful-outcome-observed",
        )

        failed_deployment["outcome_observation"]["state"] = (
            "no-meaningful-outcome-observed"
        )
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("retrospective disposition does not match", result.stdout)

    def test_direct_retrospective_requires_meaningful_observed_outcome(self) -> None:
        retrospective = find_scenario(self.receipt, "ROUTE-018")
        retrospective["outcome_observation"]["state"] = (
            "no-meaningful-outcome-observed"
        )
        retrospective["outcome_observation"]["evidence"] = [
            "No completed outcome can be established from available evidence."
        ]
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "selects retrospective-improvement without a meaningful observed outcome",
            result.stdout,
        )

    def test_direct_retrospective_allows_unknown_intake_with_linked_gap(self) -> None:
        retrospective = find_scenario(self.receipt, "ROUTE-018")
        gap_id = "GAP-ROUTE-018-OUTCOME"
        retrospective["outcome_observation"] = {
            "state": "unknown",
            "evidence": [
                f"{gap_id} records that measured outcome evidence is unavailable."
            ],
        }
        retrospective["gaps"] = [
            {
                "id": gap_id,
                "kind": "missing-evidence",
                "summary": "Measured outcome evidence is not available for this intake.",
                "related_field": "outcome_observation",
                "route_effect": "nonblocking",
                "next_action": "Collect an outcome measure before producing findings or lessons.",
            }
        ]
        result = run_checker(self.receipt, self.installed_root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_trigger_requires_linked_structured_gap(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-014")
        disposition = item["conditional_dispositions"]["delivery-coordination"]
        disposition["state"] = "deferred"
        disposition["trigger_evaluation"]["result"] = "unknown"
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires a linked structured gap", result.stdout)

        item["gaps"] = [
            {
                "id": "GAP-ROUTE-014-001",
                "kind": "missing-evidence",
                "summary": "Provider logs needed to resolve the branch are unavailable.",
                "related_field": (
                    "conditional_dispositions.delivery-coordination."
                    "trigger_evaluation.result"
                ),
                "route_effect": "nonblocking",
                "next_action": "Obtain authorized provider-log access and reassess the trigger.",
            }
        ]
        disposition["evidence"] = [
            "GAP-ROUTE-014-001 records the unavailable provider-log evidence."
        ]
        result = run_checker(self.receipt, self.installed_root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_structured_gap_rejects_nonexistent_nested_receipt_path(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-014")
        disposition = item["conditional_dispositions"]["delivery-coordination"]
        disposition["state"] = "deferred"
        disposition["trigger_evaluation"]["result"] = "unknown"
        item["gaps"] = [
            {
                "id": "GAP-ROUTE-014-002",
                "kind": "missing-evidence",
                "summary": "Provider logs needed to resolve the branch are unavailable.",
                "related_field": (
                    "conditional_dispositions.delivery-coordination."
                    "trigger_evaluation.nonexistent"
                ),
                "route_effect": "nonblocking",
                "next_action": "Obtain authorized provider-log access and reassess the trigger.",
            }
        ]
        disposition["evidence"] = [
            "GAP-ROUTE-014-002 records the unavailable provider-log evidence."
        ]

        result = run_checker(self.receipt, self.installed_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("references an unknown related_field", result.stdout)

    def test_well_formed_extra_conditional_disposition_is_allowed(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-001")
        item["conditional_dispositions"]["documentation-knowledge"] = {
            "state": "not-applicable",
            "trigger_evaluation": {
                "trigger_statement": (
                    "canonical documentation changes or durable handoff becomes necessary"
                ),
                "source": "installed-runtime",
                "result": "not-met",
            },
            "rationale": (
                "Installed runtime guidance was evaluated and the prompt does not change "
                "canonical documentation."
            ),
            "evidence": ["Synthetic prompt contains no durable documentation change."],
        }

        result = run_checker(self.receipt, self.installed_root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_extra_conditional_cannot_duplicate_required_or_forbidden_owner(self) -> None:
        cases = ("project-context", "implementation-execution")
        for skill in cases:
            with self.subTest(skill=skill):
                receipt = copy.deepcopy(self.receipt)
                item = find_scenario(receipt, "ROUTE-001")
                item["conditional_dispositions"][skill] = {
                    "state": "not-applicable",
                    "trigger_evaluation": {
                        "trigger_statement": (
                            "additional installed-runtime evidence requires this owner"
                        ),
                        "source": "installed-runtime",
                        "result": "not-met",
                    },
                    "rationale": (
                        "Synthetic mutation verifies that conditional ownership remains disjoint."
                    ),
                    "evidence": ["Synthetic disjoint-ownership regression evidence."],
                }

                result = run_checker(receipt, self.installed_root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "extra conditional dispositions duplicate required, forbidden, "
                    f"or controller capabilities: {skill}",
                    result.stdout,
                )

    def test_blocking_gap_cannot_pass(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-001")
        item["gaps"] = [
            {
                "id": "GAP-ROUTE-001-001",
                "kind": "missing-context",
                "summary": "The prompt omits context required to assert the route safely.",
                "related_field": "actual_route",
                "route_effect": "blocks-route",
                "next_action": "Obtain the missing repository context before routing further.",
            }
        ]
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocks the route claim", result.stdout)

    def test_scenario_effect_cannot_hide_behind_empty_root(self) -> None:
        item = find_scenario(self.receipt, "ROUTE-017D")
        item["scenario_observation"]["effects_performed"] = [
            "published-production"
        ]
        result = run_checker(self.receipt, self.installed_root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("records forbidden effects_performed", result.stdout)
        self.assertIn("does not equal the sorted unique scenario union", result.stdout)

    def test_mutation_after_semantic_digest_fails(self) -> None:
        refresh_digest(self.receipt)
        self.receipt["repository_identity"]["name"] = "fabricated-repository"
        result = run_checker(self.receipt, self.installed_root, refresh=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match the canonical fresh observation", result.stdout)

    def test_source_package_is_not_accepted_as_installed_cache(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        receipt["plugin_identity"]["cache_relative_path"] = "project-delivery"
        receipt["plugin_identity"]["manifest_sha256"] = hashlib.sha256(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_bytes()
        ).hexdigest()
        receipt["plugin_identity"]["payload_sha256"] = payload_sha256(
            PLUGIN_ROOT, sorted(select_paths(PLUGIN_ROOT))
        )
        receipt["plugin_identity"]["installed_version"] = manifest["version"]
        refresh_digest(receipt)
        with tempfile.TemporaryDirectory() as temporary:
            receipt_path = Path(temporary) / "receipt.json"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER),
                    str(receipt_path),
                    "--root",
                    str(REPOSITORY_ROOT),
                    "--installed-plugin-root",
                    str(PLUGIN_ROOT),
                    "--expected-source-revision",
                    SOURCE_REVISION,
                    "--allow-unattested-v3",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires an exact cache-shaped installed root", result.stdout)


if __name__ == "__main__":
    unittest.main()
