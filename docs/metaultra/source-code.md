# Source Code & Examples — Reference and How-to

This page contains canonical examples, loading patterns, and quick snippets to help consumers integrate MetaUltra modules.

Directory layout (recommended)
```
tools/metaultra/
	├── example_module.py       # Python example strategy
	├── example_module.ts       # TypeScript example strategy
	└── templates/              # Scaffolding for new modules
```

Loading a Python module dynamically
```py
import importlib

mod = importlib.import_module('tools.metaultra.example_module')
StrategyClass = getattr(mod, 'ExampleStrategy')
strategy = StrategyClass({'name': 'demo'})
```

Minimal TypeScript usage
```ts
import { ExampleStrategy } from '../../tools/metaultra/example_module'
const s = new ExampleStrategy({ name: 'demo' })
s.onTick({ price: 123.4 })
```

Testing and smoke checks
- Python: `python -m pytest tests/test_metaultra_example.py` (fixtures in `tests/fixtures/`)
- TypeScript: add a small Jest test under `tools/metaultra/__tests__/` that imports compiled JS or uses `ts-jest`.

Notes
- Keep examples intentionally minimal and well-documented to serve as onboarding artifacts for new contributors.
- Ensure `meta.json` exists for any module intended for packaging.
