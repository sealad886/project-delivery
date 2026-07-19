#!/usr/bin/env python3
"""Build and validate a minimum self-contained plugin runtime closure."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

from check_plugin import validate


OPTIONAL_ROOT_FILES = {
    ".codexignore",
    ".github/dependabot.yml",
    "LICENSE",
    "LICENSE.md",
    "LICENSE.txt",
    "NOTICE.md",
    "README.md",
    "SECURITY.md",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "pyproject.toml",
    "yarn.lock",
}
COMPONENT_FIELDS = ("skills", "scripts", "mcpServers", "apps", "app", "appConfig", "hooks")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1]),
        help="plugin source root",
    )
    return parser.parse_args(argv)


def safe_relative_path(value: str) -> Path:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    candidate = Path(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe manifest path: {value}")
    return candidate


def add_declared_path(root: Path, selected: set[Path], value: str) -> None:
    relative = safe_relative_path(value)
    source = root / relative
    if source.is_file():
        selected.add(relative)
    elif source.is_dir():
        selected.update(path.relative_to(root) for path in source.rglob("*") if path.is_file())
    else:
        raise ValueError(f"declared path does not exist: {value}")


def select_paths(root: Path) -> set[Path]:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected = {Path(".codex-plugin/plugin.json")}
    selected.update(path for path in map(Path, OPTIONAL_ROOT_FILES) if (root / path).is_file())

    for field in COMPONENT_FIELDS:
        value = manifest.get(field)
        if isinstance(value, str):
            add_declared_path(root, selected, value)

    interface = manifest.get("interface", {})
    if isinstance(interface, dict):
        for field in ("composerIcon", "logo"):
            value = interface.get(field)
            if isinstance(value, str):
                add_declared_path(root, selected, value)
        screenshots = interface.get("screenshots", [])
        if isinstance(screenshots, list):
            for value in screenshots:
                if isinstance(value, str):
                    add_declared_path(root, selected, value)
    return selected


def validate_runtime_closure(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    try:
        selected = sorted(select_paths(root))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [str(error)], 0

    with tempfile.TemporaryDirectory(prefix="project-delivery-runtime-closure-") as temporary:
        destination = Path(temporary) / "project-delivery"
        started = time.monotonic()
        for index, relative in enumerate(selected, 1):
            elapsed = time.monotonic() - started
            eta = (elapsed / index) * (len(selected) - index)
            print(f"CLOSURE [{index}/{len(selected)}] file={relative} eta={eta:.1f}s", flush=True)
            source = root / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        bundle_errors, skill_count, _ = validate(destination, "source")
        errors.extend(bundle_errors)
        if skill_count != 13:
            errors.append(f"runtime closure must contain 13 skills, found {skill_count}")
        for required in (
            "skills/.shared/operating-model.md",
            "skills/.shared/artifact-templates.md",
            "skills/.shared/external-systems.md",
        ):
            if not (destination / required).is_file():
                errors.append(f"runtime closure is missing dependency: {required}")
    return errors, len(selected)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    errors, selected_count = validate_runtime_closure(root)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(f"PASS selected_files={selected_count} skills=13 shared_runtime=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
