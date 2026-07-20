---
name: delivery-orchestrator
description: Use first to route end-to-end, ambiguous, multi-phase, review, release, incident, or decommission work through the minimum sufficient project-delivery lifecycle when depth, state, or authority is unclear.
license: MIT
---

# Delivery Orchestrator

## Purpose

Own lifecycle routing and truthful state. Do not replace specialist work; invoke or apply the relevant skills and carry their artifacts forward.

Read `../.shared/operating-model.md` before routing. Use `../.shared/artifact-templates.md` when the repository has no canonical format.

After choosing a route, resolve each selected specialist's sibling directory and read its `SKILL.md` before applying it. Codex may shorten or omit entries from the initial skill list when many skills are installed; an omitted catalog entry is not proof that an installed specialist is unavailable. Treat a specialist as unavailable only after its installed file cannot be resolved or read, and record that as a routing blocker instead of silently absorbing its work.

## When to invoke

- An idea or request is incomplete, ambiguous, or solution-first.
- The user asks to plan and implement, deliver, ship, or manage a change end to end.
- Work spans multiple PRs, releases, systems, or teams.
- A design-only, review-only, documentation-only, or release-only request needs bounded routing.
- Risk/scale is unclear or the current lifecycle state must be recovered.
- A legacy workflow is being replaced, disabled, or decommissioned.

## Inputs and evidence

Inspect the user request; applicable `AGENTS.md`; repository status/history/branches/tags; README/contributing/architecture/security docs; code/tests; issue/PR templates; CI/release config; prior plans/ADRs/decisions; authorized external systems and local memory when accessible. Treat plugin and connector capabilities as optional adapters, never assumed facts.

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
   - Coordination/tracker/status/meeting/communication-only: recover canonical sources and authority → `delivery-coordination` → documentation or planning only when durable state changes; do not turn analysis or drafts into external writes.
   - Documentation-only: compact context/AC → documentation-knowledge → appropriate link/build checks. Add security-operations and release-change checks when the documentation concerns operations, configuration, migration, deployment, rollback, or production support.
   - Hotfix/incident: detect/contain and preserve timeline/evidence → mitigate or rollback under explicit incident authority → diagnose and repair → targeted regression plus the broadest time-feasible quality gate → verify recovery and communicate when separately authorized → retrospective/follow-up. Production restoration may precede normal completeness only under incident authority; record every deferred gate and owner.
   - Migration/decommission: inventory active instructions, prompt templates, hooks/configuration, plugin-specific state, prior plans with imperative legacy calls, installed IDs/versions/enabled state, and supported reinstall sources → distinguish active directives from archival provenance → map durable requirements/decisions to canonical current artifacts → capture rollback → disable one candidate at a time → start a fresh task and run affected static and live smoke cases → re-enable on any routing or parity failure → uninstall only after the observation gate and user-confirmed scope. Do not edit consumer repositories or plugin configuration without corresponding authority.
5. Invoke `delivery-coordination` when external sources may contain requirements/decisions, after plans need synchronization, before status or meetings, after review findings need tracking, and during release communication/handoff. Detect provider/tool capability; core execution must still work without it.
6. Apply gates. Implementation may begin only when the Ready and necessary Design gates are satisfied. For low-risk work these may be concise and implicit in inspected evidence, but state that evidence.
7. Maintain a visible checklist/status for multi-stage work. Report blockers, decisions, evidence, and next transition.
8. End with the handoff contract and residual risk.

## Routing contract

Routes are capability and gate contracts, not brittle total-order scripts. Record the lead capability, required specialists, conditional branches, gate precedence, allowed re-entry, and why a conditional specialist was activated, deferred, blocked, or not applicable.

- Preserve lifecycle precedence where both stages apply: context before requirements, requirements before solution design, design before delivery planning, planning before implementation, and implementation before quality evidence. Incident containment and release evidence recovery may precede this sequence.
- Use `testing-quality` when checks must be selected, executed, measured, or triaged. `review-audit` or `release-change` may inspect existing quality evidence without a separate quality branch, but must route there when evidence is missing, failing, stale, quantitative, or needs execution.
- Use `security-operations` for explicit security/privacy/reliability/operations scope, sensitive data, privileged boundaries, infrastructure or migrations, high blast radius, incidents, and production release. Other skills retain their proportional security and operability lenses; a separate security branch is conditional for ordinary low-risk design or review.
- Use `delivery-coordination` when live external sources, trackers, status, meetings, messages, provider mutations, or handoff synchronization are actually involved. Do not append it merely to make a route look complete.
- Use `documentation-knowledge` when canonical knowledge changes or release/operational handoff requires it. Use `retrospective-improvement` after an actual meaningful outcome, incident, failure, cancellation, or recurring friction—not for a route-only simulation.
- For a hotfix or incident, `delivery-orchestrator` owns route recovery while `release-change` owns incident change control, restoration or rollback disposition, and the final recovery decision. Containment and evidence preservation precede nonessential ceremony; supporting security work must not delay an authorized emergency containment action.
- Re-entry is valid when a controller first opens evidence recovery and later makes the final decision, such as `release-change → testing-quality → release-change` or `review-audit → security-operations → review-audit`. Declare both which selected owners require prior controller entry and which owners must finish before the controller's final return; incident containment may be an explicit entry exception when immediate safety requires it.
- Extra proportional safety capabilities are allowed. A behavioral route fails for missing required ownership, unsafe authority, forbidden dependency, invalid gate order, or unexplained conditional omission—not merely because its exact sequence differs from an example.

## Bounded delegation

For large or independently reviewable work, delegation is optional and evidence-driven, never a mandatory swarm. Give each subagent one bounded outcome, exact inputs and repository revision, authority limits, expected artifact, and completion evidence. Use dependency waves and single-writer ownership for overlapping files. A fresh-context agent is preferred for independent review or security assessment when proportionate. Delegation never expands user authority; the primary agent remains accountable for reconciling conflicts, validating evidence, applying gates, and producing the final handoff.

## Outputs and handoff

A routing decision, scale/risk rationale, lifecycle checklist, artifact/evidence index, gate status, next skill(s), and blockers or authority needs.

## Completion evidence

The path covers the requested outcome; no required gate is silently skipped; existing artifacts were checked; facts/requirements/assumptions/decisions/questions are distinct; the next transition is executable.

## Must not

- Implement a material or risky change before requirements and design are sufficiently clear.
- Force full ceremony on a trivial low-risk change.
- Auto-approve requirements/design, fabricate owners/estimates/evidence, or treat missing legacy runtimes as available.
- Create plugin-branded project state, require another plugin, or perform external/destructive/release actions beyond user authority.
