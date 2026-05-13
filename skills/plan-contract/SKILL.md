---
name: plan-contract
description: Check planned non-Micro work before coding against an Approved Base Spec.
---

Before implementation, verify:

1. Approved Base Spec exists.
2. Every Must R-ID maps to a deliverable task or MECH plus integration task.
3. MECH-required domains are not ordinary work.
4. Core MECHs define semantics, inputs, outputs, oracle, failure behavior, controlling path, and no blocking QuestionDebt.
5. OPEN high-impact QuestionDebt blocks dependent tasks, R-IDs, MECHs, readiness labels, and claims.
6. Support/foundation work cannot close Must R-IDs or imply readiness.
7. Each task has type, acceptance, verification, required TDD/debug evidence or not-applicable/waiver reason, forbidden shortcuts, allowed claim, and review checkpoint.

Task types: routine, MECH, milestone, boundary, support-only.

MECH completion, high-risk milestone, final claim, source-fidelity challenge, and recovery require `guardian_boundary_reviewer` when callable.

If plan no longer fits Base Spec, stop and state the smallest needed plan or Base Spec change.

