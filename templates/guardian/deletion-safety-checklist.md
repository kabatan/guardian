# Deletion Safety Checklist

Candidate:
Reason obsolete:
User-created or generated:
Tracked or untracked:
Import/export references checked: yes/no
Routes/config references checked: yes/no
Tests updated: yes/no
Rollback/provenance need: yes/no
Archive instead of delete: yes/no
Explicit user authorization required: yes/no

Policy:

- Never delete user-created or untracked files unless explicitly authorized.
- Delete obsolete application code only after checking imports/routes/config/tests.
- Generated AI docs may be archived more aggressively when registry/history no longer needs them.
- Automatic deletion is not part of P0/P1.
