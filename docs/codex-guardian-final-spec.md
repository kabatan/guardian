# Codex Guardian Final Specification

Date: 2026-05-13
Status: Reference design

This document is the consolidated specification for the custom Codex Guardian environment.

It is self-contained. A reader does not need access to the local `.codex`, `.agents`, or previous design files to understand the target environment.

## 1. Purpose

Codex Guardian exists to solve a specific failure mode in long-running agentic software development:

> An agent starts from an agreed spec, but gradually drifts from it while executing a large task.

The environment was inspired by Superpowers-style workflows. Superpowers is strong at planning, TDD, debugging discipline, subagent review, and execution momentum. Guardian keeps those strengths where useful, but adds stricter source fidelity, Base Spec authority, evidence binding, and closure gates for high-risk or long-running work.

The goal is not maximum simplicity. The goal is:

> Use the smallest structure that still preserves the required performance: spec fidelity, controlled execution, context efficiency, and honest completion claims.

## 2. Non-Goals

Guardian must not become a maximal process framework.

It should not:

- force full Base Specs for ordinary small work,
- create many workflow modes,
- require MECH for incidental file touches,
- require semantic review for every routine change,
- treat summaries or retrieval snippets as authority,
- hide unsafe runtime configuration behind spec discipline,
- rely on old chat history as the source of truth.

## 3. Core Architecture

The final environment has:

```text
Two execution lanes
Hierarchical Base Specs
Strict Base Spec vs Plan separation
Claim vocabulary
Evidence bound to repository state
Context-efficient artifacts
Session handoff support
Semantic boundary review
Safe default runtime posture
```

There are only two execution lanes:

```text
Default Lane
Guardian Lane
```

No additional modes such as Micro, Small, Medium, Large, Strict, Relaxed, or Research should be added. Those distinctions may inform judgment, but they are not workflow modes.

## 4. Execution Lanes

### 4.1 Default Lane

Default Lane is for ordinary work.

Use Default Lane when the task is narrow, local, and does not require strong spec-fidelity claims.

Default Lane may use a lightweight Task Contract:

```md
Task Contract
- Goal:
- Scope:
- Parent specs, if any:
- Verification:
- Stop if:
```

Default Lane still requires normal engineering discipline:

- read relevant code before changing it,
- follow local repo patterns,
- use targeted verification,
- use systematic debugging for failures,
- use TDD when behavior changes and it is practical,
- avoid broad claims not supported by evidence.

Default Lane does not need:

- full Base Spec,
- source classification,
- MECH unless escalation occurs,
- Approval Packet,
- semantic boundary review,
- full Closure ledger.

### 4.2 Guardian Lane

Guardian Lane is for high-risk, long-running, source-sensitive, or evidence-sensitive work.

Guardian Lane uses:

- hierarchical Base Specs,
- admitted Plans,
- `/goal` execution after admission,
- evidence closure,
- semantic boundary review where required.

Guardian Lane is required when a strong claim must be made, or when spec drift risk is material.

## 5. Guardian Promotion Triggers

Promote work from Default Lane to Guardian Lane when any of the following are true:

- The user provides a detailed normative spec or source document.
- The work is long-running or likely to span multiple sessions.
- The work touches public API behavior or compatibility.
- The work touches persistence, migration, retention, or data compatibility.
- The work touches security, privacy, credentials, permissions, or sensitive data.
- The work changes a core algorithm, scoring, search, filtering, selection, exactification, or verification path.
- The work changes UI state machines or source-defined workflows.
- The task has high-impact ambiguity in scope, acceptance, verification, readiness, or source fidelity.
- The final answer must claim a strong completion state.
- The change modifies, closes, supersedes, conflicts with, or makes a strong claim against an existing Base Spec.
- A previous Default Lane attempt drifted, repeatedly failed verification, or produced unclear evidence.

Do not promote merely because:

- the task is a routine bug fix with narrow scope,
- the task is a small refactor that does not alter behavior,
- the task is formatting or lint cleanup,
- the task is a small documentation edit,
- the final answer says routine "implemented" or "targeted tests pass",
- the user asks for a plan but has not authorized implementation.

## 5.1 Implementation Permission Gate

After a Guardian Base Spec and Plan are drafted or reviewed, implementation must not start until the user explicitly approves implementation of the current Base Spec and Plan.

The following do not count as implementation permission:

- the user's original broad request,
- a request to draft or review a Base Spec or Plan,
- reviewer PASS,
- the agent's confidence that the Plan is correct,
- silence after the Plan is shown.

If permission is missing or ambiguous, ask in plain language and wait.

## 5.2 User-Facing Language

Use plain, common language in progress updates, questions, and final answers.

Specialized Guardian terms may appear in Base Spec, Plan, evidence, and reviews. When talking to the user, either avoid internal shorthand or explain it briefly.

## 6. Claim Vocabulary

Claims must be precise because closure rules depend on claim strength.

### 6.1 Routine Claims

Routine claims are allowed in Default Lane when supported by scoped local evidence.

```text
IMPLEMENTED
TARGETED_TESTS_PASS
BUILD_PASS_FOR_TOUCHED_AREA
DOC_UPDATED
PATCH_PROVIDED
```

These claims mean only what they say. They do not imply production readiness, full source fidelity, migration completion, or all acceptance coverage.

### 6.2 Strong Claims

Strong claims require Guardian Lane closure unless explicitly scoped down.

```text
READY
VERIFIED
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
MIGRATION_COMPLETE
SECURITY_RELEVANT_COMPLETE
PUBLIC_API_COMPATIBLE
```

Strong claims require:

- an applicable Base Spec or acceptance contract,
- fresh evidence,
- evidence bound to git or repository state,
- required semantic review when applicable,
- no blocking QuestionDebt for the claimed scope.

### 6.3 Partial Claims

Use partial claims when evidence is incomplete:

```text
PARTIALLY_IMPLEMENTED
LOCAL_VERIFICATION_ONLY
BLOCKED_BY_QUESTION
BLOCKED_BY_ENVIRONMENT
NEEDS_USER_DECISION
NEEDS_BROADER_TESTING
```

A partial claim is better than an inflated completion claim.

## 7. Base Spec Hierarchy

Base Specs are a small layered authority model, not an open workflow graph.

The maximum Base Spec hierarchy is:

```text
Repo Base Spec
  -> Area Base Spec
      -> Change Base Spec
```

`Plan` is not a Base Spec layer. It is the implementation plan for an admitted Change Base Spec.

Area Base Specs are optional. Small repos, one-off tasks, and routine Default Lane work may use only a Repo Base Spec, a Change Base Spec, or no Base Spec when Guardian Lane is not triggered.

Recommended structure:

```text
docs/ai/
  SPEC_REGISTRY.md
  ACTIVE_CONTEXT.md
  REPO_MAP.md
  base-specs/
    repo/
      REPO-BASE-SPEC.md
      CHANGELOG.md
      DECISIONS.md
    areas/
      <area>/
        AREA-BASE-SPEC.md
        CHANGELOG.md
        DECISIONS.md
  changes/
    <spec-id>/
      BASE_SPEC.md
      PLAN.md
      CLOSURE.md
      source_map.md
      SESSION_HANDOFF.md
      evidence/
      reviews/
```

### 7.1 Authority Model

Only these records are normative authority:

- active Base Spec R-IDs in the Base Spec body,
- approved exception records that explicitly name the parent R-ID they modify.

These artifacts are indexes, history, or navigation only:

- `SPEC_REGISTRY.md`,
- Context Packets,
- `CHANGELOG.md`,
- `DECISIONS.md`,
- `SESSION_HANDOFF.md`,
- summaries, retrieval results, and handoff notes.

If an index, packet, changelog, decision note, handoff, summary, or retrieval result conflicts with the active Base Spec body, the active Base Spec body wins. Approved exception records apply only to their stated scope and do not silently weaken parent requirements elsewhere.

### 7.2 Link Model

Standard links are limited to:

```text
Parent
Supersedes
```

`Parent` is the single normative inheritance link. A child spec cannot weaken parent `MUST` requirements unless an approved exception record exists.

`Supersedes` records lineage only. It does not inherit old requirement text. The new R-ID or spec must restate the current normative content.

`References` may point to related material, but references are not authority.

Do not introduce standard `Excepts` or `Promotes` graph edges:

- Parent exceptions belong in an `Approved Exceptions` section with an `EX-ID`, target R-ID, reason, scope, expiry or review condition, approval source, and verification or claim impact.
- Promotion from Change to Area or Repo is a closure recommendation followed by a separately admitted Area or Repo Base Spec edit.

### 7.3 Repo Base Spec

`docs/ai/base-specs/repo/REPO-BASE-SPEC.md` defines repo-wide constraints.

It should include:

- repo-wide invariants,
- global security/privacy constraints,
- public API compatibility rules,
- global verification expectations,
- forbidden simplifications,
- known repo-wide debt that new work must not worsen.

It should not include:

- detailed implementation plans,
- file-by-file design,
- every desired future refactor,
- broad ideal-state prose that blocks normal work.

Repo-level requirements may use:

```text
MUST
TARGET
KNOWN_DEBT
```

Meanings:

- `MUST`: applies now. New work cannot violate it.
- `TARGET`: desired direction. Work should move toward it when touching the area, but the whole repo is not blocked by existing noncompliance.
- `KNOWN_DEBT`: known limitation or current violation. New work must not worsen it unless explicitly approved.

### 7.4 Area Base Spec

Area Base Specs define stable requirements for a subsystem or domain.

Examples:

- settings behavior,
- auth/session behavior,
- CSV export behavior,
- geometry solver core behavior,
- UI editor behavior.

Area Base Specs inherit from the Repo Base Spec through `Parent`. They may add constraints but may not weaken parent constraints.

Do not create Area Base Specs mechanically for every folder. Create one only when a domain has stable behavior that appears across multiple changes or repeatedly needs the same parent constraints.

### 7.5 Change Base Spec

Change Base Specs define the exact requirement for a specific change or feature.

Create a Change Base Spec when:

- the task is Guardian Lane work,
- the change has persistent product meaning,
- the work may span sessions,
- the change modifies an existing Area or Repo Base Spec,
- exact source fidelity matters.

Do not create a Change Base Spec for routine work that can be handled safely by a Task Contract.

Each Change Base Spec must declare `Required Parent R-IDs` during admission when parent specs apply. The agent must not guess which parent R-IDs are relevant during implementation.

If `Required Parent R-IDs` are missing, suspicious, or no longer match the implementation scope, stop dependent implementation or claims and update the Change Base Spec before continuing.

Do not copy parent requirement text into the Change Base Spec as normative content. Reference the parent R-ID instead.

### 7.6 R-ID Lifecycle and Cleanup

R-IDs are never reused.

Repo and Area Base Spec bodies should contain current truth only. They are not append-only history files.

Allowed edit types:

```text
ADD
UPDATE
REMOVE
SUPERSEDE
```

For `REMOVE` or `SUPERSEDE`, keep only the active current text in the Base Spec body. Put compact history, rationale, and tombstones in `CHANGELOG.md` or `DECISIONS.md`.

Before editing Repo or Area Base Specs, check for:

- old versions left in active requirement bodies,
- duplicate requirements across Repo, Area, and Change layers,
- parent-child conflicts,
- R-ID reuse,
- stale Context Packets,
- needed approved exception records.

Layer ownership rules:

- Repo: repo-wide invariants and global constraints.
- Area: concrete stable behavior for a domain.
- Change: exact requirement delta for the current work.

If the same requirement appears in multiple layers, keep the normative text at the owner layer and replace lower-layer copies with parent R-ID references.

### 7.7 Amendments Instead of Duplicates

Before creating a new Change Base Spec:

1. Read `SPEC_REGISTRY.md`.
2. Search for active specs with the same scope.
3. Search for closed specs that the new work corrects, extends, or supersedes.
4. Reuse, amend, or supersede when appropriate.

Do not create parallel active specs for the same scope unless explicitly justified.

## 8. Base Spec vs Plan

This distinction is mandatory.

### 8.1 Base Spec

The Base Spec defines what correctness means.

It may include:

- purpose,
- scope and out of scope,
- parent spec constraints,
- source scope,
- source unit classification,
- R-IDs,
- acceptance criteria,
- verification requirements,
- QuestionDebt,
- MECH definitions when required,
- forbidden simplifications,
- explicit adaptations and exclusions,
- allowed claims.

It should avoid:

- file paths unless required for acceptance,
- implementation order,
- low-level task steps,
- test command details unless part of acceptance,
- speculative implementation choices.

### 8.2 Plan

The Plan defines how to implement the Base Spec.

It may include:

- tasks,
- file paths,
- implementation order,
- test commands,
- review checkpoints,
- which R-IDs each task supports or closes,
- allowed claim after each task,
- blockers,
- rollback or migration steps.

It must not:

- add new requirements,
- change acceptance,
- weaken parent specs,
- silently reinterpret source,
- mark support or foundation tasks as closing Must R-IDs,
- upgrade final claims beyond the evidence available.

### 8.3 Boundary Rule

If Plan and Base Spec conflict, the Plan loses.

The agent must stop and do one of:

- amend the Base Spec and get required approval,
- record an approved exception with an `EX-ID`, target parent R-ID, scope, review condition, approval source, and verification or claim impact,
- adjust the Plan to match the Base Spec.

## 9. Source Classification

When converting Original Source into a Base Spec, classify each normative source unit:

```text
EXACT
ADAPTED
PARTIAL
OUT_OF_SCOPE
REFERENCE_ONLY
QUESTION
NON_REQUIREMENT
```

Meanings:

- `EXACT`: implemented or preserved exactly as stated.
- `ADAPTED`: intentionally changed to fit repo/runtime constraints; requires rationale.
- `PARTIAL`: only part of the source unit is in scope or feasible.
- `OUT_OF_SCOPE`: explicitly excluded from the current change.
- `REFERENCE_ONLY`: informative context, not a requirement.
- `QUESTION`: ambiguous or unresolved; may block dependent work.
- `NON_REQUIREMENT`: not normative for implementation.

High-impact `QUESTION` items block dependent work. They cannot be resolved by agent confidence.

High-impact areas include:

- UI/UX behavior,
- algorithm semantics,
- public API behavior,
- data/security/privacy,
- persistence,
- scope,
- acceptance,
- verification validity,
- readiness,
- source fidelity.

If `source_map.md` is absent in a Guardian environment, the Change Base Spec must carry the needed source location or excerpt for any source-fidelity-dependent R-ID. Without `source_map.md` or an equivalent source anchor in the Change Base Spec, the agent must not make `SOURCE_FAITHFUL` or equivalent source-fidelity claims.

## 10. QuestionDebt

QuestionDebt is an explicit unresolved decision record.

Template:

```md
Q-ID:
Source anchor:
Question:
Impact:
Blocks R-IDs:
Allowed interim work:
Decision needed from:
Status: OPEN | DECIDED | DEFERRED | OUT_OF_SCOPE
Decision:
```

Rules:

- High-impact QuestionDebt blocks dependent R-IDs.
- Low-impact QuestionDebt may be deferred if the final claim is scoped accordingly.
- The agent may propose options, but it must not silently choose for the user when the decision affects high-impact behavior.
- A reviewer cannot close QuestionDebt without an explicit decision source.

## 11. MECH Requirements

MECH entries are required for core R-ID mechanisms unless explicitly excluded by the Base Spec.

This is narrower than requiring MECH for every touch in a broad domain.

MECH is required when an R-ID's correctness depends on a core mechanism in these domains:

- algorithms,
- search/discovery,
- scoring,
- selection,
- filtering,
- verification paths,
- exactification paths,
- public APIs,
- data/security/privacy,
- persistence/migration,
- UI state machines,
- source-defined workflows.

MECH is not required merely because the change incidentally touches:

- a file that also contains an algorithm,
- styling around a UI workflow,
- a test fixture,
- documentation,
- a type or constant unrelated to the R-ID closure mechanism,
- a small local bug whose behavior is fully captured by ordinary tests.

MECH template:

```md
MECH-ID:
Supports R-IDs:
Domain:
Required: yes | no | excluded-by-spec
Reason required or excluded:
Semantics:
Inputs:
Outputs:
Oracle:
Failure behavior:
Controlling execution path:
Verification method:
Required evidence:
Residual risks:
```

A MECH closes only when:

```text
MECH definition
-> implementation path
-> oracle or tests
-> evidence
-> required review when applicable
```

If the mechanism exists but is untested, the claim must say so.

## 12. Context Reduction Architecture

The final design implements these context reduction mechanisms as required components:

```text
ACTIVE_CONTEXT.md
Context Packet
Hot / Warm / Cold Context
REPO_MAP.md
Long log slicing
Evidence as files
SESSION_HANDOFF.md
guardian-session-handoff skill
```

The following are not required in the initial implementation:

```text
Vector DB
GraphRAG/RAPTOR implementation
Prompt compression as routine workflow
Automatic memory service
Automatic repo-map generation
Every-turn retrieval
Every-turn context整理 subagent
```

These may be introduced later only if repeated failures or scale problems prove the need.

### 12.1 Active Context

`ACTIVE_CONTEXT.md` is the light context entry point.

It should contain only current working state:

```md
# Active Context

Current lane:
Current spec:
Current task:
Parent specs:
Open R-IDs:
Open QuestionDebt:
Required MECHs:
Forbidden claims:
Allowed next claim:
Evidence needed:
Current git state:
Next action:
Read next:
Full artifacts:
Last updated:
```

Rules:

- Keep it short enough to read every recovery turn.
- Practical target: fewer than 80 lines.
- Do not duplicate the full Base Spec or Plan.
- Do not use it to change requirements.
- If it conflicts with Base Spec, Plan, or Closure, the authoritative artifact wins.

### 12.2 Context Packet

Every major Guardian artifact starts with a short Context Packet.

Template:

```md
## Context Packet

Spec ID:
Type:
Status:
Parent:
Scope:
Applies To:
Required Parent R-IDs:
Blocking Questions:
Non-blocking Debt:
Known Exceptions:
Read-First R-IDs:
Last Reviewed:
Read full file only when:
Context Packet Authority: non-authoritative digest.
```

Context Packet is a navigation layer, not authority. If it conflicts with the artifact body, the artifact body wins. It must not contain `Children`; child lookup belongs in `SPEC_REGISTRY.md` or a targeted search.

### 12.3 Hot / Warm / Cold Context

Guardian uses three context tiers:

```text
Hot Context
- always loaded or checked first
- short, current, operational

Warm Context
- loaded when relevant to the current task
- summaries, indexes, current R-IDs, current Plan task

Cold Context
- loaded only at boundaries
- full source, full specs, full logs, old reviews, closed specs
```

Hot Context usually includes:

- `ACTIVE_CONTEXT.md`,
- current lane,
- current spec ID,
- current task,
- current R-IDs,
- open QuestionDebt,
- forbidden claims,
- evidence needed,
- next action,
- read-next pointers,
- current git state or command needed to obtain it.

Warm Context may include:

- `SPEC_REGISTRY.md`,
- `docs/ai/base-specs/repo/REPO-BASE-SPEC.md` Context Packet or required `MUST` R-IDs,
- relevant Area Base Spec Context Packet,
- declared `Required Parent R-IDs`,
- current Change Base Spec R-ID and Acceptance sections,
- current Plan task,
- `REPO_MAP.md` for file discovery,
- targeted code files,
- targeted test files.

Cold Context includes:

- full Original Source,
- full `source_map.md`,
- full Base Spec body,
- full logs,
- old closed specs,
- old review packets,
- broad diffs,
- archived discussion.

Cold-read triggers:

- Base Spec admission,
- Approval Packet review,
- source-fidelity challenge,
- parent-child spec conflict,
- MECH completion review,
- final strong claim,
- recovery after stale context when Hot Context is insufficient,
- verification failure where a summary hides the root cause.

### 12.4 Repo Map

`REPO_MAP.md` is a compact map of the codebase.

Recommended content:

```md
# Repo Map

## Areas
| Area | Responsibility | Key files | Tests |
|---|---|---|---|

## Public APIs
| API | Owner file | Stability | Notes |
|---|---|---|---|

## Important Symbols
| Symbol | File | Purpose |
|---|---|---|

## Test Entrypoints
| Purpose | Command |
|---|---|

## Known Risk Areas
| Area | Risk | Notes |
|---|---|---|
```

Rules:

- `REPO_MAP.md` is a discovery aid, not a source of truth for behavior.
- It should point to files and tests; it should not replace reading the files being changed.
- It can be maintained manually at first.
- Automatic generation may be added later if repo size justifies it.

### 12.5 Long Log Handling

Long logs should not be pasted into chat by default.

Preferred workflow:

```text
1. Capture full log as an artifact file.
2. Search for failure markers with targeted commands.
3. Extract the smallest exact failure slice.
4. Use the slice for diagnosis.
5. Keep the full log path as evidence.
```

If a summary hides the root cause, it is not valid closure evidence.

### 12.6 Evidence as Files

Verification outputs should be stored as files when they are long or likely to matter later.

Examples:

```text
docs/ai/changes/<spec-id>/logs/test-20260513-001.txt
docs/ai/changes/<spec-id>/logs/build-20260513-001.txt
docs/ai/changes/<spec-id>/reviews/guardian-boundary-001.md
```

`ACTIVE_CONTEXT.md` should point to these files and include only exact slices needed for immediate reasoning.

### 12.7 Retrieval and Summaries

Retrieval and summaries are allowed as navigation, not authority.

Allowed uses:

- finding related specs,
- finding likely files,
- finding tests,
- finding old decisions,
- finding source anchors,
- summarizing old discussion into `ACTIVE_CONTEXT.md`,
- summarizing long logs after exact slices are saved.

Disallowed uses:

- replacing Base Spec acceptance,
- replacing `source_map.md` for source-fidelity claims,
- replacing verification logs when the root cause matters,
- resolving QuestionDebt by confident wording,
- supporting strong final claims without reading authoritative evidence.

### 12.8 Normal Execution Read Algorithm

```text
1. Read ACTIVE_CONTEXT.md.
2. Read current Plan task.
3. Read current Change Base Spec R-ID and Acceptance sections.
4. Read declared Required Parent R-IDs and relevant parent Context Packets.
5. Read source_map slice, or the equivalent source location/excerpt in the Change Base Spec when source fidelity matters.
6. Read REPO_MAP.md only if file discovery is needed.
7. Read files being changed.
8. Execute the smallest useful step.
9. Run targeted verification.
10. Record evidence pointers and git state when verification matters.
11. Update ACTIVE_CONTEXT.md and CLOSURE.md as needed.
```

Do not infer parent relevance from memory. If Required Parent R-IDs are missing, suspicious, or no longer match the implementation scope, stop and update the Change Base Spec before dependent implementation or claims.

### 12.9 Boundary Read Algorithm

```text
1. Identify the boundary type.
2. Read required full artifacts for that boundary.
3. Build a compact review or claim packet.
4. Run required semantic review when applicable.
5. Record exact evidence, git state, and forbidden claims.
6. Update ACTIVE_CONTEXT.md and CLOSURE.md.
```

Boundary-specific full reads:

- Base Spec admission: Original Source anchors, `source_map.md` or equivalent source anchors, Base Spec, Approval Packet.
- Plan admission: Base Spec, declared parent constraints, Plan, blockers, QuestionDebt.
- Source-fidelity challenge: challenged source slice, `source_map.md` or equivalent source anchor, Base Spec slice, old claim.
- MECH completion: MECH entry, controlling path, oracle, evidence.
- Final strong claim: relevant R-IDs, acceptance, declared Required Parent R-IDs, applicable approved exceptions, blocking questions, verification output, closure evidence, required reviews, git state. Read full ancestor Base Specs only for repo-wide claims, parent conflict, exception review, missing Required Parent R-IDs, or suspected drift.
- Recovery: `ACTIVE_CONTEXT.md`, current `/goal` objective, current task, last evidence, blockers, required boundary status.

## 13. Session Rotation and Handoff

Starting a fresh session is an official context-reduction strategy.

It is most useful when:

- a major boundary has completed,
- the active conversation contains large logs or broad exploration,
- stale assumptions are accumulating,
- the next step is a clean implementation or review checkpoint,
- the user wants to continue later,
- a strong final claim is approaching and evidence should be reloaded fresh.

Avoid rotating in the middle of:

- partially applied edits,
- unresolved merge/conflict state,
- commands whose results are still needed,
- high-impact user decisions not yet recorded,
- verification failures whose exact root cause has not been captured.

### 13.1 Handoff Artifact

Use `SESSION_HANDOFF.md` as a transient resume index.

Recommended locations:

```text
docs/ai/SESSION_HANDOFF.md
docs/ai/changes/<spec-id>/SESSION_HANDOFF.md
```

`SESSION_HANDOFF.md` is not authority. It may summarize and point, but it cannot override:

- Base Spec,
- Plan,
- Closure,
- source_map,
- git state,
- user decisions.

Template:

```md
# Session Handoff

Handoff ID:
Created:
Created by:
Current lane:
Current spec:
Current task:
Goal or /goal objective:

## Resume Packet

Read first:
- AGENTS.md or project rules:
- SPEC_REGISTRY.md:
- ACTIVE_CONTEXT.md:
- Base Spec:
- Plan:
- Closure:

Exact resume point:
Next action:
Stop if:
Forbidden claims:
Allowed next claim:

## State

Git commit:
Diff hash:
Git status summary:
Changed files:
Untracked relevant files:
Running processes or servers:

## Evidence

Commands run:
Evidence files:
Exact output slices needed:
Tests not run:

## Decisions and Blockers

User decisions recorded:
Open QuestionDebt:
Blockers:
Risks:

## Cold Reads Required Before Claims

Before strong claim, read:
Before source-fidelity claim, read:
Before MECH closure, read:
```

### 13.2 Handoff Skill

Add a dedicated skill:

```text
name: guardian-session-handoff
description: Prepare or consume a session handoff for Guardian work without treating summaries as authority.
```

Modes:

```text
prepare-handoff
resume-handoff
```

`prepare-handoff` must:

1. Read `ACTIVE_CONTEXT.md`, current Plan task, `CLOSURE.md`, and git state.
2. Record exact next action, blockers, forbidden claims, and evidence pointers.
3. Record command outputs by path or exact slice, not broad summary.
4. Record cold-read requirements for any future strong claim.
5. Update `SESSION_HANDOFF.md`.

`resume-handoff` must:

1. Read project rules and `SESSION_HANDOFF.md`.
2. Read `ACTIVE_CONTEXT.md` and authoritative artifacts listed in `Read first`.
3. Verify git state against the handoff.
4. Treat mismatches as recovery, not as permission to guess.
5. Resume only the exact next action or ask the smallest blocking question.

Smoke tests:

```text
1. Handoff after Plan admission -> new session resumes current task without reading full old chat.
2. Handoff with changed git state -> resume detects mismatch and enters recovery.
3. Handoff with unresolved QuestionDebt -> resume refuses dependent R-ID closure.
4. Handoff before final strong claim -> resume performs required cold reads before claiming.
5. Handoff summary contradicts Base Spec -> Base Spec wins.
```

## 14. Guardian Lane Workflow

Guardian Lane flow:

```text
Spec lookup
-> source classification
-> Base Spec draft
-> Base Spec admission review when required
-> Approval Packet for Base Spec authority
-> user approval or explicit decisions
-> Plan
-> Plan admission when required
-> /goal execution
-> targeted verification
-> semantic boundary review when required
-> closure evidence with git state
-> promotion/amendment decision
```

### 14.1 `/goal` Usage

Use `/goal` when the work has:

- one durable objective,
- a clear stopping condition,
- a validation loop,
- enough room for independent progress,
- an admitted Plan.

In Guardian Lane, `/goal` is the execution mechanism after Base Spec and Plan admission.

### 14.1.1 Blocked Goal Stop Rule

If the agent cannot make productive progress during `/goal` execution:

1. Record the blocker, evidence, and the smallest needed user decision or external change.
2. Try only bounded recovery that could change the state.
3. Report the blocker to the user once in plain language.
4. If `update_goal(status=blocked)` is rejected by the goal gate, record that rejection and wait for user input instead of repeating the same blocked report.

Do not claim completion when blocked. Do not keep looping through the same status report.

### 14.2 Approval Packet

Before approval, show a compact packet covering:

- `QUESTION`,
- `ADAPTED`,
- `PARTIAL`,
- `OUT_OF_SCOPE`,
- high-risk `EXACT`,
- required MECHs,
- reviewer objections,
- conversion risks,
- explicit user decisions.

A Change Base Spec becomes implementation authority only after explicit approval or equivalent recorded user decision.

The Approval Packet does not need to be a permanent artifact unless it contains decisions that must be preserved. Durable decisions should be stored in `BASE_SPEC.md`, `CLOSURE.md`, or optional `DECISIONS.md`.

## 15. Review Roles

### 15.1 guardian_boundary_reviewer

`guardian_boundary_reviewer` is the semantic/spec boundary reviewer.

It checks:

- Base Spec admission,
- Approval Packet review,
- Plan admission,
- MECH completion,
- closure claims,
- source-fidelity challenge,
- recovery.

For Base Spec management, require `guardian_boundary_reviewer` for:

- Repo or Area Base Spec meaning changes,
- parent `MUST` approved exceptions,
- removing, merging, or superseding already-referenced Repo or Area R-IDs,
- security, privacy, persistence, public API, algorithm, or global verification impacts,
- final strong claims.

Do not require Guardian boundary review for every Change-local light edit or ordinary Default Lane task. If the reviewer is not runtime-callable, do not admit Repo/Area Base Spec changes or make strong claims that depend on that review; narrow the claim or ask for a user decision.

Return statuses:

```text
PASS
FAIL_FIXABLE
USER_DECISION_REQUIRED
BLOCKED
BLOCKED_PACKET_TOO_BROAD
```

It must never mark R-IDs `VERIFIED`.

For Codex, the intended personal path is:

```text
~/.codex/agents/guardian_boundary_reviewer.toml
```

Project-scoped repos may use:

```text
.codex/agents/guardian_boundary_reviewer.toml
```

Legacy `boundary_reviewer.toml` files outside Codex's custom-agent search path should be migrated or treated as archival reference only.

### 15.2 spec_verifier

`spec_verifier` checks implementation against approved R-IDs and Base Spec.

Use it when:

- R-ID closure is nontrivial,
- source fidelity is important,
- a change touches public API, security, persistence, or algorithms,
- final strong claim depends on multiple files or tests.

It must not create new requirements.

### 15.3 quality_reviewer

`quality_reviewer` checks correctness risks, regressions, maintainability, and test adequacy.

Use it when:

- the code change is broad,
- implementation is complex,
- there are regression risks outside the exact spec,
- test adequacy is uncertain.

It is not required for every small routine task.

### 15.4 Codex Auto-review Is Separate

Codex Auto-review is about sandbox-boundary approval requests.

Guardian boundary review is about semantic/spec boundaries.

Do not use:

```text
approvals_reviewer = "auto_review"
```

as a replacement for:

```text
guardian_boundary_reviewer
```

## 16. Closure Rules

Final strong claims require fresh evidence.

Forbidden shortcuts:

- reviewer PASS alone,
- worker DONE alone,
- manual-only confidence,
- broad test summary with hidden root cause,
- support task counted as Must R-ID closure,
- old PASS/VERIFIED reused after challenge or drift,
- evidence gathered before relevant code changed,
- claim broader than verification scope.

Closure evidence should connect:

```text
Base Spec R-ID
-> implementation behavior
-> verification output
-> review result when required
-> git state
-> final claim
```

If evidence is partial, the final claim must be partial.

If closure is blocked and cannot be advanced without user input or external state, record the blocker and stop repeating the same final-status message. A goal-gate refusal to mark blocked is evidence of tool state, not permission to loop or claim success.

### 16.1 Closure Evidence Template

```md
# Closure

## Context Packet

Spec ID:
Claim:
Status: OPEN | PARTIAL | CLOSED | BLOCKED
Evidence summary:
Git state:
Residual risk:
Read full file only when:

## Claim

Claim type:
Claim text:
Scope:
Forbidden broader claims:

## R-ID Evidence

| R-ID | Status | Evidence | Review | Notes |
|---|---|---|---|---|

## Verification Evidence

| Evidence ID | Command or method | Result | Output path or exact slice | Timestamp | Git state | Scope |
|---|---|---|---|---|---|---|

## Git State

Commit:
Diff hash:
Dirty tree status:
Files changed:
Untracked files relevant to claim:

## Reviews

| Review | Reviewer | Result | Packet | Notes |
|---|---|---|---|---|

## Residual Risk

Known limitations:
Untested areas:
Deferred QuestionDebt:
Reason claim is still valid:
```

### 16.2 Git State Policy

For every strong claim, record at least one of:

```text
git commit hash
git diff --stat + git diff hash
git status --short
```

Recommended diff hash for uncommitted tracked changes:

```bash
git diff --binary -- . | git hash-object --stdin
```

This hash does not include untracked files unless they are staged or recorded separately.

For relevant untracked files:

- list paths, and
- either stage them before hashing or record separate file hashes.

If the claim refers to a commit, the commit hash is the primary state anchor and dirty tree status must still be recorded.

If verification occurred before material code changes, rerun verification or downgrade the claim.

## 17. Security Posture

Default posture:

```text
sandbox_mode = "workspace-write"
approval_policy = "on-request" or "untrusted"
network_access = false unless needed
trusted paths limited to the project repo
```

Recommendations:

- Do not trust broad paths such as an entire user directory by default.
- Trust individual project repos instead.
- Do not use `danger-full-access`, `--yolo`, or `--dangerously-bypass-approvals-and-sandbox` as everyday defaults.
- Do not use `approval_policy = "never"` as an everyday default.
- Keep `workspace-write` as the normal low-friction local automation mode.
- Separate safe and power profiles if practical.
- Treat secrets, auth files, token stores, browser profiles, wallet files, SSH keys, and API key stores as protected.
- Keep optional MCP servers disabled unless needed.
- Require approval for destructive commands, dependency installs, network operations, external writes, and GUI automation when outside the normal project workflow.
- Do not let convenience settings silently weaken the Guardian safety model.

A power profile, if it exists, should be explicit, rare, manually selected, and documented outside the default Guardian profile.

Do not provide a copy-paste `danger-full-access` + `approval_policy = "never"` example in Guardian docs.

## 18. Superpowers Integration

Guardian should keep the Superpowers practices that improve everyday engineering quality:

- test-driven development,
- systematic debugging,
- verification before completion,
- worktree or branch hygiene,
- finishing workflow,
- review discipline.

Guardian should not duplicate Superpowers as a second full workflow layer.

Intended relationship:

```text
Superpowers-like discipline = execution quality
Guardian = source/spec/evidence authority
Codex sandbox/approval = runtime safety boundary
```

These layers should reinforce each other, not duplicate each other.

## 19. Implementation Priorities

### Priority 1: Clarify Core Contracts

- Update top-level instructions to state the two lanes.
- Add Guardian promotion triggers.
- Add claim vocabulary.
- Add Base Spec vs Plan boundary rule.
- State that hierarchy is a spec data model, not a set of workflow modes.

### Priority 2: Simplify and Add Artifacts

- Add/update `SPEC_REGISTRY.md` template.
- Add/update `ACTIVE_CONTEXT.md` template.
- Add/update `docs/ai/base-specs/repo/REPO-BASE-SPEC.md` template.
- Add Area and Change Base Spec templates.
- Add Plan and Closure templates aligned to Base Spec/Plan boundary.
- Remove `ACTIVE_PLAN.md` as a required artifact.
- If `ACTIVE_PLAN.md` exists, document it as a legacy alias or generated view.

### Priority 3: Fix Reviewer Runtime

- Add `~/.codex/agents/guardian_boundary_reviewer.toml`.
- Migrate old `boundary_reviewer.toml`.
- Update reviewer instructions to use `ACTIVE_CONTEXT.md`, not `ACTIVE_PLAN.md`.
- Keep Codex `approvals_reviewer = "auto_review"` separate from Guardian review.
- Add smoke tests for:
  - Base Spec admission,
  - Approval Packet,
  - Plan/Base Spec conflict,
  - final claim without evidence,
  - unresolved high-impact QuestionDebt,
  - source-fidelity challenge.

### Priority 4: Implement Context Reduction

- Make `ACTIVE_CONTEXT.md` the default recovery entry point.
- Add Context Packets to Repo, Area, Change, Plan, and Closure artifacts.
- Use Hot/Warm/Cold Context tiers.
- Require full artifact reads only at boundary events and exact claims.
- Keep R-ID summaries compact.
- Avoid copying full source text into every artifact.
- Add `REPO_MAP.md` for codebase discovery.
- Treat retrieval and summaries as pointers, not authority.
- Add long-log handling.
- Add `SESSION_HANDOFF.md`.
- Add `guardian-session-handoff` skill.
- Add docs lifecycle rules for AI-created markdown so stale docs do not become active context.

### Priority 5: Narrow MECH

- Require MECH for core R-ID mechanisms in MECH-sensitive domains.
- Do not require MECH for incidental touches.
- Add `Required: yes | no | excluded-by-spec` to MECH entries.
- Require MECH closure evidence only when MECH is required.

### Priority 6: Harden Security Defaults

- Narrow trusted project paths.
- Keep `workspace-write` plus `on-request` or `untrusted` as everyday local posture.
- Avoid full-access/no-approval modes as defaults.
- Keep sensitive paths out of routine read/write scope.
- Disable optional MCP servers unless needed.

### Priority 7: Bind Evidence to Git State

- Add git state to `CLOSURE.md`.
- Record verification timestamps.
- Record command outputs or exact output slices.
- Define diff hash calculation for uncommitted tracked changes.
- Record relevant untracked files separately or stage/hash them deliberately.
- Rerun verification when code changes after evidence collection.

### Priority 8: Add Session Handoff Skill

- Add `guardian-session-handoff`.
- Support `prepare-handoff` and `resume-handoff`.
- Require handoff before intentional session rotation during Guardian Lane work.
- Require resume to verify git state and read authoritative artifacts before continuing.

## 20. Minimal Operating Rules

These are the essential operating rules:

1. Use Default Lane unless Guardian triggers are present.
2. Routine "done" or "implemented" claims do not automatically trigger Guardian Lane.
3. Strong claims require Guardian closure.
4. In Guardian Lane, Base Spec defines correctness; Plan defines implementation.
5. Plan cannot add requirements or change acceptance.
6. Base Spec layers are at most Repo, Area, and Change; Plan is not a Base Spec layer.
7. Standard Base Spec links are `Parent` and `Supersedes`; references are non-authority.
8. Child specs cannot weaken parent specs without an approved exception record.
9. `SPEC_REGISTRY.md`, Context Packets, changelogs, decisions, handoffs, summaries, and retrieval results are not authority.
10. Change Base Specs must declare Required Parent R-IDs when parent specs apply; do not guess parent relevance.
11. Repo and Area Base Spec bodies contain current truth only; move history to compact changelog or decisions records.
12. R-IDs are never reused; `Supersedes` is lineage, not inheritance of old text.
13. Area Base Specs are optional and should cover stable multi-change domains, not every folder.
14. High-impact QuestionDebt blocks dependent work.
15. Support work cannot close Must R-IDs.
16. MECH is required only for core R-ID mechanisms in MECH-sensitive domains, unless explicitly excluded by the Base Spec.
17. Final strong claims require fresh evidence bound to repository state.
18. Before creating a new Change Base Spec, check `SPEC_REGISTRY.md`.
19. On stale context, resume from `ACTIVE_CONTEXT.md`, not from old chat memory.
20. Do not maintain `ACTIVE_PLAN.md` as an independent source of truth.
21. Use Context Packets and Hot/Warm/Cold Context instead of reading every artifact every turn.
22. Retrieval and summaries can guide work, but final claims must read authoritative artifacts or exact evidence.
23. Keep Codex Auto-review separate from Guardian semantic boundary review.
24. Do not use full-access/no-approval modes as default Guardian-safe operation.
25. Use session rotation deliberately at clean boundaries.
26. Handoff summaries are resume indexes, not authority.
27. Before resuming from a handoff, verify git state and reload authoritative artifacts needed for the next claim.
28. Before Guardian implementation, get explicit user permission for the current Base Spec and Plan.
29. Use plain language in user-facing messages; keep internal shorthand inside artifacts or explain it.
30. If blocked work cannot progress, report the needed decision once and wait instead of repeating the same blocked message.
31. New AI-created markdown must declare its purpose, status, and authority; active indexes must point to current docs.

## 21. Research and OSS Basis

This design follows established patterns from agent tooling and LLM research:

- Long-context models can underuse information buried in the middle of long prompts. See `Lost in the Middle`: https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long
- Retrieval-augmented generation separates knowledge storage from prompt context. See the original RAG paper: https://nlp.cs.ucl.ac.uk/publications/2020-05-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks/
- MemGPT supports the memory hierarchy idea behind Hot/Warm/Cold Context: https://huggingface.co/papers/2310.08560
- OpenHands Context Condenser supports condensing old event history while preserving important information: https://docs.openhands.dev/sdk/guides/context-condenser
- SWE-agent handles long command output by saving large output and opening exact slices: https://swe-agent.com/0.7/config/summarizers/
- Cline Memory Bank supports structured Markdown memory across context resets: https://docs.cline.bot/features/memory-bank
- aider's repo map supports compact codebase structure plus targeted file reads: https://aider.chat/docs/repomap.html
- Continue context providers support context by type, such as file, code, diff, terminal, docs, and search: https://docs.continue.dev/customize/custom-providers
- GraphRAG and RAPTOR support hierarchical summary/index layers above detailed sources: https://microsoft.github.io/graphrag/ and https://arxiv.org/abs/2401.18059
- LLMLingua-style compression is useful for exploration but should not replace authoritative source text for fidelity-sensitive claims: https://www.microsoft.com/en-us/research/project/llmlingua/llmlingua/
- Prompt caching can reduce stable-prefix cost, but it is an optimization rather than a correctness mechanism: https://openai.com/index/api-prompt-caching/

## 22. Final Expected Environment

After implementation, the Codex environment should be:

- light for everyday work,
- strict for large or high-risk work,
- resistant to source/spec drift,
- structured enough for repeated work in the same repo,
- safer by default,
- context-efficient across long sessions,
- clear about requirements, plans, evidence, and runtime permission boundaries.

The key is not to use Guardian everywhere.

The key is:

```text
Default Lane remains genuinely light.
Guardian Lane is used when source fidelity, evidence, and boundary review materially reduce failure risk.
Context is managed through artifacts and handoff, not through endless chat history.
```
