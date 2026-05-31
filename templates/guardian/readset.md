# ReadSet

## ReadSet

MUST_READ_AUTHORITY:

- BASE_SPEC.md#R-...
- source_map.md#S-...

MUST_READ_CODE:

- path/to/code
- path/to/test

MAY_READ_NAVIGATION:

- REPO_MAP.md#...
- SPEC_REGISTRY.md#...

DISCOVERY_ALLOWED:

- rg "pattern" path

STOP_AND_UPDATE_PLAN_IF:

- editing file outside MUST_READ_CODE
- claim requires authority outside MUST_READ_AUTHORITY
- source anchor required for intended claim is missing
- implementation requires Plan task split
- permission scope digest would change

Read outside ReadSet is allowed only for bounded navigation or root-cause discovery. Record the reason if a later strong or source-fidelity claim is expected. Extra reads do not automatically expand claim authority.

Edit outside MUST_READ_CODE stops for Plan/ReadSet update. Claim outside MUST_READ_AUTHORITY is not allowed for broad, strong, or source-fidelity claims.
