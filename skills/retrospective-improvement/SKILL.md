---
name: retrospective-improvement
description: Close delivery by capturing outcomes, learning, technical debt, follow-up work, reusable decisions, and measurable process improvements in canonical project knowledge.
license: MIT
---

# Retrospective and Continuous Improvement

Read `../.shared/operating-model.md`; use the retrospective template in `../.shared/artifact-templates.md`.

## When to invoke

Use after a meaningful release/initiative, incident/hotfix, failed/cancelled effort, recurring delivery friction, or when maintaining the backlog/knowledge base. Small changes need only notable learning or follow-ups; do not manufacture ceremony.

## Inputs and evidence

Inspect project brief/success measures, requirements/design/plan/RAID/status history, commits/PRs/CI/test/review/release evidence, production metrics/incidents/support feedback when authorized, decisions/assumptions, and existing debt/backlog/knowledge locations.

## Workflow

1. Compare intended outcome and success measures with actual observed results. Separate missing data from failure.
2. Build an evidence-based timeline for material surprises, delays, regressions, incidents, rework, and decision changes.
3. Identify contributing system/process factors without blame. Trace escaped defects or repeated friction to root causes and existing controls.
4. Capture what should continue, stop, or change; prefer one or a few measurable experiments over a large wish list.
5. Record technical debt and follow-ups with rationale, impact, priority, owner or `unassigned`, target/revisit trigger, dependencies, and acceptance/evidence. Do not use vague TODOs.
6. Update canonical ADRs, runbooks, tests, templates, instructions, roadmap/issues, and decision/assumption logs. Link to source evidence; do not create a parallel memory store.
7. Close or explicitly carry forward RAID items, deprecated paths, flags, temporary compatibility, and migration cleanup. Reconcile external tasks, decisions, meeting actions, status pages, and cross-system divergence; retire temporary coordination artifacts when safe.
8. Protect privacy: persist durable project learning, not psychographic profiles, hidden telemetry, or unnecessary personal data.

## Outputs and handoff

Outcome assessment, learning summary, root causes, debt/follow-up ledger, process experiments with measures, RAID closure, and canonical artifacts updated. Route follow-up work through `delivery-orchestrator` as new scoped delivery items.

## Completion evidence

Claims link to delivery/production evidence; open debt has actionable metadata; durable decisions/knowledge live canonically; temporary rollout/migration work is closed or owned; no redundant retrospective file was created when an existing system suffices.

## Must not

- Fabricate metrics/feedback, blame individuals, auto-modify skills/process policy, collect hidden telemetry, or create busywork for small changes.
- Mark follow-ups complete without evidence or treat unowned debt as a plan.
