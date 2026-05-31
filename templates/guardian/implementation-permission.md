# Implementation Permission

Status: NOT_GRANTED | GRANTED | REVOKED | STALE
Granted by:
Granted at:
Permission text:

Scope:

- Base Spec path:
- Base Spec sha256:
- Plan path:
- Plan sha256:
- Task ids:
- Requirement/source anchor ids:
- Open QuestionDebt ids:
- Measurement method sha256:
- Allowed claim ceiling:

Scope digest:

- scope_digest_sha256:

Carryover after change:

- Status: PRESERVED | STALE | REGRANTED
- Reason:
- Regrant text:

Scope digest inputs are normalized Base Spec path and sha256, normalized Plan path and sha256, sorted task ids, sorted requirement/source anchor ids, sorted open QuestionDebt ids, measurement method sha256 when present, and allowed claim ceiling.

Scope digest excludes timestamps, free-form enthusiasm, reviewer PASS, transient command output, and unstated user intent.

Permission becomes STALE when Base Spec or Plan content changes scope, task ids or source anchors change, open QuestionDebt changes materially, measurement method changes, allowed claim ceiling expands, or edit target moves outside approved task scope.
