# Contributing

Before opening a pull request:

1. Run `python -m unittest discover -s tests`.
2. Run `python scripts/doctor.py` in an installed guardian environment.
3. Test install and uninstall with a temporary home directory.
4. Run `git diff --check`.
5. Do not add workflow rules that silently weaken user safety.
6. Keep each skill focused and documented.
7. Update `CHANGELOG.md` for user-visible changes.

For unit tests:

```bash
python -m unittest discover -s tests
```

For temporary-home smoke testing on macOS or Linux:

```bash
tmp_home="$(mktemp -d)"
python scripts/install.py --codex-home "$tmp_home/.codex" --agents-home "$tmp_home/.agents" --agents-mode merge --install-mode copy
python scripts/doctor.py --codex-home "$tmp_home/.codex" --agents-home "$tmp_home/.agents"
python scripts/uninstall.py --codex-home "$tmp_home/.codex" --agents-home "$tmp_home/.agents" --restore-config
```

For Windows PowerShell:

```powershell
$tmpHome = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
python scripts/install.py --codex-home "$tmpHome\.codex" --agents-home "$tmpHome\.agents" --agents-mode merge --install-mode copy
python scripts/doctor.py --codex-home "$tmpHome\.codex" --agents-home "$tmpHome\.agents"
python scripts/uninstall.py --codex-home "$tmpHome\.codex" --agents-home "$tmpHome\.agents" --restore-config
```

Use explicit `--codex-home` and `--agents-home` paths pointing at disposable directories
instead of your real Codex environment.

Do not commit local Codex history, evidence, trust settings, or personal configuration.
