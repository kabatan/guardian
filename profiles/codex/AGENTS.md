# Guardian Runtime Contract

Default Lane is for narrow routine work. Use normal engineering discipline and make only scoped claims such as `implemented` or `targeted tests pass`.

Use Guardian Lane when work is long-running, spec-heavy, security/privacy/data-sensitive, public-API/persistence/algorithmic, source-fidelity-sensitive, or when a strong readiness/verified/complete claim is needed.

## Guardian Lane

1. Convert Original Source into an Approved Base Spec before implementation.
2. Classify source units: EXACT, ADAPTED, PARTIAL, OUT_OF_SCOPE, REFERENCE_ONLY, QUESTION, NON_REQUIREMENT.
3. High-impact QUESTION blocks dependent work, readiness, and strong claims.
4. Plan against the Approved Base Spec with R-IDs, MECHs, blockers, acceptance, verification, allowed claims, and review checkpoints.
5. Base Spec defines correctness. Plan defines implementation. If they conflict, Plan loses.
6. Execute admitted plans under `/goal`. Inspect goal state before create/resume; do not treat `update_goal(status=complete)` as clear.
7. Resume stale work from `ACTIVE_CONTEXT.md`, current Plan task, evidence, and Base Spec. Summaries and handoffs are indexes, not authority.

MECH is required only when an R-ID depends on a core mechanism in algorithms, discovery/search, scoring/selection/filtering, verification/exactification, public APIs, data/security/privacy, persistence/migration, UI state machines, or source-defined workflows.

Execution quality: behavior-changing code requires test-first evidence unless explicitly not applicable or waived. Observe RED from a new or existing failing test, implement minimal GREEN, then verify. Bugs, test failures, build failures, and unexpected behavior require evidence-first debugging before fixes: capture the failure, inspect relevant error/log/diff, state the root-cause hypothesis, make one targeted change, and verify. Missing evidence or skipped discipline narrows the claim. Do not import a full Superpowers workflow.

Failure gates: do not guess through high-impact ambiguity, broaden scope, silently simplify or defer Must behavior, satisfy Must behavior with placeholders, patch failures before evidence, claim success without fresh verification, or let summaries/subagent reports replace source/evidence.

## Reviewers

Use `guardian_boundary_reviewer` for Base Spec admission, Approval Packet, Plan admission, MECH completion, final strong claims, source-fidelity challenges, and recovery. It must be runtime-callable; TOML existence alone is not readiness.

Use `spec_verifier` after implementation to check changed files against assigned R-IDs. Use `quality_reviewer` only after spec review passes. Reviewers never mark R-IDs VERIFIED.

Completion needs fresh evidence for the exact claim, including verification output and git state or an explicit non-git fallback.

