---
name: delivery-orchestrator
description: Route an idea, change, review, or release through the minimum sufficient project-delivery lifecycle. Use for end-to-end delivery, ambiguous requests, multi-PR initiatives, or when the correct workflow depth is unclear.
---

# Delivery Orchestrator

## Purpose

Own lifecycle routing and truthful state. Do not replace specialist work; invoke or apply the relevant skills and carry their artifacts forward.

Read `../../references/operating-model.md` before routing. Use `../../assets/artifact-templates.md` when the repository has no canonical format.

## When to invoke

- An idea or request is incomplete, ambiguous, or solution-first.
- The user asks to plan and implement, deliver, ship, or manage a change end to end.
- Work spans multiple PRs, releases, systems, or teams.
- A design-only, review-only, documentation-only, or release-only request needs bounded routing.
- Risk/scale is unclear or the current lifecycle state must be recovered.

## Inputs and evidence

Inspect the user request; applicable `AGENTS.md`; repository status/history/branches/tags; README/contributing/architecture/security docs; code/tests; issue/PR templates; CI/release config; prior plans/ADRs/decisions; available local memory only when authorized and accessible. Treat marketplace/plugin capabilities as optional tools, never assumed facts.

## Workflow

1. Resolve authority and target: report-only, planning-only, design-only, change/build, review, release preparation, hotfix, or authorized release execution. Planning, review, and reporting do not authorize edits.
2. Classify scale and risk using the shared model. Record why.
3. Establish lifecycle state. Reuse valid existing artifacts; do not restart completed phases.
4. Choose the path:
   - Planning-only: context → requirements → solution design at the depth needed for a responsible plan → delivery planning; stop with plan evidence and open decisions, without edits. For a bug, require reproduction evidence or a labeled root-cause hypothesis, the regression proof to add/run, and rollback/recovery notes.
   - Small/low-risk change/build: `project-context` delta → `requirements-acceptance` compact AC → lightweight design/plan if needed → implementation → targeted quality → docs/review/release checks proportional to impact.
   - Medium change/build: context → requirements → solution design → delivery plan → implementation → quality → docs → independent review/security/operations → release → retrospective.
   - Large/multi-PR change/build: full medium path plus ADRs, RAID, milestones, critical path, PR/release slicing, integration gates, status cadence, staged rollout, and post-release learning.
   - Design-only: context → requirements → solution design; stop with decision/open-question handoff.
   - Review-only: resolve exact scope/base → review-audit; add security-operations and release-change checks when risk warrants.
   - Release-only: recover requirements/test/review evidence → route missing test, documentation, review, or security/operations evidence to its owning skill → return to release-change; do not retroactively claim missing proof.
   - Documentation-only: compact context/AC → documentation-knowledge → appropriate link/build checks. Add security-operations and release-change checks when the documentation concerns operations, configuration, migration, deployment, rollback, or production support.
   - Hotfix/incident: establish incident facts and authority → compact requirements/design for the safest bounded fix → root-cause implementation → targeted regression plus the broadest time-feasible quality gate → authorized release/rollback and post-release verification → retrospective/follow-up. Record every deferred normal gate and owner.
5. Apply gates. Implementation may begin only when the Ready and necessary Design gates are satisfied. For low-risk work these may be concise and implicit in inspected evidence, but state that evidence.
6. Maintain a visible checklist/status for multi-stage work. Report blockers, decisions, evidence, and next transition.
7. End with the handoff contract and residual risk.

## Outputs

A routing decision, scale/risk rationale, lifecycle checklist, artifact/evidence index, gate status, next skill(s), and blockers or authority needs.

## Completion evidence

The path covers the requested outcome; no required gate is silently skipped; existing artifacts were checked; facts/requirements/assumptions/decisions/questions are distinct; the next transition is executable.

## Must not

- Implement a material or risky change before requirements and design are sufficiently clear.
- Force full ceremony on a trivial low-risk change.
- Auto-approve requirements/design, fabricate owners/estimates/evidence, or treat missing legacy runtimes as available.
- Create plugin-branded project state, require another plugin, or perform external/destructive/release actions beyond user authority.
