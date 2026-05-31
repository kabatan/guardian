# Guardian Doc Frontmatter

Use this frontmatter for new Guardian-created Markdown.

```yaml
---
guardian_doc: true
status: active | closed | archived | evidence | scratch
authority: normative | execution-control | evidence | navigation | history
owner: guardian | user | mixed
origin: generated | copied-from-user | edited-by-user | external
delete_policy: never | archive_preferred | generated_temp_only
---
```

`delete_policy` semantics:

- `never`: default for user, mixed, copied, external, normative, history, and evidence docs. Deletion requires explicit user authorization.
- `archive_preferred`: generated but potentially useful historical/provenance docs. Archive before deletion unless the user explicitly asks deletion.
- `generated_temp_only`: temporary Guardian-generated scratch artifacts. May be deleted only when in current task scope and not referenced by active artifacts.

Do not use `safe_delete_default`.
