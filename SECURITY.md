# Security Policy

## Reporting a vulnerability

If you find a security issue in guardian, please report it privately before public disclosure.
Use GitHub private vulnerability reporting if it is enabled for the repository.

If a private channel is not available, open a minimal public issue asking for a secure
contact path and do not include exploit details in the issue.

## Scope

Security-sensitive areas include:

- installer behavior
- uninstall behavior
- modification of `~/.codex/AGENTS.md`
- modification of `~/.codex/config.toml`
- symlink and junction handling
- path traversal or unintended file deletion
- backup and rollback behavior

## Supported versions

guardian is currently in public alpha. Security fixes are expected to target the latest
published release and the `main` branch.
