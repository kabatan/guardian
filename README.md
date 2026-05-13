# Codex Guardian

Codex Guardian is a compact Codex environment profile for long-running, spec-sensitive engineering work.

It keeps the useful discipline of Superpowers-style workflows while adding stricter source fidelity, Base Spec authority, reviewer checkpoints, and honest completion claims.

## What It Installs

- Guardian skills under `~/.agents/skills`
- Guardian reviewer agents under `~/.codex/agents`
- A Guardian `AGENTS.md` profile for `~/.codex/AGENTS.md`
- A small Guardian artifact template under `~/.agents/templates/guardian`
- Required `config.toml` entries for `multi_agent`, `goals`, and the reviewer agents

The installer does not copy personal project trust settings, MCP settings, enabled plugins, history, or local evidence.

## Install

Clone the repository:

```bash
git clone https://github.com/kabatan/codex-guardian.git ~/.codex/codex-guardian
```

Run the installer:

```bash
python ~/.codex/codex-guardian/scripts/install.py --agents-mode replace
python ~/.codex/codex-guardian/scripts/doctor.py
```

Restart Codex after installation.

On Windows PowerShell, the same commands work with:

```powershell
git clone https://github.com/kabatan/codex-guardian.git "$env:USERPROFILE\.codex\codex-guardian"
python "$env:USERPROFILE\.codex\codex-guardian\scripts\install.py" --agents-mode replace
python "$env:USERPROFILE\.codex\codex-guardian\scripts\doctor.py"
```

## Safer AGENTS.md Merge

If you do not want to replace `~/.codex/AGENTS.md`, use:

```bash
python ~/.codex/codex-guardian/scripts/install.py --agents-mode merge
```

`replace` backs up the existing file and installs the full Guardian profile. `merge` appends a marked Guardian block instead.

## Update

```bash
cd ~/.codex/codex-guardian
git pull
python scripts/install.py --agents-mode replace
python scripts/doctor.py
```

## Uninstall

```bash
python ~/.codex/codex-guardian/scripts/uninstall.py
```

The uninstaller removes Guardian-managed files and the marked AGENTS block. It does not delete backups.

## Guardian Lane

Use Guardian Lane for long-running, spec-heavy, review-sensitive, data/security-sensitive, public API, persistence, algorithmic, source-fidelity-sensitive, or strong readiness/verified/complete claims.

The core flow is:

1. Convert Original Source into an Approved Base Spec.
2. Plan against R-IDs, MECHs, blockers, acceptance, verification, allowed claims, and review checkpoints.
3. Execute admitted plans with fresh evidence.
4. Use reviewers at boundary checkpoints.
5. Make only claims supported by exact evidence.

Default Lane remains available for narrow routine work with scoped claims.

## Requirements

- Codex with native skill discovery
- Python 3.9+
- Git for clone/update

Reviewer agent registration depends on the Codex runtime. If a current session does not expose newly installed custom agents, restart Codex and run `doctor.py` again.

