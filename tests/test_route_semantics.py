from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
CONTRACT_CHECKER = REPOSITORY_ROOT / "scripts" / "check_routes.py"
RECEIPT_CHECKER = REPOSITORY_ROOT / "scripts" / "check_route_receipts.py"
BLIND_FIXTURE = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "blind-route-observations-v1.3.1.json"
)


def run_contract_checker() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CONTRACT_CHECKER), str(REPOSITORY_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )


def run_contract_checker_with_contract(
    contract: dict[str, object],
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "tests").mkdir()
        (root / "tests" / "route-contracts.json").write_text(
            json.dumps(contract), encoding="utf-8"
        )
        for skill_file in (REPOSITORY_ROOT / "skills").glob("*/SKILL.md"):
            target = root / "skills" / skill_file.parent.name
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("fixture\n", encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(CONTRACT_CHECKER), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )


def run_receipt_checker(
    receipts: dict[str, object], *, allow_historical: bool = True
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temporary:
        receipt_path = Path(temporary) / "receipts.json"
        receipt_path.write_text(json.dumps(receipts), encoding="utf-8")
        command = [
            sys.executable,
            str(RECEIPT_CHECKER),
            str(receipt_path),
            "--root",
            str(REPOSITORY_ROOT),
            "--allow-subset",
        ]
        if allow_historical:
            command.append("--allow-historical-annotations")
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )


def load_fixture() -> dict[str, object]:
    return json.loads(BLIND_FIXTURE.read_text(encoding="utf-8"))


def load_contracts() -> dict[str, object]:
    return json.loads((REPOSITORY_ROOT / "tests" / "route-contracts.json").read_text())


def make_fresh_receipts(receipts: dict[str, object]) -> dict[str, object]:
    receipts["evidence_class"] = "fresh-task semantic route observation"
    receipts["semantic_fields_were_frozen_before_contract_comparison"] = True
    receipts["semantic_freeze_scope"] = [
        "actual_route",
        "authority",
        "conditional_dispositions",
        "evidence",
        "extra_capability_justifications",
        "gaps",
        "risk",
        "scale",
        "taxonomy_evidence",
        "taxonomy_rationale",
    ]
    receipts["semantic_freeze_evidence"] = [
        "Synthetic fresh-task fixture froze every semantic field before comparison."
    ]
    receipts["annotation_provenance"] = (
        "Synthetic fresh-task regression record with all semantic fields fixed before comparison."
    )
    return receipts


def scenario(receipts: dict[str, object], scenario_id: str) -> dict[str, object]:
    scenarios = receipts["scenarios"]
    assert isinstance(scenarios, list)
    return next(item for item in scenarios if item["id"] == scenario_id)


def synthetic_policy_scenario(contract: dict[str, object]) -> dict[str, object]:
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
        assert eligible, f"cyclic synthetic contract: {contract['id']}"
        selected = eligible[0]
        remaining.remove(selected)
        route.append(selected)
    for controller in contract.get("required_reentry", []):
        owners = contract.get("required_reentry_after", {}).get(controller, [])
        if any(owner in route for owner in owners):
            route.append(controller)
    return {
        "id": contract["id"],
        "scale": contract["scale"],
        "risk": contract["risk"],
        "authority": contract["authority"],
        "taxonomy_rationale": (
            "Synthetic classification rationale fixed before contract comparison for this "
            "route-policy regression scenario."
        ),
        "taxonomy_evidence": ["Synthetic pre-comparison taxonomy evidence."],
        "actual_route": route,
        "conditional_dispositions": {
            item["skill"]: {
                "state": "not-applicable",
                "rationale": "Synthetic policy test leaves this evidence-triggered branch inactive.",
                "evidence": ["Synthetic route-policy regression fixture."],
            }
            for item in contract["conditional_capabilities"]
        },
        "extra_capability_justifications": {},
        "delivery_result": "not-run",
        "evidence": ["Synthetic route-policy regression fixture."],
        "gaps": [],
    }


class RouteSemanticTests(unittest.TestCase):
    def test_authored_semantic_contracts_pass(self) -> None:
        result = run_contract_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("evidence=semantic-contracts", result.stdout)

    def test_blind_v131_routes_pass_historical_shape_compatibility(self) -> None:
        result = run_receipt_checker(load_fixture())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("historical_route_shape_records=17", result.stdout)
        self.assertIn("current_policy_claim=not-established", result.stdout)
        self.assertIn("historical contract-blind route", result.stdout)

    def test_historical_annotations_require_explicit_flag(self) -> None:
        result = run_receipt_checker(load_fixture(), allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("require --allow-historical-annotations", result.stdout)

    def test_fresh_receipt_requires_all_semantic_fields_frozen(self) -> None:
        receipts = load_fixture()
        receipts["evidence_class"] = "fresh-task semantic route observation"
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "requires all semantic fields frozen before contract comparison",
            result.stdout,
        )
        self.assertIn("fresh-task semantic freeze omits fields", result.stdout)

    def test_missing_required_capability_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.remove("delivery-planning")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("misses required capabilities: delivery-planning", result.stdout)

    def test_authority_forbidden_capability_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.append("implementation-execution")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("uses authority-forbidden capabilities", result.stdout)

    def test_missing_conditional_disposition_fails(self) -> None:
        receipts = load_fixture()
        dispositions = scenario(receipts, "ROUTE-004")["conditional_dispositions"]
        assert isinstance(dispositions, dict)
        del dispositions["testing-quality"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("omits conditional dispositions: testing-quality", result.stdout)

    def test_required_controller_reentry_fails_when_omitted(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-005")["actual_route"]
        assert isinstance(route, list)
        route.pop()
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("misses required controller re-entry: release-change", result.stdout)

    def test_controller_return_before_evidence_fails(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-005")["actual_route"] = [
            "release-change",
            "release-change",
            "testing-quality",
            "documentation-knowledge",
            "review-audit",
            "security-operations",
        ]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("controller release-change does not return after", result.stdout)

    def test_controller_must_enter_before_recovery_owners(self) -> None:
        cases = {
            "ROUTE-005": [
                "delivery-orchestrator",
                "testing-quality",
                "documentation-knowledge",
                "review-audit",
                "security-operations",
                "release-change",
                "release-change",
            ],
            "ROUTE-015": [
                "delivery-orchestrator",
                "security-operations",
                "release-change",
                "release-change",
            ],
        }
        for scenario_id, malformed_route in cases.items():
            with self.subTest(scenario=scenario_id):
                receipts = load_fixture()
                scenario(receipts, scenario_id)["actual_route"] = malformed_route
                result = run_receipt_checker(receipts)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("does not enter before", result.stdout)

        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-017B")
        package = synthetic_policy_scenario(contract)
        package["actual_route"] = [
            "testing-quality",
            "release-change",
            "release-change",
        ]
        receipts["scenarios"] = [package]
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not enter before: testing-quality", result.stdout)

    def test_late_incident_controller_fails(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-010")["actual_route"] = [
            "delivery-orchestrator",
            "project-context",
            "requirements-acceptance",
            "solution-design",
            "security-operations",
            "implementation-execution",
            "testing-quality",
            "release-change",
            "release-change",
            "delivery-planning",
            "documentation-knowledge",
            "review-audit",
            "security-operations",
            "delivery-coordination",
            "retrospective-improvement",
        ]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "violates precedence: release-change must precede project-context",
            result.stdout,
        )

    def test_incident_planning_after_implementation_fails(self) -> None:
        receipts = load_fixture()
        incident = scenario(receipts, "ROUTE-010")
        route = incident["actual_route"]
        assert isinstance(route, list)
        route.remove("delivery-planning")
        route.insert(route.index("testing-quality") + 1, "delivery-planning")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "violates precedence: delivery-planning must precede implementation-execution",
            result.stdout,
        )

    def test_equivalent_evidence_owner_order_passes(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-005")["actual_route"] = [
            "delivery-orchestrator",
            "release-change",
            "security-operations",
            "review-audit",
            "documentation-knowledge",
            "testing-quality",
            "release-change",
        ]
        result = run_receipt_checker(receipts)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_precedence_violation_fails(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-001")["actual_route"] = [
            "delivery-orchestrator",
            "project-context",
            "requirements-acceptance",
            "delivery-planning",
            "solution-design",
        ]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "violates precedence: solution-design must precede delivery-planning",
            result.stdout,
        )

    def test_legacy_dependency_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-008")["actual_route"]
        assert isinstance(route, list)
        route.append("superpowers")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("uses forbidden dependencies: superpowers", result.stdout)

    def test_undeclared_reentry_fails(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.append("project-context")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repeats capabilities without a re-entry contract", result.stdout)

    def test_blocked_conditional_cannot_pass_route_policy(self) -> None:
        receipts = load_fixture()
        disposition = scenario(receipts, "ROUTE-004")["conditional_dispositions"][
            "testing-quality"
        ]
        disposition["state"] = "blocked"
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocked conditional branch", result.stdout)

    def test_conditional_disposition_requires_substantive_rationale(self) -> None:
        receipts = load_fixture()
        disposition = scenario(receipts, "ROUTE-004")["conditional_dispositions"][
            "testing-quality"
        ]
        disposition["rationale"] = "x"
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks a substantive rationale", result.stdout)

    def test_conditional_disposition_requires_evidence(self) -> None:
        receipts = load_fixture()
        disposition = scenario(receipts, "ROUTE-004")["conditional_dispositions"][
            "testing-quality"
        ]
        disposition["evidence"] = []
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disposition for testing-quality lacks evidence", result.stdout)

    def test_route_only_checker_rejects_delivery_pass(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-001")["delivery_result"] = "pass"
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("this checker is route-only", result.stdout)

    def test_route_evidence_cannot_be_empty(self) -> None:
        receipts = load_fixture()
        scenario(receipts, "ROUTE-001")["evidence"] = []
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence must be a non-empty string list", result.stdout)

    def test_extra_capability_requires_justification(self) -> None:
        receipts = load_fixture()
        route = scenario(receipts, "ROUTE-001")["actual_route"]
        assert isinstance(route, list)
        route.append("documentation-knowledge")
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks justification for extra capabilities", result.stdout)

    def test_unloaded_specialist_fails(self) -> None:
        receipts = load_fixture()
        loaded = receipts["loaded_specialists"]
        assert isinstance(loaded, list)
        loaded[:] = [item for item in loaded if item["skill"] != "solution-design"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("without load evidence: solution-design", result.stdout)

    def test_route_only_observation_rejects_effects(self) -> None:
        receipts = load_fixture()
        receipts["effects_performed"] = ["ad-hoc signing"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty effects_performed", result.stdout)

    def test_legacy_runtime_event_fails(self) -> None:
        receipts = load_fixture()
        receipts["legacy_runtime_events"] = ["epic hook started"]
        result = run_receipt_checker(receipts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no legacy runtime events", result.stdout)

    def test_contract_cycle_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["precedence"].append(["delivery-planning", "project-context"])
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("precedence graph contains a cycle", result.stdout)

    def test_conditional_forbidden_contradiction_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["forbidden_capabilities"].append("solution-design")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("both conditional and forbidden: solution-design", result.stdout)

    def test_duplicate_required_capability_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["required_capabilities"].append("project-context")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repeats required_capabilities: project-context", result.stdout)

    def test_required_forbidden_contradiction_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["forbidden_capabilities"].append("project-context")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("both required and forbidden: project-context", result.stdout)

    def test_unselectable_allowed_reentry_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["allowed_reentry"].append("documentation-knowledge")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("allows re-entry for unselectable capabilities", result.stdout)

    def test_missing_return_after_contract_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-005")
        del route["required_reentry_after"]
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required re-entry lacks return-after owners", result.stdout)

    def test_missing_entry_before_contract_fails(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-005")
        del route["required_reentry_before"]
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required re-entry lacks entry-before owners", result.stdout)

    def test_contract_requires_all_superseded_runtime_identities(self) -> None:
        contracts = load_contracts()
        dependencies = contracts["forbidden_runtime_dependencies"]
        assert isinstance(dependencies, list)
        dependencies.remove("epic-harness")
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must forbid the known superseded runtime dependencies", result.stdout)

    def test_contract_rejects_empty_scenario_metadata(self) -> None:
        contracts = load_contracts()
        route = scenario(contracts, "ROUTE-001")
        route["prompt"] = ""
        route["scale"] = ""
        route["risk"] = ""
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("field prompt must be a non-empty string", result.stdout)
        self.assertIn("field scale must be a non-empty string", result.stdout)
        self.assertIn("field risk must be a non-empty string", result.stdout)

    def test_contract_rejects_malformed_scenario_id(self) -> None:
        contracts = load_contracts()
        scenario(contracts, "ROUTE-001")["id"] = "route one"
        result = run_contract_checker_with_contract(contracts)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("has malformed scenario ID", result.stdout)

    def test_natural_package_controller_return_passes(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contract = scenario(load_contracts(), "ROUTE-017B")
        receipts["scenarios"] = [
            {
                "id": "ROUTE-017B",
                "scale": contract["scale"],
                "risk": contract["risk"],
                "authority": contract["authority"],
                "taxonomy_rationale": (
                    "Synthetic package classification fixed before contract comparison for "
                    "the route-policy regression scenario."
                ),
                "taxonomy_evidence": ["Synthetic pre-comparison taxonomy evidence."],
                "actual_route": [
                    "release-change",
                    "testing-quality",
                    "release-change",
                ],
                "conditional_dispositions": {
                    item["skill"]: {
                        "state": "not-applicable",
                        "rationale": "Synthetic policy test leaves this evidence-triggered branch inactive.",
                        "evidence": ["Synthetic route-policy regression fixture."],
                    }
                    for item in contract["conditional_capabilities"]
                },
                "extra_capability_justifications": {},
                "delivery_result": "not-run",
                "evidence": ["Synthetic route-policy regression fixture."],
                "gaps": [],
            }
        ]
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_synthetic_route_policy_matrix_passes_all_21_contracts(self) -> None:
        receipts = make_fresh_receipts(load_fixture())
        contracts = load_contracts()["scenarios"]
        receipts["scenarios"] = [
            synthetic_policy_scenario(contract) for contract in contracts
        ]
        result = run_receipt_checker(receipts, allow_historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("route_policy_records=21", result.stdout)

    def test_mutation_does_not_modify_source_fixture(self) -> None:
        first = load_fixture()
        second = copy.deepcopy(first)
        scenario(second, "ROUTE-001")["actual_route"] = []
        self.assertNotEqual(
            scenario(first, "ROUTE-001")["actual_route"],
            scenario(second, "ROUTE-001")["actual_route"],
        )


if __name__ == "__main__":
    unittest.main()
