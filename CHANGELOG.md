# Changelog

## v0.2.0

- Adds the explicit Guardian implementation permission gate to the distributed Codex profile and skills.
- Adds blocked `/goal` stop guidance so agents report the blocker once instead of repeating the same status.
- Adds user-facing plain-language guidance.
- Updates Guardian artifact templates with Base Spec hierarchy, authority, cleanup, and docs lifecycle rules.
- Adds reference docs for the detailed Guardian design and AI-created markdown lifecycle.
- Keeps per-task Base Specs, Plans, evidence logs, and release-work artifacts out of the distribution.

## v0.1.1

- Clarifies the canonical public repository URL in install documentation.
- Puts dry-run before mutating install and update commands.
- Adds a minimal Guardian usage example and glossary.
- Expands compatibility, model-access, and release-trust notes.
- Strengthens security reporting guidance without publishing a contact address or PGP key.
- Expands CI coverage to an OS and Python version matrix.
- Updates GitHub Actions to `actions/checkout@v6.0.2` and `actions/setup-python@v6.2.0`.

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
