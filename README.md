# guardian

guardian is a Codex profile pack that adds spec-driven planning, guarded execution,
review agents, completion checks, and session handoff workflows to your Codex environment.

It installs Codex skills, custom agents, a Guardian section in `~/.codex/AGENTS.md`,
and required Guardian Codex config entries. It is designed to be inspectable, reversible,
and safe to test with `--dry-run` before changing your local Codex environment.

Use a tagged release for normal installation. The `main` branch may contain unreleased changes.

## What guardian installs

guardian may install or modify the following local files:

- `~/.agents/skills/*` - guardian skills
- `~/.agents/templates/guardian/*` - Guardian artifact templates
- `~/.codex/agents/*` - guardian review agents
- `~/.codex/AGENTS.md` - Guardian Lane rules and workflow contract
- `~/.codex/config.toml` - Codex feature and review-agent configuration
- `~/.codex/guardian-state.json` - install state used by uninstall and doctor
- `~/.codex/guardian-backups/*` - timestamped backups created before changes

guardian does not modify project repositories unless you explicitly ask Codex to work inside
them. The installer does not copy personal project trust settings, MCP settings, enabled
plugins, history, or local evidence.

## Install

Use a tagged release for normal installation:

```bash
git clone --branch v0.1.0 https://github.com/kabatan/codex-guardian.git ~/.codex/guardian
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy
python ~/.codex/guardian/scripts/doctor.py
```

Restart Codex after installation.

On Windows PowerShell, use:

```powershell
git clone --branch v0.1.0 https://github.com/kabatan/codex-guardian.git "$env:USERPROFILE\.codex\guardian"
python "$env:USERPROFILE\.codex\guardian\scripts\install.py" --agents-mode merge --install-mode copy
python "$env:USERPROFILE\.codex\guardian\scripts\doctor.py"
```

For most users, `merge` and `copy` are recommended:

- `--agents-mode merge` preserves existing global Codex instructions and appends a marked Guardian block.
- `--install-mode copy` keeps the installed runtime files independent from later edits in the cloned repo.

Preview the install without changing files:

```bash
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy --dry-run
```

## Safety Model

guardian writes sidecar managed markers next to installed skills, templates, and review agents.
If a same-name skill, template, or review-agent file already exists and is not guardian-managed,
the installer stops unless you pass `--force`.

When `--force` is used, guardian backs up the existing target before replacing it.
Backups are stored under:

```text
~/.codex/guardian-backups/YYYYMMDD-HHMMSS/
```

The installer records previous `features.multi_agent` and `features.goals` values in:

```text
~/.codex/guardian-state.json
```

Those recorded values can be restored during uninstall with `--restore-config`.

## Advanced Options

Use symlinks when you want updates in the cloned repo to be reflected immediately:

```bash
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode link
```

`--install-mode link` can propagate later edits, `git pull` changes, or local mistakes in the
cloned repo directly into your active Codex runtime. Use it only if you intentionally want that
live-update behavior. For most users, `--install-mode copy` is recommended.

Replace your global `AGENTS.md` only when you want guardian to fully manage it:

```bash
python ~/.codex/guardian/scripts/install.py --agents-mode replace --install-mode copy
```

`--agents-mode replace` overwrites your global Codex instructions after creating a backup.
Use it only if you want guardian to fully manage your global `AGENTS.md`.
For most users, `--agents-mode merge` is recommended.

Other install options:

```bash
python scripts/install.py --no-config
python scripts/install.py --no-agents
python scripts/install.py --no-skills
python scripts/install.py --backup-dir /path/to/backups
python scripts/install.py --version
```

## Update

If you installed from a tagged release, update by checking out a newer release and reinstalling:

```bash
cd ~/.codex/guardian
git fetch --tags
git checkout v0.1.1
python scripts/install.py --agents-mode merge --install-mode copy
python scripts/doctor.py
```

Avoid installing directly from `main` unless you want development changes.

## Uninstall And Rollback

Remove guardian-managed files and the marked Guardian `AGENTS.md` block:

```bash
python ~/.codex/guardian/scripts/uninstall.py
```

Restore recorded Codex feature flag values while uninstalling:

```bash
python ~/.codex/guardian/scripts/uninstall.py --restore-config
```

Preview uninstall without changing files:

```bash
python ~/.codex/guardian/scripts/uninstall.py --dry-run
```

The uninstaller removes only sidecar-marker-managed skills, templates, and review agents.
Unmarked same-name files are preserved. Backups are kept.

To manually roll back, restore `AGENTS.md`, `config.toml`, or replaced skill/agent paths from
the latest backup directory under `~/.codex/guardian-backups/`.

## Doctor

Run doctor after install or update:

```bash
python ~/.codex/guardian/scripts/doctor.py
```

Doctor checks installed skills, templates, review agents, managed markers, broken symlinks,
the marked Guardian `AGENTS.md` block, `config.toml`, install state, version, and backup
directory.

## Requirements

- Codex CLI with skills support
- Python 3.9+
- Python 3.11+ uses built-in TOML parsing
- Python 3.9 or 3.10 requires `tomli` for TOML parsing
- Git

Tested on:

- macOS: TBD
- Linux: CI on Ubuntu with Python 3.11
- Windows / WSL: local script and unit-test development on Windows

Reviewer agent registration depends on the Codex runtime. If a current session does not expose
newly installed custom agents, restart Codex and run `doctor.py` again.

## Guardian Lane

Use Guardian Lane for long-running, spec-heavy, review-sensitive, data/security-sensitive,
public API, persistence, algorithmic, source-fidelity-sensitive, or strong readiness,
verified, or complete claims.

The core flow is:

1. Convert Original Source into an Approved Base Spec.
2. Plan against R-IDs, MECHs, blockers, acceptance, verification, allowed claims, and review checkpoints.
3. Execute admitted plans with fresh evidence.
4. Use reviewers at boundary checkpoints.
5. Make only claims supported by exact evidence.

Default Lane remains available for narrow routine work with scoped claims.

## Disclaimer

guardian is an independent project and is not affiliated with OpenAI.
It changes local Codex configuration files, so review the installer and run `--dry-run`
before installing if you are unsure.
