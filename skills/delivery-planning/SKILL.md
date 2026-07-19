---
name: delivery-planning
description: Turn accepted requirements and design into a risk-scaled delivery plan with WBS, milestones, dependencies, critical path, ownership, estimates, RAID, communication, change control, and multi-PR/release slicing.
---

# Project Planning and Delivery Management

Read `../../references/operating-model.md`; use the plan/RAID/status templates in `../../assets/artifact-templates.md`.

## When to invoke

Use before implementation, for roadmap or multi-PR decomposition, for replanning after scope/risk change, and for status/escalation. A small change can use a short ordered checklist.

## Inputs and evidence

Expect approved requirements/design or explicitly record what is provisional. Inspect code ownership, module boundaries, tests/CI, release cadence, branch conventions, team/reviewer/deployment constraints when discoverable, existing roadmap/issues, and working-tree state. Never invent people, capacity, dates, or commitments.

## Workflow

1. Build outcome-oriented `WI-*` work breakdown items small enough to own, review, test, and rollback. Keep implementation/tests/docs for the same outcome together when practical.
2. Map dependencies and identify the critical path, integration points, write-set conflicts, external lead times, and decision gates.
3. Define `MS-*` milestones by demonstrable outcomes, not activity completion.
4. Assign confirmed owners or mark `unassigned`; distinguish accountable decision owner, implementer, reviewer, release/operator roles where relevant.
5. Estimate using the repository/team convention. State range/unit and confidence plus uncertainty drivers; do not present agent guesses as commitments.
6. Create/update the RAID log with probability/impact, response, trigger, owner, due/review point, and state.
7. Decompose PRs so each is coherent, independently reviewable, integration-safe, and either value-delivering or a clear enabling slice. Specify base dependencies, contract/compatibility strategy, feature flags, evidence gates, merge order, and rollback boundaries.
8. For multi-release work, define incremental value, migration/coexistence/deprecation phases, release train/cutover gates, and follow-up removal.
9. Define communication/status cadence, stakeholder decisions, escalation triggers, scope baseline, and change-control process proportional to risk.
10. Check DoR/DoD, requirement coverage, resource/conflict constraints, and stop conditions.

## Outputs and handoff

Ordered WBS, dependency/critical-path view, milestones, ownership, estimates/confidence, RAID, PR/release map, evidence waves, communication/change-control plan, and readiness status. Handoff to `implementation-execution` one ready slice at a time.

## Completion evidence

Every in-scope requirement maps to work and evidence; sequence is dependency-safe; critical path and risks are visible; slices are reviewable/releasable; assumptions and unassigned ownership are explicit.

## Must not

- Fabricate owners, deadlines, capacity, velocity, or certainty.
- Use heavyweight ceremony for a trivial change or split PRs solely by technical layer when that creates broken intermediate states.
- Begin implementation, hide contingency, or let plan detail duplicate code that will immediately go stale.
