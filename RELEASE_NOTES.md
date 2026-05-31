# guardian v0.3.0

Public alpha release that publishes the tightened Guardian runtime kernel and supporting artifact templates.

## Highlights

- Tightens Default Lane behavior so routine work avoids Guardian artifacts and reviewers by default.
- Clarifies the hard triggers for Guardian Lane, including source-fidelity, strong claims, security/privacy/data, public API, persistence, algorithmic, UI state machine, long-running work, recovery, and repeated verification failures.
- Adds direct invocation guards to phase skills and ships `agents/openai.yaml` metadata that disables implicit invocation for phase skills.
- Expands Guardian templates for scoped implementation permission, ReadSet control, evidence capture, claim ceilings, read ledgers, source safety, verification oracles, deletion safety, plan cleanup, and research protocol support.
- Updates docs lifecycle guidance to use structured Guardian frontmatter and exact `delete_policy` semantics.

This release intentionally does not ship per-task Base Specs, Plans, evidence logs, active context indexes, local install locks, or release-work artifacts.

## Install

```bash
git clone --branch v0.3.0 https://github.com/kabatan/guardian.git ~/.codex/guardian
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy --dry-run
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy
python ~/.codex/guardian/scripts/doctor.py
```

Run the `--dry-run` command first to preview changes before installing.
