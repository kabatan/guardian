# guardian v0.2.0

Public alpha release that publishes the updated Guardian runtime contract and documentation hygiene rules.

## Highlights

- Adds an explicit user permission gate before Guardian implementation starts.
- Clarifies that blocked `/goal` execution should report the needed decision once and stop repeating the same blocked status.
- Requires plain language in user-facing reports and questions while allowing Guardian terms inside artifacts.
- Updates Guardian skills and the Codex profile with the new Base Spec / Plan permission boundary.
- Expands artifact templates with Repo -> Area -> Change Base Spec hierarchy, authority rules, cleanup rules, and AI-created markdown lifecycle requirements.
- Adds reference docs for the detailed Guardian design and docs lifecycle policy.

This release intentionally does not ship per-task Base Specs, Plans, evidence logs, or release-work artifacts.

## Install

```bash
git clone --branch v0.2.0 https://github.com/kabatan/guardian.git ~/.codex/guardian
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy --dry-run
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy
python ~/.codex/guardian/scripts/doctor.py
```

Run the `--dry-run` command first to preview changes before installing.
