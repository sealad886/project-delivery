# Project Delivery

Project Delivery is a self-contained Codex plugin for taking software work from an incomplete idea to a maintained production change. It is intended to replace fragmented project-management and software-delivery workflow plugins after its decommission gates pass. It uses repository evidence and existing project conventions, scales ceremony to risk, and keeps requirements, design, implementation, verification, documentation, review, security, release, and follow-up traceable.

## Canonical lifecycle

`Context → Requirements → Solution Design → Delivery Plan → Implementation → Quality → Documentation → Review and Operational Audit → Release → Retrospective`

Start with `delivery-orchestrator` for end-to-end work or invoke a lifecycle skill directly for a bounded request. The plugin has no MCP server, app, hook, external CLI, telemetry, or dependency on another plugin.

## Skills

- `delivery-orchestrator`: classify work and route the minimum sufficient lifecycle.
- `project-context`: refine an idea into an evidence-backed project brief.
- `requirements-acceptance`: define traceable requirements and acceptance criteria.
- `solution-design`: design production-ready changes and ADRs.
- `delivery-planning`: build scalable WBS, RAID, milestone, and multi-PR plans.
- `implementation-execution`: implement approved work safely and incrementally.
- `testing-quality`: select and run risk-based verification with real results.
- `documentation-knowledge`: update canonical user, developer, operator, and release knowledge.
- `review-audit`: independently review design or changes with actionable findings.
- `security-operations`: assess security, privacy, reliability, and operational readiness.
- `release-change`: prepare, execute when authorized, and verify releases and change rollouts.
- `retrospective-improvement`: capture learning, debt, and bounded follow-up work.

Shared conventions are in `references/operating-model.md`; reusable templates are in `assets/artifact-templates.md`.

The audit, capability-parity map, and safe uninstall sequence are in `references/environment-audit.md` and `references/migration-and-decommission.md`. Coexistence with legacy plugins is a validation phase, not an ongoing dependency model.

## Safety and dependencies

Repository instructions and user authority always win. External issue trackers, source hosts, CI systems, deployment platforms, and memory tools are optional surfaces used only when present and authorized. Publishing, merging, deploying, destructive operations, and external writes require the authority appropriate to their impact.
