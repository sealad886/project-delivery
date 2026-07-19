---
name: release-change
description: Prepare, validate, and—when explicitly authorized—execute integration, CI/CD, versioning, deployment, rollback, monitoring, post-release verification, and hotfix/change-management work.
---

# Release, CI/CD, and Change Management

Read `../../references/operating-model.md`; use the release template in `../../assets/artifact-templates.md`.

## When to invoke

Use for PR/branch integration strategy, failing CI, release preparation, version/changelog/release notes, deployment/cutover, migration, rollback, post-release verification, incident/hotfix follow-up, or release-only audit.

## Inputs and evidence

Resolve exact change set/revision, host/branch/PR conventions, required reviewers/status checks, CI workflows and artifacts, version/release/changelog policy, deploy/IaC/config/data migration path, environments, feature flags, approvals/change windows, monitoring/alerts/runbooks, rollback, and prior release evidence. Use repository reality over assumed GitHub flow.

## Workflow

1. Recover traceability: requirements, accepted design, work/PRs, actual tests, docs, review/security findings, and unresolved risks. Missing proof remains a blocker/gap, not a retrospective assertion.
2. Define branch/PR/merge strategy, base/head, dependency order, required approvals/checks, merge queue/rebase policy, and integration test point from repository rules.
3. Diagnose CI failures from actual logs/config; separate change-caused, flaky, infrastructure, and pre-existing failures. Fix only within authority and rerun required checks.
4. Decide version from the project’s release policy/public contract. If Semantic Versioning applies: breaking public contract → major, backward-compatible feature → minor, backward-compatible fix → patch. Prerelease/build metadata follow repository rules.
5. Update canonical changelog/release notes with audience-relevant added/changed/deprecated/removed/fixed/security/migration/known-risk information. Do not use commit dumps as release communication.
6. Plan flags/config/secrets and data/schema migrations, compatibility/coexistence, backfill/verification, deployment order, traffic/canary/staged rollout, stop conditions, and rollback/roll-forward.
7. Confirm monitoring, alerts, ownership, support/runbooks, capacity/cost, observation window, post-release checks, and incident/hotfix route.
8. Produce a release gate decision. Preparation does not authorize merge/tag/push/publish/deploy. Execute each external or production-changing action only when user authority is clear; record timestamp, actor/tool, revision/artifact, result, and rollback readiness.
9. Verify production/user outcome, not only pipeline success. If degraded, stop/rollback/escalate per plan and preserve evidence.

## Outputs and handoff

Release plan/gate, PR/CI/version/changelog/release artifacts, migration/rollout/rollback plan, approvals and actual evidence, post-release result, incidents/hotfixes, and residual risk. Handoff completed work to `retrospective-improvement`.

## Completion evidence

Exact released/prepared revision is known; required checks/approvals and findings are accounted for; rollout/rollback/monitoring/support exist; actual actions/results are distinguished from plans; post-release verification is recorded when deployment occurred.

## Must not

- Merge, tag, push, publish, deploy, change production, or close external work without authority.
- Invent approvals/check results/release dates, assume GitHub, bump versions mechanically, bypass gates, or call pipeline green equivalent to user success.
