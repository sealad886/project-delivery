# Changelog

This file records user-visible changes to Project Delivery. Dates use ISO 8601 and versions follow Semantic Versioning.

## Unreleased

No unreleased changes.

## 1.3.0 - 2026-07-19

### Added

- Reproducible, machine-readable contracts for all 17 canonical routing scenarios.
- Standard-library regression tests for source and installed-cache validation.
- Pinned validation and HOL security-scanner workflows, Dependabot configuration, a security policy, and contribution guidance.
- Live route-receipt fields that distinguish static contract checks from fresh agent behavior.

### Changed

- Security finding suppression now requires counterevidence, closure authority, sibling analysis, revalidation triggers, release treatment, and explicit residual uncertainty.
- Risk and decision records now participate in requirement-to-release traceability.
- Public documentation now explains installation, verification, trust boundaries, and migration claims more precisely.

### Fixed

- Installed-cache validation now recognizes the versioned Codex cache layout without weakening source-layout checks.
- Validation evidence no longer presents static routing analysis as interactive proof or reports a stale file count.

## 1.2.2 - 2026-07-19

### Added

- Initial public release with 13 lifecycle skills, shared artifacts, migration guidance, validation references, and a complete plugin and per-skill icon family.
- MIT License with copyright assigned to Andrew Cox.
