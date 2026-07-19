---
name: release-change
description: Prepare, validate, and—when explicitly authorized—execute integration, CI/CD, versioning, deployment, rollback, monitoring, post-release verification, and hotfix/change-management work.
---

# Release, CI/CD, and Change Management

Read `../../references/operating-model.md`; use the release template in `../../assets/artifact-templates.md`.

## When to invoke

Use for PR/branch integration strategy, failing CI, release preparation, version/changelog/release notes, deployment/cutover, migration, rollback, post-release verification, incident/hotfix follow-up, or release-only audit.

## Inputs and evidence

Resolve exact change set/revision, host/provider and available read/write capabilities, base/head/PR conventions, required reviewers/status checks, native versus external CI and artifacts, version/release/changelog policy, deploy/IaC/config/data migration path, environments, feature flags, approvals/change windows, monitoring/alerts/runbooks, rollback, and prior release evidence. Use repository reality over an assumed host or provider.

## Workflow

1. Recover traceability: requirements, accepted design, work/PRs, actual tests, docs, review/security findings, and unresolved risks. Missing proof remains a blocker/gap, not a retrospective assertion.
2. Declare the release unit: commit, artifact/deployment ID or digest, provenance/build result, promotion history, and target account/project/service/region/environment/configuration identity. Prefer build-once/promotion of the exact validated artifact when the platform supports it; record exceptions.
3. Define branch/PR/merge strategy, exact base/head, dependency order, required approvals/checks, native versus external check providers, missing/pending-log gaps, merge queue/rebase policy, and integration test point from repository rules.
4. Diagnose the first causal CI failure from actual logs/config using the quality failure taxonomy. Use same-revision reproduction and narrow evidence-backed retry; never repeatedly retry or redeploy unchanged work. Fix only within authority and rerun required checks.
5. Decide version from the project’s release policy/public contract. If Semantic Versioning applies: breaking public contract → major, backward-compatible feature → minor, backward-compatible fix → patch. Prerelease/build metadata follow repository rules.
6. Update canonical changelog/release notes with audience-relevant added/changed/deprecated/removed/fixed/security/migration/known-risk information. Do not use commit dumps as release communication.
7. Define preview/ephemeral policy (revision, isolated data, secrets, parity gaps, TTL/cost, teardown) and deployment states: build → pre-deploy/migrate → start capacity → readiness → traffic switch/ramp → drain → observe → complete. Record stop signals, readiness/liveness policy, backward-compatible migration window, restore rehearsal, and why code rollback can or cannot undo data/config changes.
8. For every flag record provider/key, safe default/failure behavior, environments/cohorts, owner, ramp, exposure metric, guardrail/stop threshold, kill path, expiry/removal work, and cleanup proof. Flag/config writes require separate external authority.
9. Establish pre-release baseline and release-correlated observation: provider/source, environment, revision/release marker, query/metric, window, threshold, observed delta, redaction/limitations, and stop/rollback decision. Confirm alerts, support/runbooks, drain behavior, capacity/cost, and incident route.
10. Produce a release gate decision. Preparation does not authorize merge/tag/push/publish/deploy, tracker updates, flag changes, or communications. Execute each action only under its authority; record timestamp, actor/tool, target, revision/artifact, result, readback where available, and rollback readiness. Include packaging/signing/notarization/distribution evidence when the platform requires it.
11. Verify production/user outcome, not only pipeline success. If degraded: detect/contain → preserve timeline/evidence → mitigate/rollback → diagnose → repair → verify recovery → communicate when authorized → follow up.

## Outputs and handoff

Release plan/gate, PR/CI/version/changelog/release artifacts, migration/rollout/rollback plan, approvals and actual evidence, post-release result, incidents/hotfixes, and residual risk. Handoff completed work to `retrospective-improvement`.

## Completion evidence

Exact released/prepared revision is known; required checks/approvals and findings are accounted for; rollout/rollback/monitoring/support exist; actual actions/results are distinguished from plans; post-release verification is recorded when deployment occurred.

## Must not

- Merge, tag, push, publish, deploy, change production, or close external work without authority.
- Invent approvals/check results/release dates, assume GitHub, bump versions mechanically, bypass gates, or call pipeline green equivalent to user success.
