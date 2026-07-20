# Artifact templates

Use only the sections proportional to the work. Update existing canonical artifacts instead of duplicating them.

## Project brief

```markdown
# Project brief: <outcome>
Status/owner/date:
## Problem and desired outcome
## User and business value
## Scope / non-scope
## Existing context (with evidence)
## Constraints
## Confirmed facts / user requirements / assumptions / agent decisions
## Risks / open questions
## Success measures
## Definition of Ready / Definition of Done
```

## Requirements and traceability

```markdown
| ID | Requirement | Rationale/source | Priority | Acceptance criteria | Status |
|---|---|---|---|---|---|
| REQ-001 | ... | ... | Must | AC-001, AC-002 | proposed |

### AC-001: <observable behavior>
Given <state>, when <event>, then <outcome>.
Evidence method: <test/inspection/metric>
Edge cases: <boundaries/failures>

| Requirement | Design/decision | Risk/response | Work/PR | Test/finding | Release disposition |
|---|---|---|---|---|---|
```

## Solution design / ADR

```markdown
# Design: <change>
## Current state and constraints
## Proposed state and responsibilities
## Interfaces, data, failure contracts
## Alternatives and tradeoffs (including no change when meaningful)
## Compatibility, migration, rollback
## Security, privacy, reliability, observability
## Test and release implications
## Decisions / assumptions / open questions

# ADR-NNNN: <decision>
Status: Proposed | Accepted | Superseded | Rejected
Context / Decision / Alternatives / Consequences / Revisit triggers / References
```

## Delivery plan, RAID, and status

```markdown
| WI | Outcome | Depends on | Owner | Estimate/confidence | Evidence gate | PR/release |
|---|---|---|---|---|---|---|
| WI-001 | ... | ... | unassigned | M / medium | TEST-001 | PR-1 |

Milestones: MS-001 ...
Critical path: WI-... → WI-...
Incremental value/rollback boundaries: ...

| ID | Type | Description | Probability/impact | Owner | Response/trigger | State | Trace links |
|---|---|---|---|---|---|---|---|

Status: Green | Amber | Red
Completed / In progress / Next / Evidence / RAID changes / Decisions needed
```

## Test strategy and evidence

```markdown
| Test ID | Risk/requirement | Level/type | Environment/data | Command or method | Expected | Result/evidence |
|---|---|---|---|---|---|---|
Failures and triage:
Not run and reason:
Residual gaps:
```

For CI/runtime evidence add: first causal job/step; category; same-revision rerun; retry rationale; focused scenario; revision/device/runtime/build; fresh artifact; baseline/result; limitations.

## Review report

```markdown
Overall decision: approve | approve with residual risk | changes required | blocked
Scope/base/head/environment:
| ID | Severity | Priority | Location | Evidence | Impact | Recommended fix | Blocks release? |
|---|---|---|---|---|---|---|---|
Assessment mode/snapshot/reviewed surfaces/exclusions/deferred/coverage:
Candidate proof (source → control → sink → reachable boundary), counterevidence, proof gaps, affected-location roles, and disposition:
Closure record for suppressed/duplicate/not-reproducible candidates: category, rationale, counterevidence, sibling checks, reviewer/date, revalidation trigger, release treatment, residual uncertainty, canonical finding if duplicate:
Residual risks and accepted-by:
Positive evidence (brief):
```

## Release plan and evidence

```markdown
Change set/version/target and provider capability:
Release unit (commit, artifact/deployment ID or digest, provenance, promotion history):
Environment identity (account/project/service/region/config; never secret values):
Required checks and approvals:
Trace disposition for REQ/AC, RISK, DEC/ADR, TEST, and FIND records:
Preview environment (revision, isolation, parity gaps, TTL/cost, teardown):
Feature flags (key/provider/default/failure behavior/cohorts/owner/ramp/metric/guardrail/kill/expiry/removal):
Config/data migrations, compatibility window, restore evidence:
Deployment state (build → predeploy → capacity → readiness → traffic/ramp → drain → observe) and stop conditions:
Rollback trigger, owner, tested procedure, and data/config limitation:
Monitoring/alerts/support/runbook and telemetry classification/redaction:
Post-release source/query/metric, release marker, baseline, threshold, window, observed result, decision:
Actual results, timestamps, revision/artifact IDs:
Incidents/hotfix/follow-up:
```

## Delivery coordination

```markdown
Source-of-truth map: artifact/field | canonical system + ID/URL | owner | as-of | derived copies | conflict
System inventory: provider | workspace/project | capability | authorization | limitation
Mapping: internal ID | external provider/ID/URL | native status | normalized status | last verified
Sync ledger: proposed action | exact target | authority | result | readback | residual divergence
Meeting brief/record: objective | evidence/pre-read | decisions (confirmed only) | actions/owner/date provenance | unresolved
Communication: audience | channel/recipient | purpose | draft/authorized-to-send | source facts | result
Write receipt: provider | target | actor | timestamp | changed fields | prior/new state | ID/URL | verification
```

## Plugin recovery record

Keep consumer-specific paths and state in the consumer's canonical private artifact. Never record secret values.

```markdown
Identity and display name:
Canonical selector:
Owning control plane:
Pre-action installed and enabled state:
Configured source and immutable source identity:
Marketplace identity and immutable revision:
Cache identity:
Manifest SHA-256:
Payload SHA-256 and deterministic hashing method:
Configuration locations (names/paths only; no secret values):
Supported temporary-disable method:
Supported uninstall method:
Supported reinstall/recovery method and exact version behavior:
Pre-action readback:
Action performed:
Post-action readback:
Fresh-task verification:
Recovery drill result: pass | fail | blocked | not run
Limitations and unresolved control-plane gaps:
Owner and timestamp:
```

## Live semantic route receipt

```markdown
Scenario/prompt:
Plugin source version and commit:
Installed plugin/cache identity:
Task/model identity and timestamp:
Repository revision and relevant instructions:
Discovery evidence: packaged files / Skills UI / initial task list / explicitly loaded specialists
Observation scope and effects performed:
Semantic freeze declaration, complete field scope, evidence, and annotation provenance:
Lead capability and actual route:
Required capabilities and dispositions:
Conditional capabilities: trigger / activated | not applicable | deferred | blocked / evidence and rationale
Gate precedence and controller re-entry:
Loaded specialist source paths:
Justified extra capabilities:
Scale/risk/authority taxonomy rationale and evidence:
Expected / produced artifacts:
Authority classification and actions refused or deferred:
Legacy dependency check: administrative visibility / invocation / runtime or hook start / branded state
Commands/evidence and actual results:
Route outcome: pass | fail | blocked | insufficient receipt
Delivery outcome: pass | fail | blocked | not run
Residual gaps:
```

Semantic route-policy validation checks required owners, evidence-bearing taxonomy and conditional dispositions, entry precedence, two-sided occurrence-aware controller entry/return, route-only authority, specialist loading, justified extras, and forbidden dependencies. It intentionally allows justified proportional specialists and equivalent unconstrained evidence-owner ordering. A fresh behavioral receipt must declare and evidence that its route, taxonomy and rationale, branch dispositions, extra-capability decisions, evidence, and gaps were all frozen before contract comparison. Post-hoc semantic annotations can establish only historical route-shape compatibility. A capability such as retrospective learning may be named `planned-future` when its outcome trigger has not occurred; that is not present activation. The route-policy checker accepts only no-effect observations with delivery marked not run; delivery artifacts and execution evidence require a separate delivery receipt and review.

## Retrospective

```markdown
Expected vs actual outcome:
What helped / what hindered (with evidence):
Escaped defects or surprises and root causes:
Decisions worth retaining:
Debt/follow-ups (owner, priority, target, evidence):
Process experiment and success measure:
Canonical artifacts updated:
```
