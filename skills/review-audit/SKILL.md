---
name: review-audit
description: Independently review a design, plan, diff, PR, repository slice, or release candidate against requirements, architecture, conventions, tests, security, operations, and release criteria with exact evidence-backed findings.
---

# Code Review and Audit

Read `../../references/operating-model.md`; use the review template in `../../assets/artifact-templates.md`.

## When to invoke

Use for design review, normal code review, security-aware review, adversarial audit, review feedback adjudication, or release-readiness audit. Preserve reviewer independence: use a fresh context or subagent when available and proportionate, but remain useful without one.

## Inputs and evidence

Resolve exact scope/base/head/revision and review mode. Inspect requirements/AC, design/ADRs, plan, diff plus supporting code, applicable instructions, tests/results, docs, CI/release config, Git history, security/operational guidance, and existing findings. Do not review only the patch when unchanged context controls behavior.

## Workflow

1. Select lenses:
   - Design: requirements coverage, alternatives, interfaces, compatibility, migration/rollback, security/operations/test/release feasibility.
   - Code: correctness, invariants, errors, data/concurrency, maintainability, conventions, duplication, compatibility, tests/docs.
   - Security: trust boundaries, attacker inputs, authn/authz, secrets, sensitive data/privacy, dependencies, abuse paths, severity/exploitability.
   - Release readiness: requirement/test evidence, CI, approvals, migrations, flags, observability, rollback, support, residual risk.
2. Trace `REQ/AC → design → diff/work → test/docs/release evidence`; identify omissions and unsupported claims.
3. Validate each candidate finding against source and reachable behavior. Deduplicate by root cause while retaining every affected location.
4. Report only actionable findings with `FIND-*`, severity, priority, exact location, evidence, impact, recommended fix, release-blocking state, and residual risk. Label inference and confidence.
5. Distinguish confirmed defect, design concern, test/evidence gap, question, and accepted residual risk. Do not inflate style preference into correctness.
6. Technically adjudicate incoming review comments; verify before accepting or rejecting them.
7. Re-review fixes and rerun relevant evidence before closing findings. Final states: fixed, not reproducible, accepted residual risk (with authority), deferred/blocked (with owner/action).

## Outputs and handoff

Review decision, scope/revision, finding ledger, requirement coverage, positive evidence (brief), residual risks, blockers, and re-review needs. Handoff fixes to `implementation-execution`, evidence gaps to `testing-quality`, security/operations depth to `security-operations`, and cleared work to `release-change`.

## Completion evidence

Exact scope is pinned; all material lenses were applied or marked not applicable; findings are reproducible and located; blockers/residual risk are explicit; reviewer did not self-approve unverified work.

## Must not

- Implement fixes in a review-only request, fabricate findings for volume, or approve because tests merely exist.
- Require a particular hosting platform/plugin, expose secrets, or claim exhaustive security assurance from a normal review.
