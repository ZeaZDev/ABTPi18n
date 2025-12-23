# Data Structures & Schemas — Canonical Formats

This document defines canonical schemas and in-memory structures used across MetaUltra modules. Use these as the contract for interoperability.

Module manifest (`meta.json`) — minimal contract
```json
{
  "name": "example",
  "version": "0.1.0",
  "entrypoint": "tools.metaultra.example_module:ExampleStrategy",
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "name": {"type": "string"},
      "params": {"type": "object"}
    },
    "required": ["name"]
  }
}
```

Schema conventions
- Use JSON Schema (draft-07 or later) to describe module configuration and exchange formats.
- Explicitly list types and required fields; avoid free-form polymorphism for public contracts.
- Keep schemas small but explicit; large nested unions complicate validation and auditing.

Runtime structures
- Python: prefer dataclasses for exported public contracts and simple dicts for internal transforms.
- TypeScript: prefer explicit interfaces and `readonly` where possible for configuration objects.

Example Python dataclass for strategy config
```py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class StrategyConfig:
    name: str
    params: Dict[str, Any]
```

Best practices
- Keep metadata `meta.json` adjacent to module source, commit it, and include a loader-friendly `entrypoint` reference.
- Validate incoming configs early and provide human-friendly error messages that include the path to the failing property.
