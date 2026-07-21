#!/usr/bin/env python3
"""Validate repository marketplace identity, containment, and legal-file parity."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path


PLUGIN_NAME = "project-delivery"
EXPECTED_SOURCE_TYPE = "git-subdir"
EXPECTED_SOURCE_URL = "https://github.com/sealad886/project-delivery.git"
EXPECTED_SOURCE_REF = "v1.4.0"
EXPECTED_SOURCE_PATH = "./plugins/project-delivery"
EXPECTED_LICENSE_SHA256 = "486b9c74f1d5bf1a5be12a8fe070db7cfad5a4901f083d4810a677b32f2d4993"
EXPECTED_COPYRIGHT = "Copyright (c) 2026 Andrew Cox"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1]),
        help="repository root containing .agents/plugins/marketplace.json",
    )
    return parser.parse_args(argv)


def safe_source_path(root: Path, value: object) -> tuple[Path | None, list[str]]:
    if not isinstance(value, str) or not value:
        return None, ["marketplace source.path must be a non-empty string"]
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    relative = Path(normalized)
    if relative.is_absolute() or ".." in relative.parts:
        return None, [f"marketplace source.path escapes the repository: {value}"]
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        return None, [f"marketplace source.path resolves outside the repository: {value}"]
    return resolved, []


def validate_repository_marketplace(root: Path) -> list[str]:
    errors: list[str] = []
    marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"cannot read repository marketplace: {error}"]

    if marketplace.get("name") != PLUGIN_NAME:
        errors.append(f"marketplace name must be {PLUGIN_NAME!r}")
    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != "Project Delivery":
        errors.append("marketplace interface.displayName must be 'Project Delivery'")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        return errors + ["marketplace plugins must be an array"]
    if len(plugins) != 1:
        errors.append("single-plugin repository marketplace must contain exactly one entry")
    matching = [entry for entry in plugins if isinstance(entry, dict) and entry.get("name") == PLUGIN_NAME]
    if len(matching) != 1:
        return errors + [f"marketplace must contain exactly one {PLUGIN_NAME!r} entry"]

    started = time.monotonic()
    for index, entry in enumerate(plugins, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(plugins) - index)
        print(
            f"MARKETPLACE [{index}/{len(plugins)}] plugin={entry.get('name') if isinstance(entry, dict) else '<invalid>'} eta={eta:.1f}s",
            flush=True,
        )

    entry = matching[0]
    source = entry.get("source")
    if not isinstance(source, dict):
        return errors + ["marketplace plugin source must be an object"]
    if source.get("source") != EXPECTED_SOURCE_TYPE:
        errors.append(
            f"repository marketplace source.source must be {EXPECTED_SOURCE_TYPE!r}"
        )
    if source.get("url") != EXPECTED_SOURCE_URL:
        errors.append(
            f"repository marketplace source.url must be {EXPECTED_SOURCE_URL!r}"
        )
    if source.get("ref") != EXPECTED_SOURCE_REF:
        errors.append(
            f"repository marketplace source.ref must be immutable release {EXPECTED_SOURCE_REF!r}"
        )
    if source.get("path") != EXPECTED_SOURCE_PATH:
        errors.append(
            f"repository marketplace source.path must be {EXPECTED_SOURCE_PATH!r}"
        )
    plugin_root, path_errors = safe_source_path(root, source.get("path"))
    errors.extend(path_errors)
    if plugin_root is None:
        return errors

    expected_root = (root / "plugins" / PLUGIN_NAME).resolve()
    if plugin_root != expected_root:
        errors.append(
            f"marketplace source.path must resolve to {expected_root}, found {plugin_root}"
        )

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("marketplace plugin policy must be an object")
    else:
        if policy.get("installation") != "AVAILABLE":
            errors.append("marketplace policy.installation must be 'AVAILABLE'")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append("marketplace policy.authentication must be 'ON_INSTALL'")

    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"cannot read marketplace target manifest: {error}")
        manifest = {}
    if manifest.get("name") != entry.get("name"):
        errors.append("marketplace entry name must match target manifest name")
    manifest_interface = manifest.get("interface")
    manifest_category = (
        manifest_interface.get("category") if isinstance(manifest_interface, dict) else None
    )
    if entry.get("category") != manifest_category:
        errors.append("marketplace entry category must match manifest interface.category")

    root_license = root / "LICENSE"
    package_license = plugin_root / "LICENSE"
    try:
        root_bytes = root_license.read_bytes()
        package_bytes = package_license.read_bytes()
    except OSError as error:
        errors.append(f"cannot read required MIT license copy: {error}")
    else:
        if root_bytes != package_bytes:
            errors.append("root and packaged MIT license files must be byte-identical")
        actual_hash = hashlib.sha256(root_bytes).hexdigest()
        if actual_hash != EXPECTED_LICENSE_SHA256:
            errors.append(
                "MIT license text differs from the approved Andrew Cox license: "
                f"sha256={actual_hash}"
            )
        if EXPECTED_COPYRIGHT not in root_bytes.decode("utf-8", errors="replace").splitlines():
            errors.append(f"MIT license must contain exactly: {EXPECTED_COPYRIGHT}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    errors = validate_repository_marketplace(root)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(
        "PASS marketplace=project-delivery source=git-subdir "
        "ref=v1.4.0 target=plugins/project-delivery "
        "policy=AVAILABLE/ON_INSTALL license_parity=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
