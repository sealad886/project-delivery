# Research sources

Accessed 2026-07-19 through 2026-07-20. Principles were synthesized; no source text is copied as a plugin dependency.

## Codex and local conventions

- Current Codex manual, fetched with the local `openai-docs` helper: plugin manifests live at `.codex-plugin/plugin.json`; skills use progressive disclosure and concise trigger descriptions; installed local copies require an explicit refresh and a new task before changed components are available. Source pages: [Build plugins](https://learn.chatgpt.com/docs/build-plugins) and [Build skills](https://learn.chatgpt.com/docs/build-skills).
- Local Plugin Creator: `<codex-home>/skills/.system/plugin-creator/SKILL.md`, `references/plugin-json-spec.md`, and `references/installing-and-updating.md`. These define the scaffold, manifest validation, supported local-source registration, cachebuster, reinstall, and handoff flow used here.
- Codex CLI `0.144.6` installer implementation at official tag commit [`5d1fbf26c43abc65a203928b2e31561cb039e06d`](https://github.com/openai/codex/blob/5d1fbf26c43abc65a203928b2e31561cb039e06d/codex-rs/core-plugins/src/store.rs#L520-L682): `copy_dir_recursive` traverses every source directory and copies every regular file without consulting `.codexignore` or a manifest allowlist. Current upstream `main` at inspected commit [`bf3c1972b7d045c0a3a48dff91f381070f8f69e1`](https://github.com/openai/codex/blob/bf3c1972b7d045c0a3a48dff91f381070f8f69e1/codex-rs/core-plugins/src/store.rs#L662-L685) retained the same behavior on 2026-07-20. This evidence drove the strict nested package boundary and `git-subdir` policy.
- Statically inspected official and third-party plugin snapshots supplied capability-level comparison evidence. Relevant manifests, skills, references, and scripts were read without executing apps, MCP servers, hooks, installers, or downloaded binaries. Project Delivery reimplements only provider-neutral patterns and retains no runtime dependency on those sources.
- [HOL AI Plugin Scanner action](https://github.com/hashgraph-online/ai-plugin-scanner-action) and [HOL Guard](https://github.com/hashgraph-online/hol-guard): the public workflow pins the action to commit `8f0a503ca2a7`; local inspection used `plugin-scanner==2.0.1015` after verifying the reviewed wheel's published SHA-256 digest.

## Delivery and flow

- [The Scrum Guide, November 2020](https://scrumguides.org/download.html): shared product goal, transparent artifacts, inspection/adaptation, and a common Definition of Done. The plugin uses these ideas without requiring Scrum roles or events.
- [Open Guide to Kanban, 2025.7](https://kanbanguides.org/open-guide-to-kanban/2025.7/pdf/open-guide-to-kanban.en.pdf): explicit workflow, control of work in progress, flow, and improvement. The plugin applies dependency visibility and bounded work without imposing a board.

## Security and operations

- [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): integrate secure practices throughout the SDLC, protect software and development environments, produce well-secured releases, and respond to vulnerabilities. This informs cross-lifecycle security rather than a final scanner-only gate.
- [Google SRE Release Engineering](https://sre.google/sre-book/release-engineering/): repeatable builds, intentional changes, gated operations, tested release revisions, canaries/staged rollout, traceable artifacts, and rollback-aware delivery.
- [Google SRE Launch Checklist](https://sre.google/sre-book/launch-checklist/): monitoring, capacity, dependencies, graceful degradation, security review, repeatable release, staged rollout, and operational ownership.

## Versioning and change communication

- [Semantic Versioning 2.0.0](https://semver.org/): use major/minor/patch according to public compatibility when the repository adopts SemVer.
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/): maintain human-readable, reverse-chronological, categorized notable changes; do not substitute raw commit logs.
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches): approvals and successful required checks can be enforced. The plugin detects the actual host and does not assume GitHub.

## Assumptions and decisions

- Fact: the target is a personal local Codex plugin created by the supported Plugin Creator flow.
- User requirement: it must fully replace superseded PM/delivery plugins after release.
- Decision: retain no runtime dependency on inspected plugins, because standalone usefulness and uninstallability are mandatory.
- Assumption: “superseded plugins” initially means Boss, Epic, Superpowers, and overlapping generic lifecycle packs; specialist connectors/security/platform plugins require explicit scope before removal.
- Open question for adoption, not implementation: the final uninstall list should be confirmed after the decommission smoke suite because some installed plugins contain specialist capabilities outside generic project delivery.
