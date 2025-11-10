from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import List, Type

from core.strategy_base import Strategy
from core.strategy_registry import StrategyRegistry

def _load_module_from_path(py_path: Path):
    spec = importlib.util.spec_from_file_location(py_path.stem, str(py_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {py_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[py_path.stem] = module
    spec.loader.exec_module(module)
    return module

def load_external_strategies(search_dir: str = "strategies/external") -> List[str]:
    """
    Dynamically import all .py files under search_dir and register any Strategy subclasses.
    Returns a list of registered strategy names.
    """
    registered: List[str] = []
    root = Path(search_dir)
    if not root.exists():
        return registered

    for py_file in root.rglob("*.py"):
        try:
            mod = _load_module_from_path(py_file)
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, Strategy) and obj is not Strategy:
                    # If the class didn't self-register, attempt registry here.
                    name = getattr(obj, "name", "").strip().upper()
                    if name:
                        try:
                            StrategyRegistry.register(obj)
                            registered.append(name)
                        except Exception:
                            # Ignore duplicates or bad classes
                            pass
        except Exception as e:
            # Avoid crashing init due to external file issues; surface minimal info
            print(f"[strategy_autoload] Skipped {py_file}: {e}")
    return registered