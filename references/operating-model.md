# Shared operating model

## Principles

1. Inspect before inventing. Read applicable instructions, canonical docs, source, tests, history, CI/release configuration, and relevant prior artifacts.
2. Reuse before create. Extend canonical modules and documents; do not introduce shadow implementations or parallel process folders.
3. Scale to risk. Use the smallest path that still protects users, data, operations, and compatibility.
4. Separate epistemic states. Label repository/tool facts, user requirements, assumptions, agent decisions, open questions, and residual risks.
5. Trace outcomes. Give requirements stable IDs and connect them to design decisions, work items, tests, findings, and release evidence.
6. Evidence before claims. Completion requires actual command results or directly inspected artifacts, with failures and omissions disclosed.
7. Preserve authority. Do not merge, publish, deploy, delete, rewrite history, or communicate externally without appropriate authorization.

## Scale and risk classification

Classify on two axes before routing.

| Scale | Typical shape | Default depth |
|---|---|---|
| Small | Docs/config/isolated fix; one PR; known pattern | Brief delta, acceptance checks, compact plan, targeted verification |
| Medium | Cross-module feature/refactor; one or a few PRs | Full requirements/design, WBS, risk-based test strategy, independent review |
| Large | Cross-team/system/migration; multi-PR or multi-release | Formal brief, traceability, ADRs, RAID, milestones, dependency/critical path, staged release |

Raise rigor for authentication/authorization, sensitive or regulated data, money, destructive migrations, public APIs, infrastructure, high blast radius, weak rollback, novel technology, irreversible decisions, concurrency, or production incidents. Lower ceremony only when evidence supports low risk—not merely because the diff is small.

## Lifecycle gates

- Context gate: problem, desired outcome, scope, constraints, success measures, facts/assumptions/questions are understandable.
- Ready gate: acceptance criteria are testable; dependencies and material unknowns are owned; design depth matches risk.
- Design gate: interfaces, compatibility, migration/rollback, security, operability, tests, and release effects are addressed.
- Plan gate: work is ordered, owned or explicitly unassigned, dependency-safe, incrementally deliverable, and verifiable.
- Implementation gate: approved scope is implemented using repository conventions; unrelated changes are preserved.
- Quality gate: selected checks ran against the relevant revision/environment and results are recorded.
- Release gate: blockers are closed or explicitly accepted by an authorized owner; rollback and post-release checks exist.
- Learning gate: outcomes, debt, decisions, and follow-ups are captured in canonical locations.

For a small low-risk change, gates may be short sections in one status update. Never erase the gate; compress it.

## Canonical artifacts

Prefer existing repository locations and formats. If none exist, use the templates in `../assets/artifact-templates.md` and place artifacts where maintainers will find them, such as `docs/`, an issue/PR, or the user-requested path. Do not create `.boss`, `.harness`, `.superpowers`, or plugin-specific project state.

- Project brief: problem, outcome/value, scope/non-scope, context, constraints, facts, assumptions, risks, questions, success, DoR/DoD.
- Requirements set: `REQ-*` functional/non-functional requirements, stories/work items if useful, `AC-*`, edge cases, traceability.
- Solution design: current/proposed state, alternatives, contracts, compatibility, migration/rollback, observability, security, testing, release.
- ADR: durable decision, status, context, decision, alternatives, consequences, implementation/revisit conditions.
- Delivery plan: WBS (`WI-*`), milestones (`MS-*`), dependencies, critical path, estimates/confidence, PR/release slices, communication/change control.
- RAID log: risks (`RISK-*`), assumptions (`ASM-*`), issues (`ISS-*`), dependencies (`DEP-*`) with owner, response, trigger/due date, state.
- Test strategy/evidence: scope, risk coverage, environments/data, commands/results, requirement mapping, gaps.
- Review report: findings (`FIND-*`) with severity, priority, location, evidence, impact, fix, release-blocking state, residual risk.
- Release plan/evidence: version/change set, gates, approvals, rollout, migrations, observability, rollback, post-release result.
- Status report: outcome/health, completed, in progress, next, RAID changes, decisions needed, evidence links.
- Decision/assumption log: durable decision/assumption, evidence, owner, date, consequences, revisit trigger.

## Traceability

Use stable IDs only when they add value. Recommended chain:

`Outcome → REQ-* → AC-* → DESIGN/ADR → WI-*/PR → TEST-* → FIND-* → RELEASE-*`

A compact change may use a small table. Large work should use a matrix. Do not manufacture precision: mark links `planned`, `implemented`, `verified`, `deferred`, or `not applicable`.

## Definitions

Definition of Ready means implementation can begin responsibly: objective and boundaries are clear, acceptance is testable, material dependencies/risks are understood, required decisions are made or owned, and a feasible verification path exists.

Definition of Done means the accepted scope is implemented, relevant requirements are verified, regression/security/operational checks match risk, canonical docs are current, review blockers are resolved or accepted, release/rollback needs are addressed, and evidence plus residual risk is recorded. It does not imply deployment unless deployment is in scope and authorized.

## Severity, priority, and confidence

Severity measures impact: Critical (catastrophic/exploitable or release unsafe), High (major user/system impact), Medium (material but bounded), Low (minor/local), Informational. Priority measures response order: P0 immediate, P1 before release/near term, P2 planned, P3 optional. Keep them separate.

Confidence: High = direct, reproducible evidence; Medium = strong evidence with an unverified link; Low = metadata, inference, or incomplete source. Label inference.

## Handoff contract

Every skill handoff states:

- requested outcome and current lifecycle state;
- artifacts/locations and key IDs;
- facts, requirements, assumptions, decisions, and open questions;
- completed evidence and failed/not-run checks;
- active risks/blockers, owner or needed authority;
- recommended next skill and why.

## Git and working-tree safety

Inspect status before edits. Preserve unrelated user changes; do not stage them. Use the repository’s branch and commit conventions. Conventional Commits are appropriate when required by repository/user instructions. Never bypass hooks, use destructive cleanup, rewrite shared history, or publish without authority. For Python, use the repository `.venv` or an isolated environment; never install into a global interpreter.
