# Definitions and Templates for CHANGELOG.md, SESSION_LOG.md, and TODO.md

## 1. Overall Principles

The three files have distinct responsibilities and should not bleed into one another:

- `CHANGELOG.md`: release-facing; targets users and future maintainers; records significant, externally meaningful changes.
- `SESSION_LOG.md`: agent-facing; tracks per-session operational changes and unresolved items.
- `TODO.md`: a project-level backlog under user authority, agent-assisted; records important pending and completed items.

Avoid the following anti-patterns: treating `CHANGELOG.md` as a per-session activity log; attaching minute-level operational timestamps to every changelog entry (release-level timestamps are fine); using `TODO.md` as the agent's scratchpad for the current task; requiring the agent to read all tracking files at every session start.

---

## 2. CHANGELOG.md

### 2.1 Definition

`CHANGELOG.md` is a release-facing changelog. It records user-visible, release-relevant changes that have long-term reference value.

Suitable entries:

- New features
- Behavior changes
- Bug fixes
- Breaking changes
- Security fixes
- Removed or deprecated features

Unsuitable entries:

- The list of files modified in each session
- The agent's intermediate attempts
- Temporary tasks
- Internal refactoring details, unless they affect users or maintainers
- Issues that were both raised and resolved within the same session

### 2.2 Creation Rules

`CHANGELOG.md` does not need to be created on every workspace initialization. Create it only when:

- The user explicitly requests a changelog;
- The project is a publishable package, application, library, or product;
- The repository already exhibits release semantics (versioning, releases, packaging, distribution);
- A `CHANGELOG.md` already exists—keep it and maintain it under release-changelog conventions.

### 2.3 Template

Use version-level timestamps. Do not timestamp individual entries.

```md
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

### Security

## [0.1.0] - 2026-05-04 14:30

### Added

- Initial release-facing change summary.
```

For projects requiring cross-timezone collaboration, audit trails, or automated releases, ISO 8601 is acceptable:

```md
## [0.1.0] - 2026-05-04T14:30:00-07:00
```

Categories may be trimmed based on project complexity. Lightweight projects typically keep only `Added`, `Changed`, and `Fixed`.

### 2.4 Maintenance Rules

- Record only user-facing or release-relevant changes.
- Release time may appear in the version section heading, with minute precision when needed. Recommended format: `## [version] - YYYY-MM-DD HH:MM`. Cross-timezone projects may use ISO 8601.
- Do not attach minute-level operational timestamps to individual entries; that level of detail belongs in `SESSION_LOG.md`.
- Do not record the agent's intermediate reasoning, attempts, or temporary edits.
- Do not record internal implementation tweaks unless they change usage or affect maintenance judgment.
- On release, move entries from `[Unreleased]` into a versioned, dated section.
- Use minute-level release timestamps only when there may be multiple releases per day, audit ordering matters, or the user explicitly requests them.

---

## 3. SESSION_LOG.md

### 3.1 Definition

`SESSION_LOG.md` is the agent's operational log. It records session-level operational changes, file-level edits, and unresolved items. It supports context recovery, audit of edit paths, and cross-session handoff.

Suitable entries:

- Files modified, added, or removed during the session
- Summaries of key operations
- Issues left unresolved that need future attention
- Brief hints for the next continuation of work

Unsuitable entries:

- Release notes
- Long-form process explanations
- Full command outputs
- Transient lines of reasoning
- Trivial intermediate steps already resolved

### 3.2 Creation Rules

`SESSION_LOG.md` is the default tracking file at workspace initialization, since it directly supports agent work continuity.

First, multiple changes may share a single timestamp. This aggregates one continuous operation and avoids fragmenting the log.

Second, bug-fix entries should record reusable debugging context. This is one of the log's core purposes—"do not fall into the same pit twice." Restrict entries to pitfalls with reuse value; do not log every failed attempt.

If a comparable file already exists (e.g. `WORKLOG.md`, `.agent/log.md`, `.claude/session-log.md`), do not duplicate it; follow the existing convention.

### 3.3 Template

```md
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
```

For Chinese-language projects, use:

```md
# Session Log

<!--
面向 Agent 的操作日志。仅在会话修改了文件或留下未解决事项时追加简短记录。

规则：
- 同一时间戳下可以聚合多条相关更改。
- 记录应简短、可审计。
- 修 bug 时，如有复用价值，记录现象、根因、踩坑点和最终修复。
-->

## YYYY-MM-DD

- HH:MM | 修改: `path/to/file` - 简要说明
- HH:MM | 新增: `path/to/file` - 简要说明
- HH:MM | 删除: `path/to/file` - 简要说明
- HH:MM | 待解决: 简要说明

- HH:MM | 批量:
  - 修改: `path/a` - 简要说明
  - 修改: `path/b` - 简要说明
  - 新增: `path/c` - 简要说明

- HH:MM | 修复: bug 修复摘要
  - 现象: 出了什么问题
  - 根因: 为什么发生
  - 踩坑: 误判、无效尝试或调试陷阱
  - 修复: 最终如何解决
  - 文件: `path/a`, `path/b`
```

---

## 4. TODO.md

### 4.1 Definition

`TODO.md` is a project-level backlog. It is primarily for humans, with the agent permitted to assist in maintenance under user authorization. It records important, persistent, actionable items—not the agent's transient execution steps for the current session.

Suitable entries:

- Important items deferred for later
- Project-level tasks not yet completed
- Items requiring user confirmation before continuing
- Summaries of completed important tasks

Unsuitable entries:

- Transient steps in the agent's current execution plan
- Process-level todos resolved within the same session
- Low-signal reminders
- Internal checklists generated by the model to organize its own thinking
- Trivia unrelated to long-term project progress

### 4.2 Whether to Use an "In Progress" Section

An `In Progress` section is generally not recommended.

Rationale:

- `In Progress` state changes rapidly and tends to induce frequent agent edits;
- The current session's execution plan belongs in the conversation or in a plan;
- A long-lived `TODO.md` is best limited to "pending" and "done";
- Reduces model read/write maintenance overhead.

Recommended structure:

- `Pending`
- `Done`

When needed, the agent may suggest new entries in its final response rather than writing them autonomously.

### 4.3 Template

```md
# TODO

<!--
Project-level backlog for important pending and completed work.
User-governed and agent-assisted. Agents may suggest updates and edit this file after user approval or an explicit request.
-->

## Pending

- [ ] Important pending item

## Done

### YYYY-MM-DD

- [x] Completed item
```

For Chinese-language projects, use:

```md
# TODO

<!--
项目级 backlog，用于记录重要的待办和已完成事项。
由用户授权、AI 辅助维护。Agent 可在用户同意或明确请求后建议更新和编辑此文件。
-->

## 待完成

- [ ] 重要待办事项

## 已完成

### YYYY-MM-DD

- [x] 已完成事项
```

### 4.4 Maintenance Rules

- `TODO.md` is a user-governed, agent-assisted project backlog. The agent may maintain it, but only when triggered by user authorization.
- The agent does not read or edit it by default.
- The agent reads it when the user says things like "continue from the previous backlog," "what's left to do," or "pick up from the backlog."
- The agent does not write transient implementation steps into it.
- The agent does not move process-level items resolved within the same session into `TODO.md`.
- When important items are deferred at task end, the agent should suggest entries to add and ask whether to write them.
- When the current task completes an existing `TODO.md` item, the agent may ask whether to mark it done; only edit after user approval.
- When the user explicitly requests a TODO update or approves the agent writing, checking, or moving entries, the agent may edit `TODO.md`.
- When the agent does update TODO, it should make the smallest change within the user's approved scope: add an important pending item, check off a completed item, move an item to Done, or remove an item the user explicitly requests.

A recommended prompt format in the agent's final response:

```md
Suggested additions to TODO.md:

- [ ] Confirm whether a release-facing CHANGELOG.md is needed
- [ ] Add an archival policy for SESSION_LOG.md

The current task also appears to have completed the following item in TODO.md:

- [x] Separate the session log from the release changelog

Would you like me to update TODO.md?
```

---

## 5. Short Notes for CLAUDE.md / AGENTS.md

These rules should not be expanded into long sections inside `CLAUDE.md` or `AGENTS.md`. The main rule files only need to tell the agent: which files exist, what they are for, when to read them, and when to write them.

### 5.1 Recommended Minimal Form

```md
- `SESSION_LOG.md`: append concise session-level notes after file changes or unresolved issues. One timestamp may group related changes. For bugfixes, record reusable debugging context: symptom, root cause, pitfall, and final fix.
- `TODO.md`: user-governed, agent-assisted backlog for important pending/completed work; do not read or edit by default, but suggest updates and apply them after user approval.
- `CHANGELOG.md`: optional release-facing changelog; update only for user-facing or release-relevant changes.
```

### 5.2 Recommended Chinese Form

```md
- `SESSION_LOG.md`：会话级操作日志；仅在修改文件或留下未解决事项后追加简短记录。同一时间戳可聚合多条相关更改；修 bug 时记录有复用价值的现象、根因、踩坑点和最终修复。
- `TODO.md`：用户授权下由 AI 辅助维护的项目级待办；默认不读取、不编辑，必要时建议新增或勾选条目，并在用户同意后更新。
- `CHANGELOG.md`：可选的 release 变更日志；只记录用户可见或发布相关变化。
```

### 5.3 Single-Line Variant

```md
- Tracking files: use `SESSION_LOG.md` for session-level operational notes, `TODO.md` for user-governed agent-assisted backlog, and `CHANGELOG.md` only for release-facing changes; do not read or edit them by default unless relevant to the task or approved by the user.
```

Chinese:

```md
- 追踪文件：`SESSION_LOG.md` 记录会话级操作，`TODO.md` 记录用户授权下由 AI 辅助维护的项目级待办，`CHANGELOG.md` 仅记录 release 变化；默认不读取或编辑，除非与当前任务相关或用户同意。
```

---

## 6. Recommended workspace-init Behavior

The initialization skill should follow this strategy:

1. Create `SESSION_LOG.md` by default, unless an equivalent work log already exists.
2. Create `TODO.md` by default, but make explicit that it is a user-governed, agent-assisted backlog.
3. Do not create `CHANGELOG.md` by default; create it only when the project has release semantics or the user requests it.
4. If `CHANGELOG.md` already exists, do not overwrite it; only document in the rules that it is a release-facing changelog.
5. If `TODO.md` already exists, do not overwrite it; do not auto-rewrite it as an agent task list.
6. If `SESSION_LOG.md` already exists, do not overwrite it; append only, and do not reorder history.
7. In `CLAUDE.md` / `AGENTS.md`, inject only the short note; do not expand into long rule sections.

Recommended skill rule fragment:

```md
## Tracking files

- Create `SESSION_LOG.md` if no equivalent work/session log exists.
- Create `TODO.md` if missing; it is a user-governed, agent-assisted project backlog, not an agent scratchpad.
- Do not create `CHANGELOG.md` unless the user asks or the project has clear release/versioning semantics.
- Never overwrite existing tracking files.
- Do not read or edit tracking files by default; use them only when relevant to the task.
```

---

## 7. Decision Checklists

### 7.1 Should an entry go into CHANGELOG.md?

Write only when most answers are "yes":

- Does a user or external consumer need to know?
- Does it affect functionality, behavior, compatibility, security, or release notes?
- Will it remain valuable when reviewing version history later?

### 7.2 Should an entry go into SESSION_LOG.md?

Write only when most answers are "yes":

- Does it help recover context from the previous session?
- Does it describe a file-level edit or key operation?
- Does it leave an unresolved item or follow-up note?

### 7.3 Should an entry go into TODO.md?

Suggest writing only when most answers are "yes":

- Is it project-level, persistent, and important?
- Is it not just a transient step in the current session?
- Does a human need to remember or decide on it later?
- Will it not be resolved within the same session?

---

## 8. Final Recommendation

Default file set:

```text
SESSION_LOG.md  # session-level operations
TODO.md         # user-governed, agent-assisted backlog
CHANGELOG.md    # release-facing changelog
```

Default read policy:

```text
Do not read these three files automatically at every session start.
Read them only when the current task needs historical context, the backlog, release notes, or the user explicitly requests it.
```

Default write policy:

```text
SESSION_LOG.md: append after session end when files actually changed or items remain unresolved.
TODO.md: do not write by default; suggest additions, check-offs, or moves, and write only after explicit user approval.
CHANGELOG.md: do not write by default; record only release-level / user-visible changes.
```
