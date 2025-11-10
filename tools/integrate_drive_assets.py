#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Dict, Any, List

def load_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as e:
        raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from e
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def expand_patterns(root: Path, patterns: List[str]) -> List[Path]:
    files: List[Path] = []
    for pat in patterns:
        files.extend(root.glob(pat))
    # Keep only files
    return [p for p in files if p.is_file()]

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def copy_file(src: Path, dst: Path) -> None:
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)

def main() -> int:
    parser = argparse.ArgumentParser(description="Integrate assets downloaded from Google Drive into repo structure.")
    parser.add_argument("--assets-dir", default="external/drive_assets", help="Source dir containing downloaded assets")
    parser.add_argument("--map", default="configs/drive_assets.map.yaml", help="YAML mapping file")
    parser.add_argument("--dry-run", action="store_true", help="Do not copy, just print actions")
    args = parser.parse_args()

    src_root = Path(args.assets_dir)
    if not src_root.exists():
        print(f"Assets dir not found: {src_root}")
        return 1

    mapping = load_yaml(Path(args.map))
    rules = mapping.get("rules", [])

    if not rules:
        print("No rules found in mapping YAML.")
        return 2

    actions = []
    for rule in rules:
        patterns = rule.get("patterns", [])
        dest_root = Path(rule.get("dest"))
        strip_prefix = rule.get("strip_prefix", "")
        keep_tree = bool(rule.get("keep_tree", True))

        for src_file in expand_patterns(src_root, patterns):
            rel = src_file.relative_to(src_root)
            if strip_prefix and rel.as_posix().startswith(strip_prefix.rstrip("/") + "/"):
                rel = Path(rel.as_posix()[len(strip_prefix.rstrip('/') + '/'):])

            dst_path = dest_root / (rel if keep_tree else src_file.name)
            actions.append((src_file, dst_path))

    for src_file, dst_path in actions:
        if args.dry_run:
            print(f"Would copy: {src_file} -> {dst_path}")
        else:
            copy_file(src_file, dst_path)
            print(f"Copied: {src_file} -> {dst_path}")

    print(f"Completed integration of {len(actions)} files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())