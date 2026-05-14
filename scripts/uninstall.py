#!/usr/bin/env python3
"""Remove guardian managed files."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

from guardian_common import (
    BEGIN,
    END,
    BackupManager,
    GuardianError,
    InvalidStateError,
    load_state,
    managed_targets,
    marker_path,
    path_exists,
    read_version,
    remove_existing,
    remove_marker,
    render_config_uninstall,
    repo_root,
    target_matches_source,
    valid_marker,
)


def remove_managed_target(item: dict[str, Any], dry_run: bool) -> bool:
    target = item["target"]
    marker = marker_path(target)
    if valid_marker(target, item["kind"], item["name"], item["source"]):
        if not target_matches_source(item["source"], target):
            print(f"skipped modified managed target {target}")
            return False
        if dry_run:
            print(f"Would remove managed target: {target}")
            print(f"Would remove marker: {marker}")
            return True
        remove_existing(target)
        remove_marker(target)
        print(f"removed {target}")
        return True
    if path_exists(target):
        print(f"skipped unmanaged target {target}")
    return False


def update_agents_md(path: Path, backup: BackupManager, dry_run: bool) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(rf"\n?{re.escape(BEGIN)}.*?{re.escape(END)}\n?", re.S)
    if not pattern.search(original):
        return False
    updated = pattern.sub("\n", original)
    if updated == original:
        return False
    if dry_run:
        print(f"Would modify: {path}")
        print(f"Would back up: {path} -> {backup.session_dir / backup.relative_backup_path(path)}")
        return True
    backed_up = backup.backup(path)
    if backed_up:
        print(f"backed up {path} -> {backed_up}")
    path.write_text(updated, encoding="utf-8")
    print(f"updated {path}")
    return True


def update_config(path: Path, backup: BackupManager, restore_values: Optional[dict[str, Optional[Any]]], dry_run: bool) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8", errors="replace")
    has_guardian_sections = any(f"[agents.{name}]" in original for name in ("guardian_boundary_reviewer", "spec_verifier", "quality_reviewer"))
    if not has_guardian_sections and restore_values is None:
        return False
    updated = render_config_uninstall(original, restore_values)
    if updated == original:
        return False
    if dry_run:
        print(f"Would modify: {path}")
        print(f"Would back up: {path} -> {backup.session_dir / backup.relative_backup_path(path)}")
        return True
    backed_up = backup.backup(path)
    if backed_up:
        print(f"backed up {path} -> {backed_up}")
    path.write_text(updated, encoding="utf-8")
    print(f"updated {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--agents-home", type=Path, default=Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents")))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore-config", action="store_true")
    parser.add_argument("--keep-backups", action="store_true", help="Explicitly keep backups. Backups are kept by default.")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    version = read_version()
    if args.version:
        print(f"guardian {version}")
        return 0

    codex_home = args.codex_home.expanduser()
    agents_home = args.agents_home.expanduser()
    root = repo_root()
    backup = BackupManager(codex_home, agents_home, args.backup_dir, args.dry_run)

    if args.dry_run:
        print("guardian uninstall dry run")
    if args.keep_backups:
        print("Backups will be kept.")

    try:
        state = load_state(codex_home)
    except (json.JSONDecodeError, InvalidStateError, OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: guardian state is invalid: {exc}", file=sys.stderr)
        return 1
    if args.restore_config and state is None:
        print(f"ERROR: --restore-config requested but {codex_home / 'guardian-state.json'} is missing.", file=sys.stderr)
        return 1

    restore_values = None
    if args.restore_config:
        restore_values = state.get("previous_config_values", {}) if state else {}

    try:
        for item in managed_targets(root, codex_home, agents_home, include_skills=True, include_agents=True):
            remove_managed_target(item, args.dry_run)

        update_agents_md(codex_home / "AGENTS.md", backup, args.dry_run)
        update_config(codex_home / "config.toml", backup, restore_values, args.dry_run)

        if args.dry_run:
            print("Dry run complete. No files were modified.")
            return 0

        backup.ensure_session()
    except (OSError, GuardianError) as exc:
        print(f"ERROR: uninstall failed: {exc}", file=sys.stderr)
        return 1

    print("guardian uninstall complete. Backups were kept.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
