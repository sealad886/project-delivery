# Validation report

Validation date: 2026-07-20

Release candidate: `v1.4.0-rc.1`

Evidence scope: source working tree on `codex/remediate-canary-findings`, the exact canonical package at `plugins/project-delivery/`, Plugin Creator-generated repository marketplace metadata, local validators/scanners, historical contract-blind route observations from the installed `1.3.1` canary, one pre-hardening isolated nested-package install/removal rehearsal, and one pre-boundary recovery drill. The isolated/recovery observations are retained as historical evidence only; final-package forward/back recovery, active personal replacement, fresh-task `1.4.0-rc.1` behavior, final commit identity, refreshed hosted CI, merged-main identity, Git transport, and release-tag identity remain separate gates.

## Decision

The in-progress `1.4.0-rc.1` candidate passes the local structural, authored semantic route-contract, historical route-shape compatibility, exact package-boundary, regression, marketplace/legal-parity, Plugin Creator, Skill Creator, scanner-policy, and scanner-verification gates listed below. Final install, recovery, fresh-task, repository-canary, hosted, merge, Git-transport, tag, and publication gates remain pending.

The first active local install exposed an unacceptable packaging defect: Codex copied the development checkout's `.git`, `.venv`, CI, tests, audit records, validators, and bytecode because `.codexignore` is not an installer filter. That installed payload is rejected as candidate evidence. The repository now makes `plugins/project-delivery/` the canonical 62-file package boundary and keeps all maintainer-only material outside it. A pre-hardening working-tree snapshot installed cleanly in an isolated repository marketplace and was removed through supported commands, but later safety and trust-boundary changes changed the payload; it is not final-candidate parity evidence.

## Reproducible local results

| Gate | Command or method | Result |
|---|---|---|
| Canonical package structure, links, inline runtime references, naming, placeholders | `.venv/bin/python scripts/check_plugin.py plugins/project-delivery --layout source` | Pass: 62 files, 13 skills |
| Semantic authored route contracts | `.venv/bin/python scripts/check_routes.py .` | Pass: 21 scenarios, all 13 skills referenced, evidence class `semantic-contracts` |
| Historical blind route shapes with post-hoc annotations | `.venv/bin/python scripts/check_route_receipts.py tests/fixtures/blind-route-observations-v1.3.1.json --root . --allow-subset --allow-historical-annotations` | Pass: 17 preserved route shapes remain structurally compatible; current-policy and candidate-behavior conformance are explicitly not established |
| Exact package boundary and deterministic payload | `.venv/bin/python scripts/check_distribution_bundle.py plugins/project-delivery` | Pass: exactly 62 declared regular files with their exact parent-directory set, 13 skills, three shared runtime documents, zero symlinks/executables/source-only or undeclared entries; working-tree payload SHA-256 `c4ca4e628a7786141a90b767707198c3a7f05d411444395a9d6097a85a8016f9` |
| Validator regressions | `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v` | Pass: 67/67, including exact materialization/parity positives and adversarial extra-file/directory, forbidden empty-directory, symlink, executable, unsafe-replacement, swap-recovery, marketplace-containment, semantic-freeze, evidence, authority, controller, privacy, and dependency cases |
| Repository marketplace and legal parity | `.venv/bin/python scripts/check_marketplace.py .` | Pass: sole entry resolves inside the repository to `plugins/project-delivery`, identity/category/policies match, and root/package MIT text is byte-identical to the approved Andrew Cox license |
| Plugin Creator | system `plugin-creator/scripts/validate_plugin.py plugins/project-delivery` in the project `.venv` | Pass |
| Skill Creator | system `skill-creator/scripts/quick_validate.py` over every skill with visible 13-item progress | Pass: 13/13 |
| HOL scanner lint | `.venv/bin/plugin-scanner lint plugins/project-delivery --format text` | Policy pass; effective score 92; no critical, high, or medium finding |
| HOL scanner full scan | `.venv/bin/plugin-scanner scan plugins/project-delivery --profile default --format text --min-score 80 --fail-on-severity high` | Pass: 92/100, grade A; 0 critical/high/medium, 1 low, 3 informational findings |
| HOL scanner runtime verification | `.venv/bin/plugin-scanner verify plugins/project-delivery --format text` | Pass: manifest, capability enumeration, interface assets, 13 skill manifests/frontmatter/references, and asset-size checks |
| Pre-hardening isolated repository-marketplace install | `CODEX_HOME=<isolated> codex plugin marketplace add <repo>` then `codex plugin add project-delivery@project-delivery` | Historical pass: repository marketplace resolved `./plugins/project-delivery`, installed a 62-file `1.4.0-rc.1` working-tree payload, and supported removal; later candidate bytes differ |
| Pre-hardening isolated source/cache parity | `.venv/bin/python scripts/check_installed_parity.py plugins/project-delivery <isolated-cache-version-dir>` | Historical pass at payload SHA-256 `e5f66a442bc7815a7199a28cf24b3da5e6a0bf0dc95e34ba92d23cd915bb8a1b`; does not establish parity for the final package |
| Supported pre-hardening isolated cleanup | `codex plugin remove project-delivery@project-delivery` then `codex plugin marketplace remove project-delivery` under the isolated home | Historical pass: plugin and marketplace removed before the temporary home was deleted |
| Independent packaging/security/release review | Three bounded read-only reviewers over the package-boundary working tree | Review found unsafe replace/empty-directory coverage gaps, missing 1.3.x migration, external-content authority gaps, marketplace regression gaps, and evidence overclaims. Fixes were incorporated; a final independent review after install/canary stabilization remains pending |
| JSON syntax | `python -m json.tool` over the manifest, route contracts, and frozen receipt fixture | Pass |
| Patch whitespace | `git diff --check` | Pass |

The local scanner is `plugin-scanner==2.0.1015` inside the project `.venv`. Its low finding rejects the prerelease-form candidate version `1.4.0-rc.1`; Plugin Creator validation accepts that Semantic Versioning value. The candidate retains an explicit prerelease identity rather than presenting uncanaried work as `1.4.0`. The three informational findings concern absent optional `privacyPolicyURL`, `termsOfServiceURL`, and screenshots. This local, service-free plugin does not fabricate inapplicable legal endpoints or claim UI screenshots that have not yet been captured.

Cisco skill-scanner evidence remains unavailable under the inspection host's Python 3.14 because that optional integration requires an older Python range. HOL Guard continued without that integration. Hosted scanner evidence must be read from the exact pushed candidate or release commit and is not inferred from this local result.

## Corrected interpretation of the prior canary

The prior report's `4/17` result compared one exact expected skill array with each blind selected array. That is not a valid conformance rule for a risk-scaled workflow: several specialists are evidence-triggered, equivalent specialist ordering can be safe, and controller skills can re-enter after recovering evidence.

The original blind route selections are linked from `tests/fixtures/blind-route-observations-v1.3.1.json` through sanitized public identity and SHA-256 digests of the private source observations. Their schema-v2 taxonomy, taxonomy rationales, and conditional dispositions were added afterward, so the fixture declares that its complete semantic records were not frozen and the checker requires a conspicuous opt-in flag. The checker reports these 17 cases as historical route-shape records with `current_policy_claim=not-established`; it does not label them route-policy passes. Retrospective stages named before an outcome are recorded as `planned-future`, not presently activated. This evidence rebuts exact-array scoring only by preserving compatible capability shapes; it does not turn post-hoc interpretation into blind evidence or a route-only observation into implementation, testing, release, or `1.4.0-rc.1` runtime evidence.

The canonical suite now contains 21 cases: the original 17 plus distinct performance, packaging, signing/notarization, and distribution claims. These variants make the combined scenario's hidden authority and evidence branches explicit without removing the original ambiguous catch-all.

## Skill discovery and progressive loading

The source and exact distribution payload contain 13 structurally valid Project Delivery skills, 13 agent manifests, and 26 skill icons. The three skills absent from the crowded desktop task's initial model-visible list—`solution-design`, `testing-quality`, and `security-operations`—were present in source and installed payloads.

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

## Exact package-boundary integrity

Codex CLI `0.144.6` and current inspected upstream source recursively copy every regular file under the selected local plugin source. `.codexignore` is ordinary copied content, not a packaging filter. Project Delivery therefore treats the nested plugin subtree itself as the complete package and rejects any file not in the manifest-derived allowlist.

The distribution check inventories every package file and directory with progress/ETA, rejects symlinks, unsupported file types, executable files, undeclared entries, source-only path components, and missing declared content, materializes the exact payload in a fresh staging directory, reruns structural/internal-reference validation, and emits a deterministic length-prefixed path/content SHA-256. Replacement additionally requires an exact clean destination outside checkout/environment ancestry and retains recoverable prior state across the atomic swap. The independent parity checker compares every prepared-source and installed-cache file and directory and rejects any missing, extra, changed, forbidden, executable, or symlink entry.

The validated bundle contains:

- `.codex-plugin/plugin.json`, README, SECURITY, LICENSE, and the explicitly advisory `.codexignore`;
- plugin composer and logo assets;
- all 13 skills, 13 agent manifests, and 26 skill icons; and
- the shared operating model, artifact templates, and external-systems contract.

No manifest field was invented to force packaging. The canonical subtree contains exactly 62 regular non-executable files and no symlink. No source-only audit, CI file, test fixture, validation script, MCP server, hook, app, executable binary, credential, or legacy plugin is a runtime dependency.

## Decommission and rollback disposition

The migration policy now treats CLI-managed plugins, product-managed or remote-synced plugins, direct skill registrations, symlink discovery, standalone clones, configured sources, and cached payloads as distinct identities and control planes.

An exact rollback record requires selector, owning control plane, enabled state, source revision, manifest and payload hashes, configuration locations without secret values, supported reinstall mechanism, readback, fresh-task verification, and limitations. A mutable marketplace selector or retained cache alone is not exact rollback.

These requirements are now documented, but exact rollback has not yet been proven for every superseded plugin. The available evidence also does not establish a supported disable/uninstall control for every product-managed or remote-synced source. Therefore:

- The polluted active personal installation must be replaced through the supported Plugin Creator cachebuster/reinstall flow before any fresh-task candidate claim. Its cache is not release evidence.
- Superseded plugins may be disabled one at a time only in reversible canaries after exact state capture.
- Permanent uninstall remains blocked.
- The withdrawn external `awesome-codex-plugins` publication must remain closed; no resubmission is part of this candidate.

## Candidate gates still required

Before promoting to `1.4.0`:

1. Freeze an exact RC commit; record its clean state, manifest hash, deterministic package hash, and tag-eligible marketplace path. **Pending after package remediation.**
2. Rehearse exact `1.3.1 → final nested-package candidate → 1.3.1 → candidate` recovery through the same isolated personal marketplace/control plane. **Pending; earlier drills are pre-boundary/pre-hardening evidence only.**
3. Materialize the committed nested package into the personal source path, apply Plugin Creator's cachebuster there, reinstall `project-delivery@personal`, and verify exact prepared-source/cache parity. **Pending.**
4. Confirm the development source manifest retains the committed RC bytes and the source tree is clean. **Pending commit.**
5. Start genuinely fresh Codex tasks under catalog pressure. **Pending.**
6. Record blind semantic receipts for the 21 scenarios, including taxonomy rationale and the complete semantic freeze declaration/evidence, before comparing them with the authored contracts. **Pending.**
7. Verify 13/13 Skills UI cards where expected, 13/13 fully qualified selectors, and orchestrated loading of `solution-design`, `testing-quality`, and `security-operations` even if absent from the initial list. **Pending.**
8. Run bounded repository canaries without unauthorized signing, publishing, deployment, provider mutation, or destructive action. **Pending.**
9. Obtain a refreshed independent diff/release review over package, installed-canary, and recovery evidence. **Pending.**
10. Push the exact candidate, update and merge the PR, require hosted validation/scanner success on the exact merged `main` revision, verify immutable Git/tag transport, and only then create the authorized `v1.4.0-rc.1` tag and GitHub release. **Pending.**

## Release status

Local package-candidate status: **structural and isolated-install gates pass; exact commit and active personal replacement remain pending**.

`v1.4.0-rc.1` tag/release status: **blocked pending exact commit, active installed-cache parity, fresh-task candidate behavior, repository canary, refreshed independent review, and exact-commit hosted CI/scanner evidence**.

Legacy-plugin uninstall status: **blocked pending exact per-control-plane rollback, disable-one-at-a-time observations, stable post-observation state, and explicit user confirmation of the final superseded set**.
