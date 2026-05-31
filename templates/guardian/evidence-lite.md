# Evidence-lite

Use when new evidence will support a Guardian Lane strong claim and cross-session reuse is not expected.

Fields:

- id
- kind
- command
- cwd
- exit_code
- started_at
- full_output
- full_output_sha256
- git_head
- git_status_porcelain
- claim_ceiling

Evidence freshness rule:

Evidence becomes stale when relevant code, dependencies, environment, Base Spec, Plan, measurement method, fixture/data, or claim scope changes. Targeted evidence cannot support a broader claim unless the missing scope is separately verified.
