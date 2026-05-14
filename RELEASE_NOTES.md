# guardian v0.1.1

Follow-up public alpha release aligning the latest release with the improved `main`
distribution docs, CI matrix, and safe install guidance.

## Highlights

- Uses the canonical public repository URL `https://github.com/kabatan/guardian.git`.
- Puts installer `--dry-run` before the mutating install command.
- Adds the Guardian minimal usage example and glossary.
- Expands compatibility, model-access, release-trust, and security reporting guidance.
- Expands CI to Ubuntu, macOS, and Windows across Python 3.9, 3.10, 3.11, and 3.12.
- Updates GitHub Actions to `actions/checkout@v6.0.2` and `actions/setup-python@v6.2.0`.

## Install

```bash
git clone --branch v0.1.1 https://github.com/kabatan/guardian.git ~/.codex/guardian
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy --dry-run
python ~/.codex/guardian/scripts/install.py --agents-mode merge --install-mode copy
python ~/.codex/guardian/scripts/doctor.py
```

Run the `--dry-run` command first to preview changes before installing.
