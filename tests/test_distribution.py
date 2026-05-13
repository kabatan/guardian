from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.py"
DOCTOR = ROOT / "scripts" / "doctor.py"
UNINSTALL = ROOT / "scripts" / "uninstall.py"


class DistributionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.codex_home = self.root / ".codex"
        self.agents_home = self.root / ".agents"
        self.env = os.environ.copy()
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"
        self.env.pop("CODEX_HOME", None)
        self.env.pop("AGENTS_HOME", None)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_script(self, script: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--codex-home",
                str(self.codex_home),
                "--agents-home",
                str(self.agents_home),
                *args,
            ],
            cwd=ROOT,
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if check and result.returncode != 0:
            self.fail(
                f"{script.name} failed with {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
        return result

    def install(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.run_script(INSTALL, "--agents-mode", "merge", "--install-mode", "copy", *args, check=check)

    def marker_for(self, path: Path) -> Path:
        return path.with_name(path.name + ".guardian-managed")

    def is_link_like(self, path: Path) -> bool:
        if path.is_symlink():
            return True
        attrs = getattr(path.stat(), "st_file_attributes", 0)
        return bool(attrs & 0x400)

    def test_fresh_install_doctor_and_state(self) -> None:
        self.install()

        self.assertTrue((self.agents_home / "skills" / "plan-contract" / "SKILL.md").exists())
        self.assertTrue(self.marker_for(self.agents_home / "skills" / "plan-contract").exists())
        self.assertTrue((self.agents_home / "templates" / "guardian" / "project-artifacts.md").exists())
        self.assertTrue(self.marker_for(self.agents_home / "templates" / "guardian").exists())
        self.assertTrue((self.codex_home / "agents" / "spec_verifier.toml").exists())
        self.assertTrue(self.marker_for(self.codex_home / "agents" / "spec_verifier.toml").exists())

        state_path = self.codex_home / "guardian-state.json"
        self.assertTrue(state_path.exists())
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["version"], "0.1.0")
        self.assertTrue(Path(state["backup_dir"]).exists())

        doctor = self.run_script(DOCTOR)
        self.assertIn("PASS version v0.1.0", doctor.stdout)

    def test_install_is_idempotent(self) -> None:
        self.install()
        second = self.install()
        self.assertEqual(second.returncode, 0)
        self.run_script(DOCTOR)

    def test_agents_merge_creates_central_backup(self) -> None:
        self.codex_home.mkdir(parents=True)
        agents_md = self.codex_home / "AGENTS.md"
        agents_md.write_text("# User instructions\n\nKeep this line.\n", encoding="utf-8")

        self.install()

        merged = agents_md.read_text(encoding="utf-8")
        self.assertIn("Keep this line.", merged)
        self.assertIn("<!-- BEGIN CODEX-GUARDIAN -->", merged)
        backups = list((self.codex_home / "guardian-backups").glob("*/codex/AGENTS.md"))
        self.assertEqual(len(backups), 1)
        self.assertIn("Keep this line.", backups[0].read_text(encoding="utf-8"))

    def test_config_restore_preserves_unrelated_config(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        config.write_text('[features]\ngoals = false\n\n[other]\nvalue = "kept"\n', encoding="utf-8")

        self.install()
        installed = config.read_text(encoding="utf-8")
        self.assertIn("multi_agent = true", installed)
        self.assertIn("goals = true", installed)

        self.run_script(UNINSTALL, "--restore-config")
        restored = config.read_text(encoding="utf-8")
        self.assertNotIn("multi_agent", restored)
        self.assertIn("goals = false", restored)
        self.assertIn('[other]\nvalue = "kept"', restored)
        self.assertNotIn("[agents.spec_verifier]", restored)

    def test_config_restore_after_idempotent_reinstall_uses_original_values(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        config.write_text('[features]\ngoals = false\n\n[other]\nvalue = "kept"\n', encoding="utf-8")

        self.install()
        self.install()
        self.run_script(UNINSTALL, "--restore-config")

        restored = config.read_text(encoding="utf-8")
        self.assertNotIn("multi_agent", restored)
        self.assertIn("goals = false", restored)
        self.assertIn('[other]\nvalue = "kept"', restored)

    def test_config_restore_after_no_config_reinstall_uses_original_values(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        config.write_text("[features]\ngoals = false\n", encoding="utf-8")

        self.install()
        self.install("--no-config")
        self.run_script(UNINSTALL, "--restore-config")

        restored = config.read_text(encoding="utf-8")
        self.assertNotIn("multi_agent", restored)
        self.assertIn("goals = false", restored)

    def test_unmanaged_skill_conflict_stops_and_force_backs_up(self) -> None:
        conflict = self.agents_home / "skills" / "plan-contract"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("user skill\n", encoding="utf-8")

        failed = self.install(check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("not managed by guardian", failed.stdout + failed.stderr)
        self.assertEqual((conflict / "SKILL.md").read_text(encoding="utf-8"), "user skill\n")

        self.install("--force")
        self.assertNotEqual((conflict / "SKILL.md").read_text(encoding="utf-8"), "user skill\n")
        backups = list((self.codex_home / "guardian-backups").glob("*/agents/skills/plan-contract/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "user skill\n")

    def test_forged_marker_does_not_bypass_install_conflict(self) -> None:
        conflict = self.agents_home / "skills" / "plan-contract"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("user skill\n", encoding="utf-8")
        self.marker_for(conflict).write_text(
            json.dumps({"managed_by": "guardian", "kind": "skill", "name": "other"}),
            encoding="utf-8",
        )

        failed = self.install(check=False)

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("not managed by guardian", failed.stdout + failed.stderr)
        self.assertEqual((conflict / "SKILL.md").read_text(encoding="utf-8"), "user skill\n")

    def test_marker_missing_version_does_not_bypass_install_conflict(self) -> None:
        conflict = self.agents_home / "skills" / "plan-contract"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("user skill\n", encoding="utf-8")
        self.marker_for(conflict).write_text(
            json.dumps(
                {
                    "managed_by": "guardian",
                    "kind": "skill",
                    "name": "plan-contract",
                    "target": str(conflict),
                    "source": str(ROOT / "skills" / "plan-contract"),
                }
            ),
            encoding="utf-8",
        )

        failed = self.install(check=False)

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("not managed by guardian", failed.stdout + failed.stderr)
        self.assertEqual((conflict / "SKILL.md").read_text(encoding="utf-8"), "user skill\n")

    def test_dry_run_does_not_mutate(self) -> None:
        result = self.install("--dry-run")
        self.assertIn("guardian install dry run", result.stdout)
        self.assertFalse((self.codex_home / "AGENTS.md").exists())
        self.assertFalse((self.agents_home / "skills" / "plan-contract").exists())
        self.assertFalse((self.codex_home / "guardian-state.json").exists())

    def test_uninstall_removes_managed_and_preserves_unmanaged(self) -> None:
        self.install()
        managed = self.agents_home / "skills" / "plan-contract"
        unmanaged = self.agents_home / "skills" / "base-spec-gate"
        self.marker_for(unmanaged).unlink()

        self.run_script(UNINSTALL)

        self.assertFalse(managed.exists())
        self.assertFalse(self.marker_for(managed).exists())
        self.assertTrue(unmanaged.exists())
        self.assertTrue((unmanaged / "SKILL.md").exists())

    def test_uninstall_preserves_target_with_forged_marker(self) -> None:
        target = self.agents_home / "skills" / "plan-contract"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("user skill\n", encoding="utf-8")
        self.marker_for(target).write_text("{}", encoding="utf-8")

        self.run_script(UNINSTALL)

        self.assertTrue(target.exists())
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "user skill\n")

    def test_uninstall_preserves_target_with_marker_missing_version(self) -> None:
        target = self.agents_home / "skills" / "plan-contract"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("user skill\n", encoding="utf-8")
        self.marker_for(target).write_text(
            json.dumps(
                {
                    "managed_by": "guardian",
                    "kind": "skill",
                    "name": "plan-contract",
                    "target": str(target),
                    "source": str(ROOT / "skills" / "plan-contract"),
                }
            ),
            encoding="utf-8",
        )

        self.run_script(UNINSTALL)

        self.assertTrue(target.exists())
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "user skill\n")

    def test_uninstall_preserves_drifted_target_with_complete_marker(self) -> None:
        self.install()
        target = self.agents_home / "skills" / "plan-contract"
        (target / "SKILL.md").write_text("user modified skill\n", encoding="utf-8")

        self.run_script(UNINSTALL)

        self.assertTrue(target.exists())
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "user modified skill\n")

    def test_uninstall_preserves_structural_drift_file_replaced_by_directory(self) -> None:
        self.install()
        target = self.agents_home / "skills" / "plan-contract"
        (target / "SKILL.md").unlink()
        (target / "SKILL.md").mkdir()
        (target / "SKILL.md" / "user.txt").write_text("user data\n", encoding="utf-8")

        self.run_script(UNINSTALL)

        self.assertTrue((target / "SKILL.md" / "user.txt").exists())

    def test_reinstall_copy_replaces_linked_skill(self) -> None:
        result = self.run_script(
            INSTALL,
            "--agents-mode",
            "merge",
            "--install-mode",
            "link",
            check=False,
        )
        if result.returncode != 0:
            self.skipTest(f"link install unavailable: {result.stderr or result.stdout}")
        target = self.agents_home / "skills" / "plan-contract"
        if not self.is_link_like(target):
            self.skipTest("link install did not create a detectable link or junction")

        self.install()

        self.assertFalse(self.is_link_like(target))

    def test_uninstall_does_not_rewrite_unmarked_agents_md(self) -> None:
        self.codex_home.mkdir(parents=True)
        agents_md = self.codex_home / "AGENTS.md"
        original = "# User instructions\n\nKeep trailing spaces.   \n"
        agents_md.write_text(original, encoding="utf-8")

        self.run_script(UNINSTALL)

        self.assertEqual(agents_md.read_text(encoding="utf-8"), original)

    def test_uninstall_does_not_rewrite_unrelated_config(self) -> None:
        self.codex_home.mkdir(parents=True)
        config = self.codex_home / "config.toml"
        original = '[other]\nvalue = "kept"\n\n'
        config.write_text(original, encoding="utf-8")

        self.run_script(UNINSTALL)

        self.assertEqual(config.read_text(encoding="utf-8"), original)

    def test_uninstall_keep_backups_flag_is_explicitly_supported(self) -> None:
        self.install()

        result = self.run_script(UNINSTALL, "--keep-backups")

        self.assertIn("Backups will be kept.", result.stdout)
        self.assertTrue((self.codex_home / "guardian-backups").exists())

    def test_doctor_detects_broken_symlink(self) -> None:
        self.install()
        target = self.agents_home / "skills" / "plan-contract"
        if target.exists():
            shutil.rmtree(target)
        try:
            target.symlink_to(self.root / "missing-target", target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")

        result = self.run_script(DOCTOR, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken symlink", result.stdout)

    def test_doctor_reports_unmanaged_conflict(self) -> None:
        self.install()
        target = self.agents_home / "skills" / "plan-contract"
        marker = self.marker_for(target)
        marker.unlink()
        (target / "SKILL.md").write_text("user modified skill\n", encoding="utf-8")

        result = self.run_script(DOCTOR, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unmanaged conflict", result.stdout)

    def test_doctor_reports_managed_content_drift(self) -> None:
        self.install()
        target = self.agents_home / "skills" / "plan-contract"
        (target / "SKILL.md").write_text("managed but modified\n", encoding="utf-8")

        result = self.run_script(DOCTOR, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("content drift", result.stdout)

    def test_doctor_reports_structural_drift_file_replaced_by_directory(self) -> None:
        self.install()
        target = self.agents_home / "skills" / "plan-contract"
        (target / "SKILL.md").unlink()
        (target / "SKILL.md").mkdir()

        result = self.run_script(DOCTOR, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("content drift", result.stdout)

    def test_doctor_rejects_malformed_guardian_agents_block(self) -> None:
        self.install()
        agents_md = self.codex_home / "AGENTS.md"
        agents_md.write_text(
            "Guardian Runtime Contract\nFailure gates:\n\n"
            "<!-- BEGIN CODEX-GUARDIAN -->\n"
            "not the bundled guardian profile\n"
            "<!-- END CODEX-GUARDIAN -->\n",
            encoding="utf-8",
        )

        result = self.run_script(DOCTOR, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AGENTS.md Guardian section", result.stdout)

    def test_doctor_reports_invalid_state_json_without_traceback(self) -> None:
        self.install()
        (self.codex_home / "guardian-state.json").write_text("{invalid json", encoding="utf-8")

        result = self.run_script(DOCTOR, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("guardian state", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_doctor_reports_wrong_state_type_without_traceback(self) -> None:
        self.install()
        (self.codex_home / "guardian-state.json").write_text("[]", encoding="utf-8")

        result = self.run_script(DOCTOR, check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("guardian state", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_install_reports_invalid_state_json_without_traceback(self) -> None:
        self.codex_home.mkdir(parents=True)
        (self.codex_home / "guardian-state.json").write_text("{invalid json", encoding="utf-8")

        result = self.install(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("guardian state", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_install_reports_wrong_state_type_without_traceback(self) -> None:
        self.codex_home.mkdir(parents=True)
        (self.codex_home / "guardian-state.json").write_text("[]", encoding="utf-8")

        result = self.install(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("guardian state", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_uninstall_reports_invalid_state_json_without_traceback(self) -> None:
        self.codex_home.mkdir(parents=True)
        (self.codex_home / "guardian-state.json").write_text("{invalid json", encoding="utf-8")

        result = self.run_script(UNINSTALL, "--restore-config", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("guardian state", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_uninstall_reports_wrong_state_type_without_traceback(self) -> None:
        self.codex_home.mkdir(parents=True)
        (self.codex_home / "guardian-state.json").write_text("[]", encoding="utf-8")

        result = self.run_script(UNINSTALL, "--restore-config", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("guardian state", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_non_utf8_marker_is_treated_as_invalid(self) -> None:
        conflict = self.agents_home / "skills" / "plan-contract"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("user skill\n", encoding="utf-8")
        self.marker_for(conflict).write_bytes(b"\xff\xfe\x00")

        failed = self.install(check=False)

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("not managed by guardian", failed.stdout + failed.stderr)


if __name__ == "__main__":
    unittest.main()
