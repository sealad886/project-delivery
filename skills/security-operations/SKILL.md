---
name: security-operations
description: Assess and improve security, privacy, risk, reliability, observability, supportability, and operational readiness across requirements, design, implementation, review, or release.
---

# Security, Risk, and Operational Readiness

Read `../../references/operating-model.md`.

## When to invoke

Use for sensitive data, authentication/authorization, public/privileged interfaces, dependencies, infrastructure, migrations, high blast radius, reliability/incident work, explicit security review, or production release. Scale a compact checklist into a formal threat model/readiness review as risk rises.

## Inputs and evidence

Inspect repository/security/privacy policies, data flows/classification/retention, trust boundaries and deployment topology, identities/permissions/secrets, dependencies/lockfiles/SBOM or provenance, config/IaC, failure history, SLOs/runbooks/on-call ownership, telemetry/alerts, backups/restore/DR, tests/scans, and current authoritative standards/vendor docs.

## Workflow

1. Define assets, actors, attacker capabilities, entry points, trust boundaries, sensitive data, privileges, invariants, and assumptions. Reuse/update a repository threat model if current; otherwise create one only when risk warrants.
2. Analyze abuse paths and controls: authentication, authorization and tenant isolation, validation/encoding, injection, filesystem/network boundaries, cryptography/session handling, secrets, least privilege, auditability, dependency/supply chain, build/deploy integrity, and denial/resource exhaustion.
3. Analyze privacy: collection/minimization, purpose, consent where applicable, retention/deletion, residency, access/export, logs/telemetry, third parties, and migration/backfill exposure. Escalate legal conclusions to qualified owners.
4. Analyze failure modes and reliability: dependency/timeouts/retries/backoff/circuit breaking, idempotency, consistency, capacity, graceful degradation, backups/restore, DR, partial rollout, config skew, and human error.
5. Define operational readiness: health, logs/metrics/traces, actionable alerts, dashboards, ownership/on-call/support, runbooks, incident/hotfix path, cost/capacity signals, post-release verification.
6. Validate with appropriate static/dynamic/dependency/config/IaC/permission tests and recovery exercises. Calibrate severity using reachability, exploitability, impact, existing controls, and evidence.
7. Produce mitigations with owner/order, verification, rollback, residual risk, and release-blocking decision. Risk acceptance requires authorized ownership.

## Outputs and handoff

Threat/readiness model, finding/risk ledger, required controls, validation evidence, operational checklist, residual risk/acceptance needs, and release decision. Handoff implementation to `implementation-execution`, tests to `testing-quality`, findings to `review-audit`, and gates to `release-change`.

## Completion evidence

Material assets/boundaries/data/permissions/failure modes/operations are covered; mitigations and tests map to risks; severity/confidence are evidence-based; acceptance authority and residual risk are explicit.

## Must not

- Guarantee security/compliance/reliability, run intrusive tests outside authorization, expose credentials/personal data, or add dependencies/integrations by default.
- Treat a scanner’s output as validated or accept security risk on behalf of an unknown owner.
