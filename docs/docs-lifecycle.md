# Guardian Docs Lifecycle

This file is policy reference, not authority. Active Base Spec R-IDs and approved exception records remain authority.

## Classes

| Class | Examples | Authority |
|---|---|---|
| authority | Base Spec active R-IDs, approved exception records | yes |
| plan | Plan, task list | implementation only |
| index | SPEC_REGISTRY, ACTIVE_CONTEXT, SESSION_HANDOFF, REPO_MAP | no |
| evidence | logs, verification output, review packets | evidence only |
| history | CHANGELOG, DECISIONS, archived specs | no |
| reference | final design docs, guides, old discussion summaries | no |

## Required Header

New AI-created markdown must state:

```md
Purpose:
Status:
Authority:
Owner/current spec:
Read when:
```

## Lifecycle

- Keep active docs current and short.
- Do not copy old versions into active Base Spec bodies.
- Move old rationale, superseded text, and decisions to history files.
- At closure, update indexes and mark stale docs as closed, superseded, archival, or evidence.
- If a doc's authority is unclear, treat it as non-authority until an active Base Spec says otherwise.

## Read Rule

Read active authority first, then the current Plan task, then indexes/evidence as needed. Do not read broad history unless a boundary review, recovery, source-fidelity question, or contradiction requires it.
