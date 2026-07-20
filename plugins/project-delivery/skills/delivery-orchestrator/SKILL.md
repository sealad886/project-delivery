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
   - Medium change/build: context → requirements → solution design → delivery plan → implementation → quality → docs → independent review/security/operations → release. Activate retrospective only after a meaningful outcome, failure, cancellation, or recurring friction; a prospective route records a `planned-future` conditional disposition but omits retrospective from the present route.
   - Large/multi-PR change/build: full medium path plus ADRs, RAID, milestones, critical path, PR/release slicing, integration gates, status cadence, staged rollout, and post-release learning after an actual outcome trigger.
   - Design-only: context → requirements → solution design; stop with decision/open-question handoff.
   - Review-only: resolve exact scope/base → review-audit; add security-operations and release-change checks when risk warrants.
   - Release-only: recover requirements/test/review evidence → route missing test, documentation, review, or security/operations evidence to its owning skill → return to release-change; do not retroactively claim missing proof.
   - Coordination/tracker/status/meeting/communication-only: recover canonical sources and authority → `delivery-coordination` → documentation or planning only when durable state changes; do not turn analysis or drafts into external writes.
   - Operational documentation and handoff: compact context/AC → documentation-knowledge → security-operations → release-change → delivery-coordination. Add testing-quality when examples, runbook steps, configuration, recovery, or docs builds require executable or measurable validation. Handoff is coordination work even when no external provider write is authorized.
   - Documentation-only: compact context/AC → documentation-knowledge → testing-quality for the appropriate link, example, build, or rendered-output checks. Add security-operations and release-change when the documentation concerns operations, configuration, migration, deployment, rollback, a versioned contract, or production support.
   - Flaky CI or missing-provider-evidence review: testing-quality leads causal triage and same-revision evidence → release-change decides release impact. Add delivery-coordination only for authorized provider reads, status reconciliation, escalation, or communication. Do not insert release-change before quality unless an actual incident or declared controller-entry rule requires it.
   - Failed staged deployment or feature-flag incident: release-change enters for change control and containment disposition → security-operations assesses operational risk → testing-quality recovers evidence → release-change returns for the stop, rollback, or recovery decision. Assessment authority alone does not authorize flag changes, rollback, redeployment, or communication.
   - Preview environment with a data migration: full large change path with security-operations before implementation, executable quality evidence, documentation/runbooks, independent review, and release-change. Delivery-coordination is conditional on provider mutation, shared ownership, status, handoff, or teardown synchronization; retrospective is omitted from the present route with a `planned-future` disposition until an outcome exists.
   - Combined platform performance, packaging, signing, or distribution claim: testing-quality leads the focused, artifact-bound evidence route; security-operations and release-change are required. Add review or documentation only when their declared evidence triggers apply. Testing evidence must precede the release decision.
   - Performance-only claim: testing-quality leads. Security/operations, review, release, and documentation are conditional on the exercised surface and the decision the measurement gates.
   - Package-only claim: release-change enters to pin artifact identity and provenance → testing-quality validates the artifact → release-change returns for the disposition. Security/operations is conditional on contents, permissions, dependencies, provenance, or supply-chain exposure.
   - Signing/notarization claim: security-operations leads, with testing-quality and release-change required; both evidence owners precede the release decision. Review authority never authorizes signing, credential use, notarization submission, or publication.
   - Distribution/installability claim: release-change leads and must enter before, then return after, required testing-quality and security-operations evidence. Delivery-coordination is conditional on authorized provider reads or status work. Review authority never authorizes publishing, deploying, installing, or changing external state.
   - Hotfix/incident: detect/contain and preserve timeline/evidence → mitigate or rollback under explicit incident authority → diagnose and repair → targeted regression plus the broadest time-feasible quality gate → verify recovery and communicate when separately authorized → retrospective/follow-up. Production restoration may precede normal completeness only under incident authority; record every deferred gate and owner.
   - Migration/decommission: inventory active instructions, prompt templates, hooks/configuration, plugin-specific state, prior plans with imperative legacy calls, installed IDs/versions/enabled state, and supported reinstall sources → distinguish active directives from archival provenance → map durable requirements/decisions to canonical current artifacts → capture rollback → disable one candidate at a time → start a fresh task and run affected static and live smoke cases → re-enable on any routing or parity failure → uninstall only after the observation gate and user-confirmed scope. Do not edit consumer repositories or plugin configuration without corresponding authority.
5. Invoke `delivery-coordination` when external sources may contain requirements/decisions, after plans need synchronization, before status or meetings, after review findings need tracking, and during release communication/handoff. Detect provider/tool capability; core execution must still work without it.
6. Apply gates. Implementation may begin only when the Ready and necessary Design gates are satisfied. For low-risk work these may be concise and implicit in inspected evidence, but state that evidence.
7. Maintain a visible checklist/status for multi-stage work. Report blockers, decisions, evidence, and next transition.
8. End with the handoff contract and residual risk.

## Routing contract

Routes are capability and gate contracts, not brittle total-order scripts. Record the lead capability, required specialists, conditional branches, gate precedence, allowed re-entry, required final disposition after selected evidence, and why a conditional specialist was `activated`, `deferred`, `blocked`, `not-applicable`, or `planned-future`.

For a machine-comparable or cross-agent route receipt, use the normalized scale/risk/authority values and conditional-state vocabulary from the shared operating model and the exact closed envelope in `../.shared/live-route-receipt-v3.schema.json`. Preserve a range such as `small-or-medium` or `risk-dependent` when evidence is insufficient; put provisional detail in the rationale instead of inventing a new label. Derive conditional triggers blind from installed runtime instructions; do not open or copy an expected test contract before an external coordinator captures the raw observation. Record only runtime-identified conditional branches in `conditional_dispositions`, and reserve `extra_capability_justifications` for genuinely additional proportional capabilities.

- Preserve lifecycle precedence where both stages apply: context before requirements, requirements before solution design, design before delivery planning, planning before implementation, and implementation before quality evidence. Incident containment and release evidence recovery may precede this sequence.
- Use `testing-quality` when checks must be selected, executed, measured, or triaged. `review-audit` or `release-change` may inspect existing quality evidence without a separate quality branch, but must route there when evidence is missing, failing, stale, quantitative, or needs execution.
- Use `security-operations` for explicit security/privacy/reliability/operations scope, sensitive data, privileged boundaries, infrastructure or migrations, high blast radius, incidents, and production release. Other skills retain their proportional security and operability lenses; a separate security branch is conditional for ordinary low-risk design or review.
- Use `delivery-coordination` when live external sources, trackers, status, meetings, messages, provider mutations, or handoff synchronization are actually involved. Do not append it merely to make a route look complete.
- Use `documentation-knowledge` when canonical knowledge changes or release/operational handoff requires it. Use `retrospective-improvement` after a meaningful observed outcome, incident, failure, cancellation, recovery, or recurring friction. A route-only canary may observe such a pre-existing outcome even though the canary itself performs no delivery; never activate retrospective merely because the canary imagines a future delivery.
- When no meaningful outcome is yet observed, record a conditional retrospective as `planned-future` with `future-pending` and omit it from `actual_route`. When outcome evidence is unknown, defer or block it with a linked structured gap. A future-only branch must not be described as loaded, activated, applied, or complete.
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
