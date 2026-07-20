# Validation report

Validation date: 2026-07-20

Release candidate: `v1.4.0-rc.1`

Evidence scope: source working tree on `codex/remediate-canary-findings`, the exact canonical package at `plugins/project-delivery/`, Plugin Creator-generated repository marketplace metadata, local validators/scanners, historical contract-blind route observations from the installed `1.3.1` canary, one pre-hardening isolated install/removal rehearsal, one pre-remediation active personal RC install, one pre-remediation forward/back recovery drill, and fresh-task UI/loadability, routing, independent-grading, and iOS Backup Viewer canaries against those pre-remediation bytes. All pre-remediation behavioral/recovery observations are retained as failure-discovery or bounded historical evidence only. Final-package install/cache parity, corrected fresh-task behavior, final-byte recovery, final commit identity, refreshed hosted CI, merged-main identity, Git transport, and release-tag identity remain separate gates.

## Decision

The in-progress `1.4.0-rc.1` candidate passes the local structural, authored semantic route-contract, historical route-shape compatibility, exact package-boundary, regression, marketplace/legal-parity, Plugin Creator, Skill Creator, scanner-policy, and scanner-verification gates listed below. The first fresh-task RC routing attempt failed because its hand-written blind harness used the wrong prompts/envelope and because the plugin had genuine ownership/order defects. Adversarial review then found candidate-identity, exact-load-set, exact-envelope, trigger/outcome, conditional-final-disposition, self-attestation, and unsealed-task-wrapper false positives. Those defects are covered by current regressions and a sealed three-record protocol, but final install, recovery, corrected fresh-task, repository-canary, hosted, merge, Git-transport, tag, and publication gates remain pending.

The first active local install exposed an unacceptable packaging defect: Codex copied the development checkout's `.git`, `.venv`, CI, tests, audit records, validators, and bytecode because `.codexignore` is not an installer filter. That installed payload is rejected as candidate evidence. The repository now makes `plugins/project-delivery/` the canonical 63-file package boundary and keeps all maintainer-only material outside it. A pre-hardening working-tree snapshot installed cleanly in an isolated repository marketplace and was removed through supported commands, but later safety and trust-boundary changes changed the payload; it is not final-candidate parity evidence.

## Reproducible local results

| Gate | Command or method | Result |
|---|---|---|
| Canonical package structure, links, inline runtime references, naming, placeholders | `.venv/bin/python scripts/check_plugin.py plugins/project-delivery --layout source` | Pass: 63 files, 13 skills |
| Semantic authored route contracts | `.venv/bin/python scripts/check_routes.py .` | Pass: 22 scenarios, all 13 skills referenced, evidence class `semantic-contracts` |
| Historical blind route shapes with post-hoc annotations | `.venv/bin/python scripts/check_route_receipts.py tests/fixtures/blind-route-observations-v1.3.1.json --root . --allow-subset --allow-historical-annotations` | Pass: 17 preserved route shapes remain structurally compatible; current-policy and candidate-behavior conformance are explicitly not established |
| Exact package boundary and deterministic payload | `.venv/bin/python scripts/check_distribution_bundle.py plugins/project-delivery` | Pass: exactly 63 declared regular files with their exact parent-directory set, 13 skills, four shared runtime documents, zero symlinks/executables/source-only or undeclared entries; working-tree payload SHA-256 `171583417962def6dda119fc337d1d8db20e40a6b30bb34c431c994815ae38e3` |
| Validator regressions | `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v` | Pass: 117/117, including exact materialization/parity, prompt-only export, canonical task-prompt generation, coordinator freshness/privacy/task binding, closed schema-v3 envelope, semantic and raw-byte digests, three-record grading, installed candidate/instruction identity, exact present-route load set, trigger/outcome/gap/effect matrices, lead ordering, required/final controller ordering, privacy, authority, marketplace, wrapper substitution, and adversarial package-boundary cases |
| Repository marketplace and legal parity | `.venv/bin/python scripts/check_marketplace.py .` | Pass: sole entry resolves inside the repository to `plugins/project-delivery`, identity/category/policies match, and root/package MIT text is byte-identical to the approved Andrew Cox license |
| Plugin Creator | system `plugin-creator/scripts/validate_plugin.py plugins/project-delivery` in the project `.venv` | Pass |
| Skill Creator | system `skill-creator/scripts/quick_validate.py` over every skill with visible 13-item progress | Pass: 13/13 |
| Icon inventory and dimensions | `sips` over plugin and per-skill PNG assets with visible 28-item progress | Pass: 28/28 non-empty decodable PNGs; plugin/skill small icons are 128×128 and large/logo assets are 512×512 |
| HOL scanner lint | project `.venv` Python invoking `codex_plugin_scanner.cli` with `lint plugins/project-delivery --format text` | Policy pass; effective score 92; no critical, high, or medium finding |
| HOL scanner full scan | project `.venv` Python invoking `codex_plugin_scanner.cli` with `scan plugins/project-delivery --profile default --format text --min-score 80 --fail-on-severity high` | Pass: 92/100, grade A; 0 critical/high/medium, 1 low, 3 informational findings |
| HOL scanner runtime verification | project `.venv` Python invoking `codex_plugin_scanner.cli` with `verify plugins/project-delivery --format text` | Pass: manifest, capability enumeration, interface assets, 13 skill manifests/frontmatter/references, and asset-size checks |
| Pre-hardening isolated repository-marketplace install | `CODEX_HOME=<isolated> codex plugin marketplace add <repo>` then `codex plugin add project-delivery@project-delivery` | Historical pass: repository marketplace resolved `./plugins/project-delivery`, installed a 62-file `1.4.0-rc.1` working-tree payload, and supported removal; later candidate bytes differ |
| Pre-hardening isolated source/cache parity | `.venv/bin/python scripts/check_installed_parity.py plugins/project-delivery <isolated-cache-version-dir>` | Historical pass at payload SHA-256 `e5f66a442bc7815a7199a28cf24b3da5e6a0bf0dc95e34ba92d23cd915bb8a1b`; does not establish parity for the final package |
| Supported pre-hardening isolated cleanup | `codex plugin remove project-delivery@project-delivery` then `codex plugin marketplace remove project-delivery` under the isolated home | Historical pass: plugin and marketplace removed before the temporary home was deleted |
| Pre-remediation active personal install/cache parity | Plugin Creator cachebuster/reinstall followed by `scripts/check_installed_parity.py` | Historical pass for installed version `1.4.0-rc.1+codex.20260720090546` and its then-current payload SHA-256 `596da051cd50440390010f3d3a0fba992d87958a16c0ed8d0e381f712d9bca62`; current package bytes differ |
| Pre-remediation isolated forward/back recovery | supported personal-marketplace sequence `1.3.1 → candidate → 1.3.1 → candidate` with readback after each transition | Historical pass for the same `596da051…` candidate; final-byte repetition remains required |
| Pre-remediation fresh-task canaries | UI/loadability, 21-case routing, independent grading, and bounded iOS Backup Viewer task | Static/loadability and bounded repository authority behavior passed; live icon rendering unverified; routing evidence failed because of both invalid harness structure and genuine route defects; current remediation requires a fresh rerun |
| Independent packaging/security/release review | Bounded read-only reviewers over the package-boundary and route-checker working trees | Reviews found unsafe replace/empty-directory coverage gaps, missing 1.3.x migration, external-content authority gaps, marketplace regression gaps, stale identity acceptance, excess load claims, missing exact-envelope enforcement, conditional evidence after release disposition, stale documentation, and evidence overclaims. Fixes through the current local gate were incorporated; a final independent review after install/canary stabilization remains pending |
| JSON syntax | `python -m json.tool` over the manifest, route contracts, closed live-receipt schema, and frozen receipt fixture | Pass |
| Patch whitespace | `git diff --check` | Pass |

The local scanner is `plugin-scanner==2.0.1015` inside the project `.venv`. The checkout move left its ignored console-script shebang pointing at the former path, so the recorded runs use the same environment's Python to invoke `codex_plugin_scanner.cli` directly. This is an environment-launcher limitation, not a distributed-plugin dependency. The scanner's low finding rejects the prerelease-form candidate version `1.4.0-rc.1`; Plugin Creator validation accepts that Semantic Versioning value. The candidate retains an explicit prerelease identity rather than presenting uncanaried work as `1.4.0`. The three informational findings concern absent optional `privacyPolicyURL`, `termsOfServiceURL`, and screenshots. This local, service-free plugin does not fabricate inapplicable legal endpoints or claim UI screenshots that have not yet been captured.

Cisco skill-scanner evidence remains unavailable under the inspection host's Python 3.14 because that optional integration requires an older Python range. HOL Guard continued without that integration. Hosted scanner evidence must be read from the exact pushed candidate or release commit and is not inferred from this local result.

## Corrected interpretation of the prior canary

The prior report's `4/17` result compared one exact expected skill array with each blind selected array. That is not a valid conformance rule for a risk-scaled workflow: several specialists are evidence-triggered, equivalent specialist ordering can be safe, and controller skills can re-enter after recovering evidence.

The original blind route selections are linked from `tests/fixtures/blind-route-observations-v1.3.1.json` through sanitized public identity and SHA-256 digests of the private source observations. Their schema-v2 taxonomy, taxonomy rationales, and conditional dispositions were added afterward, so the fixture declares that its complete semantic records were not frozen and the checker requires a conspicuous opt-in flag. The checker reports these 17 cases as historical route-shape records with `current_policy_claim=not-established`; it does not label them route-policy passes. Retrospective stages named before an outcome are recorded as `planned-future`, not presently activated. This evidence rebuts exact-array scoring only by preserving compatible capability shapes; it does not turn post-hoc interpretation into blind evidence or a route-only observation into implementation, testing, release, or `1.4.0-rc.1` runtime evidence.

The canonical suite now contains 22 cases: 16 general lifecycle/provider scenarios, one explicit combined claim spanning performance, packaging, signing, and distribution, four focused performance, package, signing/notarization, and distribution variants, and one direct retrospective request. The prompt-only exporter derives their IDs and exact text without exposing expected route semantics.

## First RC fresh-task canaries and remediation

The first cache-busted personal RC candidate was structurally exact for its then-current package bytes. A fresh static/UI task found all 13 skills loadable, including `solution-design`, `testing-quality`, and `security-operations`, and found all 28 declared non-empty icon files. Protected-app automation could not inspect Codex's own plugin or skill cards, so visible icon rendering remains unverified and is not claimed.

The first 21-case routing task used three subagents and performed no repository or provider effects, but its hand-written harness was invalid: it supplied at least one wrong prompt, returned a noncanonical envelope, omitted required identity/evidence fields, and used noncanonical state vocabulary. Independent grading therefore produced zero machine-valid fresh records. Narrative comparison still exposed genuine candidate defects: missing coordination for operational handoff, missing quality for documentation validation, missing security for distribution, release decisions before selected evidence, and premature prospective retrospective activation.

The current working tree derives prompt-only inputs from the contracts and has the external coordinator generate the only permitted projectless task wrapper before task creation. The private launch state binds that wrapper, the public slug, clean source revision, prompt manifest, controlling instructions, canonical/prepared/cache identities, marketplace target, and exact parity. A private task record binds the actual task and wrapper digest; capture rechecks the launch state within six hours and publishes only normalized hashes and identities. The closed schema-v3 observation carries structured trigger, outcome, gap, effect, legacy, and complete installed-instruction-closure records. The independent checker reconstructs the canonical wrapper, binds raw bytes, rejects schema-v2 or unattested candidate claims, applies the 22 semantic contracts, and emits a separate digest-linked grade without rewriting failed semantics. Current adversarial regressions reproduce and reject each discovered false-positive class. A new cachebuster, fresh 22-case task, and independent fresh-task review remain required because synthetic three-record tests are not fresh Codex behavior.

The bounded iOS Backup Viewer canary against the pre-remediation candidate preserved the repository's clean tracked state and passed a safe `swift build --build-tests` invocation. It deliberately skipped wrapper, signing, notarization, packaging, launch, deployment, and deletion-capable commands after authority/preflight inspection. This is a plugin authority-behavior pass and a repository release-readiness block, not a release pass. Routing bytes changed afterward, so the bounded repository canary must be repeated.

## Skill discovery and progressive loading

The source and exact distribution payload contain 13 structurally valid Project Delivery skills, 13 agent manifests, and 26 skill icons. A fresh crowded-catalog task statically resolved and loaded all 13, including `solution-design`, `testing-quality`, and `security-operations` when they were absent from the initial model-visible list. Static inspection also found the two plugin icons and every per-skill small/large PNG present and non-empty.

OpenAI's Build Skills documentation states that Codex applies a global initial skill-metadata budget and may shorten or omit entries while loading a selected skill's full instructions later. The candidate therefore:

- frontloads the orchestrator description;
- instructs the orchestrator to resolve every selected specialist from its installed sibling directory;
- requires that specialist's complete `SKILL.md` to be read before application;
- distinguishes initial-list visibility, UI/selector visibility, installed-file presence, successful loading, and actual invocation; and
- treats an unreadable specialist as a blocker rather than silently absorbing its work.

This is package, selector/loadability, and policy evidence for pre-remediation bytes. A freshly installed final candidate must repeat sibling loading under the same crowded catalog. Live plugin-card and skill-card icon rendering remains unverified because the available protected-app automation path cannot inspect Codex itself; the RC must either obtain supported observation or explicitly carry that bounded limitation without claiming visible rendering.

## Authority and wrapper execution

Implementation and quality skills now inspect unfamiliar wrappers and lifecycle scripts before execution. The preflight records writes, deletion, fixed temporary paths, signing/notarization, credential access, network/provider access, package installation, publication, deployment, and permission changes.

Technical success and authority compliance are separate gates. A wrapper that signs an ad-hoc artifact during a test run may produce passing tests while the authority gate still fails. The candidate does not reinterpret a request to build or test as permission to sign, publish, deploy, or mutate an external provider.

The pre-remediation iOS canary passed direct safe build/test compilation but skipped unfamiliar wrappers and every signing, notarization, packaging, launch, deployment, deletion-capable, or provider-mutating path. This confirms bounded authority handling only for the inspected task. It does not establish final-candidate repository or release readiness, and the canary must be repeated after reinstall.

## Exact package-boundary integrity

Codex CLI `0.144.6` and current inspected upstream source recursively copy every regular file under the selected local plugin source. `.codexignore` is ordinary copied content, not a packaging filter. Project Delivery therefore treats the nested plugin subtree itself as the complete package and rejects any file not in the manifest-derived allowlist.

The distribution check inventories every package file and directory with progress/ETA, rejects symlinks, unsupported file types, executable files, undeclared entries, source-only path components, and missing declared content, materializes the exact payload in a fresh staging directory, reruns structural/internal-reference validation, and emits a deterministic length-prefixed path/content SHA-256. Replacement additionally requires an exact clean destination outside checkout/environment ancestry and retains recoverable prior state across the atomic swap. The independent parity checker compares every prepared-source and installed-cache file and directory and rejects any missing, extra, changed, forbidden, executable, or symlink entry.

The validated bundle contains:

- `.codex-plugin/plugin.json`, README, SECURITY, LICENSE, and the explicitly advisory `.codexignore`;
- plugin composer and logo assets;
- all 13 skills, 13 agent manifests, and 26 skill icons; and
- the shared operating model, artifact templates, external-systems contract, and closed live-route schema.

No manifest field was invented to force packaging. The canonical subtree contains exactly 63 regular non-executable files and no symlink. No source-only audit, CI file, test fixture, validation script, MCP server, hook, app, executable binary, credential, or legacy plugin is a runtime dependency.

## Decommission and rollback disposition

The migration policy now treats CLI-managed plugins, product-managed or remote-synced plugins, direct skill registrations, symlink discovery, standalone clones, configured sources, and cached payloads as distinct identities and control planes.

An exact rollback record requires selector, owning control plane, enabled state, source revision, manifest and payload hashes, configuration locations without secret values, supported reinstall mechanism, readback, fresh-task verification, and limitations. A mutable marketplace selector or retained cache alone is not exact rollback.

These requirements are now documented, but exact rollback has not yet been proven for every superseded plugin. The available evidence also does not establish a supported disable/uninstall control for every product-managed or remote-synced source. Therefore:

- The polluted checkout-root installation was replaced through the supported Plugin Creator flow, but the active personal cache now contains pre-remediation RC bytes. It must be replaced with a new cachebuster and exact source/cache parity before any final-candidate claim.
- Superseded plugins may be disabled one at a time only in reversible canaries after exact state capture.
- Permanent uninstall remains blocked.
- The withdrawn external `awesome-codex-plugins` publication must remain closed; no resubmission is part of this candidate.

## Candidate gates still required

Before promoting to `1.4.0`:

1. Freeze an exact RC remediation commit; record its clean state, manifest hash, deterministic package hash, and tag-eligible marketplace path. **Pending commit; current manifest SHA-256 is `b3b7d72234698a6e5788ff2ac839b65453585ee76b5326365f20b1ab6cfc34c2` and current package SHA-256 is `171583417962def6dda119fc337d1d8db20e40a6b30bb34c431c994815ae38e3`.**
2. Rehearse exact `1.3.1 → final nested-package candidate → 1.3.1 → candidate` recovery through the same isolated personal marketplace/control plane. **Pre-remediation sequence passed; final-byte repetition pending.**
3. Materialize the committed nested package into the personal source path, apply Plugin Creator's cachebuster there, reinstall `project-delivery@personal`, and verify exact prepared-source/cache parity. **Pre-remediation candidate passed; final-byte replacement pending.**
4. Confirm the development source manifest retains the committed RC bytes and the source tree is clean. **Pending commit.**
5. Start genuinely fresh Codex tasks under catalog pressure. **Pre-remediation tasks completed; corrected final-byte tasks pending.**
6. Run the coordinator-generated canonical wrapper in a fresh projectless task for all 22 prompt-only scenarios, preserve the exact schema-v3 bytes before contract comparison, capture the coordinator attestation, and obtain the independent digest-linked grade against the exact installed cache and release revision. **First hand-written harness invalid and semantic defects found; sealed corrected run pending.**
7. Verify 13/13 fully qualified selectors and orchestrated loading of `solution-design`, `testing-quality`, and `security-operations` even if absent from the initial list. **Pre-remediation static/loadability pass; final-byte repeat pending. Live Skills UI icon rendering remains unverified.**
8. Repeat bounded repository canaries without unauthorized signing, publishing, deployment, provider mutation, or destructive action. **Pre-remediation authority handling passed and repository release remained blocked; final-byte repeat pending.**
9. Obtain a refreshed independent diff/release review over package, installed-canary, and recovery evidence. **Current-code adversarial review triggered additional fixes; final stabilized-evidence review pending.**
10. Push the exact candidate, update and merge the PR, require hosted validation/scanner success on the exact merged `main` revision, verify immutable Git/tag transport, and only then create the authorized `v1.4.0-rc.1` tag and GitHub release. **Pending.**

## Release status

Local package-candidate status: **structural, semantic-contract, adversarial-regression, scanner, and historical-compatibility gates pass; exact commit and final active personal replacement remain pending**.

`v1.4.0-rc.1` tag/release status: **blocked pending exact commit, active installed-cache parity, fresh-task candidate behavior, repository canary, refreshed independent review, and exact-commit hosted CI/scanner evidence**.

Legacy-plugin uninstall status: **blocked pending exact per-control-plane rollback, disable-one-at-a-time observations, stable post-observation state, and explicit user confirmation of the final superseded set**.
