---
name: base-spec-gate
description: Convert Original Source and user intent into an Approved Base Spec before Guardian implementation.
---

Original Source is reference. Approved Base Spec is authority after approval.

Classify each normative source unit: EXACT, ADAPTED, PARTIAL, OUT_OF_SCOPE, REFERENCE_ONLY, QUESTION, NON_REQUIREMENT.

High-impact QUESTION blocks dependent UI/UX, algorithm, public API, data/security/privacy, persistence, scope, acceptance, verification, readiness, or source-fidelity work. Do not close QUESTION by confidence.

Base Spec must include purpose, source scope, requirements, adaptations, exclusions, QuestionDebt, Must R-IDs, MECHs, acceptance, verification, and forbidden simplifications.

Before approval, provide an Approval Packet covering QUESTION, ADAPTED, PARTIAL, OUT_OF_SCOPE, high-risk EXACT, MECH-required items, objections, conversion risks, and explicit decisions.

Use `guardian_boundary_reviewer` for dense, workflow-heavy, API/data/security/UI/algorithmic, or 5+ R-ID source conversion. If unavailable, record the blocker and narrow any claim.

