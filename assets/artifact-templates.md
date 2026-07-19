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

| Requirement | Design | Work/PR | Test evidence | Release evidence |
|---|---|---|---|---|
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

| ID | Type | Description | Probability/impact | Owner | Response/trigger | Status |
|---|---|---|---|---|---|---|

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
Assessment mode/snapshot/reviewed surfaces/exclusions/deferred/coverage:
Candidate proof (source → control → sink → reachable boundary), counterevidence, proof gaps, affected-location roles, and disposition:
Residual risks and accepted-by:
Positive evidence (brief):
```

## Release plan and evidence

```markdown
Change set/version/target and provider capability:
Release unit (commit, artifact/deployment ID or digest, provenance, promotion history):
Environment identity (account/project/service/region/config; never secret values):
Required checks and approvals:
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
