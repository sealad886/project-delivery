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

## Review report

```markdown
Overall decision: approve | approve with residual risk | changes required | blocked
Scope/base/head/environment:
| ID | Severity | Priority | Location | Evidence | Impact | Recommended fix | Blocks release? |
Residual risks and accepted-by:
Positive evidence (brief):
```

## Release plan and evidence

```markdown
Change set/version/target:
Required checks and approvals:
Feature flags/config/data migrations:
Deployment sequence and stop conditions:
Rollback trigger, owner, and tested procedure:
Monitoring/alerts/support/runbook:
Post-release checks and observation window:
Actual results, timestamps, revision/artifact IDs:
Incidents/hotfix/follow-up:
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
