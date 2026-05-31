# Guardian Artifact Templates

Detailed templates live here so agent-read instructions can stay compact.

Use the focused companion templates in this directory when a task needs them:

- `implementation-permission.md`
- `readset.md`
- `evidence-lite.md`
- `evidence-full.jsonl.example`
- `claim-matrix.md`
- `read-ledger.md`
- `docs-frontmatter.md`
- `source-safety-classification.md`
- `verification-oracle.md`
- `plan-change-cleanup.md`
- `deletion-safety-checklist.md`
- `research-protocol.md`

## Base Spec

Required sections: Context Packet, purpose, source scope, requirements, approved exceptions, adaptations, exclusions, QuestionDebt, MECHs, acceptance, verification, forbidden simplifications, approval status.

Each requirement needs an R-ID, status, acceptance, and verification.

Hierarchy:

- Repo Base Spec: repo-wide invariants, security/privacy posture, architecture rules, verification defaults.
- Area Base Spec: subsystem/domain requirements. Must include `Parent: <Repo Base Spec path>`.
- Change Base Spec: exact change requirements. Must include `Parent: <Area or Repo Base Spec path>`.

Maximum Base Spec layers are Repo -> Area -> Change. Plan is not a Base Spec layer.

Area Base Specs are optional. Do not create them mechanically for every folder.

Authority:

- Active Base Spec R-IDs and approved exception records are authority.
- `SPEC_REGISTRY.md`, Context Packets, `CHANGELOG.md`, `DECISIONS.md`, handoffs, retrieval results, and summaries are not authority.
- If a non-authority artifact conflicts with the Base Spec body, the Base Spec body wins.

Links:

- Standard links: `Parent`, `Supersedes`.
- `References` is optional and non-authoritative.
- Do not use `Excepts` or `Promotes` as graph edges.
- `Supersedes` records lineage only; new R-IDs must state current normative content.

Change Base Specs:

- Declare `Required Parent R-IDs` during admission when parent specs apply.
- Do not copy parent requirement text as normative child text.
- If Required Parent R-IDs are missing, suspicious, or stale after scope changes, stop and update the Base Spec before dependent implementation or claims.

Repo/Area cleanup:

- Bodies contain current truth only.
- R-IDs are never reused.
- Allowed edit types: ADD, UPDATE, REMOVE, SUPERSEDE.
- Move history, rationale, and tombstones to `CHANGELOG.md` or `DECISIONS.md`; do not keep long old versions in active bodies.

Before creating a Change Base Spec, check `SPEC_REGISTRY.md` for an active related spec. Prefer amendment over duplicate.

Context Packet template:

```md
## Context Packet

Spec ID:
Type:
Status:
Parent:
Scope:
Applies To:
Required Parent R-IDs:
Blocking Questions:
Non-blocking Debt:
Known Exceptions:
Read-First R-IDs:
Last Reviewed:
Read full file only when:
Context Packet Authority: non-authoritative digest.
```

Do not include `Children` in Context Packets. Use registry or search for child lookup.

## Source Map

Columns: source anchor, unit summary, classification, Base Spec target, decision, notes.

Classifications: EXACT, ADAPTED, PARTIAL, OUT_OF_SCOPE, REFERENCE_ONLY, QUESTION, NON_REQUIREMENT.

If `source_map.md` is absent and source fidelity matters, include source location or excerpt in the Change Base Spec. Without `source_map.md` or equivalent source anchors, do not make source-fidelity claims.

## Approval Packet

Show QUESTION, ADAPTED, PARTIAL, OUT_OF_SCOPE, high-risk EXACT, MECH-required items, objections, conversion risks, and explicit decisions.

## Plan

Each task needs type, closes/supports, R-IDs, MECHs, blockers, acceptance, verification, TDD/debug evidence or exception, review checkpoint, and allowed claim.

Task types: routine, MECH, milestone, boundary, support-only.

## Active Context

Keep it short. Include current task, read-first paths, open QuestionDebt, required MECHs, next action, and resume/read precedence.

Normative authority remains only active Base Spec R-IDs and approved exception records. Active Context is a resume index and must not define a broader normative hierarchy.

Include a Context Packet:

- Spec ID, Parent, status
- current R-IDs and task
- open QuestionDebt
- required MECHs
- read-first paths
- forbidden claims

Context tiers:

- Hot: ACTIVE_CONTEXT, current Plan task, current evidence, open blockers.
- Warm: relevant Base Spec slices, source_map slices, REPO_MAP, recent review results.
- Cold: full specs, full logs, old chats, broad docs.

Long logs:

- Store long command output as evidence files.
- Put only exact relevant slices in ACTIVE_CONTEXT or Closure.
- Never use summaries to override Base Spec, Plan, or evidence.

Read-set rule:

- For Change work, read the current Change R-ID and declared Required Parent R-IDs.
- Do not infer parent relevance from memory.
- Read full ancestor specs only for admission, parent conflict, exception, source-fidelity challenge, repo-wide claim, missing/suspect Required Parent R-IDs, or suspected drift.

## Closure

Record exact claim, R-ID evidence, execution-discipline evidence, verification output, git/non-git state, review results, and residual risk.

## AI-Created Markdown

Every new Guardian markdown artifact must declare frontmatter equivalent to `docs-frontmatter.md`:

- `guardian_doc: true`
- `status`
- `authority`
- `owner`
- `origin`
- `delete_policy`

Use `delete_policy`, not `safe_delete_default`.

Active indexes should point to current docs. Closed or stale docs should be marked non-authority, archived under the relevant change, or left only as evidence/history.

Default Lane creates no Guardian artifacts by default. Guardian Lane uses minimum artifacts plus conditional add-ons. Strong claims require fresh full-output-backed evidence, claim ceilings, and required review.
