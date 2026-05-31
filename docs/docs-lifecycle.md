# Guardian Docs Lifecycle

This file is policy reference, not per-task authority. Active Base Spec R-IDs and
approved exception records remain authority.

## Frontmatter

New Guardian-created Markdown should use:

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

Do not use `safe_delete_default`.

## Delete Policy

- `never`: default for user, mixed, copied, external, normative, history, and evidence docs. Deletion requires explicit user authorization.
- `archive_preferred`: generated but potentially useful historical/provenance docs. Archive before deletion unless the user explicitly asks deletion.
- `generated_temp_only`: temporary Guardian-generated scratch artifacts. Delete only when in current task scope and unreferenced by active artifacts.

## Lifecycle

- Active docs must be few and current.
- Closed or superseded docs move out of read-first paths.
- Archive docs are cold context, not hot context.
- `ACTIVE_CONTEXT.md` contains pointers and current decisions, not copied requirements.
- Keep `ACTIVE_CONTEXT.md` at <=60 logical lines target, 80 line hard max, and <=4,000 chars.
- Full Base Spec duplication in `ACTIVE_CONTEXT.md` is not allowed.

## Docs Lint Rollout

- P0/P1: warn-only for existing docs, strict only for changed Guardian-generated docs.
- P2+: baseline mode for existing docs; strict profile may fail lifecycle violations.

## Read Rule

Read active authority first, then the current Plan task, then indexes/evidence as needed.
Do not read broad history unless a boundary review, recovery, source-fidelity question,
or contradiction requires it.
