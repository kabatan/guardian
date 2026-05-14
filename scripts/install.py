#!/usr/bin/env python3
"""Install guardian into a Codex home directory."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Tuple

from guardian_common import (
    AGENT_NAMES,
    BEGIN,
    END,
    BackupManager,
    GuardianError,
    InvalidStateError,
    copy_path,
    is_link_like,
    load_state,
    managed_targets,
    marker_path,
    path_exists,
    previous_feature_values,
    read_version,
    remove_existing,
    render_config_update,
    repo_root,
    state_path,
    target_matches_source,
    valid_marker,
    write_marker,
    write_state,
)


def classify_target(item: dict[str, Any], force: bool, install_mode: str) -> tuple[str, bool]:
    source = item["source"]
    target = item["target"]
    target_mode = item["mode"]
    exists = path_exists(target)
    marker = valid_marker(target, item["kind"], item["name"], source)
    exact = target_matches_source(source, target)
    if target_mode == "file":
        mode_ok = True
    elif install_mode == "copy":
        mode_ok = not is_link_like(target)
    else:
        mode_ok = is_link_like(target)
    needs_replace = exists and (not exact or not mode_ok)

    if not exists:
        return "create", False
    if marker:
        return ("replace-managed" if needs_replace else "refresh-managed"), needs_replace
    if exact and mode_ok:
        return "adopt-legacy", False
    if force:
        return "force-replace-unmanaged", True
    return "conflict", False


def install_directory(source: Path, target: Path, install_mode: str) -> None:
    if install_mode == "link":
        target.parent.mkdir(parents=True, exist_ok=True)
        if platform.system() == "Windows":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(target), str(source)], check=True)
        else:
            target.symlink_to(source, target_is_directory=True)
        return
    copy_path(source, target)


def install_target(item: dict[str, Any], action: str, needs_replace: bool, backup: BackupManager, install_mode: str, dry_run: bool) -> dict[str, str]:
    source = item["source"]
    target = item["target"]
    kind = item["kind"]
    mode = item["mode"]

    if dry_run:
        print(f"Will {action}: {target}")
        if needs_replace:
            print(f"Will back up: {target} -> {backup.session_dir / backup.relative_backup_path(target)}")
        return {"kind": kind, "path": str(target), "marker": str(marker_path(target)), "source": str(source)}

    if needs_replace:
        backed_up = backup.backup(target)
        if backed_up:
            print(f"backed up {target} -> {backed_up}")
        remove_existing(target)

    if action in {"create", "replace-managed", "force-replace-unmanaged"} or needs_replace:
        if mode == "dir":
            install_directory(source, target, install_mode)
        else:
            copy_path(source, target)

    write_marker(target, kind, item["name"], source)
    print(f"{action}: {target}")
    return {"kind": kind, "path": str(target), "marker": str(marker_path(target)), "source": str(source)}


def install_agents_md(source: Path, target: Path, mode: str, backup: BackupManager, dry_run: bool) -> bool:
    if mode == "skip":
        print("Skipping AGENTS.md update.")
        return False

    content = source.read_text(encoding="utf-8").rstrip() + "\n"
    managed = f"{BEGIN}\n{content}{END}\n"
    existing = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""

    if mode == "replace":
        updated = managed
    else:
        import re

        pattern = re.compile(rf"{re.escape(BEGIN)}.*?{re.escape(END)}\n?", re.S)
        if pattern.search(existing):
            updated = pattern.sub(managed, existing)
        elif existing.strip():
            updated = existing.rstrip() + "\n\n" + managed
        else:
            updated = managed

    if existing == updated:
        print(f"unchanged {target}")
        return False

    if dry_run:
        print(f"Will modify: {target}")
        if target.exists():
            print(f"Will back up: {target} -> {backup.session_dir / backup.relative_backup_path(target)}")
        return True

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backed_up = backup.backup(target)
        if backed_up:
            print(f"backed up {target} -> {backed_up}")
    target.write_text(updated, encoding="utf-8")
    print(f"updated {target}")
    return True


def update_config(path: Path, include_agents: bool, backup: BackupManager, dry_run: bool) -> Tuple[bool, dict[str, Optional[Any]]]:
    previous = previous_feature_values(path)
    original = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    updated = render_config_update(original, include_agents)
    if original == updated:
        print(f"unchanged {path}")
        return False, previous

    if dry_run:
        print(f"Will modify: {path}")
        if path.exists():
            print(f"Will back up: {path} -> {backup.session_dir / backup.relative_backup_path(path)}")
        return True, previous

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backed_up = backup.backup(path)
        if backed_up:
            print(f"backed up {path} -> {backed_up}")
    path.write_text(updated, encoding="utf-8")
    print(f"updated {path}")
    return True, previous


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--agents-home", type=Path, default=Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents")))
    parser.add_argument("--install-mode", choices=["link", "copy"], default="copy")
    parser.add_argument("--agents-mode", choices=["replace", "merge", "skip"], default="merge")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--no-config", action="store_true")
    parser.add_argument("--no-agents", action="store_true")
    parser.add_argument("--no-skills", action="store_true")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    version = read_version()
    if args.version:
        print(f"guardian {version}")
        return 0

    root = repo_root()
    codex_home = args.codex_home.expanduser()
    agents_home = args.agents_home.expanduser()
    backup = BackupManager(codex_home, agents_home, args.backup_dir, args.dry_run)
    try:
        existing_state = load_state(codex_home)
    except (json.JSONDecodeError, InvalidStateError, OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: guardian state is invalid: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        print("guardian install dry run")

    include_skills = not args.no_skills
    include_agents = not args.no_agents
    targets = managed_targets(root, codex_home, agents_home, include_skills, include_agents)

    planned: list[tuple[dict[str, Any], str, bool]] = []
    conflicts: list[Path] = []
    for item in targets:
        action, needs_replace = classify_target(item, args.force, args.install_mode)
        if action == "conflict":
            conflicts.append(item["target"])
        planned.append((item, action, needs_replace))

    if conflicts:
        for target in conflicts:
            print(
                f"ERROR: {target} already exists and is not managed by guardian. "
                "Please remove it manually, rename it, or rerun with --force after reviewing the conflict.",
                file=sys.stderr,
            )
        return 1

    state: dict[str, Any] = {
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "codex_home": str(codex_home),
        "agents_home": str(agents_home),
        "backup_dir": str(backup.session_dir),
        "managed_paths": [],
        "modified_files": [],
        "previous_config_values": (
            existing_state["previous_config_values"]
            if existing_state and isinstance(existing_state.get("previous_config_values"), dict)
            else {}
        ),
        "agents_mode": args.agents_mode,
        "install_mode": args.install_mode,
    }

    try:
        for item, action, needs_replace in planned:
            state["managed_paths"].append(install_target(item, action, needs_replace, backup, args.install_mode, args.dry_run))

        agents_changed = install_agents_md(root / "profiles" / "codex" / "AGENTS.md", codex_home / "AGENTS.md", args.agents_mode, backup, args.dry_run)
        if agents_changed:
            state["modified_files"].append(str(codex_home / "AGENTS.md"))

        if not args.no_config:
            config_changed, previous = update_config(codex_home / "config.toml", include_agents, backup, args.dry_run)
            if not state["previous_config_values"]:
                state["previous_config_values"] = previous
            if config_changed:
                state["modified_files"].append(str(codex_home / "config.toml"))
        else:
            print("Skipping config.toml update.")

        if args.dry_run:
            print("Dry run complete. No files were modified.")
            return 0

        backup.ensure_session()
        write_state(codex_home, state)
    except (OSError, subprocess.CalledProcessError, GuardianError) as exc:
        print(f"ERROR: install failed: {exc}", file=sys.stderr)
        return 1

    print(f"Installed guardian into {codex_home} and {agents_home}.")
    print("Restart Codex, then run scripts/doctor.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
