# Options, Flags and Integration Points

The MetaUltra installer is intentionally small and predictable. These are the supported options and example usage patterns.

Primary flags
- `--help`: Show usage and examples.
- `--preview` / `--dry-run`: Print planned actions and paths without modifying the filesystem.
- `--generate`: Create a snapshot bundle under `build/metaultra/` including `docs/`, `tools/`, `meta.json` manifest and example artifacts.
- `--install`: Copy generated artifacts into the repository (idempotent). When a file already exists it will be skipped; use `--force` to overwrite.
- `--release`: After `--generate`, package the build directory into `metaultra-release-<timestamp>.tar.gz`.
- `--verbose`: Emit detailed logging for debugging or CI traceability.

Integration points
- CI: run `--preview` as a lightweight validation on pull requests to show which files would be added.
- Release pipelines: use `--generate` then run tests and `--release` if validations pass.

Examples
- Preview planned changes:
	bash scripts/zeaz_meta_installer.sh --preview
- Generate artifacts locally:
	bash scripts/zeaz_meta_installer.sh --generate --verbose
- Create a release tarball:
	bash scripts/zeaz_meta_installer.sh --generate --release

Best practices
- Always run `--preview` in CI as an extra safeguard before `--generate` or `--install`.
- Commit `meta.json` to the repo root when making breaking API or manifest changes.
