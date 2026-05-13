#!/usr/bin/env python3
"""Install Codex Guardian into a Codex home directory."""

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
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


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def backup(path: Path) -> None:
    if not path.exists():
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak-{stamp}")
    if path.is_dir() and not path.is_symlink():
        shutil.copytree(path, backup_path)
    else:
        shutil.copy2(path, backup_path)


def remove_existing(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def link_dir(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    remove_existing(target)
    if platform.system() == "Windows":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(target), str(source)], check=True)
    else:
        target.symlink_to(source, target_is_directory=True)


def copy_dir(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    remove_existing(target)
    shutil.copytree(source, target)


def install_dir(source: Path, target: Path, mode: str) -> None:
    if mode == "link":
        link_dir(source, target)
    else:
        copy_dir(source, target)


def install_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and source.read_bytes() != target.read_bytes():
        backup(target)
    shutil.copy2(source, target)


def install_agents_md(source: Path, target: Path, mode: str) -> None:
    content = source.read_text(encoding="utf-8").rstrip() + "\n"
    target.parent.mkdir(parents=True, exist_ok=True)

    if mode == "skip":
        return

    if mode == "replace":
        if target.exists() and target.read_text(encoding="utf-8", errors="replace") != content:
            backup(target)
        target.write_text(content, encoding="utf-8")
        return

    managed = f"{BEGIN}\n{content}{END}\n"
    existing = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
    pattern = re.compile(rf"{re.escape(BEGIN)}.*?{re.escape(END)}\n?", re.S)
    if pattern.search(existing):
        updated = pattern.sub(managed, existing)
    elif existing.strip():
        updated = existing.rstrip() + "\n\n" + managed
    else:
        updated = managed

    if target.exists() and existing != updated:
        backup(target)
    target.write_text(updated, encoding="utf-8")


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


def find_section(lines: list[str], section: str) -> tuple[int, int] | None:
    header = f"[{section}]"
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == header:
            start = idx
            break
    if start is None:
        return None
    end = len(lines)
    for idx in range(start + 1, len(lines)):
        if re.match(r"\s*\[.+\]\s*$", lines[idx]):
            end = idx
            break
    return start, end


def set_key(lines: list[str], section: str, key: str, value: str) -> list[str]:
    found = find_section(lines, section)
    if found is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([f"[{section}]", f"{key} = {value}"])
        return lines

    start, end = found
    key_re = re.compile(rf"\s*{re.escape(key)}\s*=")
    new_section = [lines[start]]
    wrote = False
    for line in lines[start + 1 : end]:
        if key_re.match(line):
            if not wrote:
                new_section.append(f"{key} = {value}")
                wrote = True
            continue
        new_section.append(line)
    if not wrote:
        new_section.append(f"{key} = {value}")
    return lines[:start] + new_section + lines[end:]


def update_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    lines = text.splitlines()

    for name in AGENT_NAMES:
        lines = strip_section(lines, f"agents.{name}")

    lines = set_key(lines, "features", "multi_agent", "true")
    lines = set_key(lines, "features", "goals", "true")

    if lines and lines[-1].strip():
        lines.append("")

    agent_blocks = {
        "guardian_boundary_reviewer": [
            '[agents.guardian_boundary_reviewer]',
            'description = "Read-only semantic reviewer for Guardian Base Spec, Plan, MECH, closure, source-fidelity, and recovery boundaries."',
            'config_file = "agents/guardian_boundary_reviewer.toml"',
        ],
        "spec_verifier": [
            '[agents.spec_verifier]',
            'description = "Read-only reviewer that checks whether changed files satisfy assigned R-IDs and approved requirements."',
            'config_file = "agents/spec_verifier.toml"',
        ],
        "quality_reviewer": [
            '[agents.quality_reviewer]',
            'description = "Read-only reviewer that checks implementation quality, correctness risks, regressions, and test adequacy after spec review passes."',
            'config_file = "agents/quality_reviewer.toml"',
        ],
    }

    for name in AGENT_NAMES:
        lines.extend(agent_blocks[name])
        lines.append("")

    updated = "\n".join(lines).rstrip() + "\n"
    if path.exists() and text != updated:
        backup(path)
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--agents-home", type=Path, default=Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents")))
    parser.add_argument("--install-mode", choices=["link", "copy"], default="link")
    parser.add_argument("--agents-mode", choices=["replace", "merge", "skip"], default="merge")
    args = parser.parse_args()

    root = repo_root()
    codex_home = args.codex_home.expanduser()
    agents_home = args.agents_home.expanduser()

    for skill in SKILL_NAMES:
        install_dir(root / "skills" / skill, agents_home / "skills" / skill, args.install_mode)

    install_dir(root / "templates" / "guardian", agents_home / "templates" / "guardian", args.install_mode)

    for name in AGENT_NAMES:
        install_file(root / "agents" / f"{name}.toml", codex_home / "agents" / f"{name}.toml")

    install_agents_md(root / "profiles" / "codex" / "AGENTS.md", codex_home / "AGENTS.md", args.agents_mode)
    update_config(codex_home / "config.toml")

    print(f"Installed Codex Guardian into {codex_home} and {agents_home}.")
    print("Restart Codex, then run scripts/doctor.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

