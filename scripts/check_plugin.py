#!/usr/bin/env python3
"""Check local plugin links, skill metadata, naming, and placeholders."""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1]).resolve()
    files = sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
    )
    errors: list[str] = []
    started = time.monotonic()
    for index, path in enumerate(files, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(files) - index) if index else 0
        print(f"CHECK [{index}/{len(files)}] file={path.relative_to(root)} eta={eta:.1f}s", flush=True)
        text = path.read_text(encoding="utf-8", errors="replace")
        placeholder_marker = "[" + "TODO:"
        if placeholder_marker in text:
            errors.append(f"placeholder: {path}")
        if path.name == "SKILL.md":
            if not text.startswith("---\n") or not re.search(r"^name: [a-z0-9-]+$", text, re.M):
                errors.append(f"invalid skill frontmatter: {path}")
            if not re.search(r"^description: .+", text, re.M):
                errors.append(f"missing skill description: {path}")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" not in target and not target.startswith("#"):
                    resolved = (path.parent / target.split("#", 1)[0]).resolve()
                    if not resolved.exists():
                        errors.append(f"broken link: {path} -> {target}")
    manifest = json.loads((root / ".codex-plugin" / "plugin.json").read_text())
    if manifest.get("name") != root.name:
        errors.append("manifest name does not match plugin directory")
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    print(f"PASS files={len(files)} skills={len(list((root / 'skills').glob('*/SKILL.md')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
