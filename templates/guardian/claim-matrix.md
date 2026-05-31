# Claim Matrix

Use only for broad, multi-evidence, or final strong claims.

| Claim | Scope | Required evidence | Evidence IDs | Review | Blockers | Allowed? |
|---|---|---|---|---|---|---|
| SOURCE_FAITHFUL | R-07 | source anchor + implementation + verifier | EV-... | PASS | none | yes |
| VERIFIED | full change | all Must R-IDs + state + review | missing | n/a | R-09 open | no |

Claim ceiling rule:

- A targeted test supports a targeted claim, not global READY or VERIFIED.
- Reviewer PASS supports review confidence, not executable proof.
- Compressed output is evidence only when backed by full output path, sha256, and exact slice or rerun.
