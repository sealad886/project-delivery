# Validation report

Validation date: 2026-07-19

Release target: `v1.3.1`

Evidence scope: source candidate and deterministic mirror simulation; installed-cache and hosted-CI receipts are recorded after publication

## Decision

The `1.3.1` source candidate passes the local structural, route-contract, marketplace-mirror, regression, Plugin Creator, Skill Creator, and HOL scanner gates listed below. This supports publication as a marketplace candidate. It does not by itself establish fresh-task routing, successful delivery in every downstream repository, production deployment readiness, or legacy-plugin uninstall readiness.

Resolve the exact source and installed identities from the release tag, `.codex-plugin/plugin.json`, Codex plugin registry, and cache path. Do not use an embedded Git `HEAD` inside an installed cache as payload provenance; compare the selected source and cache payloads directly.

## Reproducible local results

| Gate | Command or method | Result |
|---|---|---|
| Source structure, links, inline runtime references, naming, placeholders | `python3 scripts/check_plugin.py . --layout source` | Pass: 87 files, 13 skills |
| Validator regressions | `python3 -m unittest discover -s tests -p 'test_*.py' -v` | Pass: 7/7 tests, including source/cache layout, wrong source name, malformed manifest, missing skills, an incomplete skill contract, and a missing required release file |
| Authored route contracts | `python3 scripts/check_routes.py .` | Pass: 17 scenarios, all 13 skills referenced, evidence class `static-contracts` |
| Awesome marketplace mirror simulation | `python3 scripts/check_marketplace_bundle.py .` | Pass: 63 selected files, 13 skills, all three shared runtime documents, in-bundle references valid |
| Plugin Creator | system `plugin-creator/scripts/validate_plugin.py .` in project `.venv` with PyYAML 6.0.3 | Pass |
| Skill Creator | system `skill-creator/scripts/quick_validate.py` over every skill with visible 13-item progress | Pass: 13/13 |
| HOL scanner lint | `plugin-scanner lint . --profile public-marketplace --format text` | Pass: effective score 97; no high/critical finding |
| HOL scanner full scan | `plugin-scanner scan . --profile public-marketplace --format text --min-score 80 --fail-on-severity high` | Pass: 97/100, grade A; 0 critical/high/medium/low, 3 informational findings |
| HOL scanner runtime verification | `plugin-scanner verify . --format text` | Pass: manifest, capabilities, assets, 13 skills, skill references, and optional-component handling |
| Patch whitespace | `git diff --check` | Pass |

The local scanner used the marketplace guide's pinned `plugin-scanner==2.0.1015` wheel. Its SHA-256 matched the guide's reviewed digest `c1302897304e`; the wheel was installed only into the project `.venv`. The three informational findings concern absent optional `privacyPolicyURL`, `termsOfServiceURL`, and screenshots. The plugin has no hosted service and does not fabricate privacy/terms URLs merely to gain points.

Cisco skill-scanner evidence was unavailable under the inspection host's Python 3.14 because that optional integration requires Python below 3.14. The HOL scanner explicitly continued without that integration; the pinned GitHub scanner action runs on Ubuntu and provides the hosted source-repository result used for marketplace submission.

## Static routing evidence

The 17 canonical scenarios are versioned in `tests/route-contracts.json`. The route checker validates:

- unique, complete scenario records;
- supported authority classifications;
- non-empty artifacts, evidence, and stop conditions;
- references to actual Project Delivery skills;
- coverage of all 13 discoverable skills; and
- absence of Boss, Epic/Epic Harness, and Superpowers from expected runtime routes.

This is accurately described as **17/17 authored scenarios statically mapped and contract-valid**. It is not interactive proof. A fresh task must record expected versus actual route, plugin/cache/task identity, scale/risk, authority, artifacts, evidence, forbidden-dependency result, timestamp, and residual gaps using the live receipt template.

## Marketplace bundle integrity

The current Awesome Codex Plugins generator mirrors manifest-declared component trees and selected root metadata/assets from default-branch `HEAD`. Earlier Project Delivery skills depended on root references that such a mirror would omit. Version 1.3.0 makes the installable documents canonical under the hidden, recursively mirrored `skills/.shared/` directory and keeps root files as source-documentation pointers only.

The deterministic mirror check copies only the documented selected paths into a temporary `project-delivery` root and runs the structural/reference validator there. The simulated bundle includes:

- `.codex-plugin/plugin.json`, README, SECURITY, LICENSE, `.codexignore`, and Dependabot metadata;
- plugin composer and logo assets;
- all 13 skills, 13 agent manifests, and 26 skill icons; and
- the shared operating model, artifact templates, and external-systems contract.

No manifest field was invented to force packaging, and no root audit dossier is a runtime dependency.

## Canary remediation disposition

The iOS Backup Viewer read-only canary against Project Delivery 1.2.2 identified five plugin-owned release gaps. Version 1.3.0 addresses them as follows:

| Canary gap | Disposition in 1.3.0 |
|---|---|
| Ungoverned security suppression | Shared finding lifecycle plus explicit closure category, counterevidence, sibling checks, qualified review, revalidation trigger, release treatment, and residual-risk authority |
| Installed-cache false failure | Source/cache/auto layouts plus regression coverage for the Codex `<name>/<version>` cache shape |
| Unqualified `17/17` claim | Machine-readable static contracts, deterministic validation, explicit evidence classes, and live receipt template |
| Detached risk/decision records | Requirement-to-risk-mitigation-test/finding-release and decision-to-affected-work/test-release trace branches |
| Stale file-count evidence | Revision-bound commands and current 87-file result in this report |

The canary also found active Epic instructions, imperative Superpowers text in historical consumer plans, no real small/medium change receipts, and no pre-disable rollback inventory. Those are consumer migration/decommission gates, not core plugin defects. Version 1.3.0 adds an explicit migration route and inventory checks, but does not silently edit a consumer repository or claim those gates have passed.

## Originality and dependency review

The runtime is independently implemented and contains no imported executable, hook, MCP/app declaration, credential, telemetry, binary dependency, or mandatory provider integration. A fresh long-line comparison during independent review found no matching line of at least 80 characters against the inspected installed Boss, Epic, and Superpowers sources, and no matching line of at least 100 characters across the broader inspected Awesome and OpenAI-curated snapshots. This is useful negative-overlap evidence, not a legal originality guarantee.

## Residual limitations

- Fresh-task live route receipts for the 1.3.1 installed cache remain distinct post-install evidence.
- Real small-change and medium/multi-PR canaries remain required before uninstalling superseded generic workflow plugins.
- Active legacy instructions and historical imperative calls must be neutralized in each consumer environment before disabling those plugins.
- Specialist tools remain necessary where actual provider access, platform measurement, security scanning, signing/notarization, deployment, observability, or communication is required.
- Marketplace inclusion depends on upstream review and automation; a submitted PR is not acceptance.
- Hosted CI/scanner success must be read from the exact release commit after push and must not be inferred from this local report.
- Hosted Cisco scanning treats the required PNG interface icons as informational binary assets. Optional privacy, terms, and screenshot metadata also remains absent rather than linking to inapplicable or fabricated policies; neither class is a high/critical finding.

## Release status

Local source-candidate status: **pass for publication and upstream marketplace submission after hosted scanner CI succeeds**.

Legacy-plugin uninstall status: **blocked pending consumer migration, rollback, live canaries, disable-one-at-a-time observation, and explicit user confirmation**.
