# Guardian Project Artifacts

Use these for Guardian Lane work. Keep active files short and link to detail.

## SPEC_REGISTRY.md

Track existing Repo, Area, and Change Base Specs. Check before creating a new Change Base Spec.

Columns: ID, Scope, Parent, Status, Path, Updated, Notes.

Path patterns:

- Repo Base Spec: `docs/ai/base-specs/repo/<id>.md`
- Area Base Spec: `docs/ai/base-specs/areas/<area>/<id>.md`
- Change Base Spec: `docs/ai/changes/<spec-id>/BASE_SPEC.md`

Children include `Parent: <path>`.

## source_map.md

Map source units to Base Spec R-IDs. Classify units as EXACT, ADAPTED, PARTIAL, OUT_OF_SCOPE, REFERENCE_ONLY, QUESTION, or NON_REQUIREMENT.

## BASE_SPEC.md

Defines correctness: purpose, source scope, R-IDs, QuestionDebt, MECHs, acceptance, verification, forbidden simplifications, approval status.

## PLAN.md

Defines implementation: task type, R-IDs, MECHs, blockers, acceptance, verification, TDD/debug evidence or exception, allowed claim, review checkpoint.

## ACTIVE_CONTEXT.md

Small resume entry point. It is not authority.

Include Context Packet, Hot/Warm/Cold context pointers, current R-IDs, current task, open blockers, required MECHs, and forbidden claims.

Long logs go in evidence files. Active context links exact slices only.

## SESSION_HANDOFF.md

Transient resume index for session rotation. It cannot override Base Spec, Plan, or evidence.

## CLOSURE.md

Exact claim, execution-discipline evidence, verification output, git/non-git state, reviews, and residual risk.

