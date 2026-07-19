# Environment and marketplace audit

Audit date: 2026-07-19. Sources were inspected statically; downloaded installation/build/hook/MCP code was not executed. Facts below distinguish installed implementation evidence from marketplace claims.

## Environment facts

- The audited Codex skills workspace was a small Git repository with three commits and extensive pre-existing untracked skill directories. It had no remote, tags, README, CI, issue/PR templates, changelog, or release configuration. Those unrelated changes were preserved.
- Applicable instructions require repository-first reuse, evidence-based verification, current authoritative docs for third-party APIs, visible progress, project `.venv` use, Conventional Commits, and safe handling of unrelated changes.
- Codex config explicitly lists five marketplaces with 182 total entries. The official `openai-curated` marketplace is a complete local Git snapshot with 180 entries; sibling `openai-api-curated` has 29 overlapping API-oriented entries and is not double-counted.
- The personal marketplace did not exist before Plugin Creator created it for this plugin.

## Marketplace inventory

| Marketplace | Status/source | Revision/update | Entries | Confidence |
|---|---|---|---:|---|
| openai-bundled | configured local bundled marketplace snapshot | updated 2026-07-18 | 5 | High |
| openai-primary-runtime | configured local primary-runtime marketplace snapshot | updated 2026-07-16 | 5 | High |
| mlx-optimizer-local | configured Git `https://github.com/sealad886/mlx-optimizer-plugin.git` | `7762ed1c…` | 1 | High |
| everything-claude-code | configured Git `https://github.com/WorldFlowAI/everything-claude-code.git` | `432485ba…` | 1 | High |
| awesome-codex-plugins | configured Git `https://github.com/hashgraph-online/awesome-codex-plugins.git`, sparse main | `fa1d122e…` | 170 | High |
| openai-curated | official local Git snapshot; manifest `.agents/plugins/marketplace.json` | Git snapshot `11c74d6ba24d`, 2026-07-13 | 180 | High exact local contents/medium upstream transport (checkout had no remote) |

Every marketplace manifest was parsed and searched across names, descriptions, categories, skills, and source paths. Shortlisted sources already existed in pinned local snapshots, so no temporary downloads were needed.

### OpenAI curated implementation evidence

Relevant source trees were inspected statically at the exact snapshot above; no app, MCP server, hook, script, installer, or provider operation was executed.

| Source/version | Implementation evidence | Capability adopted | Treatment/confidence |
|---|---|---|---|
| Atlassian Rovo 1.0.3; Notion 0.1.5; Linear 0.0.3; Airtable 0.1.3 | skills/references and manifests | read-first source-of-truth, schema/status mapping, backlog sync, audience status, duplicate detection | Adapt → `delivery-coordination`; High static |
| Box 0.0.3; Drive 0.1.7; SharePoint 0.1.3 | skills/references | exact document/revision, permission boundary, backlink/readback | Adapt → coordination/docs; High static |
| Google Calendar 1.2.3; Outlook Calendar 0.1.3; Outlook Email 0.1.3; Slack 0.1.2; Teams 0.1.3 | skills/references | meeting prep/follow-up, exact destination, draft/send split, no silent task creation | Adapt → coordination; High static |
| Codex Security 0.1.11 | 12 skills, shared scan/assessment references | scope/coverage, candidate proof/counterevidence, stable findings, closure | Adapt → security/review/templates; High static; exclude runtime/schemas |
| GitHub 0.1.6; CircleCI 1.0.4 | skills, references, helper source | capability-aware host routing, native/external checks, first-failure taxonomy, narrow retry | Adapt → release/quality/coordination; High static |
| Render 0.1.3; Vercel 0.21.3; Netlify 1.1.2; Cloudflare 0.1.2 | deployment/monitoring/preview/operations skills | artifact promotion, deployment states, readiness/drain, preview isolation, observability | Adapt provider-neutral release/operations contract; High static |
| Sentry 0.1.2; PostHog 0.1.2 | read-only/API helper and static skills | environment/release-bound telemetry, redaction, flag/experiment lifecycle | Adapt general evidence; High/medium-high static |
| Datadog 0.1.2; Statsig 2.0.3; Asana/ClickUp/Monday/Teamwork | app declarations/marketplace prompts only | advertised optional operational/work surfaces | Metadata-only optional adapters; Medium; no behavior inferred |
| build iOS/macOS/web and test Android | platform skills/references | focused scenario, fresh artifact identity, comparable measurement, packaging/distribution gates | Adapt generic evidence contract; High static |
| Plugin Eval 0.1.2 | skill/package/benchmark references | fresh-task scenario benchmarking and comparison | Optional authoring validation only; High static |
| CodeRabbit 1.1.4 | skill source | specialized review | Exclude dependency/installer; remote-pipe installation guidance does not meet the local policy; High |

All ten user-visible recommended connectors (Atlassian Rovo, Box, Google Calendar, Google Drive, Notion, Outlook Calendar, Outlook Email, SharePoint, Slack, Teams) had locally inspectable implementations in this snapshot. They are available but not installed and remain optional adapters, not dependencies.

## Installed-source matrix

| Source | Status/location | Capability/pattern | Strengths | Weakness/conflicts | Disposition → destination | Confidence |
|---|---|---|---|---|---|---|
| Superpowers 6.1.1 | Installed openai-curated-remote cache | discovery, design, plans, TDD/debug, subagents, review, worktrees/branch finish | repo-first intent, root cause, fresh evidence, independent review, destructive safety | universal ceremony, absolute TDD, forced agents/artifact paths; Python guidance can violate `.venv` policy | Adapt/merge across context/design/planning/execution/quality/review/release | High |
| Epic 0.8.2 | Installed awesome cache | routed lifecycle, specs, TDD/debug/perf, audit/security, ship, orchestration/memory/learning | traceability, phase gates, dedup, security chain, CI evidence, retro | CLI absent; hook installer path and registry absent; MCP unavailable; contradictory paths/terms; auto-approval/telemetry/self-modification | Adapt portable concepts; exclude runtime → all lifecycle skills | High source/high-negative runtime |
| Boss 3.10.1 | Installed awesome cache | nine-role artifact DAG from idea through deploy | repo preflight, evidence waves, contract matrix, actual QA results, progressive artifacts | CLI/scripts/runtime/assets absent; hook enforcement unavailable; fixed conflicting thresholds; mandatory roles; no retro | Adapt portable concepts; exclude runtime → orchestrator/planning/quality/release | High source/high-negative runtime |
| Everything Claude Code | Installed configured Git revision | architect/planner/reviewer/docs/E2E/security/TDD/verify/checkpoint plus language patterns | broad execution and verification patterns | mixed Claude/Codex conventions, universal thresholds, generic delivery duplication | Replace generic lifecycle; leave domain pattern skills optional | High |
| Codex Security 0.1.11 | Installed remote record/cache | repo/diff/deep scans, threat model, validation, attack path, finding fix/writeup | deep evidence ledgers and calibrated security workflow | large app/MCP/runtime-specific system; not generic PM | Integrate security gates; retain as optional specialist unless explicitly superseded | High |
| GitHub 0.1.x | Installed official | PR/issue triage, Actions diagnosis, review feedback, publish | real host integration and bounded workflows | GitHub-specific external surface | Core is host-neutral; retain optional connector | High |
| CodeRabbit 1.1.4 | Installed official | code review | specialized independent review | not an end-to-end lifecycle | Retain optional; review-audit works without it | High |
| GrayMatter 0.3.1 | Installed awesome | durable memory/context/receipts | prior decision retrieval | proprietary MCP/auth/data dependency | Treat authorized memory as optional context; no dependency | High |
| Ditto 0.3.8 | Installed awesome | session-derived work/design/writing profiles | user-specific context | privacy/profile scope; catalog identity drift to emulo 0.5.0 | Exclude profiling; accept explicit preferences as input | High installed/medium catalog identity |
| Cloudflare/build-web/iOS/macOS/test-Android | Installed official | platform implementation/test/deploy guidance | domain depth and current platform patterns | platform-specific, not PM replacement | Retain optional specialists; router can invoke when available | High |
| Documents/PDF/Presentations/Spreadsheets | Installed runtime | artifact creation/editing | canonical office artifact support | not delivery lifecycle | Retain optional output tools | High |
| Standalone create-plan/ADR/quality/adversarial/security/commit skills | Local skills | narrow planning/design/review/security/Git workflows | useful focused patterns | fragmented terms/artifacts and differing scopes | General behavior merged; deeper specialist use optional | High |

## Available marketplace matrix

Marketplace entries prove advertised intent, not runtime safety. Awesome paths below are relative to the configured `awesome-codex-plugins` marketplace root.

| Source | Status/location | Capability/pattern | Strength/gap | Disposition → destination | Confidence |
|---|---|---|---|---|---|
| A Team | Available `plugins/RBraga01/a-team` | 25 specialists/lead router | broad but agent-heavy | Adapt routing → orchestrator | Medium |
| Aegis | Available `plugins/GanyuanRan/Aegis` | plan/TDD/debug/collaboration | coherent engineering loop | Merge → execution/quality | Medium |
| Agent Harness Skills | Available `plugins/yfge/agent-harness-skills` | repo entrypoints/evidence/delivery records | strong readiness/receipts | Adapt → context/evidence | Medium |
| AgentOps | Available `plugins/boshu2/agentops` | flow/feedback/improvement | durable learning; process risk | Adapt → retrospective | Medium |
| AgiFlow | Available `plugins/AgiFlow/ai-plugin` | grooming→review with MCP | end-to-end; dependency | Adapt workflow, exclude MCP | Medium |
| AIBoarding | Available `plugins/gustavo-meilus/aiboarding` | instruction onboarding/drift | useful repo context | Adapt → context/docs | Medium |
| Archcore | Available `plugins/archcore-ai/plugin` | architecture/rules/decisions | prior context; hooks/MCP | Adapt evidence, exclude runtime → design | Medium |
| BABOK Analyst | Available `plugins/GSkuza/BABOK_ANALYST` | formal BA pipeline | rigorous but heavy | Adapt → brief/requirements | Medium |
| Brooks Lint | Available `plugins/hyhmrright/brooks-lint` | severity review/debt/tests | broad finding lenses | Adapt → review | Medium |
| Codebase Recon | Available `plugins/yujiachen-y/codebase-recon-skill` | Git-history hotspots/risk | strong repository grounding | Adopt → context/design/risk | Medium |
| CodeTruss | Available `plugins/DeliriumPulse/codetruss-plugins` | snapshot acceptance receipts | evidence integrity; machinery | Adapt → quality/release | Medium |
| Codex Reviewer | Available `plugins/schuettc/codex-reviewer` | independent plan/code pass | fresh-eyes validation | Merge → review | Medium |
| debt-ops | Available `plugins/bcanfield/agentic-tech-debt` | debt deferral/churn ranking | actionable follow-up; hook risk | Adapt → retrospective | Medium |
| Dev Skills | Available `plugins/Jason-chen-coder/dev-skills` | spec through branch finish | lifecycle coverage | Merge concepts across lifecycle | Medium |
| Development Skills | Available `plugins/reidemeister94/development-skills` | PASS/LIGHT/FULL and fresh review | best scale-down pattern | Adopt → orchestrator/review | Medium |
| Docflow | Available `plugins/MedAdemBHA/docflow` | docs readiness/validation/changelog | useful docs gate; forced tree risk | Adapt → documentation | Medium |
| HOTL | Available `plugins/yimwoo/hotl-plugin` | planning/review/verification guards | clear gates | Adapt → orchestrator | Medium |
| Krypton | Available `plugins/jturntdev/krypton` | ownership/cutover/acceptance | strong release evidence | Adapt → planning/release | Medium |
| Ontoly | Available `plugins/0xsarwagya/ontoly-codex-plugin` | impact/config/request tracing | useful design context; graph dependency | Adapt concepts → design/review | Medium |
| Praxis | Available `plugins/ouonet/praxis` | triage-first design→release | scalable intent | Adopt → orchestrator | Medium |
| Project Autopilot | Available `plugins/AlexMi64/codex-project-autopilot` | idea→handoff | coherent lifecycle | Merge → orchestrator | Medium |
| River Review | Available `plugins/s977043/river-review` | multi-perspective diff review | strong review coverage | Adapt → review | Medium |
| RoadmapSmith | Available `plugins/PapiScholz/roadmapsmith` | evidence roadmap/sync | multi-release planning | Adapt → planning | Medium |
| Session Orchestrator | Available `plugins/Kanevry/session-orchestrator` | waves/VCS/gates/closeout | multi-PR depth; huge taxonomy | Adapt → orchestrator/planning/release | Medium |
| Spec-Driven Development | Available `plugins/Habib0x0/spec-driven-plugin` | requirements→design→tasks/EARS | strong traceability | Adopt → requirements/design/planning | Medium |
| spec-superflow | Available `plugins/MageByte-Zero/spec-superflow` | spec-first evidence gates | useful but Superpowers-linked | Adapt without dependency | Medium |
| Staff Engineer Mode | Available `plugins/sirmarkz/staff-engineer-mode` | design/delivery/reliability/security routing | broad risk view | Adapt → orchestrator | Medium |
| Wingman | Available `plugins/lsshym/wingman.ai` | local memory/project map/contracts | strong contract checks; dependency | Adapt → context/design/quality | Medium |
| Workflow Kit | Available `plugins/Le-Xuan-Thang/workflow-kit` | vision→maintenance advertised | no standard SKILL.md found | Leave partially unverified/excluded | Low implementation |
| Zagrosi Forge | Available `plugins/zagrosi-code/zagrosi-forge` | brief/research/TDD/gates | broad traceability | Adapt → planning/execution/quality | Medium |
| OpenProject Codex | Available `plugins/varaprasadreddy9676/openproject-codex-plugin` | work packages/boards/wiki/reporting | external PM integration | Exclude core dependency; optional ecosystem | Medium |
| Task Scheduler | Available marketplace entry by `6Delta9` | capacity/block dates | scheduling depth; MCP | Adapt estimation only | Medium |
| Costguard | Available `plugins/mbanderas/costguard` | CI/cloud cost audit | operational cost lens | Adapt → release/operations | Medium |
| HOL Guard | Available `plugins/hashgraph-online/hol-guard-plugin` | plugin/release security receipts | trust/release checks; runtime | Adapt concepts → security/release | Medium |
| Linear/Asana/ClickUp/Monday/Teamwork | Official available, not installed | external issue/project systems | useful live coordination | Optional surfaces; no dependency | High metadata |
| CircleCI | Official available, not installed | CI/build/deploy | platform depth | Optional CI specialist | High metadata |
| Sentry/Datadog | Official available, not installed | production issues/telemetry | operations evidence | Optional observability specialists | High metadata |
| Statsig | Official available, not installed | flags/experiments/rollouts | controlled release | Optional rollout specialist | High metadata |
| Netlify/Vercel | Official available, not installed | platform deployment/flags/observability | deep but platform-specific | Optional deployment specialists | High metadata |

## Recommended but not installed

All ten user-visible recommendations exist in the official catalog and were not found as named enabled or remote-installed plugins: Atlassian Rovo 1.0.3, Box 0.0.3, Google Calendar 1.2.3, Google Drive 0.1.7, Notion 0.1.5, Outlook Calendar 0.1.3, Outlook Email 0.1.3, SharePoint 0.1.3, Slack 0.1.2, and Teams 0.1.3. They offer task/status/spec/document/meeting/communication access, but are excluded as core dependencies. Opaque remote `app-*` records prevent absolute name mapping, a bounded status caveat.

## Provenance and gaps

- Epic inspected: manifest, hooks, MCP config, package/README/security, all 27 skills. Superpowers inspected: manifest, all 14 skills, agents, prompts, scripts/references. Boss inspected: 94 files covering manifest, marketplace metadata, root/nested skills, agents, commands, prompts, hooks, references, templates, package/README/security.
- Exact upstream commits for installed Epic/Superpowers/Boss caches were not recorded; versions and repository URLs come from local manifests. Confidence is high for installed snapshots, medium for upstream identity beyond those declarations.
- The exact local official-catalog snapshot commit is recorded above; correspondence to an authoritative upstream transport revision remains unverified because that checkout had no configured remote. The Awesome configured source was pinned, and all candidates were already local, so no downloads were necessary.
- No plugin installer, hook, lifecycle script, binary, MCP server, or downloaded executable was run.
