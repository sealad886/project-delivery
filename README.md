<p align="center">
  <img src="plugins/project-delivery/assets/project-delivery-logo.png" width="160" alt="Project Delivery compass and route logo">
</p>

# Project Delivery

[![Validate plugin](https://github.com/sealad886/project-delivery/actions/workflows/validate.yml/badge.svg)](https://github.com/sealad886/project-delivery/actions/workflows/validate.yml)
[![HOL Plugin Scanner](https://github.com/sealad886/project-delivery/actions/workflows/hol-plugin-scanner.yml/badge.svg)](https://github.com/sealad886/project-delivery/actions/workflows/hol-plugin-scanner.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Project Delivery is a self-contained Codex plugin for taking software work from an incomplete idea through requirements, design, planning, implementation, verification, documentation, review, security and operational readiness, release, and learning. It scales from small fixes to multi-PR and multi-release initiatives while preserving repository conventions, user authority, traceability, and evidence-based gates.

The complete user and capability guide lives with the installable package in [plugins/project-delivery/README.md](plugins/project-delivery/README.md).

## Safe package boundary

The canonical plugin is the exact subtree at [plugins/project-delivery](plugins/project-delivery). Repository-only CI, tests, audit evidence, contributor tooling, and virtual environments stay outside that directory.

```text
project-delivery/
├── .github/                     repository CI and templates
├── references/                  research, audit, and release evidence
├── scripts/                     dependency-free validation and packaging tools
├── tests/                       semantic contracts and regression tests
└── plugins/
    └── project-delivery/        canonical installable plugin
        ├── .codex-plugin/plugin.json
        ├── assets/
        └── skills/
```

This boundary is a security and reproducibility requirement. Codex `0.144.6` copies every regular file beneath a local plugin source into its cache; `.codexignore` is not an installation filter. Local and Git-backed marketplace entries must therefore point at the prepared plugin directory or use `git-subdir`, never the development checkout root.

## Local development install

Clone the source outside the personal plugin destination, then materialize the exact validated package:

```bash
git clone https://github.com/sealad886/project-delivery.git ~/src/project-delivery
cd ~/src/project-delivery
python3 scripts/check_distribution_bundle.py plugins/project-delivery \
  --output ~/plugins/project-delivery
```

For later iterations, add `--replace`. Replacement first proves that the destination is an exact, clean Project Delivery distribution and is not inside a Git checkout or Python environment. Missing, extra, forbidden, executable, symlinked, or unsupported entries block the swap; a failed atomic swap restores the prior clean distribution or retains its backup path for recovery.

Then use Codex's system Plugin Creator skill to validate, register, cachebust, and install the prepared `~/plugins/project-delivery` folder through the personal marketplace. Do not hand-edit Codex configuration. Start a fresh Codex task after each reinstall.

The repository also carries marketplace metadata for Git-backed installation. The public entry uses `git-subdir` with `./plugins/project-delivery` and is pinned to immutable stable release ref `v1.4.0`; future package releases must advance that ref in a separate untagged catalog commit after the new tag exists.

### Upgrade from the 1.3.x checkout layout

Project Delivery 1.3.x told users to clone the development repository directly to `~/plugins/project-delivery`. Do not use `--replace` on that checkout: the refusal is deliberate, because a materializer must never erase Git history, local changes, or repository-only files.

1. Record the current plugin selector, enabled/version state, source revision, Git status, remotes, manifest hash, and any local changes without copying credentials into the record.
2. Move the entire 1.3.x checkout intact to a separate source/rollback location such as `~/src/project-delivery-1.3-backup`; do not delete it. Verify its revision and status after the move.
3. Clone or update the candidate in a separate development path, validate `plugins/project-delivery/`, and materialize it into the now-vacant `~/plugins/project-delivery` destination without `--replace` for the first migration.
4. Use Plugin Creator's supported validation, cachebuster, and `project-delivery@personal` reinstall flow. Read back the personal marketplace name and installed source; do not hand-edit marketplace or cache state.
5. Compare the prepared source and versioned installed cache with `scripts/check_installed_parity.py`, then start a fresh task and verify selectors, icons, routing, and a bounded repository canary.
6. Keep both the 1.3.x checkout and the clean candidate source until forward and backward recovery have been rehearsed. To recover, use the recorded owning control plane and supported reinstall path, restore the recorded source identity, read back state, and verify from another fresh task; a retained cache alone is not rollback proof.

The [migration and decommission record](references/migration-and-decommission.md) defines the complete rollback evidence and legacy-plugin observation gates.

## Validation

Use the project `.venv` when present; the checks themselves use only Python's standard library.

```bash
python3 scripts/check_plugin.py plugins/project-delivery --layout source
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py \
  tests/fixtures/blind-route-observations-v1.3.1.json \
  --root . --allow-subset --allow-historical-annotations
python3 scripts/check_distribution_bundle.py plugins/project-delivery
python3 scripts/check_marketplace.py .
python3 scripts/check_installed_parity.py <prepared-plugin-source> <installed-cache-version-dir>
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The package-boundary check rejects undeclared files, symlinks, unsupported file types, source-only directories, broken internal references, and missing skill metadata. Release validation additionally uses Plugin Creator, Skill Creator, the pinned HOL scanner, an isolated install/rollback rehearsal, fresh-task behavioral canaries, and independent review.

Routing policy has two deliberately separated representations: installed `skills/.shared/route-profiles-v1.json` supplies runtime semantics, while repository-only `tests/route-contracts.json` supplies schema-v3 canary prompts and expected semantics. `scripts/check_routes.py` requires their profile IDs and semantic fields to remain in exact parity before either representation can support release evidence.

## Governance

- [Plugin guide](plugins/project-delivery/README.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Security policy](SECURITY.md)
- [Support](SUPPORT.md)
- [Design brief](references/design-brief.md)
- [Environment and capability audit](references/environment-audit.md)
- [Migration and decommission map](references/migration-and-decommission.md)
- [Validation report](references/validation-report.md)

Project Delivery is maintained by Andrew Cox and licensed under the [MIT License](LICENSE). Copyright © 2026 Andrew Cox.
