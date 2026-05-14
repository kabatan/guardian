# guardian v0.1.0

Initial public alpha release of guardian, a Guardian-style Codex profile pack for
spec-driven planning, execution, review, and handoff.

## Highlights

- Installs Guardian Lane skills, review agents, and artifact templates.
- Recommends `--agents-mode merge --install-mode copy` for safer first-time installs.
- Adds managed markers and conflict detection so unmanaged same-name files are preserved.
- Adds centralized timestamped backups under `~/.codex/guardian-backups/`.
- Records install state in `~/.codex/guardian-state.json`.
- Adds `--dry-run`, `--force`, `--backup-dir`, `--no-config`, `--no-agents`, `--no-skills`, and `--version` to the installer.
- Adds uninstall dry runs and `--restore-config`.
- Expands `doctor.py` to check installed paths, markers, symlinks, Guardian `AGENTS.md`, config, state, version, and backups.
- Adds unit tests and a GitHub Actions workflow.

## Install

```bash
git clone --branch v0.1.0 https://github.com/kabatan/guardian.git ~/.codex/guardian
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy --dry-run
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy
python ~/.codex/guardian/scripts/doctor.py
```

Run the `--dry-run` command first to preview changes before installing.
