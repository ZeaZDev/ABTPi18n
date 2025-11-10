#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

def parse_folder_id(link_or_id: str) -> str:
    """
    Accepts either a Google Drive folder URL or the raw folder ID and returns the ID.
    Examples:
      https://drive.google.com/drive/folders/<FOLDER_ID>?usp=...
      <FOLDER_ID>
    """
    txt = link_or_id.strip()
    if "drive.google.com" in txt:
        # Expecting .../drive/folders/<ID>
        parts = txt.split("/folders/")
        if len(parts) >= 2:
            tail = parts[1]
            folder_id = tail.split("?")[0].split("/")[0]
            return folder_id
        raise ValueError("Could not parse folder ID from URL. Please provide the raw folder ID.")
    return txt

def main() -> int:
    parser = argparse.ArgumentParser(description="Download a Google Drive folder into external/drive_assets using gdown.")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder URL or raw folder ID")
    parser.add_argument("--out-dir", default="external/drive_assets", help="Destination directory")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    try:
        import gdown  # type: ignore
    except ImportError:
        print("ERROR: gdown is not installed. Install with: pip install gdown", file=sys.stderr)
        return 2

    folder_id = parse_folder_id(args.folder_id)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://drive.google.com/drive/folders/{folder_id}"
    # gdown.download_folder supports URL or id=... param
    try:
        gdown.download_folder(url=url, output=str(out_dir), quiet=args.quiet, use_cookies=False)
    except Exception as e:
        print(f"ERROR: Failed to download folder: {e}", file=sys.stderr)
        return 3

    print(f"Downloaded Google Drive folder {folder_id} into {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())