#!/usr/bin/env python3
"""Check a guardian installation."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from guardian_common import (
    AGENT_NAMES,
    BEGIN,
    END,
    InvalidStateError,
    config_agent_expected,
    is_broken_symlink,
    load_state,
    managed_targets,
    marker_path,
    path_exists,
    read_version,
    repo_root,
    target_matches_source,
    tomllib,
    valid_marker,
)


def pass_line(label: str, detail: str = "") -> None:
    suffix = f": {detail}" if detail else ""
    print(f"PASS {label}{suffix}")


def fail_line(label: str, detail: str, errors: list[str]) -> None:
    print(f"FAIL {label}: {detail}")
    errors.append(label)


def check_target(item: dict, errors: list[str]) -> None:
    source = item["source"]
    target = item["target"]
    label = f"{item['kind']} {item['name']}"
    if is_broken_symlink(target):
        fail_line(label, f"broken symlink {target}", errors)
        return
    if not path_exists(target):
        fail_line(label, f"missing {target}", errors)
        return
    exact = target_matches_source(source, target)
    if not valid_marker(target, item["kind"], item["name"], source):
        if target_matches_source(source, target):
            fail_line(label, f"missing managed marker {marker_path(target)}; rerun install to adopt", errors)
        else:
            fail_line(label, f"unmanaged conflict at {target}", errors)
        return
    if not exact:
        fail_line(label, f"content drift at {target}", errors)
        return
    pass_line(label, str(target))
    pass_line(f"{label} managed marker", str(marker_path(target)))


def check_agents_md(path: Path, errors: list[str]) -> None:
    if not path.exists():
        fail_line("AGENTS.md", f"missing {path}", errors)
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    expected = (repo_root() / "profiles" / "codex" / "AGENTS.md").read_text(encoding="utf-8").strip()
    pattern = re.compile(rf"{re.escape(BEGIN)}\n(?P<body>.*?){re.escape(END)}", re.S)
    match = pattern.search(content)
    if match and match.group("body").strip() == expected:
        pass_line("AGENTS.md Guardian section found")
    else:
        fail_line("AGENTS.md Guardian section", "expected marked bundled Guardian profile not found", errors)


def check_config(path: Path, errors: list[str]) -> None:
    if not path.exists():
        fail_line("config.toml", f"missing {path}", errors)
        return
    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail_line("config.toml parse", str(exc), errors)
        return
    pass_line("config.toml parse")
    features = parsed.get("features", {})
    for key in ("multi_agent", "goals"):
        if features.get(key) is True:
            pass_line(f"config features.{key}")
        else:
            fail_line(f"config features.{key}", "expected true", errors)
    agents = parsed.get("agents", {})
    for name in AGENT_NAMES:
        entry = agents.get(name, {})
        expected = config_agent_expected(name)
        if entry.get("config_file") == expected:
            pass_line(f"config agents.{name}.config_file")
        else:
            fail_line(f"config agents.{name}.config_file", f"expected {expected}", errors)


def check_state(codex_home: Path, errors: list[str]) -> None:
    try:
        state = load_state(codex_home)
    except (json.JSONDecodeError, InvalidStateError, UnicodeDecodeError) as exc:
        fail_line("guardian state", f"invalid state: {exc}", errors)
        return
    if state is None:
        fail_line("guardian state", f"missing {codex_home / 'guardian-state.json'}", errors)
        return
    version = read_version()
    if state.get("version") == version:
        pass_line(f"version v{version}")
    else:
        fail_line("version", f"expected {version}, got {state.get('version')}", errors)
    backup_dir = state.get("backup_dir")
    if backup_dir and Path(backup_dir).exists():
        pass_line("backup directory", backup_dir)
    else:
        fail_line("backup directory", f"missing {backup_dir}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--agents-home", type=Path, default=Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents")))
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    version = read_version()
    if args.version:
        print(f"guardian {version}")
        return 0

    codex_home = args.codex_home.expanduser()
    agents_home = args.agents_home.expanduser()
    root = repo_root()
    errors: list[str] = []

    print("guardian doctor")
    for item in managed_targets(root, codex_home, agents_home, include_skills=True, include_agents=True):
        check_target(item, errors)

    check_agents_md(codex_home / "AGENTS.md", errors)
    check_config(codex_home / "config.toml", errors)
    check_state(codex_home, errors)

    if errors:
        print("")
        print("guardian installation has blockers:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("")
    print("guardian installation checks passed. Restart Codex if this session was already open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
