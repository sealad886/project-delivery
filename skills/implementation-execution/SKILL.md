---
name: implementation-execution
description: Implement an approved delivery-plan slice safely in the existing repository. Use for features, fixes, refactors, infrastructure, configuration, migrations, or documentation changes that require edits and incremental verification.
license: MIT
---

# Implementation and Execution

Read `../.shared/operating-model.md` before editing.

## When to invoke

Use when Ready/Design gates are satisfied and the user has authorized changes. For incident/hotfix work, use the smallest safe hypothesis-driven fix and record any deferred lifecycle work.

## Inputs and evidence

Expect accepted scope/criteria/design and a ready work slice. Inspect applicable instructions, repository status, target modules and abstractions, tests, build/package tooling, lint/type/format conventions, dependency policy, Git history, CI parity, and canonical docs. Retrieve current authoritative docs before relying on external APIs.

## Workflow

1. Resolve repository root, instructions, branch/revision, dirty working tree, and exact write scope. Preserve and report unrelated changes; do not absorb or revert them.
2. Find existing abstractions and canonical paths. Extend them before creating modules; resolve duplicates toward one canonical implementation incrementally.
3. Choose the smallest coherent patch that satisfies the work slice and maintains compatibility. Keep generated files, migrations, config, tests, and docs synchronized as required.
4. For bugs, reproduce and trace root cause before changing code. Form one falsifiable hypothesis at a time; add characterization/regression evidence when practical.
5. Use test-first development when it improves confidence; accept characterization, contract-first, invariant, snapshot, or post-change verification when domain/tooling makes strict red-green unsuitable. Never delete useful work solely to satisfy ceremony.
6. Implement in checkpoints. After each logical patch set, run the narrowest meaningful checks and update visible progress/RAID/status for multi-stage work.
7. Handle dependencies using the project’s lockfile/tooling. For Python, use project `.venv` or isolated compatible environment; never global install.
8. Use Git safely: no destructive cleanup, hook bypass, history rewriting, merge/push/publish without authority. When commits are requested or repository instructions require them, inspect all changes, stage only owned scope, use Conventional Commits, and verify the index.
9. Hand completed code to `testing-quality`; do not self-certify release readiness.

## Outputs and handoff

Changed files/symbols, behavior summary, requirement/work IDs, checkpoint/commit references, checks run and results, unrelated changes preserved, deviations/decisions, and residual risks. Handoff to `testing-quality`, then documentation/review.

## Completion evidence

The approved slice is implemented in canonical paths; diffs are coherent; targeted checks ran; unrelated state is intact; no undocumented scope creep or unsafe operation occurred.

## Must not

- Implement unclear material requirements, build parallel abstractions, or silently widen scope.
- Claim tests pass without running them, log secrets for debugging, or mutate global environments.
- Merge, deploy, publish, delete, or rewrite history without explicit authority.
