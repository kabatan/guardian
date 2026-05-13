#!/usr/bin/env python3
"""Check a Codex Guardian installation."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


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


def check_file(path: Path, label: str, errors: list[str]) -> None:
    if path.exists():
        print(f"PASS {label}: {path}")
    else:
        print(f"FAIL {label}: missing {path}")
        errors.append(label)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--agents-home", type=Path, default=Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents")))
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser()
    agents_home = args.agents_home.expanduser()
    errors: list[str] = []

    for skill in SKILL_NAMES:
        check_file(agents_home / "skills" / skill / "SKILL.md", f"skill {skill}", errors)

    check_file(agents_home / "templates" / "guardian" / "project-artifacts.md", "guardian template", errors)

    for name in AGENT_NAMES:
        check_file(codex_home / "agents" / f"{name}.toml", f"agent {name}", errors)

    agents_md = codex_home / "AGENTS.md"
    check_file(agents_md, "AGENTS.md", errors)
    if agents_md.exists():
        content = agents_md.read_text(encoding="utf-8", errors="replace")
        if "Guardian Runtime Contract" in content and "Failure gates:" in content:
            print("PASS AGENTS.md Guardian contract")
        else:
            print("FAIL AGENTS.md Guardian contract: expected Guardian text not found")
            errors.append("AGENTS.md content")

    config = codex_home / "config.toml"
    check_file(config, "config.toml", errors)
    if config.exists():
        try:
            parsed = tomllib.loads(config.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"FAIL config.toml parse: {exc}")
            errors.append("config parse")
        else:
            features = parsed.get("features", {})
            for key in ("multi_agent", "goals"):
                if features.get(key) is True:
                    print(f"PASS config features.{key}")
                else:
                    print(f"FAIL config features.{key}: expected true")
                    errors.append(f"features.{key}")
            agents = parsed.get("agents", {})
            for name in AGENT_NAMES:
                entry = agents.get(name, {})
                expected = f"agents/{name}.toml"
                if entry.get("config_file") == expected:
                    print(f"PASS config agents.{name}.config_file")
                else:
                    print(f"FAIL config agents.{name}.config_file: expected {expected}")
                    errors.append(f"agents.{name}")

    if errors:
        print("")
        print("Codex Guardian installation has blockers:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("")
    print("Codex Guardian installation checks passed. Restart Codex if this session was already open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

