---
name: closure-recovery
description: Use when a current task, claim under review, evidence target, stale state, source-fidelity challenge, or recovery path must be checked before a strong claim.
---

## Direct Invocation Guard

This phase skill is normally called by `using-spec-guardian`.

Required precondition: current task, claim under review, evidence target, or recovery/resume state.

If the precondition is missing:

- do not continue by guessing
- state the missing artifact or claim target
- route back to `using-spec-guardian` or the prior required phase
- do not implement code
- do not create a strong claim

## Claim Gate

Before readiness, complete, verified, or source-faithful claims, check:

- Approved Base Spec and admitted Plan
- source_map when source fidelity matters
- OPEN QuestionDebt
- support-vs-deliverable status
- MECH-vs-parent R-ID closure
- fresh behavior evidence and verification output
- required TDD/debug evidence or a recorded not-applicable/waiver reason
- required reviews
- git state or explicit non-git fallback

Missing execution-discipline evidence blocks strong claims and narrows routine fixed, passing, or complete claims.

Subagent reports and summaries are evidence inputs only; inspect source and exact evidence before claims.

Use `guardian_boundary_reviewer` for source conversion, Plan admission, MECH completion, final claims, source-fidelity challenge, and recovery. If unavailable, state the narrower supported claim.

Recovery: stop broad coding, read ACTIVE_CONTEXT, Base Spec, Plan/current task, current goal text, last evidence, and boundary blockers. Resume only the current task or claim.

If recovery cannot progress without user input or an external change, report the needed decision/action once in plain language and wait. A goal-gate refusal to mark blocked is not permission to repeat the same report or claim completion.
