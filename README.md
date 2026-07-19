<p align="center">
  <img src="assets/project-delivery-logo.png" width="160" alt="Project Delivery compass and route logo">
</p>

# Project Delivery

[![Validate plugin](https://github.com/sealad886/project-delivery/actions/workflows/validate.yml/badge.svg)](https://github.com/sealad886/project-delivery/actions/workflows/validate.yml)
[![HOL Plugin Scanner](https://github.com/sealad886/project-delivery/actions/workflows/hol-plugin-scanner.yml/badge.svg)](https://github.com/sealad886/project-delivery/actions/workflows/hol-plugin-scanner.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Project Delivery is a self-contained Codex plugin that turns an incomplete idea or bounded request into a traceable, production-oriented change. It provides one repository-grounded, risk-scaled evidence spine from outcome through requirements, design, planning, implementation, verification, documentation, independent review, security and operational readiness, release, and learning.

It is designed to become the sole generic project-management and software-delivery workflow after its adoption gates pass. It does not replace authenticated connectors, CI systems, platform tooling, security scanners, deployment providers, observability systems, or other specialist evidence sources.

## Why it is different

- **Repository first:** inspect instructions, code, tests, history, canonical documentation, CI/release configuration, and prior decisions before inventing new state.
- **Risk scaled:** preserve the same gates for a one-file fix and a multi-release initiative, but compress them when evidence supports low risk.
- **Evidence bound:** tie claims to exact revisions, environments, commands, artifacts, provider state, and actual results; record failures and checks not run.
- **Traceable:** connect outcomes, requirements, acceptance, decisions, risks, work, tests, findings, and release disposition.
- **Authority safe:** planning does not authorize edits; preparation does not authorize merge, publish, deploy, external writes, communication, or risk acceptance.
- **Provider neutral:** optional tools deepen evidence or perform authorized actions, while the core still produces useful plans, drafts, mappings, and receipts without them.
- **Independently implemented:** no runtime code, prompt, hook, manifest, app/MCP configuration, executable, or asset from another delivery plugin is required or re-exported.

## Canonical lifecycle

```text
Context → Requirements → Solution Design → Delivery Plan ↔ Coordination
        → Implementation → Quality → Documentation → Review / Security / Operations
        → Release → Retrospective
```

Start with `project-delivery:delivery-orchestrator` for end-to-end, incomplete, or mixed requests. Invoke a lifecycle skill directly when the target and authority are already bounded.

The lifecycle is a logical evidence and gate model, not a command that blindly invokes every skill in one total order. Required capability owners, conditional branches, valid existing evidence, safety precedence, and controller returns determine the actual route.

| Work shape | Default depth | Typical result |
|---|---|---|
| Small, low-risk change | Compact context and acceptance, design delta when needed, short plan, targeted verification, proportional review/release checks | One coherent PR with exact evidence and rollback notes |
| Medium feature or refactor | Full requirements, design, WBS, implementation, test strategy, docs, independent review, security/operations, release gate | One or a few traceable PRs |
| Large initiative | ADRs, RAID, milestones, critical path, bounded delegation, multi-PR/release slices, staged rollout, observation and learning | Incremental delivery with explicit integration and release gates |
| Review-only or release-only | Recover exact scope and missing evidence, apply only the relevant lenses | Findings or gate decision without unauthorized edits |
| Legacy-workflow migration | Instruction/state inventory, rollback capture, one-at-a-time disablement, fresh-task smoke receipts | Evidence-based replacement without deleting specialist access |

## Quick start prompts

Use the orchestrator for a full lifecycle:

```text
Use $project-delivery:delivery-orchestrator to deliver this request end to end. Inspect the current
repository, recover existing decisions and conventions, classify scale and risk,
use only the minimum sufficient lifecycle, keep facts/requirements/assumptions/
decisions/questions separate, and report actual evidence plus residual risk.

Request: <describe the outcome>
```

Use a bounded skill directly:

```text
Use $project-delivery:requirements-acceptance to turn this brief into testable requirements,
acceptance criteria, edge cases, non-functional requirements, and traceability.
```

```text
Use $project-delivery:review-audit to review this exact diff without modifying it. Pin the base and
head, report located evidence-backed findings, and state release blockers and
residual risk.
```

```text
Use $project-delivery:release-change to prepare this completed change for release. Recover missing
test, documentation, review, and security evidence; do not merge, tag, publish, or
deploy unless that action is separately authorized.
```

## Skills

| Skill | Canonical responsibility |
|---|---|
| `delivery-orchestrator` | Classify authority, scale, risk, lifecycle state, routing depth, delegation, and migration/decommission work |
| `project-context` | Refine the problem, outcome, value, scope, constraints, success, readiness, and repository context |
| `requirements-acceptance` | Produce testable requirements, acceptance criteria, edge cases, NFRs, and traceability |
| `solution-design` | Design current/proposed state, contracts, alternatives, compatibility, migration, rollback, and ADRs |
| `delivery-planning` | Build WBS, milestones, dependencies, critical path, ownership, estimates, RAID, and PR/release slices |
| `delivery-coordination` | Reconcile systems of record, meetings, status, exact external targets, authority, and readback receipts |
| `implementation-execution` | Implement an approved slice in canonical repository paths while preserving unrelated work |
| `testing-quality` | Select, run, and report risk-based tests, static checks, CI evidence, performance/security validation, and failure triage |
| `documentation-knowledge` | Maintain canonical user, developer, operator, architecture, migration, status, and release knowledge |
| `review-audit` | Independently review designs, plans, diffs, PRs, or releases with reproducible findings and governed closure |
| `security-operations` | Assess threat, privacy, dependency, reliability, observability, support, recovery, and operational readiness |
| `release-change` | Prepare and, only when authorized, execute integration, CI/CD, version, rollout, rollback, and post-release verification |
| `retrospective-improvement` | Capture outcomes, root causes, debt, decisions, bounded follow-up, and measurable process improvements |

Installable shared conventions and templates live under [`skills/.shared/`](skills/.shared/). Keeping runtime references inside the manifest-declared skill tree makes the standalone plugin self-contained without exposing a fourteenth skill.

## Artifact and evidence model

Project Delivery updates the repository's canonical artifacts instead of creating a branded process tree. When the repository has no format, it offers proportional templates for:

- project briefs, requirements, acceptance criteria, solution designs, and ADRs;
- WBS, milestones, RAID, critical path, PR/release slices, status, and coordination receipts;
- risk-to-test strategies and revision/environment-bound results;
- review and security findings with severity, priority, evidence, closure, release treatment, and residual risk;
- release units, approvals, migrations, flags, rollout, rollback, observability, and post-release outcomes; and
- retrospectives, technical debt, follow-up work, and live route receipts.

Recommended traceability:

```text
Outcome → REQ → AC → DESIGN/ADR → WI/PR → TEST → FIND → RELEASE
REQ/AC → RISK → mitigation WI → TEST/FIND → RELEASE disposition
DEC/ADR → affected REQ/WI/TEST → RELEASE disposition
```

## Install from source

Project Delivery is a standalone plugin. Clone the source repository into a stable local directory:

```bash
git clone https://github.com/sealad886/project-delivery.git ~/plugins/project-delivery
```

Then ask Codex's system Plugin Creator skill to validate and install that existing source:

```text
Use $plugin-creator to validate and install the existing local plugin at
~/plugins/project-delivery. Follow the supported local-source registration and
cache-refresh workflow, do not hand-edit Codex configuration, and report the
installed plugin version and cache identity.
```

Start a new Codex task after installation and invoke `$project-delivery:delivery-orchestrator`. The installed bundle contains all 13 skills and their presentation metadata. Codex applies a global initial skill-metadata budget, so a crowded task may omit otherwise valid skills from its initial model-visible list. The orchestrator is instructed to resolve each selected Project Delivery specialist from its installed sibling path and block truthfully if the file is actually unavailable. Disabling superseded or unused workflow plugins after their canaries pass may improve initial-list visibility; do not rename skills to game ordering.

See OpenAI's [Build skills](https://learn.chatgpt.com/docs/build-skills.md) documentation for progressive disclosure, explicit invocation, and the initial-list budget.

For local development, edit the cloned source and ask `$plugin-creator` to run its supported cachebuster and reinstall workflow after each change. Keep the source directory stable and do not edit product-managed installation state by hand.

See OpenAI's [Build plugins](https://learn.chatgpt.com/docs/build-plugins) guide for the current Codex manifest, component, and local testing contract.

## Validation

From a source checkout, the repository's dependency-free checks use only Python's standard library:

```bash
python3 scripts/check_plugin.py . --layout source
python3 scripts/check_routes.py .
python3 scripts/check_route_receipts.py tests/fixtures/blind-route-observations-v1.3.1.json --root . --allow-subset --allow-historical-annotations
python3 scripts/check_distribution_bundle.py .
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

`tests/route-contracts.json` contains 21 machine-readable semantic contracts: the original 17 prompts plus four explicit platform-claim variants. Passing them proves that policy data is complete, references disjoint real capability owners, covers the taxonomy, declares substantive conditional triggers, acyclic entry precedence, two-sided occurrence-aware controller entry/return rules, and forbidden legacy runtime dependencies. It does **not** prove that a trigger applies, which skills a fresh agent selected, or that delivery work ran. The committed v1.3.1 fixture preserves genuinely blind route choices, but its schema-v2 taxonomy, rationales, and conditional dispositions are explicitly post-hoc and accepted only with the dedicated historical flag; it establishes historical route-shape compatibility, not current-policy conformance or candidate behavior. Fresh route-policy claims require a no-effect task to freeze the route, taxonomy, branch dispositions, extra-capability decisions, evidence, and gaps before comparison; record loaded specialists; and mark delivery not run. Exact total-order equality is intentionally not a conformance rule.

The distribution check is a minimum runtime-closure simulation. It proves that a 63-file subset containing the complete skill tree, shared operating model, templates, and icons is internally valid; it does not claim that Codex's local-source installer or an external marketplace emits exactly that subset or filters maintainer-only files.

Release validation also includes Plugin Creator validation, Skill Creator validation for all 13 skills, source/cache comparison, a deterministic minimum runtime-closure simulation, the pinned HOL scanner, and independent review. Current evidence and limitations are recorded in the [validation report](https://github.com/sealad886/project-delivery/blob/main/references/validation-report.md).

## Trust, privacy, and dependencies

Project Delivery bundles no MCP server, app, hook, telemetry, network service, credential, binary, package dependency, or automatic external write. Its Python validation scripts use only the standard library. It never needs another workflow plugin to operate.

Repository instructions and user authority remain controlling. External issue trackers, source hosts, document stores, communication tools, calendars, CI systems, deployment platforms, security tools, and memory systems are optional adapters used only when available, relevant, and authorized. Secrets and personal data must not be copied into delivery artifacts or public evidence.

See [SECURITY.md](SECURITY.md) for private vulnerability reporting and the [support policy](https://github.com/sealad886/project-delivery/blob/main/SUPPORT.md) for support boundaries.

## Migration and replacement

Project Delivery is intended to replace generic project-management and software-delivery workflow authority, including fragmented planning, implementation, testing, documentation, review, security-gate, release, and retrospective entry points. Adoption is evidence-based:

1. neutralize active instructions that mandate a legacy workflow;
2. preserve historical provenance without leaving imperative legacy calls active;
3. inventory installed IDs, versions, configuration locations, and supported reinstall sources without secrets;
4. run representative small and medium canaries;
5. disable one superseded generic plugin at a time and start a fresh task;
6. confirm packaged files, explicit and orchestrated loading, semantic routing, artifacts, stable plugin state, and absence of legacy invocation/runtime requests; and
7. uninstall only after an observation period and explicit user confirmation.

Specialist platform, provider, security, CI, deployment, and observability tools may remain because they supply access or evidence rather than competing lifecycle authority. The [detailed migration map](https://github.com/sealad886/project-delivery/blob/main/references/migration-and-decommission.md) remains with the standalone plugin source.

## Project governance

- [Contributing](https://github.com/sealad886/project-delivery/blob/main/CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Support](https://github.com/sealad886/project-delivery/blob/main/SUPPORT.md)
- [Changelog](https://github.com/sealad886/project-delivery/blob/main/CHANGELOG.md)
- [Design brief](https://github.com/sealad886/project-delivery/blob/main/references/design-brief.md)
- [Environment and capability audit](https://github.com/sealad886/project-delivery/blob/main/references/environment-audit.md)
- [Research sources](https://github.com/sealad886/project-delivery/blob/main/references/research-sources.md)
- [Validation report](https://github.com/sealad886/project-delivery/blob/main/references/validation-report.md)

Project Delivery is maintained by Andrew Cox and licensed under the [MIT License](LICENSE). Copyright © 2026 Andrew Cox.
