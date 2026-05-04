# Session Log

<!--
Agent-facing operational log. Append concise entries after sessions that changed files or left unresolved issues.

Rules:
- A single timestamp may group multiple related changes.
- Keep entries concise and auditable.
- For bugfixes, record reusable debugging context when useful: symptom, root cause, pitfall, and final fix.
-->

## YYYY-MM-DD

- HH:MM | modified: `path/to/file` - concise summary
- HH:MM | added: `path/to/file` - concise summary
- HH:MM | removed: `path/to/file` - concise summary
- HH:MM | unresolved: concise follow-up note

- HH:MM | batch:
  - modified: `path/a` - concise summary
  - modified: `path/b` - concise summary
  - added: `path/c` - concise summary

- HH:MM | fixed: concise bugfix summary
  - symptom: what was broken
  - root cause: why it happened
  - pitfall: misleading assumption, failed attempt, or debugging trap
  - final fix: how it was resolved
  - files: `path/a`, `path/b`
