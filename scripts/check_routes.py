#!/usr/bin/env python3
"""Validate authored route contracts without claiming interactive behavior."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


ALLOWED_AUTHORITIES = {
    "change",
    "coordination-only",
    "design-only",
    "documentation-change",
    "incident",
    "planning-only",
    "release-preparation",
    "review-only",
}
REQUIRED_SCENARIO_FIELDS = {
    "id",
    "prompt",
    "scale",
    "risk",
    "authority",
    "expected_route",
    "expected_artifacts",
    "required_evidence",
    "stop_conditions",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1]),
        help="plugin root",
    )
    return parser.parse_args(argv)


def validate(root: Path) -> tuple[list[str], int, set[str]]:
    errors: list[str] = []
    contract_path = root / "tests" / "route-contracts.json"
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"invalid route contract file: {error}"], 0, set()

    if contract.get("evidence_class") != "static authored-route contract":
        errors.append("route suite must identify itself as static authored-route evidence")
    if not contract.get("limitations"):
        errors.append("route suite must state its behavioral-proof limitation")

    legacy_names = contract.get("forbidden_runtime_dependencies")
    if not isinstance(legacy_names, list) or not {"boss", "epic", "superpowers"}.issubset(
        set(legacy_names)
    ):
        errors.append("route suite must forbid the known superseded runtime dependencies")

    available_skills = {
        path.parent.name for path in (root / "skills").glob("*/SKILL.md")
    }
    scenarios = contract.get("scenarios")
    if not isinstance(scenarios, list):
        return errors + ["scenarios must be a list"], 0, set()
    if len(scenarios) != 17:
        errors.append(f"expected 17 canonical scenarios, found {len(scenarios)}")

    seen_ids: set[str] = set()
    referenced_skills: set[str] = set()
    started = time.monotonic()
    for index, scenario in enumerate(scenarios, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(scenarios) - index)
        scenario_id = scenario.get("id", f"index-{index}") if isinstance(scenario, dict) else f"index-{index}"
        print(f"ROUTE [{index}/{len(scenarios)}] id={scenario_id} eta={eta:.1f}s", flush=True)
        if not isinstance(scenario, dict):
            errors.append(f"scenario {index} is not an object")
            continue
        missing = REQUIRED_SCENARIO_FIELDS.difference(scenario)
        if missing:
            errors.append(f"{scenario_id} missing fields: {', '.join(sorted(missing))}")
        if scenario_id in seen_ids:
            errors.append(f"duplicate scenario ID: {scenario_id}")
        seen_ids.add(scenario_id)
        if scenario.get("authority") not in ALLOWED_AUTHORITIES:
            errors.append(f"{scenario_id} has unsupported authority: {scenario.get('authority')}")
        for field in ("expected_route", "expected_artifacts", "required_evidence", "stop_conditions"):
            value = scenario.get(field)
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                errors.append(f"{scenario_id} field {field} must be a non-empty string list")
        route = scenario.get("expected_route", [])
        if isinstance(route, list):
            referenced_skills.update(item for item in route if isinstance(item, str))
            unknown = set(route).difference(available_skills)
            if unknown:
                errors.append(f"{scenario_id} references unknown skills: {', '.join(sorted(unknown))}")
            forbidden_in_route = set(route).intersection(set(legacy_names or []))
            if forbidden_in_route:
                errors.append(
                    f"{scenario_id} routes through forbidden dependencies: "
                    f"{', '.join(sorted(forbidden_in_route))}"
                )

    missing_skill_coverage = available_skills.difference(referenced_skills)
    if missing_skill_coverage:
        errors.append(
            "canonical route suite does not exercise skills: "
            + ", ".join(sorted(missing_skill_coverage))
        )
    return errors, len(scenarios), referenced_skills


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    errors, scenario_count, referenced_skills = validate(root)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(
        f"PASS scenarios={scenario_count} referenced_skills={len(referenced_skills)} "
        "evidence=static-contracts"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
