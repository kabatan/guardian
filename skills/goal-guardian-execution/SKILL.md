---
name: goal-guardian-execution
description: Execute an Approved Base Spec under /goal with parent implementation and boundary reviews.
---

Use only after Approved Base Spec, admitted Plan, and explicit user permission to implement that current Plan exist.

Goal lifecycle:

1. Inspect existing goal before create.
2. Same plan: resume/update.
3. Different or completed old plan: ask for `/goal clear` or a new thread.
4. Never treat `update_goal(status=complete)` as clearing the slot.

Goal text references paths only: Base Spec, Plan, ACTIVE_CONTEXT, current task, forbidden claims, and stop conditions.

Loop: read ACTIVE_CONTEXT -> current Plan task -> implement only that task's allowed scope in parent -> run targeted verification -> update evidence/ACTIVE_CONTEXT -> continue until blocked, complete, interrupted, budget-limited, or boundary review is required.

Implementation loop discipline: for behavior changes, record RED -> GREEN -> verification evidence. For failures, record failure evidence, root-cause hypothesis, one targeted fix, and verification. If not applicable or waived, record the reason before claiming progress. Do not import a full Superpowers workflow.

Stop progress for unclear scope, repeated failed fixes, or review issues until clarified, re-planned, fixed, or re-reviewed.

Blocked stop protocol: when the same blocker prevents productive work, record the blocker and needed user decision/action, try only bounded recovery that could change the state, report it to the user once in plain language, then wait. If `update_goal(status=blocked)` is rejected, record that gate result and do not keep repeating the same blocked report.

Use subagents only at boundary checkpoints. Routine task completion is not VERIFIED.
