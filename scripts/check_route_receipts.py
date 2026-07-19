#!/usr/bin/env python3
"""Validate blind route receipts against semantic route contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path


ALLOWED_CONDITIONAL_STATES = {
    "activated",
    "blocked",
    "deferred",
    "not-applicable",
    "planned-future",
}
PLANNED_FUTURE_CAPABILITIES = {"retrospective-improvement"}
FRESH_EVIDENCE_CLASS = "fresh-task semantic route observation"
HISTORICAL_EVIDENCE_CLASS = (
    "historical contract-blind route with post-hoc semantic annotation"
)
FRESH_SEMANTIC_FREEZE_FIELDS = {
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
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_REVISION = re.compile(r"^[0-9a-f]{7,64}$")
REQUIRED_RECEIPT_FIELDS = {
    "id",
    "actual_route",
    "scale",
    "risk",
    "authority",
    "taxonomy_rationale",
    "taxonomy_evidence",
    "conditional_dispositions",
    "extra_capability_justifications",
    "delivery_result",
    "evidence",
    "gaps",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "receipts",
        help="JSON receipt set produced by a fresh task before contract comparison",
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).parents[1]),
        help="plugin source or installed root containing tests/route-contracts.json",
    )
    parser.add_argument(
        "--allow-subset",
        action="store_true",
        help="allow receipts for only a subset of canonical scenarios",
    )
    parser.add_argument(
        "--allow-historical-annotations",
        action="store_true",
        help=(
            "allow preserved blind route selections whose semantic taxonomy and branch "
            "annotations were added after contract comparison; never use this for candidate proof"
        ),
    )
    return parser.parse_args(argv)


def read_json(path: Path, label: str) -> tuple[dict[str, object] | None, list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [f"invalid {label}: {error}"]
    if not isinstance(value, dict):
        return None, [f"{label} root must be an object"]
    return value, []


def normalize_skill(value: str) -> str:
    prefix = "project-delivery:"
    return value[len(prefix) :] if value.startswith(prefix) else value


def validate_string_list(value: object, *, require_nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not require_nonempty)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def last_index(values: list[str], target: str) -> int:
    return len(values) - 1 - values[::-1].index(target)


def validate(
    root: Path,
    receipt_path: Path,
    allow_subset: bool = False,
    allow_historical_annotations: bool = False,
) -> tuple[list[str], int, str]:
    errors: list[str] = []
    contracts, contract_errors = read_json(
        root / "tests" / "route-contracts.json", "route contracts"
    )
    receipts, receipt_errors = read_json(receipt_path, "route receipts")
    errors.extend(contract_errors)
    errors.extend(receipt_errors)
    if contracts is None or receipts is None:
        return errors, 0, "unknown"

    if contracts.get("schema_version") != 2:
        errors.append("route contracts must use schema version 2")
    if receipts.get("schema_version") != 2:
        errors.append("route receipts must use schema version 2")
    if receipts.get("contract_schema_version") != contracts.get("schema_version"):
        errors.append("receipt contract_schema_version does not match route contracts")
    evidence_class = receipts.get("evidence_class")
    if evidence_class not in {FRESH_EVIDENCE_CLASS, HISTORICAL_EVIDENCE_CLASS}:
        errors.append("receipts have an unsupported evidence class")
        evidence_class = "unknown"
    all_semantics_blind = receipts.get(
        "semantic_fields_were_frozen_before_contract_comparison"
    )
    freeze_scope_value = receipts.get("semantic_freeze_scope")
    freeze_scope = set(freeze_scope_value) if validate_string_list(freeze_scope_value) else set()
    if not validate_string_list(freeze_scope_value):
        errors.append("semantic_freeze_scope must be a string list")
    elif len(freeze_scope) != len(freeze_scope_value):
        errors.append("semantic_freeze_scope must not contain duplicates")
    if not validate_string_list(
        receipts.get("semantic_freeze_evidence"), require_nonempty=True
    ):
        errors.append("receipts must include semantic freeze evidence")
    annotation_provenance = receipts.get("annotation_provenance")
    if not isinstance(annotation_provenance, str) or not annotation_provenance.strip():
        errors.append("receipts must explain annotation provenance")
    if evidence_class == FRESH_EVIDENCE_CLASS:
        if all_semantics_blind is not True:
            errors.append(
                "fresh-task evidence requires all semantic fields frozen before contract comparison"
            )
        if freeze_scope != FRESH_SEMANTIC_FREEZE_FIELDS:
            missing_scope = FRESH_SEMANTIC_FREEZE_FIELDS.difference(freeze_scope)
            extra_scope = freeze_scope.difference(FRESH_SEMANTIC_FREEZE_FIELDS)
            if missing_scope:
                errors.append(
                    "fresh-task semantic freeze omits fields: "
                    + ", ".join(sorted(missing_scope))
                )
            if extra_scope:
                errors.append(
                    "fresh-task semantic freeze names unknown fields: "
                    + ", ".join(sorted(extra_scope))
                )
    if evidence_class == HISTORICAL_EVIDENCE_CLASS:
        if all_semantics_blind is not False:
            errors.append(
                "historical evidence must mark the complete semantic record as post-hoc"
            )
        if "actual_route" not in freeze_scope:
            errors.append(
                "historical evidence must identify actual_route as frozen before comparison"
            )
        if not allow_historical_annotations:
            errors.append(
                "historical post-hoc semantics require --allow-historical-annotations"
            )
    for identity_field in ("plugin_identity", "task_identity", "repository_identity"):
        identity = receipts.get(identity_field)
        if not isinstance(identity, dict) or not identity:
            errors.append(f"receipts must include non-empty {identity_field}")
    plugin_identity = receipts.get("plugin_identity", {})
    if isinstance(plugin_identity, dict):
        required_plugin_identity = {
            "name",
            "installed_version",
            "source_revision",
            "manifest_sha256",
            "payload_sha256",
            "payload_hash_method",
            "cache_relative_path",
        }
        missing_identity = required_plugin_identity.difference(plugin_identity)
        if missing_identity:
            errors.append(
                "plugin_identity missing fields: " + ", ".join(sorted(missing_identity))
            )
        for field in ("name", "installed_version", "payload_hash_method", "cache_relative_path"):
            if not isinstance(plugin_identity.get(field), str) or not plugin_identity[field].strip():
                errors.append(f"plugin_identity field {field} must be a non-empty string")
        if plugin_identity.get("name") != "project-delivery":
            errors.append("plugin_identity name must be project-delivery")
        if not isinstance(plugin_identity.get("source_revision"), str) or not SOURCE_REVISION.fullmatch(
            plugin_identity["source_revision"]
        ):
            errors.append("plugin_identity source_revision must be a hexadecimal revision")
        for field in ("manifest_sha256", "payload_sha256"):
            if not isinstance(plugin_identity.get(field), str) or not SHA256.fullmatch(
                plugin_identity[field]
            ):
                errors.append(f"plugin_identity field {field} must be a SHA-256 digest")
        cache_relative_path = plugin_identity.get("cache_relative_path")
        if isinstance(cache_relative_path, str) and (
            cache_relative_path.startswith("/") or ".." in Path(cache_relative_path).parts
        ):
            errors.append("plugin_identity cache_relative_path must be portable and relative")
    task_identity = receipts.get("task_identity", {})
    if isinstance(task_identity, dict):
        required_task_identity = {"public_receipt_id", "selected_at", "source_observation_sha256"}
        missing_identity = required_task_identity.difference(task_identity)
        if missing_identity:
            errors.append(
                "task_identity missing fields: " + ", ".join(sorted(missing_identity))
            )
        for field in ("public_receipt_id", "selected_at"):
            if not isinstance(task_identity.get(field), str) or not task_identity[field].strip():
                errors.append(f"task_identity field {field} must be a non-empty string")
        source_digest = task_identity.get("source_observation_sha256")
        if not isinstance(source_digest, str) or not SHA256.fullmatch(source_digest):
            errors.append("task_identity source_observation_sha256 must be a SHA-256 digest")
    repository_identity = receipts.get("repository_identity", {})
    if isinstance(repository_identity, dict):
        required_repository_identity = {
            "name",
            "revision",
            "working_tree_state",
            "instructions_evidence",
        }
        missing_identity = required_repository_identity.difference(repository_identity)
        if missing_identity:
            errors.append(
                "repository_identity missing fields: "
                + ", ".join(sorted(missing_identity))
            )
        for field in required_repository_identity:
            if not isinstance(repository_identity.get(field), str) or not repository_identity[field].strip():
                errors.append(f"repository_identity field {field} must be a non-empty string")
    if receipts.get("observation_scope") != "route-only-no-effects":
        errors.append("receipt checker accepts only route-only-no-effects observations")
    effects_performed = receipts.get("effects_performed")
    if not validate_string_list(effects_performed) or effects_performed:
        errors.append("route-only observations must record an empty effects_performed list")
    legacy_runtime_events = receipts.get("legacy_runtime_events")
    if not validate_string_list(legacy_runtime_events) or legacy_runtime_events:
        errors.append("route-only observations must record no legacy runtime events")
    if not validate_string_list(receipts.get("legacy_administrative_visibility", [])):
        errors.append("legacy_administrative_visibility must be a string list")

    contract_items = contracts.get("scenarios")
    receipt_items = receipts.get("scenarios")
    if not isinstance(contract_items, list):
        return errors + ["route contract scenarios must be a list"], 0, str(evidence_class)
    if not isinstance(receipt_items, list):
        return errors + ["route receipt scenarios must be a list"], 0, str(evidence_class)

    contract_by_id = {
        item.get("id"): item
        for item in contract_items
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    receipt_by_id: dict[str, dict[str, object]] = {}
    for item in receipt_items:
        if not isinstance(item, dict):
            errors.append("route receipt scenario is not an object")
            continue
        scenario_id = item.get("id")
        if not isinstance(scenario_id, str):
            errors.append("route receipt scenario lacks an ID")
            continue
        if scenario_id in receipt_by_id:
            errors.append(f"duplicate route receipt scenario: {scenario_id}")
        receipt_by_id[scenario_id] = item

    unknown_receipts = set(receipt_by_id).difference(contract_by_id)
    if unknown_receipts:
        errors.append(
            "receipts reference unknown scenarios: " + ", ".join(sorted(unknown_receipts))
        )
    missing_receipts = set(contract_by_id).difference(receipt_by_id)
    if missing_receipts and not allow_subset:
        errors.append(
            "receipts omit canonical scenarios: " + ", ".join(sorted(missing_receipts))
        )
    if not receipt_by_id:
        errors.append("no route receipts found")
        return errors, 0, str(evidence_class)

    available_skills = {
        path.parent.name for path in (root / "skills").glob("*/SKILL.md")
    }
    loaded_items = receipts.get("loaded_specialists")
    loaded_skills: set[str] = set()
    if not isinstance(loaded_items, list) or not loaded_items:
        errors.append("receipts must include loaded_specialists")
        loaded_items = []
    for loaded_index, item in enumerate(loaded_items, 1):
        if not isinstance(item, dict):
            errors.append(f"loaded specialist {loaded_index} is not an object")
            continue
        skill = item.get("skill")
        relative_path = item.get("relative_path")
        state = item.get("state")
        if not isinstance(skill, str) or not skill.strip():
            errors.append(f"loaded specialist {loaded_index} lacks a skill")
            continue
        skill = normalize_skill(skill)
        if skill in loaded_skills:
            errors.append(f"duplicate loaded specialist: {skill}")
        loaded_skills.add(skill)
        if skill not in available_skills:
            errors.append(f"loaded specialist is unknown: {skill}")
        if relative_path != f"skills/{skill}/SKILL.md":
            errors.append(f"loaded specialist {skill} has an invalid relative path")
        if state != "loaded":
            errors.append(f"loaded specialist {skill} was not successfully loaded")
    forbidden_dependencies = set(contracts.get("forbidden_runtime_dependencies", []))
    started = time.monotonic()
    selected_ids = [item.get("id") for item in contract_items if item.get("id") in receipt_by_id]
    for index, scenario_id in enumerate(selected_ids, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(selected_ids) - index)
        print(
            f"RECEIPT [{index}/{len(selected_ids)}] id={scenario_id} eta={eta:.1f}s",
            flush=True,
        )
        contract = contract_by_id[scenario_id]
        receipt = receipt_by_id[scenario_id]
        missing_fields = REQUIRED_RECEIPT_FIELDS.difference(receipt)
        if missing_fields:
            errors.append(
                f"{scenario_id} receipt missing fields: {', '.join(sorted(missing_fields))}"
            )

        raw_route = receipt.get("actual_route")
        if not validate_string_list(raw_route) or not raw_route:
            errors.append(f"{scenario_id} actual_route must be a non-empty string list")
            continue
        route = [normalize_skill(item) for item in raw_route]
        unknown_skills = set(route).difference(available_skills)
        if unknown_skills:
            errors.append(
                f"{scenario_id} actual route references unknown skills: "
                + ", ".join(sorted(unknown_skills))
            )
        legacy_skills = set(route).intersection(forbidden_dependencies)
        if legacy_skills:
            errors.append(
                f"{scenario_id} actual route uses forbidden dependencies: "
                + ", ".join(sorted(legacy_skills))
            )
        unloaded_skills = set(route).difference(loaded_skills)
        if unloaded_skills:
            errors.append(
                f"{scenario_id} route includes specialists without load evidence: "
                + ", ".join(sorted(unloaded_skills))
            )

        for classification_field in ("scale", "risk", "authority"):
            if receipt.get(classification_field) != contract.get(classification_field):
                errors.append(
                    f"{scenario_id} {classification_field} does not match the contract taxonomy"
                )
        taxonomy_rationale = receipt.get("taxonomy_rationale")
        if not isinstance(taxonomy_rationale, str) or len(taxonomy_rationale.strip()) < 20:
            errors.append(f"{scenario_id} lacks a substantive taxonomy rationale")
        if not validate_string_list(
            receipt.get("taxonomy_evidence"), require_nonempty=True
        ):
            errors.append(f"{scenario_id} taxonomy_evidence must be a non-empty string list")

        required = set(contract.get("required_capabilities", []))
        missing_required = required.difference(route)
        if missing_required:
            errors.append(
                f"{scenario_id} misses required capabilities: "
                + ", ".join(sorted(missing_required))
            )
        lead = contract.get("lead_capability")
        if isinstance(lead, str) and lead not in route:
            errors.append(f"{scenario_id} misses lead capability: {lead}")
        forbidden = set(contract.get("forbidden_capabilities", []))
        unsafe = forbidden.intersection(route)
        if unsafe:
            errors.append(
                f"{scenario_id} uses authority-forbidden capabilities: "
                + ", ".join(sorted(unsafe))
            )

        allowed_reentry = set(contract.get("allowed_reentry", []))
        repeated = {skill for skill, count in Counter(route).items() if count > 1}
        invalid_reentry = repeated.difference(allowed_reentry)
        if invalid_reentry:
            errors.append(
                f"{scenario_id} repeats capabilities without a re-entry contract: "
                + ", ".join(sorted(invalid_reentry))
            )
        for controller in contract.get("required_reentry", []):
            return_owners = contract.get("required_reentry_after", {}).get(controller, [])
            entry_owners = contract.get("required_reentry_before", {}).get(controller, [])
            selected_owners = [owner for owner in return_owners if owner in route]
            selected_entry_owners = [owner for owner in entry_owners if owner in route]
            if selected_owners and route.count(controller) < 2:
                errors.append(
                    f"{scenario_id} misses required controller re-entry: {controller}"
                )
                continue
            if selected_entry_owners and route.index(controller) >= min(
                route.index(owner) for owner in selected_entry_owners
            ):
                errors.append(
                    f"{scenario_id} controller {controller} does not enter before: "
                    + ", ".join(selected_entry_owners)
                )
            if selected_owners and last_index(route, controller) <= max(
                last_index(route, owner) for owner in selected_owners
            ):
                errors.append(
                    f"{scenario_id} controller {controller} does not return after: "
                    + ", ".join(selected_owners)
                )

        for before, after in contract.get("precedence", []):
            if before in route and after in route and route.index(before) >= route.index(after):
                errors.append(
                    f"{scenario_id} violates precedence: {before} must precede {after}"
                )

        dispositions = receipt.get("conditional_dispositions")
        if not isinstance(dispositions, dict):
            errors.append(f"{scenario_id} conditional_dispositions must be an object")
            dispositions = {}
        expected_conditional = {
            item.get("skill")
            for item in contract.get("conditional_capabilities", [])
            if isinstance(item, dict) and isinstance(item.get("skill"), str)
        }
        missing_dispositions = expected_conditional.difference(dispositions)
        extra_dispositions = set(dispositions).difference(expected_conditional)
        if missing_dispositions:
            errors.append(
                f"{scenario_id} omits conditional dispositions: "
                + ", ".join(sorted(missing_dispositions))
            )
        if extra_dispositions:
            errors.append(
                f"{scenario_id} has unknown conditional dispositions: "
                + ", ".join(sorted(extra_dispositions))
            )
        for skill in expected_conditional.intersection(dispositions):
            disposition = dispositions[skill]
            if not isinstance(disposition, dict):
                errors.append(f"{scenario_id} disposition for {skill} must be an object")
                continue
            state = disposition.get("state")
            rationale = disposition.get("rationale")
            if state not in ALLOWED_CONDITIONAL_STATES:
                errors.append(f"{scenario_id} disposition for {skill} has invalid state: {state}")
            if not isinstance(rationale, str) or len(rationale.strip()) < 12:
                errors.append(f"{scenario_id} disposition for {skill} lacks a substantive rationale")
            if not validate_string_list(disposition.get("evidence"), require_nonempty=True):
                errors.append(f"{scenario_id} disposition for {skill} lacks evidence")
            if state == "planned-future" and skill not in PLANNED_FUTURE_CAPABILITIES:
                errors.append(
                    f"{scenario_id} disposition for {skill} cannot be planned-future"
                )
            if skill in route and state not in {"activated", "planned-future"}:
                errors.append(
                    f"{scenario_id} selected conditional capability {skill} without an active or planned-future state"
                )
            if skill not in route and state in {"activated", "planned-future"}:
                errors.append(
                    f"{scenario_id} marks omitted conditional capability {skill} as {state}"
                )
            if state == "blocked":
                errors.append(
                    f"{scenario_id} has a blocked conditional branch and cannot pass route policy"
                )

        extra_justifications = receipt.get("extra_capability_justifications")
        if not isinstance(extra_justifications, dict):
            errors.append(f"{scenario_id} extra_capability_justifications must be an object")
            extra_justifications = {}
        selectable = required.union(expected_conditional).union({"delivery-orchestrator"})
        extra_capabilities = set(route).difference(selectable)
        missing_extra_justifications = extra_capabilities.difference(extra_justifications)
        unexpected_extra_justifications = set(extra_justifications).difference(extra_capabilities)
        if missing_extra_justifications:
            errors.append(
                f"{scenario_id} lacks justification for extra capabilities: "
                + ", ".join(sorted(missing_extra_justifications))
            )
        if unexpected_extra_justifications:
            errors.append(
                f"{scenario_id} justifies capabilities that are not extra: "
                + ", ".join(sorted(unexpected_extra_justifications))
            )
        for skill in extra_capabilities.intersection(extra_justifications):
            justification = extra_justifications[skill]
            if not isinstance(justification, dict):
                errors.append(f"{scenario_id} extra-capability justification for {skill} must be an object")
                continue
            rationale = justification.get("rationale")
            if not isinstance(rationale, str) or len(rationale.strip()) < 12:
                errors.append(f"{scenario_id} extra-capability justification for {skill} lacks a substantive rationale")
            if not validate_string_list(justification.get("evidence"), require_nonempty=True):
                errors.append(f"{scenario_id} extra-capability justification for {skill} lacks evidence")

        if receipt.get("delivery_result") != "not-run":
            errors.append(
                f"{scenario_id} delivery_result must be not-run; this checker is route-only"
            )
        if not validate_string_list(receipt.get("evidence"), require_nonempty=True):
            errors.append(f"{scenario_id} evidence must be a non-empty string list")
        if not validate_string_list(receipt.get("gaps")):
            errors.append(f"{scenario_id} gaps must be a string list")

    return errors, len(selected_ids), str(evidence_class)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    receipt_path = Path(args.receipts).expanduser().resolve()
    errors, scenario_count, evidence_class = validate(
        root,
        receipt_path,
        args.allow_subset,
        args.allow_historical_annotations,
    )
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    if evidence_class == HISTORICAL_EVIDENCE_CLASS:
        print(
            f"PASS scenarios={scenario_count} historical_route_shape_records={scenario_count} "
            "current_policy_claim=not-established "
            f"evidence_class={evidence_class}"
        )
    else:
        print(
            f"PASS scenarios={scenario_count} route_policy_records={scenario_count} "
            f"evidence_class={evidence_class}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
