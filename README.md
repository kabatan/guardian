# guardian

guardian is a Codex profile pack that adds spec-driven planning, guarded execution,
review agents, completion checks, and session handoff workflows to your Codex environment.

It installs Codex skills, custom agents, a Guardian section in `~/.codex/AGENTS.md`,
and required Guardian Codex config entries. It is designed to be inspectable, reversible,
and safe to test with `--dry-run` before changing your local Codex environment.

Use a tagged release for normal installation. The `main` branch may contain unreleased changes.
The canonical public repository URL is `https://github.com/kabatan/guardian`.

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
git clone --branch v0.1.0 https://github.com/kabatan/guardian.git ~/.codex/guardian
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy --dry-run
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy
python ~/.codex/guardian/scripts/doctor.py
```

Restart Codex after installation.

On Windows PowerShell, use:

```powershell
git clone --branch v0.1.0 https://github.com/kabatan/guardian.git "$env:USERPROFILE\.codex\guardian"
python "$env:USERPROFILE\.codex\guardian\scripts\install.py" --agents-mode merge --install-mode copy --dry-run
python "$env:USERPROFILE\.codex\guardian\scripts\install.py" --agents-mode merge --install-mode copy
python "$env:USERPROFILE\.codex\guardian\scripts\doctor.py"
```

For most users, `merge` and `copy` are recommended:

- `--agents-mode merge` preserves existing global Codex instructions and appends a marked Guardian block.
- `--install-mode copy` keeps the installed runtime files independent from later edits in the cloned repo.

Run the dry run first to preview the install without changing files:

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
git checkout <new-version>
python scripts/install.py --agents-mode merge --install-mode copy --dry-run
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
- Access to the configured reviewer model names in `agents/*.toml`, or a Codex runtime fallback
  that can run equivalent reviewer agents

Tested on:

- Linux: GitHub Actions workflow covers Ubuntu across Python 3.9, 3.10, 3.11, and 3.12 after the workflow is run.
- macOS: GitHub Actions workflow covers macOS across Python 3.9, 3.10, 3.11, and 3.12 after the workflow is run.
- Windows: GitHub Actions workflow covers Windows across Python 3.9, 3.10, 3.11, and 3.12 after the workflow is run; local script and unit-test development also happens on Windows.

Compatibility notes:

- Codex runtime support for skills and custom agents is required. TOML files alone do not prove
  reviewer agent runtime availability.
- Reviewer agent registration depends on the Codex runtime. If a current session does not expose
  newly installed custom agents, restart Codex and run `doctor.py` again.
- Reviewer model access depends on your Codex account and configured runtime. If a configured reviewer
  model is unavailable, use a Codex-supported fallback model or edit the local agent TOML files
  before reinstalling.
- Known limitations: GitHub Actions improves OS and Python coverage, but it does not certify every
  Codex runtime, model entitlement, shell, filesystem, symlink, WSL, or local permission setup.

## Minimal Example

After installing guardian, ask Codex to use Guardian Lane for work that needs a spec, review, or
strong completion claim. A minimal flow is:

1. "Use Guardian Lane for this change. First create a Base Spec from my requirements."
2. Review the Base Spec and answer any blocking questions.
3. Ask Codex to create a Plan against the approved R-IDs and review checkpoints.
4. Approve the Plan, then let Codex implement only the admitted items.
5. Run the Guardian reviewers at the required checkpoints.
6. Close with a CLOSURE report that cites fresh verification evidence.

See [docs/glossary.md](docs/glossary.md) for the Guardian terms used in this flow.

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

## Release Trust And Verification

Use tag pinning for normal installs:

```bash
git clone --branch v0.1.0 https://github.com/kabatan/guardian.git ~/.codex/guardian
```

Before installing or updating, run the installer with `--dry-run` and review the paths listed in
the output. guardian may modify only the files listed in "What guardian installs", and it records
backups under `~/.codex/guardian-backups/` for rollback.

Current releases do not publish a signed tag guarantee or checksum file. Verify the GitHub release,
tag, and commit according to your own trust requirements before installing.

## Disclaimer

guardian is an independent project and is not affiliated with OpenAI.
It changes local Codex configuration files, so review the installer and run `--dry-run`
before installing if you are unsure.
