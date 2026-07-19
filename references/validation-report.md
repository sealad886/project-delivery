# Validation report

Validation date: 2026-07-19

Release target: `v1.3.2`

Evidence scope: standalone source checkout and deterministic installable distribution bundle. Hosted CI, release-tag identity, installed-cache parity, and fresh-task behavior remain separate post-commit or post-release evidence.

## Decision

The `1.3.2` source candidate passes the local structural, route-contract, distribution-bundle, regression, Plugin Creator, Skill Creator, and HOL scanner gates listed below. This supports a patch release of the standalone Project Delivery plugin. It does not by itself establish fresh-task routing, successful delivery in every consumer repository, production deployment readiness, or legacy-plugin uninstall readiness.

Resolve exact source and installed identities from the release tag, `.codex-plugin/plugin.json`, Codex's installed-plugin registry, and the installed cache path. Do not use an embedded Git `HEAD` inside a copied cache as payload provenance; compare selected source and installed payloads directly.

## Reproducible local results

| Gate | Command or method | Result |
|---|---|---|
| Source structure, links, inline runtime references, naming, placeholders | `python3 scripts/check_plugin.py . --layout source` | Pass: 87 files, 13 skills |
| Validator regressions | `python3 -m unittest discover -s tests -p 'test_*.py' -v` | Pass: 7/7 tests |
| Authored route contracts | `python3 scripts/check_routes.py .` | Pass: 17 scenarios, all 13 skills referenced, evidence class `static-contracts` |
| Installable distribution bundle | `python3 scripts/check_distribution_bundle.py .` | Pass: 63 selected files, 13 skills, all three shared runtime documents, in-bundle references valid |
| Plugin Creator | system `plugin-creator/scripts/validate_plugin.py .` in the project `.venv` | Pass |
| Skill Creator | system `skill-creator/scripts/quick_validate.py` over every skill with visible 13-item progress | Pass: 13/13 |
| HOL scanner lint | `plugin-scanner lint . --format text` | Pass: effective score 97; no high or critical finding |
| HOL scanner full scan | `plugin-scanner scan . --profile default --format text --min-score 80 --fail-on-severity high` | Pass: 97/100, grade A; 0 critical/high/medium/low, 3 informational findings |
| Standalone documentation | case-insensitive `rg` scan over tracked source, excluding `.git` and `.venv` | Pass: installation and usage text describe source cloning and supported local registration only |
| Patch whitespace | `git diff --check` | Pass |

The local scanner is `plugin-scanner==2.0.1015` inside the project `.venv`. Its three informational findings concern absent optional `privacyPolicyURL`, `termsOfServiceURL`, and screenshots. The plugin has no hosted service and does not fabricate privacy or terms URLs merely to gain points.

Cisco skill-scanner evidence was unavailable under the inspection host's Python 3.14 because that optional integration requires Python below 3.14. The HOL scanner continued without that integration. Hosted scanner evidence must be read from the exact release commit after push and remains distinct from this local result.

## Static routing evidence

The 17 canonical scenarios are versioned in `tests/route-contracts.json`. The route checker validates:

- unique, complete scenario records;
- supported authority classifications;
- non-empty artifacts, evidence, and stop conditions;
- references to actual Project Delivery skills;
- coverage of all 13 discoverable skills; and
- absence of Boss, Epic/Epic Harness, and Superpowers from expected runtime routes.

This is accurately described as **17/17 authored scenarios statically mapped and contract-valid**. It is not interactive proof. A fresh task must record expected versus actual route, plugin/cache/task identity, scale/risk, authority, artifacts, evidence, forbidden-dependency result, timestamp, and residual gaps using the live receipt template.

## Installable bundle integrity

The distribution check copies the standalone plugin's manifest, selected root documents and assets, manifest-declared component trees, and interface assets into a temporary `project-delivery` root, then runs the structural and internal-reference validator against that fresh bundle.

The validated bundle contains:

- `.codex-plugin/plugin.json`, README, SECURITY, LICENSE, `.codexignore`, and Dependabot metadata;
- plugin composer and logo assets;
- all 13 skills, 13 agent manifests, and 26 skill icons; and
- the shared operating model, artifact templates, and external-systems contract.

No manifest field is invented to force packaging, and no source-only audit, test fixture, or development script is a runtime dependency. Source-only README links use absolute repository URLs so they remain valid from both a clone and a reduced installed bundle.

## Documentation disposition

Version 1.3.2 presents Project Delivery only as a standalone source plugin:

- installation begins with cloning this repository into a stable local directory;
- Plugin Creator owns supported validation, local-source registration, cache refresh, and reinstall behavior;
- users are told to start a new task after installation;
- examples invoke fully qualified `project-delivery:*` skill names; and
- installation guidance is complete for the standalone source workflow.

## Canary remediation disposition

The iOS Backup Viewer read-only canary against Project Delivery 1.2.2 identified five plugin-owned release gaps. Version 1.3.0 addressed them as follows:

| Canary gap | Disposition from 1.3.0 onward |
|---|---|
| Ungoverned security suppression | Shared finding lifecycle plus explicit closure category, counterevidence, sibling checks, qualified review, revalidation trigger, release treatment, and residual-risk authority |
| Installed-cache false failure | Source/cache/auto layouts plus regression coverage for the Codex `<name>/<version>` cache shape |
| Unqualified `17/17` claim | Machine-readable static contracts, deterministic validation, explicit evidence classes, and live receipt template |
| Detached risk/decision records | Requirement-to-risk-mitigation-test/finding-release and decision-to-affected-work/test-release trace branches |
| Stale file-count evidence | Revision-bound commands and the current 87-file result in this report |

Consumer migration/decommission gates remain separate from core plugin correctness. Project Delivery does not silently edit consumer repositories or claim those gates have passed.

## Originality and dependency review

The runtime is independently implemented and contains no imported executable, hook, MCP/app declaration, credential, telemetry, binary dependency, or mandatory provider integration. Prior independent comparison found no matching long line against the inspected Boss, Epic, and Superpowers sources or the broader inspected plugin snapshots. This is useful negative-overlap evidence, not a legal originality guarantee.

## Residual limitations

- Fresh-task live route receipts for a `1.3.2` installed cache remain distinct post-install evidence.
- Real small-change and medium/multi-PR canaries remain required before uninstalling superseded generic workflow plugins.
- Active legacy instructions and historical imperative calls must be neutralized in each consumer environment before disabling those plugins.
- Specialist tools remain necessary where actual provider access, platform measurement, security scanning, signing/notarization, deployment, observability, or communication is required.
- Hosted CI/scanner success must be read from the exact release commit after push and must not be inferred from this local report.
- The scanner treats required PNG interface icons as informational binary assets. Optional privacy, terms, and screenshot metadata also remains absent rather than linking to inapplicable or fabricated policies; neither class is a high or critical finding.

## Release status

Local source-candidate status: **pass for a standalone `v1.3.2` patch release, subject to exact-commit hosted CI and scanner evidence**.

Legacy-plugin uninstall status: **blocked pending consumer migration, rollback, live canaries, disable-one-at-a-time observation, and explicit user confirmation**.
