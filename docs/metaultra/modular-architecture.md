# Modular Architecture — Packaging, Boundaries and Testing

This page defines the recommended module layout, responsibilities, cross-module contract rules, and packaging guidance for MetaUltra modules meant for release.

Recommended filesystem layout
```
tools/metaultra/
├── example_module.py         # Example strategy implementation (Python)
├── example_module.ts         # TypeScript example (frontend or node)
├── meta.json                 # Module manifest (name, entrypoint, schema)
├── templates/                # Reusable scaffolding templates
└── README.md                 # Overview and how to use the examples
```

Module responsibilities
- Single responsibility: each module should implement one prominent feature (signal generation, data adapter, or evaluation metric).
- Metadata-first: include `meta.json` describing `name`, `version`, `entrypoint`, and `schema` for configuration.
- Tests: include unit tests and deterministic fixtures under `tests/` or `tests/fixtures/`.

Cross-module rules
- Minimal dependencies: prefer to import common utilities from a `core` or `tools` module; avoid cross-plugin coupling.
- Semantic versioning: modules that change their public schema must bump major/minor version and include migration notes.

Packaging and release manifest
- The installer collects module-level `meta.json` files into a single top-level `meta.json` for the bundle. That bundle manifest includes:
	- `modules`: list of modules with `name`, `version`, `entrypoint` and `schema` path
	- `bundle_version`: semver for the release
	- `generated_at`: ISO timestamp

Example bundle manifest excerpt
```json
{
	"bundle_version": "0.1.0",
	"generated_at": "2025-12-23T00:00:00Z",
	"modules": [
		{"name": "example", "version": "0.1.0", "entrypoint": "tools.metaultra.example_module:ExampleStrategy"}
	]
}
```

Testing and packaging
- Include a `smoke` test that instantiates each module using its `meta.json` and runs `generate_signals()` or equivalent.
- Release artifact should be deterministic: `scripts/zeaz_meta_installer.sh --generate` must produce byte-stable output where possible (sorted entries, stable timestamps), or at minimum document non-deterministic fields.

Security and dependency policy
- Vendor dependencies transitively required by plugins should be declared in the bundle manifest to support supply-chain audits.

Tip: Keep cross-module dependencies minimal to ease packaging and reuse.
