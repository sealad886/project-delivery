# Orchestrator smoke tests

The canonical authored cases are machine-readable in [`../tests/route-contracts.json`](../tests/route-contracts.json) and validated by `python3 scripts/check_routes.py .`. The suite contains the original 17 canary prompts plus four explicit performance, packaging, signing/notarization, and distribution variants. It proves semantic-contract completeness, valid/disjoint capability owners, substantive conditional-trigger declarations, acyclic entry precedence, occurrence-aware controller-return declarations, taxonomy coverage, and forbidden-runtime declarations. It does not prove whether a trigger is true for a real change, execute Codex, or establish fresh-task routing.

Compare a fresh frozen blind route-only receipt set with `python3 scripts/check_route_receipts.py <receipts.json> --root .`. Before the expected contracts are revealed, freeze the route, scale/risk/authority taxonomy and rationale, conditional dispositions, extra-capability decisions, evidence, and gaps; record the complete freeze scope and evidence. The observation must load every selected specialist, perform no effects, start no legacy runtime, and mark delivery not run. Required capabilities and safety edges must pass; conditional omissions require evidence and a disposition; extras require evidence and justification. Equivalent unconstrained specialist order and declared two-sided controller entry/return are allowed. Never grade a risk-scaled route by exact total-array equality. The separate `--allow-historical-annotations` option exists only to regression-check preserved historical route shapes whose semantic annotations were added later; it cannot establish current-policy conformance, candidate behavior, or delivery/authority execution evidence.

Use the prompts below for post-install and decommission smoke tests. Record fresh behavior with the Live route receipt in [`../plugins/project-delivery/skills/.shared/artifact-templates.md`](../plugins/project-delivery/skills/.shared/artifact-templates.md).

| Scenario | Semantic routing policy | Required artifacts/evidence |
|---|---|---|
| Clarify and plan this small bug fix | orchestrator planning-only → compact context → compact AC → design delta if needed → plan; stop without edits | problem/root-cause hypothesis, scope, AC, short ordered plan, targeted test and rollback note |
| Design and implement this medium-sized feature | context → requirements → design → plan → implementation → quality → docs → review/security as risk → release prep | brief, REQ/AC, design/tradeoffs/contracts, WBS, changes, actual tests, docs, findings, release gate |
| Break this large initiative into a series of PRs | orchestrator planning-only → full context/requirements/design/planning with security/operations input; stop without edits | milestones, dependency/critical path, RAID, PR/release slices, compatibility/flags/migration, evidence waves, status/change control |
| Review this existing PR for release readiness | review-audit + testing-quality evidence recovery + security-operations as risk + release-change gate | exact base/head, traceability, actual CI/tests, located findings, release blockers/residual risk, rollout/rollback/monitoring |
| Prepare this completed change for production release | release-change, with missing-evidence routing back to quality/docs/review | exact revision, approvals/checks, version/changelog, migrations/flags, staged rollout, rollback, monitoring, post-release plan |
| Document and hand off this operational change | compact context/AC → documentation-knowledge → security-operations/release checks | canonical runbook/config/migration/support docs, validation, ownership, monitoring/rollback, handoff status |
| Design-only request | context → requirements → solution-design; stop | decision-ready design/ADR, alternatives, risks/questions; no implementation |
| Review-only request | resolve exact scope → review-audit; no edits | evidence-backed findings and decision; no implementation unless separately authorized |
| Documentation-only change | compact context/AC → documentation-knowledge → docs validation | canonical doc edit, link/example/build evidence, no invented code tests |
| Post-release incident/hotfix | orchestrator hotfix path → root-cause implementation → targeted+broad quality → release/change → retrospective | incident facts, minimal fix, regression evidence, authorized rollout/rollback, post-release checks, root cause/follow-up |
| Turn meeting notes into tracked follow-up | coordination → requirements/planning only as needed; preview before writes | source/as-of, confirmed decisions, action provenance, internal/external mapping, exact targets, authority, write receipts or drafts |
| Reconcile tracker, spec, and repository status | coordination → docs/planning as divergence requires | source-of-truth map, native/normalized states, contradictions, freshness, reconciliation actions and receipts |
| Security diff with suppressed and deferred candidates | review-audit + security-operations + quality validation | pinned revision/scope/coverage, proof and counterevidence, stable findings, explicit suppressed/deferred closure and owner |
| Flaky CI or external missing logs | quality → release-change with provider capability fallback | first causal signal, native/external provider, same-revision rerun, classification, narrow retry or explicit evidence gap |
| Flagged staged release and failed deployment | release-change + security-operations + coordination for separately authorized communications | immutable release unit, environment, flag lifecycle, state transition, telemetry baseline/window/result, stop/rollback, incident timeline |
| Preview environment with data migration | planning → security-operations → quality → release-change | revision/data/secrets isolation, parity/TTL/teardown, migration compatibility, restore rehearsal, artifact-bound evidence |
| Combined platform performance or packaging claim | quality/security/release owners as applicable; surface unresolved variant predicates | focused scenario, exact revision/device/runtime/build, fresh artifact, comparable measurements/limitations, signing/notarization/distribution evidence if applicable |
| Performance-only claim | quality leads; security/review/release/docs are evidence-triggered | focused scenario, comparable baseline, threshold, runs, variance, exact platform/build |
| Package-only claim | release and quality lead; security/review/docs are evidence-triggered | exact package and provenance, content/execution validation, no implicit signing or publication |
| Signing/notarization claim | security, quality, and release lead; no signing action under review authority | read-only signature/certificate/notarization evidence without private material |
| Distribution claim | release, quality, and security lead; coordination only for authorized provider/status work | channel/artifact identity, read-only state, integrity/access checks, no external mutation |

## Post-uninstall assertions

Before disabling a legacy workflow, inspect active `AGENTS.md` and repository instructions, prompt templates, hooks/configuration, historical plans with imperative calls, and plugin-specific state. Mark archival provenance as non-operative and capture the installed ID/version/configuration/reinstall rollback inventory without secret values.

For each live smoke test, record:

- exact prompt, repository revision, relevant instructions, task/model identity, timestamp, plugin source version, installation source, and installed cache identity;
- lead and actual route; required/conditional capability dispositions; precedence/re-entry; loaded specialist paths; scale/risk; authority; artifacts expected/produced; commands/evidence; route and delivery results; and residual gaps;
- whether a legacy identity was merely visible administratively versus actually invoked, requested, started as a hook/MCP/runtime, or used to create `.boss/`, `.harness/`, or `.superpowers/` state; and
- whether connectors remained optional and unavailable operations were truthfully reported.

A route-policy pass requires every mandatory capability, evidence-bearing branch disposition, no-effect authority boundary, specialist load, entry-precedence edge, controller return, justified extra, and forbidden-dependency check. The route-policy checker requires delivery to be not run. A separate real-repository canary may pass delivery only with expected artifacts and actual evidence reviewed at a pinned revision. Administrative inventory visibility alone is not a legacy dependency. A blocked result is not a pass. Re-enable the disabled plugin immediately if parity, state stability, or routing fails.

## Evidence classes

- **Semantic contract pass:** `check_routes.py` validates authored scenario policy. It does not establish agent behavior.
- **Blind fresh-task route-policy pass:** a new no-effect task fixes every semantic route field before seeing the expected contract, then `check_route_receipts.py` validates selection, taxonomy evidence, loading, authority scope, and legacy-runtime absence. It does not validate delivery.
- **Historical route-shape compatibility:** a preserved pre-comparison route may be checked with conspicuously post-hoc semantic annotations. It is regression evidence only and does not establish current-policy or candidate behavior.
- **Real-repository canary pass:** authorized work produces repository-native artifacts and actual validation evidence at a pinned revision.
- **Decommission pass:** affected fresh-task and real-repository cases still pass after one legacy workflow is disabled, with rollback captured.

Never collapse these evidence classes into a single `17/17` behavioral claim.
