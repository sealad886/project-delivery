---
name: testing-quality
description: Select, execute, and report risk-based validation for a change or release candidate. Use for unit, integration, end-to-end, contract, regression, invariant, static, performance, security, CI-parity, and failure-triage evidence.
---

# Testing and Quality Engineering

Read `../../references/operating-model.md`; use the test evidence template in `../../assets/artifact-templates.md`.

## When to invoke

Use after implementation, during planning/design to define strategy, when CI fails, for release gates, or for test-only/quality requests. Select depth from scale, blast radius, failure modes, and repository norms—not a universal coverage percentage.

## Inputs and evidence

Expect exact target revision/diff and requirements/acceptance when available. Inspect test layout, CI workflows, build/lint/type/format commands, coverage/performance/security thresholds, test data/fixtures, service dependencies, environments, flaky-test policy, and past related failures.

## Workflow

1. Build a risk-to-test matrix. Cover changed logic and the most consequential regressions, boundaries, permissions, failure/retry/recovery paths, data compatibility, concurrency/idempotency, and operational signals.
2. Select applicable levels: unit, component, integration, contract/API/schema, end-to-end/user journey, regression/characterization, property/invariant/fuzz, migration/rollback, static analysis, type/lint/format, dependency/security, performance/load/resource, accessibility, docs/link/example/build.
3. Prefer deterministic, isolated, maintainable tests; specify environment, versions, data provenance, seeds, credentials handling, external-service substitution, and cleanup.
4. Run targeted checks early, then the broadest practical repository/CI-parity gates. Capture command, exit status, revision, environment, counts/duration, and artifact/log locations.
5. Triage failures: reproduce, distinguish product/test/environment/flaky/pre-existing failure, isolate root cause, make the smallest authorized correction, and rerun the relevant slice plus regression gates. Never hide or blanket-retry a failure into green.
6. Compare each `AC-*`/risk to actual evidence. Mark verified, failed, not run with reason, or not applicable.
7. For performance/security claims, use representative measurements/tools and state limitations. A lack of findings is not proof of absence.
8. Produce a gate decision with residual gaps and release impact.

## Outputs and handoff

Test strategy/evidence matrix, actual commands/results, failure triage, requirement coverage, CI parity, gaps, and quality gate decision. Handoff failures to `implementation-execution`; successful evidence to `documentation-knowledge`, `review-audit`, and `release-change`.

## Completion evidence

Relevant tests actually ran; results are tied to the target revision/environment; failures and not-run checks are explicit; acceptance and risk coverage are traceable; residual confidence is calibrated.

## Must not

- Say “should pass,” use fixed coverage/E2E mandates unrelated to repository/risk, or confuse selected tests with complete system assurance.
- Alter tests merely to accept incorrect behavior, expose secrets/test personal data, or claim CI parity without comparing workflows.
