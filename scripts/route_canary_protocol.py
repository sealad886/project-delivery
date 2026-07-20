#!/usr/bin/env python3
"""Prepare and capture sealed, semantics-blind Project Delivery canary evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import secrets
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from check_distribution_bundle import payload_sha256
from check_distribution_bundle import select_paths
from check_distribution_bundle import validate_source_boundary
from check_installed_parity import compare
from check_installed_parity import file_sha256


PLUGIN_NAME = "project-delivery"
PROTOCOL = "project-delivery sealed route canary coordinator v1"
LAUNCH_EVIDENCE_CLASS = "sealed route canary launch state"
CAPTURE_EVIDENCE_CLASS = "sealed route canary coordinator capture"
PAYLOAD_HASH_METHOD = "project-delivery length-prefixed path-and-content sha256 v1"
RAW_HASH_METHOD = "sha256 of exact raw bytes"
PRIVATE_BINDING_PROTOCOL = "project-delivery private route canary task binding v1"
TASK_PROMPT_PROTOCOL = "project-delivery canonical blind route task prompt v1"
MAX_CAPTURE_AGE_SECONDS = 6 * 60 * 60
UTC_SECOND = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PUBLIC_NONCE = re.compile(r"^canary-[0-9a-f]{32}$")
PUBLIC_RECEIPT = re.compile(
    r"^route-canary-\d{8}t\d{6}z-[0-9a-f]{12}$"
)
CACHEBUSTED_VERSION = re.compile(r"^(?P<base>[^+]+)\+codex\.[a-z0-9][a-z0-9-]*$")
LAUNCH_FIELDS = {
    "schema_version",
    "protocol",
    "evidence_class",
    "launch_time_utc",
    "public_run_nonce",
    "public_receipt_slug",
    "prompt_manifest",
    "task_prompt",
    "source_git",
    "plugin_identities",
    "parity",
    "marketplace_entry",
    "observation_boundary",
    "private_task_binding_contract",
}
CAPTURE_FIELDS = {
    "captured_at_utc",
    "coordinator_attestation",
    "evidence_class",
    "launch_state_sha256",
    "launch_time_utc",
    "marketplace_entry",
    "observation_boundary",
    "parity",
    "plugin_identities",
    "private_task_binding_sha256",
    "prompt_manifest",
    "task_prompt",
    "protocol",
    "public_receipt_slug",
    "public_run_nonce",
    "raw_observation",
    "schema_version",
    "source_git",
}
BINDING_FIELDS = {
    "schema_version",
    "protocol",
    "public_run_nonce",
    "public_receipt_slug",
    "launch_state_sha256",
    "internal_task_id",
    "task_created_at_utc",
    "task_prompt_sha256",
}
PRIVATE_TASK_BINDING_CONTRACT = {
    "schema_version": 1,
    "protocol": PRIVATE_BINDING_PROTOCOL,
    "required_fields": sorted(BINDING_FIELDS),
    "privacy": (
        "Keep file owner-only; capture publishes only SHA-256 of exact binding bytes."
    ),
}
COORDINATOR_ATTESTATION = {
    "statement": (
        "Coordinator attests only to byte and launch-state bindings listed in "
        "verified_claims."
    ),
    "verified_claims": [
        "Prompt-manifest raw bytes match their launch SHA-256.",
        "Canonical blind task-prompt raw bytes match their launch SHA-256.",
        "Source Git HEAD and clean porcelain-v1 status bytes are unchanged since launch.",
        "Canonical source, prepared personal source, and installed cache identities match launch.",
        "Prepared personal source and installed cache have exact byte parity.",
        "Canonical source is either exact or differs only by the supported Codex cachebuster version transformation.",
        "Installed path has the exact marketplace/plugin/version cache shape recorded at launch.",
        "Marketplace file and selected local plugin entry identities match launch.",
        "Private task-binding and raw observation bytes are bound by SHA-256.",
    ],
    "bounded_limitations": [
        "Capture did not inspect or grade expected route semantics.",
        "Raw-observation hashing does not prove observation truthfulness or model attention.",
        "Private task-binding hashing does not independently prove task isolation or execution provenance.",
        "Coordinator does not prove absence of unrecorded effects or legacy runtime activity.",
        "Coordinator makes no claim about route correctness, delivery readiness, release readiness, or decommission readiness.",
    ],
}


class ProtocolError(ValueError):
    """A sealed-canary precondition or binding check failed."""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare", help="record immutable launch facts before creating a fresh task"
    )
    prepare.add_argument("--repository-root", required=True)
    prepare.add_argument("--prompt-manifest", required=True)
    prepare.add_argument("--source-package", required=True)
    prepare.add_argument("--prepared-source", required=True)
    prepare.add_argument("--installed-cache", required=True)
    prepare.add_argument("--marketplace", required=True)
    prepare.add_argument(
        "--task-prompt-output",
        required=True,
        help="new file that receives the canonical blind task prompt",
    )
    prepare.add_argument(
        "--instruction-file",
        action="append",
        required=True,
        help="applicable controlling instruction file; repeat for each file",
    )
    prepare.add_argument(
        "--observation-mode",
        choices=("projectless",),
        required=True,
        help="route-observation repository boundary",
    )
    prepare.add_argument("--output", required=True)

    capture = subparsers.add_parser(
        "capture", help="bind raw task output without inspecting expected semantics"
    )
    capture.add_argument("--launch-state", required=True)
    capture.add_argument(
        "--expected-launch-sha256",
        required=True,
        help="exact launch SHA-256 printed by prepare and retained by the coordinator",
    )
    capture.add_argument("--observation", required=True)
    capture.add_argument("--task-binding", required=True)
    capture.add_argument("--output", required=True)
    return parser.parse_args(argv)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def parse_utc(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not UTC_SECOND.fullmatch(value):
        raise ProtocolError(f"{label} must be UTC YYYY-MM-DDTHH:MM:SSZ")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_nonempty_bytes(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ProtocolError(f"{label} must be a regular non-symlink file: {path}")
    value = path.read_bytes()
    if not value:
        raise ProtocolError(f"{label} must not be empty: {path}")
    return value


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return sha256_bytes(encoded)


def exact_fields(value: dict[str, object], expected: set[str], label: str) -> None:
    missing = expected.difference(value)
    extra = set(value).difference(expected)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append("missing=" + ",".join(sorted(missing)))
        if extra:
            details.append("extra=" + ",".join(sorted(extra)))
        raise ProtocolError(f"{label} fields differ: {' '.join(details)}")


def write_new_json(
    path: Path,
    value: dict[str, object],
    *,
    mode: int = 0o644,
) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        try:
            path.unlink()
        except OSError:
            pass
        raise
    return rendered


def git_output(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ProtocolError(f"Git inspection failed for {' '.join(arguments)}")
    return result.stdout


def source_git_identity(root: Path) -> dict[str, object]:
    if not root.is_dir():
        raise ProtocolError(f"repository root is not a directory: {root}")
    discovered = Path(
        git_output(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    ).resolve()
    if discovered != root:
        raise ProtocolError(
            f"repository root must be exact Git top level: expected={root} found={discovered}"
        )
    head = git_output(root, "rev-parse", "--verify", "HEAD").decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", head):
        raise ProtocolError("Git HEAD is not a full hexadecimal object ID")
    status_bytes = git_output(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignore-submodules=none",
    )
    if status_bytes:
        raise ProtocolError("source Git worktree must be clean before canary launch")
    return {
        "root": str(root),
        "head": head,
        "status_format": (
            "git status --porcelain=v1 -z --untracked-files=all --ignore-submodules=none"
        ),
        "status_sha256": sha256_bytes(status_bytes),
        "status_byte_count": len(status_bytes),
        "clean": True,
    }


def count_expected_directories(selected: list[Path]) -> int:
    directories: set[Path] = set()
    started = time.monotonic()
    for index, relative in enumerate(selected, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(selected) - index)
        print(
            f"DIRECTORIES [{index}/{len(selected)}] file={relative} eta={eta:.1f}s",
            flush=True,
        )
        parent = relative.parent
        while parent != Path("."):
            directories.add(parent)
            parent = parent.parent
    return len(directories)


def plugin_identity(root: Path) -> tuple[dict[str, object], list[Path]]:
    if not root.is_dir():
        raise ProtocolError(f"plugin tree is not a directory: {root}")
    try:
        selected = sorted(select_paths(root))
        boundary_errors = validate_source_boundary(root, selected)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ProtocolError(f"plugin identity inspection failed: {error}") from error
    if boundary_errors:
        raise ProtocolError("plugin tree boundary failed: " + "; ".join(boundary_errors))

    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest_bytes = read_nonempty_bytes(manifest_path, "plugin manifest")
    try:
        manifest = json.loads(manifest_bytes)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"plugin manifest is invalid JSON: {error}") from error
    if not isinstance(manifest, dict):
        raise ProtocolError("plugin manifest root must be an object")
    name = manifest.get("name")
    version = manifest.get("version")
    if name != PLUGIN_NAME:
        raise ProtocolError(f"plugin manifest name must be {PLUGIN_NAME!r}")
    if not isinstance(version, str) or not version:
        raise ProtocolError("plugin manifest version must be a non-empty string")
    return (
        {
            "path": str(root),
            "name": name,
            "version": version,
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "file_count": len(selected),
            "directory_count": count_expected_directories(selected),
            "payload_sha256": payload_sha256(root, selected),
            "payload_hash_method": PAYLOAD_HASH_METHOD,
        },
        selected,
    )


def cache_shape(root: Path, identity: dict[str, object]) -> dict[str, str]:
    if len(root.parts) < 5:
        raise ProtocolError("installed plugin path is not cache-shaped")
    plugins, cache, marketplace, plugin, version = root.parts[-5:]
    if plugins != "plugins" or cache != "cache":
        raise ProtocolError(
            "installed plugin path must end in plugins/cache/<marketplace>/<plugin>/<version>"
        )
    if plugin != identity["name"] or version != identity["version"]:
        raise ProtocolError(
            "installed cache path plugin/version must match installed manifest"
        )
    if not marketplace or marketplace in {".", ".."}:
        raise ProtocolError("installed cache marketplace path segment is invalid")
    return {
        "marketplace": marketplace,
        "cache_relative_path": "/".join(root.parts[-5:]),
    }


def source_prepared_relation(
    source_root: Path,
    source_identity: dict[str, object],
    source_selected: list[Path],
    prepared_root: Path,
    prepared_identity: dict[str, object],
    prepared_selected: list[Path],
) -> dict[str, object]:
    if source_identity["payload_sha256"] == prepared_identity["payload_sha256"]:
        return {
            "mode": "exact-byte-parity",
            "file_count": source_identity["file_count"],
            "source_payload_sha256": source_identity["payload_sha256"],
            "prepared_payload_sha256": prepared_identity["payload_sha256"],
        }
    if source_selected != prepared_selected:
        raise ProtocolError("source/prepared selected path sets differ")

    manifest_relative = Path(".codex-plugin/plugin.json")
    started = time.monotonic()
    comparable = [path for path in source_selected if path != manifest_relative]
    for index, relative in enumerate(comparable, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(comparable) - index)
        print(
            f"CACHEBUSTER [{index}/{len(comparable)}] file={relative} eta={eta:.1f}s",
            flush=True,
        )
        if file_sha256(source_root / relative) != file_sha256(prepared_root / relative):
            raise ProtocolError(
                f"source/prepared content differs outside manifest: {relative}"
            )

    source_manifest = json.loads((source_root / manifest_relative).read_text(encoding="utf-8"))
    prepared_manifest = json.loads(
        (prepared_root / manifest_relative).read_text(encoding="utf-8")
    )
    source_version = source_manifest.get("version")
    prepared_version = prepared_manifest.get("version")
    if not isinstance(source_version, str) or not isinstance(prepared_version, str):
        raise ProtocolError("source/prepared manifest version is invalid")
    match = CACHEBUSTED_VERSION.fullmatch(prepared_version)
    expected_base = source_version.split("+", 1)[0]
    if match is None or match.group("base") != expected_base:
        raise ProtocolError(
            "prepared manifest version is not a supported Codex cachebuster of source version"
        )
    normalized = copy.deepcopy(prepared_manifest)
    normalized["version"] = source_version
    if normalized != source_manifest:
        raise ProtocolError(
            "source/prepared manifests differ by more than supported cachebuster version"
        )
    expected_prepared_manifest = copy.deepcopy(source_manifest)
    expected_prepared_manifest["version"] = prepared_version
    expected_prepared_bytes = (
        json.dumps(expected_prepared_manifest, indent=2) + "\n"
    ).encode("utf-8")
    actual_prepared_bytes = (prepared_root / manifest_relative).read_bytes()
    if actual_prepared_bytes != expected_prepared_bytes:
        raise ProtocolError(
            "prepared manifest does not match exact Plugin Creator cachebuster serialization"
        )
    return {
        "mode": "manifest-version-cachebuster-only",
        "file_count": source_identity["file_count"],
        "source_version": source_version,
        "prepared_version": prepared_version,
        "source_payload_sha256": source_identity["payload_sha256"],
        "prepared_payload_sha256": prepared_identity["payload_sha256"],
    }


def prepared_installed_relation(
    prepared_root: Path, installed_root: Path
) -> dict[str, object]:
    errors, file_count, digest = compare(prepared_root, installed_root)
    if errors:
        raise ProtocolError("prepared/installed parity failed: " + "; ".join(errors))
    return {
        "mode": "exact-byte-parity",
        "file_count": file_count,
        "payload_sha256": digest,
    }


def source_installed_relation(
    source_prepared: dict[str, object],
    source_identity: dict[str, object],
    installed_identity: dict[str, object],
) -> dict[str, object]:
    relation = {
        "mode": source_prepared["mode"],
        "file_count": source_identity["file_count"],
        "source_payload_sha256": source_identity["payload_sha256"],
        "installed_payload_sha256": installed_identity["payload_sha256"],
    }
    if source_prepared["mode"] == "manifest-version-cachebuster-only":
        relation.update(
            {
                "source_version": source_identity["version"],
                "installed_version": installed_identity["version"],
            }
        )
    return relation


def marketplace_identity(
    marketplace_path: Path,
    prepared_root: Path,
    prepared_identity: dict[str, object],
) -> dict[str, object]:
    raw = read_nonempty_bytes(marketplace_path, "marketplace file")
    try:
        marketplace = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"marketplace is invalid JSON: {error}") from error
    if not isinstance(marketplace, dict):
        raise ProtocolError("marketplace root must be an object")
    marketplace_name = marketplace.get("name")
    if not isinstance(marketplace_name, str) or not marketplace_name:
        raise ProtocolError("marketplace name must be a non-empty string")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        raise ProtocolError("marketplace plugins must be an array")
    matches: list[dict[str, object]] = []
    started = time.monotonic()
    for index, item in enumerate(plugins, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(plugins) - index)
        plugin_name = item.get("name") if isinstance(item, dict) else "<invalid>"
        print(
            f"MARKETPLACE [{index}/{len(plugins)}] plugin={plugin_name} eta={eta:.1f}s",
            flush=True,
        )
        if isinstance(item, dict) and item.get("name") == PLUGIN_NAME:
            matches.append(item)
    if len(matches) != 1:
        raise ProtocolError(
            f"marketplace must contain exactly one {PLUGIN_NAME!r} entry"
        )
    entry = matches[0]
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local":
        raise ProtocolError("selected marketplace entry must have a local source")
    source_path = source.get("path")
    if not isinstance(source_path, str) or not source_path:
        raise ProtocolError("marketplace local source path must be a non-empty string")
    relative = Path(source_path.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise ProtocolError("marketplace local source path must remain inside marketplace root")
    marketplace_root = marketplace_path.parent
    if (
        marketplace_path.name == "marketplace.json"
        and marketplace_path.parent.name == "plugins"
        and marketplace_path.parent.parent.name == ".agents"
    ):
        # Plugin Creator stores the personal catalog under ~/.agents/plugins
        # while its local source paths resolve from the home-level plugin root.
        marketplace_root = marketplace_path.parent.parent.parent
    resolved_target = (marketplace_root / relative).resolve()
    if resolved_target != prepared_root:
        raise ProtocolError(
            "marketplace selected entry does not resolve to prepared personal source"
        )
    return {
        "path": str(marketplace_path),
        "file_sha256": sha256_bytes(raw),
        "marketplace_name": marketplace_name,
        "plugin_name": PLUGIN_NAME,
        "entry_sha256": canonical_json_sha256(entry),
        "entry_hash_method": "sha256 of canonical sorted compact JSON",
        "source_type": "local",
        "source_path": source_path,
        "resolved_target": str(resolved_target),
        "target_payload_sha256": prepared_identity["payload_sha256"],
    }


def file_identity(path: Path, label: str = "prompt manifest") -> dict[str, object]:
    value = read_nonempty_bytes(path, label)
    return {
        "path": str(path),
        "sha256": sha256_bytes(value),
        "byte_count": len(value),
        "hash_method": RAW_HASH_METHOD,
    }


def validate_prompt_manifest(raw: bytes) -> dict[str, object]:
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"prompt manifest is invalid JSON: {error}") from error
    if not isinstance(manifest, dict):
        raise ProtocolError("prompt manifest root must be an object")
    exact_fields(
        manifest,
        {
            "evidence_class",
            "scenarios",
            "schema_version",
            "source_contract_schema_version",
        },
        "prompt manifest",
    )
    if (
        manifest.get("schema_version") != 1
        or manifest.get("source_contract_schema_version") != 2
        or manifest.get("evidence_class") != "prompt-only blind canary input"
    ):
        raise ProtocolError("prompt manifest protocol identity is invalid")
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ProtocolError("prompt manifest scenarios must be a non-empty array")
    seen: set[str] = set()
    for index, scenario in enumerate(scenarios, 1):
        if not isinstance(scenario, dict):
            raise ProtocolError(f"prompt manifest scenario {index} must be an object")
        exact_fields(scenario, {"id", "prompt"}, f"prompt manifest scenario {index}")
        scenario_id = scenario.get("id")
        prompt = scenario.get("prompt")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise ProtocolError(f"prompt manifest scenario {index} has an invalid ID")
        if scenario_id in seen:
            raise ProtocolError(f"prompt manifest has duplicate scenario ID: {scenario_id}")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ProtocolError(f"prompt manifest scenario {scenario_id} has an invalid prompt")
        seen.add(scenario_id)
    return manifest


def render_task_prompt(
    prompt_manifest_raw: bytes,
    public_run_nonce: str,
    public_receipt_slug: str,
    source_git: dict[str, object],
    installed_identity: dict[str, object],
) -> bytes:
    manifest = validate_prompt_manifest(prompt_manifest_raw)
    receipt_identity = {
        "name": installed_identity["name"],
        "installed_version": installed_identity["version"],
        "source_revision": source_git["head"],
        "manifest_sha256": installed_identity["manifest_sha256"],
        "payload_sha256": installed_identity["payload_sha256"],
        "payload_hash_method": installed_identity["payload_hash_method"],
        "cache_relative_path": installed_identity["cache_relative_path"],
    }
    manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
    identity_json = json.dumps(receipt_identity, indent=2, ensure_ascii=False)
    rendered = f"""{TASK_PROMPT_PROTOCOL}

Perform a blind, route-only Project Delivery canary in this projectless task. This is an observation, not delivery work.

Hard boundaries:
- Use the installed `project-delivery:delivery-orchestrator` and every selected Project Delivery specialist. Read each selected skill and every directly referenced installed `.shared` instruction file completely before freezing semantics.
- Do not open or inspect the Project Delivery source repository, route contracts, checker scripts, coordinator state, prior task output, expected routes, or grading criteria.
- Do not edit a repository; invoke a legacy workflow; start a legacy hook, MCP server, or app; create legacy-branded state; contact a provider; or perform any release, installation, publication, deployment, signing, communication, or other consequential effect.
- Use exactly three subagents for disjoint scenario partitions, then merge their blind observations in this root task. Each subagent must follow the same boundaries and load instructions from the installed plugin.
- Derive conditional trigger statements only from installed runtime instructions. Do not invent a hidden expected-contract branch. Distinguish pre-existing outcomes from canary delivery, which remains `not-run`.
- Freeze every schema-v3 semantic field before any expected-contract access. No expected-contract access is permitted in this task.

Output contract:
- Return exactly one JSON object conforming to the installed `skills/.shared/live-route-receipt-v3.schema.json`; return no Markdown fence or prose.
- Preserve the scenario order and exact IDs/prompts below.
- Use the exact mechanically supplied plugin identity and public receipt slug below. Set `repository_identity` to name `projectless-canary`, revision `not-applicable`, and working-tree state `no-repository`.
- Set `task_identity.selected_at` to the actual UTC selection time within this task. Compute the canonical semantic-envelope digest exactly as the installed template specifies.
- Root observation lists must equal the sorted unique union of their scenario-local counterparts. Record all gaps structurally and truthfully; a blocker remains a blocker.

Public run nonce: {public_run_nonce}
Public receipt slug: {public_receipt_slug}

Mechanically supplied plugin identity:
{identity_json}

Prompt-only blind manifest:
{manifest_json}
"""
    return rendered.encode("utf-8")


def observation_boundary_identity(
    mode: str,
    instruction_files: list[Path],
) -> dict[str, object]:
    if mode != "projectless":
        raise ProtocolError(f"unsupported observation mode: {mode}")
    if not instruction_files:
        raise ProtocolError("projectless observation requires instruction evidence")
    identities = []
    seen: set[Path] = set()
    for index, path in enumerate(instruction_files, 1):
        if path in seen:
            raise ProtocolError(f"duplicate controlling instruction file: {path}")
        seen.add(path)
        identities.append(
            {
                "label": f"instruction-{index}-{path.name}",
                **file_identity(path, "controlling instruction file"),
            }
        )
    return {
        "mode": "projectless",
        "repository_name": "not-applicable",
        "revision": "not-applicable",
        "working_tree_state": "no-repository",
        "instruction_files": identities,
    }


def ensure_distinct_paths(paths: dict[str, Path]) -> None:
    reverse: dict[Path, list[str]] = {}
    for label, path in paths.items():
        reverse.setdefault(path, []).append(label)
    collisions = [labels for labels in reverse.values() if len(labels) > 1]
    if collisions:
        raise ProtocolError(
            "source, prepared, and installed plugin paths must be distinct: "
            + "; ".join("/".join(labels) for labels in collisions)
        )


def collect_facts(
    repository_root: Path,
    prompt_manifest: Path,
    source_package: Path,
    prepared_source: Path,
    installed_cache: Path,
    marketplace: Path,
    observation_mode: str,
    instruction_files: list[Path],
) -> dict[str, object]:
    ensure_distinct_paths(
        {
            "source": source_package,
            "prepared": prepared_source,
            "installed": installed_cache,
        }
    )
    if not source_package.is_relative_to(repository_root):
        raise ProtocolError("canonical source package must be inside source repository")

    git_identity = source_git_identity(repository_root)
    prompt_identity = file_identity(prompt_manifest)
    source_identity, source_selected = plugin_identity(source_package)
    prepared_identity, prepared_selected = plugin_identity(prepared_source)
    installed_identity, _ = plugin_identity(installed_cache)
    installed_shape = cache_shape(installed_cache, installed_identity)
    source_prepared = source_prepared_relation(
        source_package,
        source_identity,
        source_selected,
        prepared_source,
        prepared_identity,
        prepared_selected,
    )
    prepared_installed = prepared_installed_relation(prepared_source, installed_cache)
    source_installed = source_installed_relation(
        source_prepared, source_identity, installed_identity
    )
    marketplace_entry = marketplace_identity(
        marketplace, prepared_source, prepared_identity
    )
    observation_boundary = observation_boundary_identity(
        observation_mode,
        instruction_files,
    )
    if marketplace_entry["marketplace_name"] != installed_shape["marketplace"]:
        raise ProtocolError(
            "installed cache marketplace segment does not match marketplace name"
        )
    installed_identity = {**installed_identity, **installed_shape}
    return {
        "prompt_manifest": prompt_identity,
        "source_git": git_identity,
        "plugin_identities": {
            "source_package": source_identity,
            "prepared_personal_source": prepared_identity,
            "installed_cache": installed_identity,
        },
        "parity": {
            "source_to_prepared": source_prepared,
            "prepared_to_installed": prepared_installed,
            "source_to_installed": source_installed,
        },
        "marketplace_entry": marketplace_entry,
        "observation_boundary": observation_boundary,
    }


def prepare(args: argparse.Namespace) -> int:
    repository_root = Path(args.repository_root).expanduser().resolve()
    prompt_manifest = Path(args.prompt_manifest).expanduser().resolve()
    source_package = Path(args.source_package).expanduser().resolve()
    prepared_source = Path(args.prepared_source).expanduser().resolve()
    installed_cache = Path(args.installed_cache).expanduser().resolve()
    marketplace = Path(args.marketplace).expanduser().resolve()
    instruction_files = [
        Path(value).expanduser().resolve() for value in args.instruction_file
    ]
    task_prompt_output = Path(args.task_prompt_output).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    for label, candidate in (
        ("launch state output", output),
        ("task prompt output", task_prompt_output),
    ):
        if candidate.is_relative_to(repository_root):
            raise ProtocolError(f"{label} must remain outside source repository")
    if output == task_prompt_output:
        raise ProtocolError("launch state and task prompt outputs must be distinct")

    facts = collect_facts(
        repository_root,
        prompt_manifest,
        source_package,
        prepared_source,
        installed_cache,
        marketplace,
        args.observation_mode,
        instruction_files,
    )
    launch_time = utc_now()
    nonce = "canary-" + secrets.token_hex(16)
    receipt_slug = (
        "route-canary-"
        + launch_time.replace("-", "").replace(":", "").lower()
        + "-"
        + nonce.removeprefix("canary-")[:12]
    )
    prompt_manifest_raw = read_nonempty_bytes(prompt_manifest, "prompt manifest")
    plugin_identities = facts.get("plugin_identities")
    source_git = facts.get("source_git")
    if not isinstance(plugin_identities, dict) or not isinstance(source_git, dict):
        raise ProtocolError("collected launch identities are invalid")
    installed_identity = plugin_identities.get("installed_cache")
    if not isinstance(installed_identity, dict):
        raise ProtocolError("collected installed identity is invalid")
    task_prompt_raw = render_task_prompt(
        prompt_manifest_raw,
        nonce,
        receipt_slug,
        source_git,
        installed_identity,
    )
    task_prompt_identity = {
        "path": str(task_prompt_output),
        "sha256": sha256_bytes(task_prompt_raw),
        "byte_count": len(task_prompt_raw),
        "hash_method": RAW_HASH_METHOD,
        "prompt_protocol": TASK_PROMPT_PROTOCOL,
    }
    launch = {
        "schema_version": 1,
        "protocol": PROTOCOL,
        "evidence_class": LAUNCH_EVIDENCE_CLASS,
        "launch_time_utc": launch_time,
        "public_run_nonce": nonce,
        "public_receipt_slug": receipt_slug,
        **facts,
        "task_prompt": task_prompt_identity,
        "private_task_binding_contract": PRIVATE_TASK_BINDING_CONTRACT,
    }
    task_prompt_written = False
    try:
        descriptor = os.open(
            task_prompt_output,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o644,
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(task_prompt_raw)
            handle.flush()
            os.fsync(handle.fileno())
        task_prompt_written = True
        rendered = write_new_json(output, launch, mode=0o600)
    except BaseException:
        if task_prompt_written and not output.exists():
            try:
                task_prompt_output.unlink()
            except OSError:
                pass
        raise
    print(
        f"PREPARED receipt={receipt_slug} launch_sha256={sha256_bytes(rendered)} "
        f"task_prompt_sha256={sha256_bytes(task_prompt_raw)} "
        f"output={output} task_prompt={task_prompt_output}",
        flush=True,
    )
    return 0


def read_launch(path: Path) -> tuple[dict[str, object], bytes]:
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0
    if mode & 0o077:
        raise ProtocolError("launch state permissions must be owner-only")
    raw = read_nonempty_bytes(path, "launch state")
    try:
        launch = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"launch state is invalid JSON: {error}") from error
    if not isinstance(launch, dict):
        raise ProtocolError("launch state root must be an object")
    exact_fields(launch, LAUNCH_FIELDS, "launch state")
    if (
        launch.get("schema_version") != 1
        or launch.get("protocol") != PROTOCOL
        or launch.get("evidence_class") != LAUNCH_EVIDENCE_CLASS
    ):
        raise ProtocolError("launch state protocol identity is invalid")
    nonce = launch.get("public_run_nonce")
    slug = launch.get("public_receipt_slug")
    if not isinstance(nonce, str) or not PUBLIC_NONCE.fullmatch(nonce):
        raise ProtocolError("launch public run nonce is invalid")
    if not isinstance(slug, str) or not PUBLIC_RECEIPT.fullmatch(slug):
        raise ProtocolError("launch public receipt slug is invalid")
    if not slug.endswith(nonce.removeprefix("canary-")[:12]):
        raise ProtocolError("launch public receipt slug is not bound to run nonce")
    parse_utc(launch.get("launch_time_utc"), "launch_time_utc")
    if launch.get("private_task_binding_contract") != PRIVATE_TASK_BINDING_CONTRACT:
        raise ProtocolError("launch private task-binding contract is invalid")
    return launch, raw


def private_binding_identity(
    path: Path,
    launch: dict[str, object],
    launch_sha256: str,
    captured_at: datetime,
) -> tuple[str, str]:
    if path.is_symlink() or not path.is_file():
        raise ProtocolError("private task-binding must be a regular non-symlink file")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise ProtocolError("private task-binding permissions must be owner-only")
    raw = read_nonempty_bytes(path, "private task-binding")
    try:
        binding = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"private task-binding is invalid JSON: {error}") from error
    if not isinstance(binding, dict):
        raise ProtocolError("private task-binding root must be an object")
    exact_fields(binding, BINDING_FIELDS, "private task-binding")
    if binding.get("schema_version") != 1 or binding.get("protocol") != PRIVATE_BINDING_PROTOCOL:
        raise ProtocolError("private task-binding protocol identity is invalid")
    for field in ("public_run_nonce", "public_receipt_slug"):
        if binding.get(field) != launch.get(field):
            raise ProtocolError(f"private task-binding {field} does not match launch")
    if binding.get("launch_state_sha256") != launch_sha256:
        raise ProtocolError("private task-binding launch SHA-256 does not match launch bytes")
    task_prompt = launch.get("task_prompt")
    if not isinstance(task_prompt, dict) or (
        binding.get("task_prompt_sha256") != task_prompt.get("sha256")
    ):
        raise ProtocolError(
            "private task-binding task prompt SHA-256 does not match launch"
        )
    internal_task_id = binding.get("internal_task_id")
    if not isinstance(internal_task_id, str) or len(internal_task_id.strip()) < 16:
        raise ProtocolError("private task-binding internal task ID is missing or too short")
    task_created = parse_utc(binding.get("task_created_at_utc"), "task_created_at_utc")
    launch_time = parse_utc(launch.get("launch_time_utc"), "launch_time_utc")
    if task_created < launch_time or task_created > captured_at:
        raise ProtocolError("private task-binding timestamp is outside launch/capture window")
    return sha256_bytes(raw), internal_task_id


def facts_from_launch(launch: dict[str, object]) -> dict[str, object]:
    prompt = launch.get("prompt_manifest")
    source_git = launch.get("source_git")
    identities = launch.get("plugin_identities")
    marketplace = launch.get("marketplace_entry")
    observation_boundary = launch.get("observation_boundary")
    task_prompt = launch.get("task_prompt")
    if not all(
        isinstance(item, dict)
        for item in (
            prompt,
            source_git,
            identities,
            marketplace,
            observation_boundary,
            task_prompt,
        )
    ):
        raise ProtocolError("launch facts have invalid object structure")
    assert isinstance(prompt, dict)
    assert isinstance(source_git, dict)
    assert isinstance(identities, dict)
    assert isinstance(marketplace, dict)
    assert isinstance(observation_boundary, dict)
    assert isinstance(task_prompt, dict)
    expected_identity_keys = {
        "source_package",
        "prepared_personal_source",
        "installed_cache",
    }
    if set(identities) != expected_identity_keys:
        raise ProtocolError("launch plugin identity set is invalid")
    identity_values = [identities[key] for key in sorted(expected_identity_keys)]
    if not all(isinstance(item, dict) for item in identity_values):
        raise ProtocolError("launch plugin identities must be objects")
    instruction_files = observation_boundary.get("instruction_files")
    if not isinstance(instruction_files, list) or not instruction_files:
        raise ProtocolError("launch observation boundary lacks instruction files")
    instruction_paths: list[Path] = []
    for item in instruction_files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ProtocolError(
                "launch observation boundary instruction identity is invalid"
            )
        instruction_paths.append(Path(item["path"]).expanduser().resolve())
    facts = collect_facts(
        Path(str(source_git.get("root"))).expanduser().resolve(),
        Path(str(prompt.get("path"))).expanduser().resolve(),
        Path(str(identities["source_package"].get("path"))).expanduser().resolve(),
        Path(str(identities["prepared_personal_source"].get("path"))).expanduser().resolve(),
        Path(str(identities["installed_cache"].get("path"))).expanduser().resolve(),
        Path(str(marketplace.get("path"))).expanduser().resolve(),
        str(observation_boundary.get("mode")),
        instruction_paths,
    )
    task_prompt_identity = file_identity(
        Path(str(task_prompt.get("path"))).expanduser().resolve(),
        "canonical blind task prompt",
    )
    task_prompt_identity["prompt_protocol"] = TASK_PROMPT_PROTOCOL
    facts["task_prompt"] = task_prompt_identity
    return facts


def public_file_identity(identity: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in identity.items() if key != "path"}


def public_source_git(identity: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in identity.items() if key != "root"}


def public_plugin_identities(
    identities: dict[str, object],
) -> dict[str, object]:
    projected: dict[str, object] = {}
    for label, raw_identity in identities.items():
        if not isinstance(raw_identity, dict):
            raise ProtocolError(f"plugin identity {label} is invalid")
        projected[label] = {
            key: value for key, value in raw_identity.items() if key != "path"
        }
    return projected


def public_marketplace_identity(identity: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in identity.items()
        if key not in {"path", "resolved_target"}
    }


def public_observation_boundary(identity: dict[str, object]) -> dict[str, object]:
    instruction_files = identity.get("instruction_files")
    if not isinstance(instruction_files, list):
        raise ProtocolError("observation boundary instruction files are invalid")
    public_instructions: list[dict[str, object]] = []
    for item in instruction_files:
        if not isinstance(item, dict):
            raise ProtocolError("observation boundary instruction identity is invalid")
        public_instructions.append(
            {key: value for key, value in item.items() if key != "path"}
        )
    return {
        **{
            key: value
            for key, value in identity.items()
            if key != "instruction_files"
        },
        "instruction_files": public_instructions,
    }


def capture(args: argparse.Namespace) -> int:
    launch_path = Path(args.launch_state).expanduser().resolve()
    observation_path = Path(args.observation).expanduser().resolve()
    binding_path = Path(args.task_binding).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    launch, launch_raw = read_launch(launch_path)
    source_git_at_launch = launch.get("source_git")
    if not isinstance(source_git_at_launch, dict):
        raise ProtocolError("launch source_git must be an object")
    repository_root = Path(str(source_git_at_launch.get("root"))).expanduser().resolve()
    if output.is_relative_to(repository_root):
        raise ProtocolError("capture output must remain outside source repository")
    launch_sha = sha256_bytes(launch_raw)
    if not re.fullmatch(r"[0-9a-f]{64}", args.expected_launch_sha256):
        raise ProtocolError("expected launch SHA-256 must be 64 lowercase hexadecimal characters")
    if launch_sha != args.expected_launch_sha256:
        raise ProtocolError("launch state SHA-256 does not match externally retained prepare seal")
    captured_at_text = utc_now()
    captured_at = parse_utc(captured_at_text, "captured_at_utc")
    launch_time = parse_utc(launch.get("launch_time_utc"), "launch_time_utc")
    elapsed_seconds = (captured_at - launch_time).total_seconds()
    if elapsed_seconds < 0 or elapsed_seconds > MAX_CAPTURE_AGE_SECONDS:
        raise ProtocolError(
            "capture timestamp is outside the permitted six-hour launch window"
        )
    binding_sha, internal_task_id = private_binding_identity(
        binding_path, launch, launch_sha, captured_at
    )
    observation = read_nonempty_bytes(observation_path, "raw observation")
    current_facts = facts_from_launch(launch)
    expected_facts = {
        key: launch[key]
        for key in (
            "prompt_manifest",
            "source_git",
            "plugin_identities",
            "parity",
            "marketplace_entry",
            "observation_boundary",
            "task_prompt",
        )
    }
    if current_facts != expected_facts:
        changed = [
            key
            for key in expected_facts
            if current_facts.get(key) != expected_facts.get(key)
        ]
        raise ProtocolError("launch state changed since prepare: " + ", ".join(changed))

    source_git = current_facts["source_git"]
    prompt = current_facts["prompt_manifest"]
    identities = current_facts["plugin_identities"]
    parity = current_facts["parity"]
    marketplace = current_facts["marketplace_entry"]
    observation_boundary = current_facts["observation_boundary"]
    task_prompt = current_facts["task_prompt"]
    if not all(
        isinstance(item, dict)
        for item in (
            source_git,
            prompt,
            identities,
            marketplace,
            observation_boundary,
            task_prompt,
        )
    ):
        raise ProtocolError("current facts have invalid object structure")
    assert isinstance(source_git, dict)
    assert isinstance(prompt, dict)
    assert isinstance(identities, dict)
    assert isinstance(marketplace, dict)
    assert isinstance(observation_boundary, dict)
    assert isinstance(task_prompt, dict)
    result = {
        "schema_version": 1,
        "protocol": PROTOCOL,
        "evidence_class": CAPTURE_EVIDENCE_CLASS,
        "launch_time_utc": launch["launch_time_utc"],
        "captured_at_utc": captured_at_text,
        "public_run_nonce": launch["public_run_nonce"],
        "public_receipt_slug": launch["public_receipt_slug"],
        "launch_state_sha256": launch_sha,
        "prompt_manifest": public_file_identity(prompt),
        "task_prompt": public_file_identity(task_prompt),
        "source_git": public_source_git(source_git),
        "plugin_identities": public_plugin_identities(identities),
        "parity": parity,
        "marketplace_entry": public_marketplace_identity(marketplace),
        "observation_boundary": public_observation_boundary(
            observation_boundary
        ),
        "private_task_binding_sha256": binding_sha,
        "raw_observation": {
            "sha256": sha256_bytes(observation),
            "byte_count": len(observation),
            "hash_method": RAW_HASH_METHOD,
        },
        "coordinator_attestation": COORDINATOR_ATTESTATION,
    }
    rendered = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if internal_task_id.encode("utf-8") in rendered:
        raise ProtocolError("capture output would expose private internal task ID")
    private_paths = {
        str(source_git.get("root")),
        str(prompt.get("path")),
        str(task_prompt.get("path")),
        str(marketplace.get("path")),
        str(marketplace.get("resolved_target")),
    }
    private_paths.update(
        str(item.get("path"))
        for item in identities.values()
        if isinstance(item, dict)
    )
    instruction_files = observation_boundary.get("instruction_files")
    if isinstance(instruction_files, list):
        private_paths.update(
            str(item.get("path"))
            for item in instruction_files
            if isinstance(item, dict)
        )
    leaked = sorted(
        path
        for path in private_paths
        if path and path != "None" and path.encode("utf-8") in rendered
    )
    if leaked:
        raise ProtocolError("capture output would expose private absolute paths")
    written = write_new_json(output, result)
    print(
        f"CAPTURED receipt={launch['public_receipt_slug']} "
        f"observation_sha256={sha256_bytes(observation)} output_sha256={sha256_bytes(written)} "
        f"output={output}",
        flush=True,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.command == "prepare":
            return prepare(args)
        if args.command == "capture":
            return capture(args)
        raise ProtocolError(f"unsupported command: {args.command}")
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        subprocess.SubprocessError,
        ProtocolError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
