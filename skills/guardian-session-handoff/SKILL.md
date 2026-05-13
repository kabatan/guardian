---
name: guardian-session-handoff
description: Prepare or resume Guardian session handoff while preserving authority and context efficiency.
---

Use for intentional session rotation, stale context, or long Guardian Lane work.

Prepare:

1. Read ACTIVE_CONTEXT, current Plan task, CLOSURE/evidence, and git or non-git state.
2. Write SESSION_HANDOFF as a resume index, not authority.
3. Include current task, open blockers, required cold reads, evidence paths, and forbidden claims.
4. Do not resolve QuestionDebt or change acceptance in the handoff.

Resume:

1. Read project rules, SESSION_HANDOFF, ACTIVE_CONTEXT, Base Spec, and current Plan task.
2. Treat handoff as an index only.
3. If handoff conflicts with Base Spec, Plan, or evidence, the authoritative artifact wins.
4. Resume only the current task or claim.

