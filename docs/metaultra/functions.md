# Functions, Interfaces & Contracts

This page lists recommended interfaces, lifecycle hooks, and the contract rules used by MetaUltra modules.

Design principles
- Small surface area per module: each plugin exposes a small set of deterministic functions.
- Declarative metadata: `meta.json` describes entrypoints and schemas so tools can load modules dynamically.
- Side-effect transparency: any I/O or DB writes must be documented in the module manifest.

Python example: Strategy contract
```py
from typing import Dict, Any, List

class StrategyInterface:
    def __init__(self, config: Dict[str, Any]):
        """Initialize with a validated config (must conform to JSON Schema in meta.json)."""

    async def on_tick(self, tick: Dict[str, Any]) -> None:
        """Handle a market tick; may be async for I/O friendly implementations."""

    def generate_signals(self) -> List[Dict[str, Any]]:
        """Return a deterministic list of signals; side-effects should be avoided here."""

    def metadata(self) -> Dict[str, Any]:
        """Return runtime metadata (name, version, last_run, metrics)."""
```

TypeScript example: strategy interface
```ts
export interface StrategyConfig { name: string; params?: Record<string, any> }

export interface Strategy {
  onTick(tick: { price: number; time?: string }): Promise<void> | void
  generateSignals(): Array<{ signal: string; score?: number }>
}
```

Manifest contract (`meta.json`)
- `name`: module name
- `version`: semver
- `entrypoint`: module:path (e.g., `tools.metaultra.example_module:ExampleStrategy`)
- `schema`: JSON Schema for config

Loader behavior
- Tools should validate config against `schema` before instantiating entrypoints.
- Loaders may skip modules that fail schema validation and emit a clear warning referencing the `meta.json` path.
