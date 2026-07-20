#!/usr/bin/env python3
"""Compare a prepared Project Delivery source with an installed Codex cache exactly."""

from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

from check_distribution_bundle import inventory_tree
from check_distribution_bundle import payload_sha256
from check_distribution_bundle import select_paths
from check_distribution_bundle import validate_source_boundary
from check_plugin import validate


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="prepared plugin source directory")
    parser.add_argument("installed", help="installed versioned Codex cache directory")
    return parser.parse_args(argv)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compare(source: Path, installed: Path) -> tuple[list[str], int, str]:
    errors: list[str] = []
    selected = sorted(select_paths(source))
    errors.extend(validate_source_boundary(source, selected))

    source_errors, source_skills, _ = validate(source, "source")
    installed_errors, installed_skills, _ = validate(installed, "cache")
    errors.extend(f"source validation: {error}" for error in source_errors)
    errors.extend(f"installed validation: {error}" for error in installed_errors)
    if source_skills != installed_skills:
        errors.append(
            f"skill count differs: source={source_skills} installed={installed_skills}"
        )

    source_files, source_directories, source_inventory_errors = inventory_tree(
        source,
        "source",
        "INVENTORY",
    )
    installed_files, installed_directories, installed_inventory_errors = inventory_tree(
        installed,
        "installed",
        "INVENTORY",
    )
    errors.extend(source_inventory_errors)
    errors.extend(installed_inventory_errors)

    for missing in sorted(source_files - installed_files):
        errors.append(f"installed cache is missing source file: {missing}")
    for extra in sorted(installed_files - source_files):
        errors.append(f"installed cache contains extra file: {extra}")
    for missing in sorted(source_directories - installed_directories):
        errors.append(f"installed cache is missing source directory: {missing}")
    for extra in sorted(installed_directories - source_directories):
        errors.append(f"installed cache contains extra directory: {extra}")

    common = sorted(source_files.intersection(installed_files))
    started = time.monotonic()
    for index, relative in enumerate(common, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(common) - index)
        print(f"PARITY [{index}/{len(common)}] file={relative} eta={eta:.1f}s", flush=True)
        source_hash = file_sha256(source / relative)
        installed_hash = file_sha256(installed / relative)
        if source_hash != installed_hash:
            errors.append(
                f"content differs: {relative} source={source_hash} installed={installed_hash}"
            )

    digest = ""
    if not errors:
        source_digest = payload_sha256(source, sorted(source_files))
        installed_digest = payload_sha256(installed, sorted(installed_files))
        if source_digest != installed_digest:
            errors.append(
                f"payload digest differs: source={source_digest} installed={installed_digest}"
            )
        else:
            digest = source_digest
    return errors, len(source_files), digest


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    source = Path(args.source).expanduser().resolve()
    installed = Path(args.installed).expanduser().resolve()
    errors, file_count, digest = compare(source, installed)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(
        f"PASS files={file_count} skills=13 exact_source_cache_parity=true "
        f"payload_sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
