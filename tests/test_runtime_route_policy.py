from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "project-delivery"
SHARED = PLUGIN_ROOT / "skills" / ".shared"


class RuntimeRoutePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contracts = json.loads(
            (REPOSITORY_ROOT / "tests" / "route-contracts.json").read_text(
                encoding="utf-8"
            )
        )
        cls.operating_model = (SHARED / "operating-model.md").read_text(
            encoding="utf-8"
        )
        cls.templates = (SHARED / "artifact-templates.md").read_text(
            encoding="utf-8"
        )
        cls.orchestrator = (
            PLUGIN_ROOT / "skills" / "delivery-orchestrator" / "SKILL.md"
        ).read_text(encoding="utf-8")

    def test_runtime_taxonomy_covers_every_contract_value(self) -> None:
        scenarios = self.contracts["scenarios"]
        for field in ("scale", "risk", "authority"):
            with self.subTest(field=field):
                values = {scenario[field] for scenario in scenarios}
                for value in sorted(values):
                    self.assertIn(f"`{value}`", self.operating_model)

    def test_orchestrator_names_high_value_route_owners(self) -> None:
        required_fragments = (
            "Operational documentation and handoff",
            "documentation-knowledge → testing-quality",
            "Flaky CI or missing-provider-evidence review: testing-quality leads",
            "Combined platform performance, packaging, signing, or distribution claim: testing-quality leads",
            "Package-only claim: release-change enters",
            "Signing/notarization claim: security-operations leads",
            "Distribution/installability claim: release-change leads",
            "required testing-quality and security-operations evidence",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.orchestrator)

    def test_specialist_boundaries_match_evidence_claim_routes(self) -> None:
        testing = (
            PLUGIN_ROOT / "skills" / "testing-quality" / "SKILL.md"
        ).read_text(encoding="utf-8")
        release = (
            PLUGIN_ROOT / "skills" / "release-change" / "SKILL.md"
        ).read_text(encoding="utf-8")
        security = (
            PLUGIN_ROOT / "skills" / "security-operations" / "SKILL.md"
        ).read_text(encoding="utf-8")
        documentation = (
            PLUGIN_ROOT / "skills" / "documentation-knowledge" / "SKILL.md"
        ).read_text(encoding="utf-8")
        coordination = (
            PLUGIN_ROOT / "skills" / "delivery-coordination" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Lead flaky-CI triage", testing)
        self.assertIn("Lead package-artifact and distribution/installability", release)
        self.assertIn("Lead signing/notarization claim audits", security)
        self.assertIn("never sign", security)
        self.assertIn("publishing, deploying, distributing, installing", release)
        self.assertIn("Route executable or measurable validation through `testing-quality`", documentation)
        self.assertIn("operational or stakeholder handoff", coordination)

    def test_machine_receipt_template_matches_closed_schema_v3_envelope(self) -> None:
        match = re.search(
            r"### Machine-comparable route receipt.*?```json\n(.*?)\n```",
            self.templates,
            re.DOTALL,
        )
        self.assertIsNotNone(match, "machine route receipt JSON template missing")
        envelope = json.loads(match.group(1))

        schema = json.loads(
            (SHARED / "live-route-receipt-v3.schema.json").read_text(
                encoding="utf-8"
            )
        )
        required_root_fields = set(schema["required"])
        self.assertEqual(set(envelope), required_root_fields)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(envelope["schema_version"], 3)
        self.assertEqual(envelope["contract_schema_version"], 2)
        self.assertEqual(
            envelope["evidence_class"], "fresh-task semantic route observation"
        )
        self.assertTrue(
            envelope["semantic_fields_were_frozen_before_contract_comparison"]
        )
        self.assertEqual(envelope["observation_scope"], "route-only-no-effects")
        self.assertEqual(envelope["effects_performed"], [])
        self.assertEqual(envelope["legacy_runtime_events"], [])
        self.assertEqual(
            envelope["plugin_identity"]["payload_hash_method"],
            "project-delivery length-prefixed path-and-content sha256 v1",
        )

        expected_freeze_scope = {
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
        }
        self.assertEqual(set(envelope["semantic_freeze_scope"]), expected_freeze_scope)
        self.assertEqual(envelope["legacy_invocations"], [])
        self.assertEqual(envelope["legacy_branded_state_created"], [])
        disposition = next(iter(envelope["scenarios"][0]["conditional_dispositions"].values()))
        self.assertEqual(
            set(disposition["trigger_evaluation"]),
            {"trigger_statement", "source", "result"},
        )
        self.assertEqual(disposition["trigger_evaluation"]["source"], "installed-runtime")

    def test_orchestrator_template_instruction_closure_is_complete(self) -> None:
        envelope_match = re.search(
            r"### Machine-comparable route receipt.*?```json\n(.*?)\n```",
            self.templates,
            re.DOTALL,
        )
        self.assertIsNotNone(envelope_match)
        envelope = json.loads(envelope_match.group(1))
        template_files = {
            item["relative_path"]
            for item in envelope["loaded_specialists"][0]["instruction_closure"]["files"]
        }
        references = {
            (
                PLUGIN_ROOT / "skills" / "delivery-orchestrator" / match
            ).resolve().relative_to(PLUGIN_ROOT.resolve()).as_posix()
            for match in re.findall(
                r"`(\.\./\.shared/[a-z0-9._-]+\.(?:json|md))`",
                self.orchestrator,
            )
        }
        self.assertEqual(
            template_files,
            {"skills/delivery-orchestrator/SKILL.md", *references},
        )

    def test_prospective_retrospective_is_not_present_activation(self) -> None:
        self.assertIn(
            "Activate retrospective only after a meaningful outcome",
            self.orchestrator,
        )
        self.assertIn(
            "omit it from `actual_route`",
            self.orchestrator,
        )
        self.assertIn("`planned-future` is reserved for retrospective work", self.operating_model)


if __name__ == "__main__":
    unittest.main()
