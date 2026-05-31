---
name: guardian-session-handoff
description: Use for intentional session rotation, stale context, long Guardian Lane work, or explicit resume/handoff requests.
---

## Direct Invocation Guard

This phase skill is normally called by `using-spec-guardian`.

Required precondition: current Guardian task state or resume/handoff request.

If the precondition is missing:

- do not continue by guessing
- state the missing resume context
- route back to `using-spec-guardian` or request the needed context
- do not implement code
- do not create a strong claim

## Prepare

Use for intentional session rotation, stale context, or long Guardian Lane work.

1. Read ACTIVE_CONTEXT, current Plan task, CLOSURE/evidence, and git or non-git state.
2. Write SESSION_HANDOFF as a resume index, not authority.
3. Include current task, open blockers, required cold reads, evidence paths, and forbidden claims.
4. Do not resolve QuestionDebt or change acceptance in the handoff.
5. Include the exact next task, allowed claim ceiling, and any stale permission or review gate.
6. Keep copied requirement text out of the handoff; link to the Base Spec and Plan instead.

## Resume

1. Read project rules, SESSION_HANDOFF, ACTIVE_CONTEXT, Base Spec, and current Plan task.
2. Treat handoff as an index only.
3. If handoff conflicts with Base Spec, Plan, or evidence, the authoritative artifact wins.
4. Resume only the current task or claim.
5. If the handoff is stale, recover from ACTIVE_CONTEXT, Base Spec, Plan, current goal text, and latest evidence.
6. If required artifacts are missing, state the blocker and ask for the needed context rather than guessing.

Stop for changed scope, open high-impact QuestionDebt, stale permission, missing evidence, or a claim that exceeds the declared evidence ceiling.
