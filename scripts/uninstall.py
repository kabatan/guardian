#!/usr/bin/env python3
"""Remove Codex Guardian managed files."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from datetime import datetime
from pathlib import Path


AGENT_NAMES = [
    "guardian_boundary_reviewer",
    "spec_verifier",
    "quality_reviewer",
]

SKILL_NAMES = [
    "using-spec-guardian",
    "base-spec-gate",
    "plan-contract",
    "goal-guardian-execution",
    "closure-recovery",
    "guardian-session-handoff",
]

BEGIN = "<!-- BEGIN CODEX-GUARDIAN -->"
END = "<!-- END CODEX-GUARDIAN -->"


def backup(path: Path) -> None:
    if not path.exists():
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, path.with_name(f"{path.name}.bak-{stamp}"))


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)
    print(f"removed {path}")


def strip_section(lines: list[str], header: str) -> list[str]:
    result: list[str] = []
    i = 0
    target = f"[{header}]"
    while i < len(lines):
        if lines[i].strip() == target:
            i += 1
            while i < len(lines) and not re.match(r"\s*\[.+\]\s*$", lines[i]):
                i += 1
            continue
        result.append(lines[i])
        i += 1
    return result


def update_config(path: Path) -> None:
    if not path.exists():
        return
    original = path.read_text(encoding="utf-8", errors="replace")
    lines = original.splitlines()
    for name in AGENT_NAMES:
        lines = strip_section(lines, f"agents.{name}")
    updated = "\n".join(lines).rstrip() + "\n"
    if updated != original:
        backup(path)
        path.write_text(updated, encoding="utf-8")
        print(f"updated {path}")


def update_agents_md(path: Path) -> None:
    if not path.exists():
        return
    original = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(rf"\n?{re.escape(BEGIN)}.*?{re.escape(END)}\n?", re.S)
    updated = pattern.sub("\n", original).strip() + "\n"
    if updated != original:
        backup(path)
        path.write_text(updated, encoding="utf-8")
        print(f"updated {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--agents-home", type=Path, default=Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents")))
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser()
    agents_home = args.agents_home.expanduser()

    for skill in SKILL_NAMES:
        remove_path(agents_home / "skills" / skill)
    remove_path(agents_home / "templates" / "guardian")
    for name in AGENT_NAMES:
        remove_path(codex_home / "agents" / f"{name}.toml")

    update_agents_md(codex_home / "AGENTS.md")
    update_config(codex_home / "config.toml")
    print("Codex Guardian uninstall complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

