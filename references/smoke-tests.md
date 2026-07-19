# Orchestrator smoke tests

The canonical authored cases are machine-readable in [`../tests/route-contracts.json`](../tests/route-contracts.json) and validated by `python3 scripts/check_routes.py .`. That check proves contract completeness, valid skill names, taxonomy coverage, and forbidden-runtime declarations. It is static evidence only; it does not execute Codex or prove fresh-task routing.

Use the prompts below for post-install and decommission smoke tests. Record fresh behavior with the Live route receipt in [`../skills/.shared/artifact-templates.md`](../skills/.shared/artifact-templates.md).

| Scenario | Expected routing | Required artifacts/evidence |
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
| Platform performance or packaging claim | quality → release-change | focused scenario, exact revision/device/runtime/build, fresh artifact, comparable measurements/limitations, signing/notarization/distribution evidence if applicable |

## Post-uninstall assertions

Before disabling a legacy workflow, inspect active `AGENTS.md` and repository instructions, prompt templates, hooks/configuration, historical plans with imperative calls, and plugin-specific state. Mark archival provenance as non-operative and capture the installed ID/version/configuration/reinstall rollback inventory without secret values.

For each live smoke test, record:

- exact prompt, repository revision, relevant instructions, task/model identity, timestamp, plugin source version, installation source, and installed cache identity;
- expected and actual route, scale/risk rationale, authority classification, artifacts expected/produced, commands/evidence, result, and residual gaps;
- whether any output requested `boss`, `epic`, `epic-harness`, Superpowers, `.boss/`, `.harness/`, `.superpowers/`, legacy hooks, or legacy MCP servers; and
- whether connectors remained optional and unavailable operations were truthfully reported.

A behavioral pass requires the expected artifacts, explicit actual/not-run evidence, no fabricated project history, and no legacy runtime request. A blocked result is not a pass. Re-enable the disabled plugin immediately if parity or routing fails.

## Evidence classes

- **Static contract pass:** `check_routes.py` validates authored scenario data. It does not establish agent behavior.
- **Fresh-task route pass:** a new task using the installed cache produces a complete route receipt for the prompt.
- **Real-repository canary pass:** authorized work produces repository-native artifacts and actual validation evidence at a pinned revision.
- **Decommission pass:** affected fresh-task and real-repository cases still pass after one legacy workflow is disabled, with rollback captured.

Never collapse these evidence classes into a single `17/17` behavioral claim.
