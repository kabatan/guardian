from __future__ import annotations

import filecmp
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Tuple

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

BEGIN = "<!-- BEGIN CODEX-GUARDIAN -->"
END = "<!-- END CODEX-GUARDIAN -->"
MARKER_SUFFIX = ".guardian-managed"
STATE_NAME = "guardian-state.json"


class GuardianError(RuntimeError):
    pass


class InvalidStateError(GuardianError):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_version() -> str:
    version_file = repo_root() / "VERSION"
    return version_file.read_text(encoding="utf-8").strip()


def marker_path(target: Path) -> Path:
    return target.with_name(target.name + MARKER_SUFFIX)


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def is_broken_symlink(path: Path) -> bool:
    return path.is_symlink() and not path.exists()


def write_marker(target: Path, kind: str, name: str, source: Path, dry_run: bool = False) -> None:
    marker = marker_path(target)
    if dry_run:
        return
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(
        json.dumps(
            {
                "managed_by": "guardian",
                "version": read_version(),
                "kind": kind,
                "name": name,
                "target": str(target),
                "source": str(source),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def remove_marker(target: Path, dry_run: bool = False) -> None:
    marker = marker_path(target)
    if marker.exists() or marker.is_symlink():
        if not dry_run:
            marker.unlink()


def load_marker(target: Path) -> Optional[dict[str, Any]]:
    marker = marker_path(target)
    if not marker.exists():
        return None
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def valid_marker(target: Path, kind: str, name: str, source: Path) -> bool:
    data = load_marker(target)
    if data is None:
        return False
    if data.get("managed_by") != "guardian":
        return False
    version = data.get("version")
    if not isinstance(version, str) or not re.match(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$", version):
        return False
    if data.get("kind") != kind or data.get("name") != name:
        return False
    try:
        marker_target = Path(str(data.get("target", ""))).expanduser()
        marker_source = Path(str(data.get("source", ""))).expanduser()
        if marker_target.resolve(strict=False) != target.resolve(strict=False):
            return False
        if marker_source.resolve(strict=False) != source.resolve(strict=False):
            return False
    except OSError:
        return False
    return True


def remove_existing(path: Path) -> None:
    if not path_exists(path):
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attrs = getattr(path.stat(), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attrs & 0x400)


def copy_path(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target, symlinks=True)
    else:
        shutil.copy2(source, target)


def dir_tree_equal(left: Path, right: Path) -> bool:
    if not right.is_dir():
        return False
    cmp = filecmp.dircmp(left, right)
    if cmp.left_only or cmp.right_only or cmp.funny_files or cmp.common_funny:
        return False
    for name in cmp.common_files:
        if not filecmp.cmp(left / name, right / name, shallow=False):
            return False
    return all(dir_tree_equal(left / name, right / name) for name in cmp.common_dirs)


def target_matches_source(source: Path, target: Path) -> bool:
    if is_broken_symlink(target) or not path_exists(target):
        return False
    try:
        if target.is_symlink() and target.resolve() == source.resolve():
            return True
    except OSError:
        return False
    if source.is_dir():
        return dir_tree_equal(source, target)
    if source.is_file() and target.is_file():
        return filecmp.cmp(source, target, shallow=False)
    return False


def state_path(codex_home: Path) -> Path:
    return codex_home / STATE_NAME


def load_state(codex_home: Path) -> Optional[dict[str, Any]]:
    path = state_path(codex_home)
    if not path.exists():
        return None
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise InvalidStateError("guardian state must be a JSON object")
    return parsed


def write_state(codex_home: Path, state: dict[str, Any], dry_run: bool = False) -> None:
    if dry_run:
        return
    codex_home.mkdir(parents=True, exist_ok=True)
    state_path(codex_home).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def managed_targets(root: Path, codex_home: Path, agents_home: Path, include_skills: bool, include_agents: bool) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    if include_skills:
        for skill in SKILL_NAMES:
            targets.append(
                {
                    "kind": "skill",
                    "name": skill,
                    "source": root / "skills" / skill,
                    "target": agents_home / "skills" / skill,
                    "mode": "dir",
                }
            )
        targets.append(
            {
                "kind": "template",
                "name": "guardian",
                "source": root / "templates" / "guardian",
                "target": agents_home / "templates" / "guardian",
                "mode": "dir",
            }
        )
    if include_agents:
        for name in AGENT_NAMES:
            targets.append(
                {
                    "kind": "agent",
                    "name": name,
                    "source": root / "agents" / f"{name}.toml",
                    "target": codex_home / "agents" / f"{name}.toml",
                    "mode": "file",
                }
            )
    return targets


class BackupManager:
    def __init__(self, codex_home: Path, agents_home: Path, backup_dir: Optional[Path], dry_run: bool) -> None:
        root = backup_dir.expanduser() if backup_dir else codex_home / "guardian-backups"
        self.root = root
        self.session_dir = root / datetime.now().strftime("%Y%m%d-%H%M%S")
        self.codex_home = codex_home
        self.agents_home = agents_home
        self.dry_run = dry_run

    def ensure_session(self) -> None:
        if not self.dry_run:
            self.session_dir.mkdir(parents=True, exist_ok=True)

    def relative_backup_path(self, path: Path) -> Path:
        try:
            return Path("codex") / path.relative_to(self.codex_home)
        except ValueError:
            pass
        try:
            return Path("agents") / path.relative_to(self.agents_home)
        except ValueError:
            pass
        safe = [part.replace(":", "") for part in path.parts if part not in (path.anchor, "\\", "/")]
        return Path("other").joinpath(*safe)

    def backup(self, path: Path) -> Optional[Path]:
        if not path_exists(path):
            return None
        dest = self.session_dir / self.relative_backup_path(path)
        counter = 1
        candidate = dest
        while candidate.exists():
            candidate = dest.with_name(f"{dest.name}.{counter}")
            counter += 1
        if self.dry_run:
            return candidate
        self.ensure_session()
        candidate.parent.mkdir(parents=True, exist_ok=True)
        if path.is_symlink():
            target = os.readlink(path)
            candidate.symlink_to(target, target_is_directory=path.is_dir())
        elif path.is_dir():
            shutil.copytree(path, candidate, symlinks=True)
        else:
            shutil.copy2(path, candidate)
        return candidate


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


def find_section(lines: list[str], section: str) -> Optional[Tuple[int, int]]:
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


def format_toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value)


def set_key(lines: list[str], section: str, key: str, value: Any) -> list[str]:
    rendered = format_toml_value(value)
    found = find_section(lines, section)
    if found is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([f"[{section}]", f"{key} = {rendered}"])
        return lines

    start, end = found
    key_re = re.compile(rf"\s*{re.escape(key)}\s*=")
    new_section = [lines[start]]
    wrote = False
    for line in lines[start + 1 : end]:
        if key_re.match(line):
            if not wrote:
                new_section.append(f"{key} = {rendered}")
                wrote = True
            continue
        new_section.append(line)
    if not wrote:
        new_section.append(f"{key} = {rendered}")
    return lines[:start] + new_section + lines[end:]


def remove_key(lines: list[str], section: str, key: str) -> list[str]:
    found = find_section(lines, section)
    if found is None:
        return lines
    start, end = found
    key_re = re.compile(rf"\s*{re.escape(key)}\s*=")
    new_section = [line for line in lines[start:end] if not key_re.match(line)]
    return lines[:start] + new_section + lines[end:]


def previous_feature_values(config_path: Path) -> dict[str, Optional[Any]]:
    values: dict[str, Optional[Any]] = {
        "features.multi_agent": None,
        "features.goals": None,
    }
    if not config_path.exists():
        return values
    try:
        parsed = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return values
    features = parsed.get("features", {})
    for key in ("multi_agent", "goals"):
        dotted = f"features.{key}"
        if key in features:
            values[dotted] = features[key]
    return values


def guardian_agent_blocks() -> dict[str, list[str]]:
    return {
        "guardian_boundary_reviewer": [
            "[agents.guardian_boundary_reviewer]",
            'description = "Read-only semantic reviewer for Guardian Base Spec, Plan, MECH, closure, source-fidelity, and recovery boundaries."',
            'config_file = "agents/guardian_boundary_reviewer.toml"',
        ],
        "spec_verifier": [
            "[agents.spec_verifier]",
            'description = "Read-only reviewer that checks whether changed files satisfy assigned R-IDs and approved requirements."',
            'config_file = "agents/spec_verifier.toml"',
        ],
        "quality_reviewer": [
            "[agents.quality_reviewer]",
            'description = "Read-only reviewer that checks implementation quality, correctness risks, regressions, and test adequacy after spec review passes."',
            'config_file = "agents/quality_reviewer.toml"',
        ],
    }


def render_config_update(original: str, include_agents: bool) -> str:
    lines = original.splitlines()
    for name in AGENT_NAMES:
        lines = strip_section(lines, f"agents.{name}")

    lines = set_key(lines, "features", "multi_agent", True)
    lines = set_key(lines, "features", "goals", True)

    if include_agents:
        if lines and lines[-1].strip():
            lines.append("")
        blocks = guardian_agent_blocks()
        for name in AGENT_NAMES:
            lines.extend(blocks[name])
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_config_uninstall(original: str, restore_values: Optional[dict[str, Optional[Any]]]) -> str:
    lines = original.splitlines()
    for name in AGENT_NAMES:
        lines = strip_section(lines, f"agents.{name}")

    if restore_values is not None:
        for dotted, value in restore_values.items():
            section, key = dotted.split(".", 1)
            if value is None:
                lines = remove_key(lines, section, key)
            else:
                lines = set_key(lines, section, key, value)

    return "\n".join(lines).rstrip() + "\n"


def config_agent_expected(name: str) -> str:
    return f"agents/{name}.toml"
