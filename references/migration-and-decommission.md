# Migration, capability parity, and decommission

## Replacement scope

Project Delivery is designed to remain fully useful after Boss, Epic, Superpowers, and overlapping generic delivery/workflow packs are uninstalled. Coexistence is temporary for comparison and rollback. It does not call or reference their runtime state.

Do not equate workflow replacement with live access. Project Delivery fully replaces generic PM/delivery methodology, including workflow ideas synthesized from connectors, but cannot reproduce authenticated service access without an adapter. GitHub, security scanners, deployment/platform tools, documents, and business connectors may therefore remain optional access/depth adapters; uninstalling one removes its live surface unless equivalent access remains. Decide adapter status explicitly and never copy app IDs, MCP declarations, credentials, or provider contracts into core.

## Migration map

| Legacy source/capability | Canonical destination | Migration treatment |
|---|---|---|
| Superpowers brainstorming | `project-context`, `solution-design` | Keep repo-first refinement and alternatives; scale questions/approval to risk |
| Superpowers writing/executing plans | `delivery-planning`, `implementation-execution` | Keep executable ordering and handoff; remove forced microtasks/plugin paths |
| Superpowers TDD/systematic debugging/verification | `implementation-execution`, `testing-quality` | Keep root-cause and fresh evidence; make test method domain/risk appropriate |
| Superpowers subagent development/review | `delivery-orchestrator`, `review-audit` | Keep optional independence; no mandatory model/agent or per-task review |
| Superpowers worktrees/branch finish | `implementation-execution`, `release-change` | Keep provenance/destructive safety; use repository dependency policy |
| Epic discover/spec | `project-context`, `requirements-acceptance` | Keep problem/requirement/AC traceability; no harness state or auto-approval |
| Epic go/tdd/debug/perf | `implementation-execution`, `testing-quality` | Merge implementation/debug/performance paths; remove arbitrary thresholds |
| Epic audit/eval/verify | `review-audit`, `testing-quality` | Keep exact evidence, dedup, independent review, acceptance coverage |
| Epic secure/threat-model/vuln/triage | `security-operations`, `review-audit` | Keep the evidence chain; omit runtime-specific CLI/MCP paths |
| Epic commit/ship | `implementation-execution`, `release-change` | Keep Conventional Commits/CI evidence; detect host and require authority |
| Epic context/orchestrate/team/council | `delivery-orchestrator`, shared handoff | Keep lifecycle state, dependency, delegation, and independent-decision concepts; exclude plugin-specific protocols |
| Epic document/reflect/evolve | `documentation-knowledge`, `retrospective-improvement` | Keep canonical docs/learning; exclude self-modification, telemetry, profiling |
| Boss lifecycle DAG/commands | `delivery-orchestrator` | Keep phases and slice entry points; no missing CLI/hook enforcement |
| Boss brainstorming/PM/PRD | `project-context`, `requirements-acceptance` | Keep product rigor optionally; add traceability/NFR/privacy/accessibility |
| Boss architecture/API/UI states | `solution-design`, requirements/docs | Keep contracts, states, accessibility; update existing design system |
| Boss task breakdown/risk/evidence waves | `delivery-planning` | Expand to WBS, RAID, critical path, status/change control, multi-PR/release |
| Boss frontend/backend agents | `implementation-execution` | One repository-driven execution policy; no framework personas |
| Boss QA/Playwright/testing guides | `testing-quality` | Keep actual results/attack checks; remove mandatory E2E/fixed thresholds |
| Boss tech review | `review-audit` | Add exact finding schema, independent/security/release modes |
| Boss deploy/monitor/changelog | `release-change`, `security-operations` | Add approvals/versioning/flags/migrations/rollback/post-release/incident path |
| Boss artifact/memory layer | shared operating model and canonical repo docs | Preserve artifact semantics; exclude missing renderer/memory runtime and `.boss` tree |
| Everything Claude Code plan/orchestrate/TDD/review/verify/docs | corresponding canonical lifecycle skills | Generic delivery overlap replaced; language/framework pattern skills remain separate if desired |
| Standalone create-plan/ADR/quality/adversarial/security/commit skills | planning/design/review/security/implementation | Canonical lifecycle absorbs general behavior; retain specialist skills only if deeper scope is still wanted |
| Marketplace PASS/LIGHT/FULL, acceptance receipts, fresh-eyes review, roadmaps/waves | orchestrator/planning/quality/review/release | Attribution-free synthesis; no executable/runtime dependency imported |
| Curated trackers/docs/meetings/messages/calendars | `delivery-coordination`, context/planning/docs | Absorb source-of-truth, mapping, meeting/status, exact-target, authority, and receipt method; provider access remains optional |
| Curated CI/security/deployment/observability/flags | quality/review/security/release | Absorb evidence contracts and gates; provider commands/runtimes remain optional |

## Intentionally excluded legacy behavior

- Epic runtime memory/orchestrator/hooks/MCP, which are unavailable in the inspected installation.
- Boss CLI event store/rendering/enforced gates/hooks, which are absent in the inspected cache.
- Self-modifying skills, hidden/default telemetry, psychographic profiling, external branding requests, and branded project state.
- Universal TDD/E2E/coverage/performance thresholds, auto-approved specs, mandatory agent swarms, forced squashing/rebasing, and hard-coded GitHub/Node/framework workflows.
- Plugin installation/update commands that mutate global environments.

Exclusion means the inspected mechanism is not reproduced; the user outcome is covered through independently implemented skills, canonical artifacts, explicit evidence, and repository-native tools.

## Decommission readiness gates

1. Manifest, skill, and link validators pass at the release revision.
2. All 13 skills are discoverable in a fresh task after installation.
3. Active repository instructions, prompt templates, hooks/configuration, and prior plans have been checked for imperative legacy calls; archival provenance is clearly non-operative.
4. The smoke scenarios in `smoke-tests.md` produce expected artifacts and routing without invoking legacy plugins.
5. At least one real small change and one medium or multi-PR dry run complete with requirement-to-evidence traceability.
6. Review/security/release flows work with legacy plugins disabled in a canary task.
7. Canonical repository artifacts are used; no new `.boss`, `.harness`, or `.superpowers` state appears.
8. Optional specialist-plugin decisions are recorded individually.
9. A rollback exists: preserve the pre-uninstall plugin list/config and reinstall source/version information without retaining secrets.
10. User confirms the superseded plugin list and accepts any explicitly documented parity exclusions.

## Safe decommission sequence

1. Install/refresh Project Delivery through the personal marketplace and start a new task.
2. Inspect active instructions, prompt templates, hooks/configuration, historical plans, and branded state. Convert imperative legacy calls to non-operative provenance and move durable decisions into canonical current artifacts.
3. Capture the installed plugin/configuration rollback inventory, then run the smoke suite with all plugins still installed; correct gaps using Plugin Creator's cachebuster/update flow.
4. Disable (do not immediately delete) one superseded generic lifecycle plugin at a time, beginning with the most redundant.
5. Start a fresh task and rerun affected smoke scenarios after each change.
6. If parity holds, uninstall that plugin using Codex's supported plugin workflow; do not hand-edit global configuration.
7. Retain specialist plugins unless explicitly classified as superseded.
8. After the observation window, record final plugin set, versions, smoke evidence, residual gaps, and rollback status.

This document is guidance; the plugin does not uninstall or modify any existing plugin.
