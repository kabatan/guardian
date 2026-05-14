from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_repo(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class DistributionDocsTests(unittest.TestCase):
    def test_release_version_is_current(self) -> None:
        readme = read_repo("README.md")
        release_notes = read_repo("RELEASE_NOTES.md")
        version = read_repo("VERSION")

        self.assertEqual(version.strip(), "0.1.1")
        self.assertIn("guardian v0.1.1", release_notes)
        self.assertIn("--branch v0.1.1", readme)
        self.assertIn("--branch v0.1.1", release_notes)

    def test_install_examples_use_canonical_repo_url(self) -> None:
        readme = read_repo("README.md")
        release_notes = read_repo("RELEASE_NOTES.md")

        self.assertIn("https://github.com/kabatan/guardian.git", readme)
        self.assertIn("https://github.com/kabatan/guardian.git", release_notes)
        self.assertNotIn("https://github.com/kabatan/codex-guardian.git", readme)
        self.assertNotIn("https://github.com/kabatan/codex-guardian.git", release_notes)

    def test_update_example_does_not_reference_old_unpublished_example(self) -> None:
        readme = read_repo("README.md")

        self.assertNotIn("git checkout v0.1.1", readme)
        self.assertIn("git checkout <new-version>", readme)

    def test_first_install_flow_runs_dry_run_before_install(self) -> None:
        readme = read_repo("README.md")
        install_section = readme.split("## Safety Model", 1)[0]
        dry_run_index = install_section.index("--dry-run")
        install_index = install_section.index("--agents-mode merge --install-mode copy", dry_run_index + 1)

        self.assertLess(dry_run_index, install_index)

        release_notes = read_repo("RELEASE_NOTES.md")
        release_dry_run = release_notes.index("--dry-run")
        release_install = release_notes.index("--agents-mode merge --install-mode copy", release_dry_run + 1)

        self.assertLess(release_dry_run, release_install)

    def test_update_flow_runs_dry_run_before_install(self) -> None:
        readme = read_repo("README.md")
        update_section = readme.split("## Update", 1)[1].split("## Uninstall", 1)[0]
        dry_run_index = update_section.index("--dry-run")
        install_index = update_section.index("--agents-mode merge --install-mode copy", dry_run_index + 1)

        self.assertLess(dry_run_index, install_index)

    def test_minimal_example_and_glossary_exist(self) -> None:
        readme = read_repo("README.md")
        glossary = read_repo("docs/glossary.md")

        self.assertIn("## Minimal Example", readme)
        self.assertIn("docs/glossary.md", readme)
        for term in ("R-ID", "MECH", "QuestionDebt", "Approval Packet", "ACTIVE_CONTEXT", "CLOSURE"):
            self.assertRegex(glossary, rf"(?m)^### {re.escape(term)}$")

    def test_compatibility_and_limits_are_documented(self) -> None:
        readme = read_repo("README.md")
        required_phrases = [
            "Python 3.9+",
            "tomli",
            "Python 3.9 or 3.10",
            "Codex CLI",
            "Codex runtime",
            "reviewer agent",
            "model access",
            "fallback",
            "Tested on",
            "Known limitations",
        ]

        for phrase in required_phrases:
            self.assertIn(phrase, readme)
        self.assertNotIn("certified on all supported operating systems", readme.lower())

    def test_security_reporting_guidance_is_explicit(self) -> None:
        security = read_repo("SECURITY.md")

        self.assertIn("GitHub private vulnerability reporting", security)
        self.assertIn("do not include exploit details", security)
        self.assertIn("No project security email address is currently published", security)
        self.assertIn("No project PGP key is currently published", security)

    def test_release_trust_guidance_is_documented(self) -> None:
        readme = read_repo("README.md")

        for phrase in ("tag pinning", "dry-run", "rollback", "signed tag", "checksum"):
            self.assertIn(phrase, readme)

    def test_workflow_has_os_python_matrix_and_tomli(self) -> None:
        workflow = read_repo(".github/workflows/test.yml")

        for value in ("ubuntu-latest", "macos-latest", "windows-latest"):
            self.assertIn(value, workflow)
        for value in ('"3.9"', '"3.10"', '"3.11"', '"3.12"'):
            self.assertIn(value, workflow)
        self.assertIn("tomli", workflow)
        self.assertIn("install.py", workflow)
        self.assertIn("doctor.py", workflow)
        self.assertIn("uninstall.py", workflow)
        self.assertIn("matrix:", workflow)
        self.assertIn("os:", workflow)
        self.assertIn("python-version:", workflow)
        self.assertIn("runs-on: ${{ matrix.os }}", workflow)
        self.assertIn("actions/checkout@v6.0.2", workflow)
        self.assertIn("actions/setup-python@v6.2.0", workflow)


if __name__ == "__main__":
    unittest.main()
