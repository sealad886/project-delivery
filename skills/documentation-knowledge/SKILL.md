---
name: documentation-knowledge
description: Update canonical project knowledge for users, developers, operators, reviewers, releases, and future agents. Use for docs-only work or whenever a change affects behavior, interfaces, configuration, architecture, operations, migration, status, or release communication.
license: MIT
---

# Documentation and Knowledge Management

Read `../.shared/operating-model.md`.

## When to invoke

Use during design for ADRs, during implementation for contract/config docs, before review/release for user/operator/release material, and after delivery for handoff/status/learning. Documentation-only changes still need acceptance and validation.

## Inputs and evidence

Inspect repository documentation conventions, README/contributing, docs site/config, API/schema generators, ADR/runbook locations, changelog/release policy, issue/PR templates, code/tests/config/CLI help, target audience, and authorized external canonical sources. Record source identity, freshness, ownership, and contradictions. Treat generated documentation according to repository ownership rules.

## Workflow

1. Identify audiences and changed knowledge: users, API consumers, developers, reviewers, operators/support, security/privacy, project stakeholders, and future agents.
2. Build or consult the source-of-truth registry. Update the canonical source before creating a new file; distinguish canonical from derived artifacts, preserve backlinks/citations and last-verified metadata, and surface contradictions. Link rather than duplicate; retire or redirect stale guidance when safe and authorized.
3. Cover as applicable: usage/behavior, examples, configuration/defaults, API/data contracts, compatibility/deprecation, migration/rollback, architecture/ADR, development/test workflow, deployment/runbook/troubleshooting, dashboards/queries and stop/rollback triggers, security/privacy, feature-flag lifecycle/removal, environment/configuration identity, changelog/release notes, PR description, status/decision/assumption logs.
4. Keep claims aligned with implementation and actual test/release evidence. Distinguish planned from released behavior and commands run from illustrative commands.
5. Use repository terminology and navigation. Avoid plugin-branded project folders or private session details.
6. Validate links, examples, generated docs, CLI help, docs builds, and version references using repository tools.
7. Own the content, canonical-location choice, and validation for external documents, but route live external mutation through `delivery-coordination` for exact target resolution, capability discovery, authority, execution, and readback receipt. When live access is absent, produce the exact proposed update and record the operation not performed.

## Outputs and handoff

Updated/created/retired canonical artifacts, audience/change summary, validation results, stale/duplicate docs resolved, and remaining knowledge gaps. Handoff to `review-audit` and `release-change`; feed durable learning to `retrospective-improvement`.

## Completion evidence

Every changed user/maintainer/operator contract has a canonical documented home; links/examples/builds were checked as practical; docs match the target revision; no redundant process tree was introduced.

## Must not

- Create a report merely to appear complete, copy stale behavior, or overwrite authoritative user content without inspection.
- Fabricate release dates/results, migration guarantees, support commitments, or user research.
