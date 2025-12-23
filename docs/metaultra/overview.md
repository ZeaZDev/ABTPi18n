# MetaUltra — Final Release Deep Dive

This section contains the final-release quality deep-dive for MetaUltra: design rationale, features, options, APIs, algorithms, example source, data schemas, and packaging rules. It is intended as the authoritative reference for maintainers preparing a stable release.

Goals
- Explain architecture and design decisions so reviewers can reason about trade-offs.
- Provide reproducible examples (Python + TypeScript) and manifest metadata for distribution.
- Supply an automated, idempotent generator/installer to produce release artifacts and a release tarball.

Who should read this
- Release engineers packaging MetaUltra artifacts.
- Developers implementing or auditing strategies, algorithms, or integrators.
- Security reviewers and auditors who need clear data-flow and schema descriptions.

Release Quick Start
1. Preview planned changes: `bash scripts/zeaz_meta_installer.sh --preview`
2. Generate a local bundle: `bash scripts/zeaz_meta_installer.sh --generate`
3. Validate artifacts: `bash scripts/validate-metaultra.sh`
4. Create release tarball: `bash scripts/zeaz_meta_installer.sh --release`
5. Install into repo (idempotent): `bash scripts/zeaz_meta_installer.sh --install`

Release checklist (short)
- Confirm `meta.json` manifest describes each module and entrypoint.
- Ensure examples import and run (Python: `python tools/metaultra/example_module.py`; TS: `node`/`ts-node` test).
- Run `scripts/validate-metaultra.sh` and CI lint/test workflows.
- Update `CHANGELOG.md` with Unreleased -> version and tag the repo.

For detailed topics, see the linked pages in the MetaUltra TOC.