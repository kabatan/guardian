# Guardian Glossary

## Core Terms

### Guardian Lane

The workflow for spec-heavy, review-sensitive, or high-confidence Codex work. It requires an
approved source-derived spec, an admitted plan, scoped implementation, review checkpoints, and
evidence-backed closure.

### Default Lane

The normal workflow for narrow routine work. It supports scoped claims such as "implemented" or
"targeted tests pass" without the full Guardian process.

### Base Spec

The approved requirements document derived from the user's source material. After approval, it is
the authority for correctness.

### Plan Contract

The implementation plan admitted against the Base Spec. It maps tasks to requirements, mechanisms,
acceptance criteria, verification, and allowed claims.

### R-ID

Requirement ID. A stable identifier assigned to a requirement so implementation, review, and
closure can point to the same obligation.

### MECH

Mechanism. A core implementation mechanism that must be designed and reviewed when a requirement
depends on algorithmic behavior, public APIs, persistence, security/privacy, verification logic, or
similar high-impact behavior.

### QuestionDebt

Open questions or unresolved assumptions. High-impact QuestionDebt blocks dependent work and
strong completion claims until it is resolved or explicitly scoped out.

### Approval Packet

The package used for review before admitting a Base Spec or Plan. It calls out questions,
adaptations, partial source handling, exclusions, risks, and explicit decisions.

### ACTIVE_CONTEXT

The current handoff index for an active Guardian task. It points to the current task, live evidence,
open blockers, and source artifacts. It is not a replacement for the source documents.

### CLOSURE

The final evidence-backed closeout for a Guardian task. It states the exact supported claim,
verification evidence, residual limits, and git or non-git state.

### Reviewer Agent

A read-only custom agent used at Guardian checkpoints, such as boundary review, spec conformance
review, or quality review.
