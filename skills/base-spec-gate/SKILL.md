---
name: base-spec-gate
description: Use after a user-provided source/spec/research plan or high-risk intent needs conversion into Base Spec authority before implementation.
---

## Direct Invocation Guard

This phase skill is normally called by `using-spec-guardian`.

Required precondition: user-provided source/spec/research plan or high-risk intent.

If the precondition is missing:

- do not continue by guessing
- state the missing prerequisite
- route back to `using-spec-guardian`
- do not implement code
- do not create a strong claim

## Output

Produce a Base Spec draft and Approval Packet. Original Source is reference. Approved Base Spec becomes authority only after user approval.

Classify each normative source unit: EXACT, ADAPTED, PARTIAL, OUT_OF_SCOPE, REFERENCE_ONLY, QUESTION, NON_REQUIREMENT.

High-impact QUESTION blocks dependent UI/UX, algorithm, public API, data/security/privacy, persistence, scope, acceptance, verification, readiness, or source-fidelity work. Do not close QUESTION by confidence.

Base Spec must include purpose, source scope, requirements, adaptations, exclusions, QuestionDebt, Must R-IDs, MECHs, acceptance, verification, and forbidden simplifications.

Before approval, provide an Approval Packet covering QUESTION, ADAPTED, PARTIAL, OUT_OF_SCOPE, high-risk EXACT, MECH-required items, objections, conversion risks, and explicit decisions.

Base Spec approval is not implementation permission. After Plan admission, ask the user explicitly before coding or editing implementation files.

Use `guardian_boundary_reviewer` for dense, workflow-heavy, API/data/security/UI/algorithmic, or 5+ R-ID source conversion. If unavailable, record the blocker and narrow any claim.

Stop when source authority is ambiguous, high-impact QuestionDebt is open, or the user must decide a conversion choice.
