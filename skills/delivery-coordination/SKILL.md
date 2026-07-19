---
name: delivery-coordination
description: Coordinate delivery across authorized trackers, documents, meetings, calendars, messages, and operational systems while preserving canonical sources, exact targets, write authority, traceability, and read-after-write evidence.
license: MIT
---

# Delivery Coordination

Read `../.shared/operating-model.md` and `../.shared/external-systems.md`; use the coordination templates in `../.shared/artifact-templates.md`.

## When to invoke

Use when delivery state spans external systems; work items or milestones need synchronization; preparing or following up a meeting; producing stakeholder status; reconciling contradictory sources; communicating a release; or handling a tracker-, status-, meeting-, communication-, or coordination-only request. Invoke after planning and again at release/handoff when live state must change.

## Inputs and evidence

Expect the requested outcome, authority, internal artifact IDs, and known systems. Inspect only authorized repository artifacts, trackers, documents, research stores, source hosts, email/chat threads, calendars, meeting records, CI/deployment/incident systems, and provider schemas. Record source ID/URL, native status, revision or `as of` time, and confidence. Tool availability is a fact to discover, never a dependency to assume.

## Workflow

1. Inventory authorized systems and capabilities. Classify each operation as read, draft, create/update, communicate, share/access, or destructive. Resolve the exact workspace/project/document/channel/thread/calendar/recipient/issue before writing.
2. Build a source-of-truth map by artifact and, when necessary, by field. Provider-native state remains authoritative; normalized state is an interpretation. Surface conflicts, duplicates, stale sources, missing access, and uncertain identity.
3. Read current state before proposing writes. Map `REQ-*`, `WI-*`, `MS-*`, `RISK-*`, `DEC-*`, PRs, releases, and incidents to external IDs/URLs without inventing owners, dates, commitments, approvals, or decisions.
4. Prepare the bounded action: tracker payload, status report, agenda/pre-read, decision/action record, schedule proposal, message draft, or reconciliation plan. Preview bulk, ambiguous, permission-sensitive, and meeting-derived writes. A summary or digest never silently creates work.
5. Confirm authority at the consequence boundary. “Draft/review” does not authorize send/post/share; a release action does not authorize release communication; analysis does not authorize issue creation. Re-read relative targets such as “latest” immediately before action.
6. Execute only the authorized operation through an available provider surface. Batch logically and idempotently; preserve provider semantics and source links. Access widening, shared links, deletes, permission changes, and destructive tracker actions require explicit authority.
7. Read after write. Record system, exact target, external ID/URL, actor when known, timestamp, fields changed, prior/new state when available, verification result, and residual inconsistency. Reconcile the canonical project handoff.
8. If live access is absent, remain useful: produce the source inventory, mapping/sync plan, exact proposed payloads, meeting artifacts, message drafts, and an explicit list of operations not performed.

## Outputs and handoff

Source-of-truth map, external inventory and normalization map, sync ledger, meeting/status/communication artifact as requested, mutation receipts, conflicts, freshness limits, and unresolved access/authority. Handoff requirements to `requirements-acceptance`, work structure to `delivery-planning`, durable knowledge to `documentation-knowledge`, release actions to `release-change`, and final reconciliation to `retrospective-improvement`.

## Completion evidence

Sources and freshness are explicit; internal/external IDs are traceable; conflicts are visible; exact targets and authority are known; every mutation has read-after-write evidence; drafts are distinguished from sent content; unavailable operations are not claimed.

## Must not

- Make external writes because a report, digest, transcript, or plan was requested; widen access; or send to an inferred target.
- Treat normalized state as provider truth, silently choose between contradictory sources, fabricate commitments, or require any connector/plugin.
- Copy provider credentials, app/MCP declarations, or proprietary schemas into this plugin.
