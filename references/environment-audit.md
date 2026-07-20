# Environment and capability audit

Audit date: 2026-07-19 through 2026-07-20. Sources were inspected statically; downloaded installers, hooks, MCP servers, apps, and provider operations were not executed. This document records capability evidence used to design the standalone Project Delivery plugin.

## Standalone plugin contract

- The canonical package at `plugins/project-delivery/` contains one `.codex-plugin/plugin.json` manifest, 13 lifecycle skills, 13 agent manifests, 26 skill icons, two plugin icons, and three shared runtime documents under `skills/.shared/`.
- Project Delivery bundles no MCP server, app, hook, telemetry client, credential, binary, package dependency, or automatic external write.
- Its validation scripts use Python's standard library. Development-only scanner tooling lives in the project `.venv` and is not required by the installed plugin.
- External issue trackers, source hosts, document stores, communication tools, calendars, CI systems, deployment platforms, security tools, and memory systems are optional adapters. The core workflow remains useful when none is available.
- Codex `0.144.6` recursively copies every regular file under a local plugin source and does not treat `.codexignore` as an installation filter. Repository-only CI, tests, audit evidence, tools, and environments therefore remain outside the canonical plugin subtree.
- The supported local workflow is to clone the repository outside the personal-plugin destination, materialize the exact validated package into `~/plugins/project-delivery`, use Plugin Creator to validate/cachebust/install that prepared source, and start a new task before testing updated skills. Git-backed marketplaces use `git-subdir` with the canonical package path.

## Repository and process facts

- Applicable project instructions require repository-first reuse, evidence-based verification, current authoritative documentation for third-party APIs, visible progress, project `.venv` use, Conventional Commits, and safe handling of unrelated changes.
- The source repository owns canonical lifecycle behavior. Consumer repositories keep their own instructions, artifacts, architecture, CI, release policy, and provider configuration.
- Planning, review, and release preparation do not imply authority to edit, merge, publish, deploy, communicate externally, or accept risk.
- Source identity, installed cache identity, and live task behavior are separate evidence classes and must be verified separately.

## Inspected capability sources

The following source snapshots informed capability-level design. Project Delivery does not copy or require their runtime implementations.

| Source family | Useful evidence | Treatment in Project Delivery |
|---|---|---|
| Boss, Epic, and Superpowers | repository discovery, lifecycle routing, artifact handoffs, planning, debugging, review, verification, release closeout | Independently reimplemented as risk-scaled, repository-native workflow; plugin-specific state, hooks, telemetry, mandatory swarms, and unavailable runtimes excluded |
| Codex Security and specialist review tools | assessment scope, candidate proof/counterevidence, stable finding identity, closure governance, security validation | Integrated into `review-audit`, `security-operations`, and shared finding templates; specialist tools remain optional evidence sources |
| GitHub and CI integrations | capability-aware host routing, native/external checks, first-causal-failure analysis, narrow retries, readback receipts | Generalized across `delivery-coordination`, `testing-quality`, and `release-change`; no host is assumed |
| Deployment and observability integrations | immutable release units, deployment states, readiness/drain, previews, telemetry baselines, rollback, flags | Generalized into release and operations contracts; provider commands remain outside the core |
| Document, tracker, calendar, and communication integrations | source-of-truth resolution, status mapping, meeting preparation, exact targets, draft/send separation | Generalized into `delivery-coordination` and `documentation-knowledge`; authenticated access remains optional |
| Platform build and test skills | focused scenarios, fresh artifact identity, comparable measurements, packaging, signing, distribution evidence | Generalized as quality and release evidence requirements; platform specialists may be invoked when available |

## Optional adapters

Connector and specialist availability must be discovered in the active task. Metadata is not proof that an implementation is installed, enabled, authenticated, authorized, or suitable for a specific operation.

| Adapter class | Examples | Core behavior without it |
|---|---|---|
| Work tracking | Linear, Jira, Asana, ClickUp, Monday, Teamwork | Produce mapped plans, status drafts, and exact proposed writes without claiming synchronization |
| Documents and communication | Drive, Box, SharePoint, Notion, Slack, Teams, email, calendars | Maintain repository-native canonical artifacts and draft external updates without sending them |
| Source and CI | GitHub, CircleCI | Inspect local Git/config evidence and report unavailable remote checks explicitly |
| Security and review | Codex Security, CodeRabbit, scanners | Apply repository-based review/security lenses and label dynamic or provider evidence gaps |
| Deployment and telemetry | Cloudflare, Vercel, Netlify, Sentry, Datadog, Statsig | Prepare provider-neutral rollout, monitoring, stop, and rollback contracts without fabricating execution |
| Durable memory | authorized memory providers | Use repository history and current canonical documents; do not invent prior decisions |

## Provenance and limitations

- Inspected source snapshots were read at pinned local versions when available. Exact upstream transport identity was not always recoverable, so claims are limited to the files actually inspected.
- No installer, hook, lifecycle script, binary, MCP server, app, or downloaded executable was run during the capability audit.
- Capability-level synthesis is not proof of behavioral parity. Fresh-task route receipts and real-repository canaries remain the required evidence for adoption and decommission decisions.
- Opaque connector identifiers and presentation metadata do not establish implementation behavior. Project Delivery requires live capability discovery and readback for every external operation.
- The final list of superseded generic workflow plugins remains a user decision after canary evidence. Specialist access tools are not removed merely because their planning concepts overlap.
