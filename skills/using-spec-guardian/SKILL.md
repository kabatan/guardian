---
name: using-spec-guardian
description: Use when work may require source/spec fidelity, strong claims, long execution, boundary review, recovery, or high risk.
---

Default Lane is narrow routine work: no Guardian artifacts or reviewers by default, scoped claims only.

Use Guardian Lane only for hard triggers:

- normative source/spec/research plan requiring faithful execution
- strong claim target: READY, VERIFIED, ACCEPTANCE_COMPLETE, SOURCE_FAITHFUL, PRODUCTION_SAFE
- security/privacy/data, public API, persistence/migration, core algorithm/search/scoring/filtering/ranking, UI state machine
- long/cross-session work, prior drift, repeated verification failure, unclear evidence, recovery

Guardian Lane order:

1. Convert source or intent with `base-spec-gate`.
2. Plan with `plan-contract`.
3. Ask for permission to implement the current Base Spec and Plan.
4. Execute admitted and explicitly approved plans with `goal-guardian-execution`.
5. Use `closure-recovery` before readiness, verified, complete, source-faithful, or recovery claims.

Use `guardian_boundary_reviewer` for Base Spec admission, Plan admission, MECH completion, final strong claims, source-fidelity challenges, and recovery. Use `spec_verifier` and `quality_reviewer` only at checkpoints.

After Base Spec approval, do not reinterpret Original Source except for conversion review, source-fidelity challenge, discovered gap, contradiction, or exact source-dependent claim. Use plain language in user-facing updates.
