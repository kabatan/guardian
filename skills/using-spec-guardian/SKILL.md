---
name: using-spec-guardian
description: Route non-Micro, spec-sensitive, review-sensitive, or evidence-sensitive work into Guardian Lane.
---

Use Default Lane for narrow routine work with scoped claims.

Use Guardian Lane when work is long-running, multi-step, source/spec-sensitive, security/privacy/data-sensitive, public-API/persistence/algorithmic, recovery-heavy, or needs a strong readiness/verified/complete claim.

Guardian Lane order:

1. Convert source or intent with `base-spec-gate`.
2. Plan with `plan-contract`.
3. Execute admitted plans with `goal-guardian-execution`.
4. Use `closure-recovery` before readiness, verified, complete, source-faithful, or recovery claims.

Use `guardian_boundary_reviewer` for Base Spec admission, Approval Packet, Plan admission, MECH completion, final strong claims, source-fidelity challenges, and recovery. Use `spec_verifier` and `quality_reviewer` only at their implementation review checkpoints.

After Base Spec approval, do not reinterpret Original Source except for conversion review, source-fidelity challenge, discovered gap, contradiction, or exact source-dependent claim.

