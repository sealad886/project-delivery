# Validation report

Validation date: 2026-07-19

Release candidate: `v1.4.0-rc.1`

Evidence scope: standalone source working tree on `codex/remediate-canary-findings`, a deterministic minimum runtime-closure simulation, historical contract-blind route observations from the installed `1.3.1` canary, and local validators/scanners. Candidate commit identity, installed-cache parity, fresh-task `1.4.0-rc.1` behavior, hosted CI, release-tag identity, and rollback drills remain separate evidence gates.

## Decision

The in-progress `1.4.0-rc.1` source candidate passes the local structural, authored semantic route-contract, historical route-shape compatibility, minimum runtime-closure, regression, Plugin Creator, Skill Creator, scanner-policy, and scanner-verification gates listed below.

This supports freezing the immutable source candidate. Three independent stabilized-tree reviews found no remaining P1/P2 blocker after the adversarial findings were corrected. It is not yet sufficient to update the active personal installation: exact `1.3.1 → candidate → 1.3.1` recovery must first pass in an isolated Codex home. It is not evidence for a final `1.4.0` release, successful delivery in every consumer repository, production deployment readiness, or legacy-plugin uninstall readiness.

## Reproducible local results

| Gate | Command or method | Result |
|---|---|---|
| Source structure, links, inline runtime references, naming, placeholders | `.venv/bin/python scripts/check_plugin.py . --layout source` | Pass: 90 files, 13 skills |
| Semantic authored route contracts | `.venv/bin/python scripts/check_routes.py .` | Pass: 21 scenarios, all 13 skills referenced, evidence class `semantic-contracts` |
| Historical blind route shapes with post-hoc annotations | `.venv/bin/python scripts/check_route_receipts.py tests/fixtures/blind-route-observations-v1.3.1.json --root . --allow-subset --allow-historical-annotations` | Pass: 17 preserved route shapes remain structurally compatible; current-policy and candidate-behavior conformance are explicitly not established |
| Minimum runtime-closure simulation | `.venv/bin/python scripts/check_distribution_bundle.py .` | Pass: 63 selected files, 13 skills, all three shared runtime documents; not an installer/marketplace artifact claim |
| Validator regressions | `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v` | Pass: 47/47, including a 21-contract fresh synthetic policy matrix and adversarial two-sided controller, incident-planning, semantic-freeze, evidence, authority, metadata, privacy, and dependency cases |
| Plugin Creator | system `plugin-creator/scripts/validate_plugin.py` in the project `.venv` | Pass |
| Skill Creator | system `skill-creator/scripts/quick_validate.py` over every skill with visible 13-item progress | Pass: 13/13 |
| HOL scanner lint | `.venv/bin/plugin-scanner lint . --format text` | Policy pass; effective score 94; no critical, high, or medium finding |
| HOL scanner full scan | `.venv/bin/plugin-scanner scan . --profile default --format text --min-score 80 --fail-on-severity high` | Pass: 94/100, grade A; 0 critical/high/medium, 1 low, 3 informational findings |
| HOL scanner runtime verification | `.venv/bin/plugin-scanner verify . --format text` | Pass: manifest, capability enumeration, interface assets, 13 skill manifests/frontmatter/references, and asset-size checks |
| Independent stabilized-tree review | Three bounded reviewers covering route/evidence adversarial cases, release/source integrity, and Plugin Creator recovery/decommission controls | Pass: no remaining P1/P2 blocker to source commit, branch push, or candidate PR; installation/tag/decommission/publication gates remain separate |
| JSON syntax | `python -m json.tool` over the manifest, route contracts, and frozen receipt fixture | Pass |
| Patch whitespace | `git diff --check` | Pass |

The local scanner is `plugin-scanner==2.0.1015` inside the project `.venv`. Its low finding rejects the prerelease-form candidate version `1.4.0-rc.1`; Plugin Creator validation accepts the manifest. The candidate retains an explicit prerelease identity rather than presenting uncanaried work as `1.4.0`. The three informational findings concern absent optional `privacyPolicyURL`, `termsOfServiceURL`, and screenshots. This plugin has no hosted service and does not fabricate inapplicable URLs.

Cisco skill-scanner evidence remains unavailable under the inspection host's Python 3.14 because that optional integration requires an older Python range. HOL Guard continued without that integration. Hosted scanner evidence must be read from the exact pushed candidate or release commit and is not inferred from this local result.

## Corrected interpretation of the prior canary

The prior report's `4/17` result compared one exact expected skill array with each blind selected array. That is not a valid conformance rule for a risk-scaled workflow: several specialists are evidence-triggered, equivalent specialist ordering can be safe, and controller skills can re-enter after recovering evidence.

The original blind route selections are linked from `tests/fixtures/blind-route-observations-v1.3.1.json` through sanitized public identity and SHA-256 digests of the private source observations. Their schema-v2 taxonomy, taxonomy rationales, and conditional dispositions were added afterward, so the fixture declares that its complete semantic records were not frozen and the checker requires a conspicuous opt-in flag. The checker reports these 17 cases as historical route-shape records with `current_policy_claim=not-established`; it does not label them route-policy passes. Retrospective stages named before an outcome are recorded as `planned-future`, not presently activated. This evidence rebuts exact-array scoring only by preserving compatible capability shapes; it does not turn post-hoc interpretation into blind evidence or a route-only observation into implementation, testing, release, or `1.4.0-rc.1` runtime evidence.

The canonical suite now contains 21 cases: the original 17 plus distinct performance, packaging, signing/notarization, and distribution claims. These variants make the combined scenario's hidden authority and evidence branches explicit without removing the original ambiguous catch-all.

## Skill discovery and progressive loading

The source and minimum runtime closure contain 13 structurally valid Project Delivery skills, 13 agent manifests, and 26 skill icons. The three skills absent from the crowded desktop task's initial model-visible list—`solution-design`, `testing-quality`, and `security-operations`—were present in source and installed payloads.

OpenAI's Build Skills documentation states that Codex applies a global initial skill-metadata budget and may shorten or omit entries while loading a selected skill's full instructions later. The candidate therefore:

- frontloads the orchestrator description;
- instructs the orchestrator to resolve every selected specialist from its installed sibling directory;
- requires that specialist's complete `SKILL.md` to be read before application;
- distinguishes initial-list visibility, UI/selector visibility, installed-file presence, successful loading, and actual invocation; and
- treats an unreadable specialist as a blocker rather than silently absorbing its work.

This is package and policy evidence. A freshly installed candidate must still demonstrate UI/selector behavior and sibling loading under the same crowded catalog before final release.

## Authority and wrapper execution

Implementation and quality skills now inspect unfamiliar wrappers and lifecycle scripts before execution. The preflight records writes, deletion, fixed temporary paths, signing/notarization, credential access, network/provider access, package installation, publication, deployment, and permission changes.

Technical success and authority compliance are separate gates. A wrapper that signs an ad-hoc artifact during a test run may produce passing tests while the authority gate still fails. The candidate does not reinterpret a request to build or test as permission to sign, publish, deploy, or mutate an external provider.

No `1.4.0-rc.1` wrapper canary has run yet. The earlier `199` passing tests remain technical evidence from the old canary, not authority-compliant completion evidence.

## Minimum runtime-closure integrity

The distribution check copies the standalone manifest, selected root documents and assets, manifest-declared component trees, and interface assets into a temporary `project-delivery` root, then reruns structural and internal-reference validation. This proves a minimum self-contained runtime closure. It does not invoke a Codex or marketplace packager, parse `.codexignore`, emit an archive, or prove what a local installed cache contains.

The validated bundle contains:

- `.codex-plugin/plugin.json`, README, SECURITY, LICENSE, `.codexignore`, and Dependabot metadata;
- plugin composer and logo assets;
- all 13 skills, 13 agent manifests, and 26 skill icons; and
- the shared operating model, artifact templates, and external-systems contract.

No manifest field was invented to force packaging. No source-only audit, test fixture, validation script, MCP server, hook, app, executable binary, credential, or legacy plugin is a runtime dependency.

## Decommission and rollback disposition

The migration policy now treats CLI-managed plugins, product-managed or remote-synced plugins, direct skill registrations, symlink discovery, standalone clones, configured sources, and cached payloads as distinct identities and control planes.

An exact rollback record requires selector, owning control plane, enabled state, source revision, manifest and payload hashes, configuration locations without secret values, supported reinstall mechanism, readback, fresh-task verification, and limitations. A mutable marketplace selector or retained cache alone is not exact rollback.

These requirements are now documented, but exact rollback has not yet been proven for every superseded plugin. The available evidence also does not establish a supported disable/uninstall control for every product-managed or remote-synced source. Therefore:

- Project Delivery may be installed as a controlled RC alongside existing plugins only after the isolated recovery drill and stabilized independent review pass; until then the active personal installation stays unchanged.
- Superseded plugins may be disabled one at a time only in reversible canaries after exact state capture.
- Permanent uninstall remains blocked.
- The withdrawn external `awesome-codex-plugins` publication must remain closed; no resubmission is part of this candidate.

## Candidate gates still required

Before promoting to `1.4.0`:

1. Freeze an exact RC commit; record its clean state, manifest hash, and deterministic source-payload hash.
2. Rehearse exact `1.3.1 → candidate → 1.3.1` recovery in an isolated Codex home before changing the active personal installation.
3. For the forward update, record the Plugin Creator cachebuster's before/after manifest versions and hashes, install through the supported personal-marketplace workflow, and verify payload parity against the committed RC while allowing only that recorded version delta.
4. Restore the source manifest to the committed RC bytes and confirm a clean source tree.
5. Start genuinely fresh Codex tasks under catalog pressure.
6. Record blind semantic receipts for the 21 scenarios, including taxonomy rationale and the complete semantic freeze declaration/evidence, before comparing them with the authored contracts.
7. Verify 13/13 Skills UI cards where expected, 13/13 fully qualified selectors, and orchestrated loading of `solution-design`, `testing-quality`, and `security-operations` even if absent from the initial list.
8. Run bounded repository canaries without unauthorized signing, publishing, deployment, provider mutation, or destructive action.
9. Obtain a refreshed independent diff/release review over the installed-canary and recovery evidence.
10. Push the exact candidate, require hosted validation/scanner success, and only then decide whether to promote to `1.4.0`.

## Release status

Local source-candidate status: **cleared for immutable commit, branch push, and candidate PR; active personal installation remains blocked pending the isolated exact-recovery rehearsal**.

Final `v1.4.0` release status: **blocked pending installed-cache parity, fresh-task candidate behavior, repository canaries, independent review, and exact-commit hosted CI/scanner evidence**.

Legacy-plugin uninstall status: **blocked pending exact per-control-plane rollback, disable-one-at-a-time observations, stable post-observation state, and explicit user confirmation of the final superseded set**.
