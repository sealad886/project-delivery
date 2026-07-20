# Validation report

Validation date: 2026-07-20

Release candidate: `v1.4.0-rc.1`

Verified package revision: `81b50ba`

Canonical package: `plugins/project-delivery/`

## Decision

Project Delivery is ready for an RC release after merge. The 64-file plugin package passes local validation, all 155 regression tests, hosted validation and security scanning, Plugin Creator validation, exact prepared-source/install parity, and a fresh-process smoke task bound to installed version `1.4.0-rc.1+codex.20260720142500`.

This supports an RC claim, not a stable `1.4.0` claim. Existing generic workflow plugins should remain available for rollback until the tagged RC has been used successfully in normal work. Provider connectors and domain-specific evidence plugins are outside the replacement scope.

## Evidence

| Gate | Result |
|---|---|
| Plugin structure and references | Pass: 64 files, 13 skills, five shared runtime resources |
| Route profiles and contracts | Pass: 24/24 profiles; all 13 skills covered; ownership, authority, gates, evidence, and stop conditions aligned |
| Regression suite | Pass: 155/155 with `GIT_CONFIG_GLOBAL=/dev/null` |
| Distribution boundary | Pass: no undeclared files, symlinks, executables, source-only paths, or unsupported types; source payload SHA-256 `6f4175424e9d6ec3056326d3d8e4c45f4255853fd63449e7df811b871f6bbd29` |
| Marketplace and license | Pass: repository marketplace resolves to `plugins/project-delivery`; root/package MIT text is byte-identical |
| Plugin Creator | Pass on prepared source |
| Skill validation | Pass: 13/13 skills |
| Icons | Pass: 28/28 PNGs decode; 14 small assets are 128×128 and 14 large assets are 512×512 |
| Security scanner | Pass: 92/100 (A), no critical/high/medium findings; hosted scanner passed |
| Hosted PR checks | Pass: validate, scan, plugin-scanner, and GitGuardian on `81b50ba` |
| Personal install | Pass: installed and enabled as `project-delivery@personal` version `1.4.0-rc.1+codex.20260720142500` |
| Prepared/install parity | Pass: exact 64-file prepared-source/cache comparison |
| Fresh-process smoke | Pass: exact version marker, installed manifest/orchestrator match, and expected `small-bug-planning` route under planning-only authority |

Reproduction commands:

```bash
.venv/bin/python scripts/check_plugin.py plugins/project-delivery --layout source
.venv/bin/python scripts/check_routes.py .
.venv/bin/python scripts/check_distribution_bundle.py plugins/project-delivery
.venv/bin/python scripts/check_marketplace.py .
GIT_CONFIG_GLOBAL=/dev/null .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

## Canary findings incorporated

Earlier canaries found real defects: incomplete capability ownership, controller ordering, future-retrospective activation, stale installed identity, broad specialist-load claims, and weak gap linkage. Those defects drove the schema-v3 receipts, installed route profiles, exact package boundary, and regression coverage now in the candidate.

The final pre-fix sealed 24-scenario task at `8cc215c` failed for four narrow reasons: a miscomputed semantic digest, uncited branch gaps, delivery-input gaps incorrectly marked route-blocking, and direct-retrospective intake requiring evidence that the prompt did not provide. Commit `81b50ba` corrected those semantics and added focused positive/negative tests. The heavyweight live matrix was not repeated for this RC; it remains an optional stable-release confidence check rather than a file-installation gate.

The latest iOS Backup Viewer canary correctly refused a release-ready verdict because the repository revision moved, the worktree contained concurrent changes, and the full Swift suite stalled in an external macOS Address Book/CoreData service. It preserved the checkout and stopped only its own test process. That is expected evidence handling, not a Project Delivery failure.

## Bounded limitations

- Static inspection proves icon assets and references; protected Codex UI pixels were not directly observed. A full Codex Desktop relaunch may be needed before existing tasks display refreshed cards.
- A delegated task created from a long-running parent inherited an old skill-catalog snapshot. Fresh standalone Codex resolved all 13 current selectors. Ordinary smoke prompts now require `PROJECT_DELIVERY_VERSION=<expected-version>` as the first line; sealed JSON uses `plugin_identity.installed_version`.
- Cisco's optional skill-scanner integration was unavailable under Python 3.14. The main scanner and hosted checks passed without it.
- The RC does not prove release readiness of the unrelated iOS Backup Viewer repository.

## Release and adoption disposition

- Merge the green PR and tag the merged revision `v1.4.0-rc.1` as a prerelease.
- Keep Project Delivery installed as the canonical generic PM/software-delivery workflow.
- Use the RC in normal small and medium work before promoting stable `1.4.0`.
- Uninstall Boss, Epic/Epic Harness, Superpowers, or other superseded generic workflow plugins only after confirming the tagged RC remains available and the desired rollback source is recorded.
- Keep provider connectors, platform tools, security scanners, and domain-specific plugins unless separately judged redundant.
