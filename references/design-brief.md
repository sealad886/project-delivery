# Design brief

## Purpose and users

Project Delivery is a complete, independent replacement for fragmented Codex project-management and software-delivery workflows. It serves contributors, agents, product/technical leads, QA/release owners, and multi-team initiatives across greenfield, mature, infrastructure, security, documentation, bug, feature, and refactor work.

## Operating model and lifecycle

Repository evidence and user requirements drive a single risk-scaled lifecycle:

`Context → Requirements → Solution Design → Delivery Plan → Implementation → Quality → Documentation → Review/Security/Operational Audit → Release → Retrospective`

One router owns scale and phase selection. Gates are always present but compress for low-risk changes. Existing repository artifacts and conventions outrank plugin templates.

## Skill taxonomy

Twelve substantial skills have non-overlapping ownership: orchestration; project context; requirements/acceptance; solution design; delivery planning; implementation; testing/quality; documentation/knowledge; review/audit; security/operations; release/change; retrospective/improvement.

## Evidence synthesis

- Superpowers contributes repository-first discovery, explicit design readiness, systematic debugging, test-first options, fresh verification, independent review, and safe branch completion. Rigid universal ceremony and absolute TDD are removed.
- Epic contributes lifecycle traceability, phase gates, audit deduplication, threat-to-triage thinking, CI evidence, and retrospectives. Its unavailable runtime, proprietary state, telemetry, self-modification, and auto-approval are excluded.
- Boss contributes artifact handoffs, repository preflight, write-set/dependency planning, evidence waves, contract matrices, and test result reporting. Its unavailable CLI/hooks, mandatory role swarm, fixed thresholds, and duplicate `.boss` artifacts are excluded.
- Marketplace sources reinforce PASS/LIGHT/FULL routing, acceptance receipts, fresh-eyes review, roadmaps, multi-PR waves, status closeout, and documentation readiness.
- Codex Security, GitHub, CodeRabbit, connectors, and deployment plugins remain optional specialist surfaces. Core lifecycle behavior does not depend on them.

## Dependency and safety policy

No MCP, app, hook, legacy CLI, telemetry, or external service is bundled. Standard Git/repository tools and optional installed integrations may be used when discovered and authorized. External writes, destructive changes, merge/publish/deploy, and risk acceptance respect user/owner authority.

## Replacement and migration strategy

Run a temporary coexistence/canary phase, execute representative smoke tests, close parity gaps, install the local plugin, start a fresh Codex task, then uninstall only plugins explicitly marked superseded. Preserve specialist connectors/plugins not covered by the decommission scope. The migration map translates old entry points and artifact concepts into canonical skills and neutral repository artifacts; no branded state is imported blindly.

## Maintainability

All skills share one operating model and template set. Descriptions are concise routing contracts. A standard-library checker validates metadata, internal links, names, and placeholders. Audit, research, smoke, and decommission records are versioned with the plugin.
