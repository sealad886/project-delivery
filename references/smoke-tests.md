# Orchestrator smoke tests

These are static routing simulations for authoring validation and live prompts for post-install/decommission validation.

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

## Post-uninstall assertions

For each live smoke test, record the selected skills and verify that no output asks for `boss`, `epic`, `epic-harness`, Superpowers, `.boss/`, `.harness/`, `.superpowers/`, legacy hooks, or legacy MCP servers. Verify external connectors are treated as optional. A pass requires the expected artifacts, explicit actual/not-run evidence, and no fabricated project history.
