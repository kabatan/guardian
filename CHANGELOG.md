# Changelog

## v0.1.0

Initial public alpha release of guardian.

- Adds Guardian Lane skills.
- Adds read-only review agents.
- Adds Guardian artifact templates.
- Adds installer, doctor, and uninstall scripts.
- Uses `merge` and `copy` as the recommended install path.
- Supports `merge`, `replace`, and `skip` AGENTS modes.
- Supports `copy` and `link` install modes.
- Adds `--dry-run`, `--force`, `--backup-dir`, `--no-config`, `--no-agents`, `--no-skills`, and `--version` to the installer.
- Adds managed markers and unmanaged conflict detection for installed skills, templates, and review agents.
- Stores timestamped backups under `~/.codex/guardian-backups/`.
- Stores install state under `~/.codex/guardian-state.json`.
- Supports uninstall dry runs and config restoration with `--restore-config`.
- Expands doctor checks for markers, broken symlinks, config, install state, version, and backup directory.
- Adds unit tests and GitHub Actions smoke testing.
- Adds public distribution docs for security, contributing, update, uninstall, and rollback.
