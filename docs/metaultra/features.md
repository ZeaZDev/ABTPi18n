# MetaUltra Features — Design and Release Notes

This document details the capabilities of MetaUltra, the reasoning for each feature, and release-time decisions maintainers should make.

Core Capabilities
- Deep-dive documentation: narrative and reference material for algorithms, interfaces, and data formats.
- Generator / Installer: a POSIX-compatible Bash tool that previews, generates, and installs artifact bundles into a repo or produces a release tarball.
- Modular templates: explicit scaffolding for plugin modules (strategy implementations, adapters, metadata) with `meta.json` manifests.
- Canonical examples: small, well-documented Python and TypeScript modules that demonstrate lifecycle, configuration, and metadata usage.
- Validation suite: lightweight checks for file presence, manifest consistency, and example smoke tests.

Release and Packaging Considerations
- Packaging model: prefer a single release tarball containing `docs/`, `tools/`, and `meta.json`. This simplifies redistribution and auditing.
- Versioning: follow semver for packaged artifacts and include a `version` field in `meta.json` and `metaultra-release-<timestamp>.tar.gz`.
- Breaking changes: document explicitly in `CHANGELOG.md` and increment major version; include migration notes and test fixtures.

Operational Behavior
- Idempotency: installer only writes files when `--install` is used and skips existing files unless `--force` is specified.
- Preview mode: `--preview` prints planned actions with file paths and diffs when possible.
- Verbosity: `--verbose` outputs full logs and stack traces; default is quiet with concise summary.

Trade-offs and Rationale
- Why a Bash installer? Portability and minimal build dependencies for maintainers across most Unix-like environments.
- Why not a heavyweight generator? Simplicity and auditability: small, readable scripts are easier to review in release audits.

When to extend
- Add language-specific adapters (Go, Rust) only when consumers request native modules — keep the core small.
