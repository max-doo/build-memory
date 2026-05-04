# CHANGELOG.md、SESSION_LOG.md 与 TODO.md 定义和模板指南

## 1. 总体原则

这三个文件的职责应明确分离，避免互相污染：

- `CHANGELOG.md`：面向 release / 用户 / 未来维护者，记录重要的、对外有意义的变化。
- `SESSION_LOG.md`：面向 agent 工作追踪，记录每次会话中的操作性变化和未解决事项。
- `TODO.md`：用户授权下由 AI 辅助维护的项目级 backlog，记录重要的待完成事项和已完成事项。

不要把 `CHANGELOG.md` 当作每次会话的流水账；`CHANGELOG.md` 可以记录 release 级时间戳，但不应给每条变更都加分钟级操作时间；不要把 `TODO.md` 当作 agent 的临时任务列表；不要要求 agent 每次会话都读取所有追踪文件。

---

## 2. CHANGELOG.md

### 2.1 定义

`CHANGELOG.md` 是 release-facing changelog，用于记录用户可见、发布相关、长期有参考价值的变化。

适合记录：

- 新增功能
- 行为变化
- Bug 修复
- 破坏性变更
- 安全修复
- 移除或废弃的功能

不适合记录：

- 每次会话修改了哪些文件
- agent 的中间尝试
- 临时待办
- 内部重构细节，除非影响用户或维护者
- 已在同一 session 中解决的过程问题

### 2.2 创建规则

`CHANGELOG.md` 不必在所有 workspace 初始化时强制创建。建议仅在以下情况创建：

- 用户明确要求创建 changelog；
- 项目是可发布的软件包、应用、库或产品；
- 仓库已有版本号、release、package、distribution 等明显发布语义；
- 仓库已存在 `CHANGELOG.md`，则保留并按 release changelog 语义维护。

### 2.3 模板

推荐使用版本级时间戳，而不是每条变更都加时间戳。

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

如果项目需要跨时区协作、审计或自动发布，也可以使用 ISO 8601 时间格式：

```md
## [0.1.0] - 2026-05-04T14:30:00-07:00
```

可以根据项目复杂度删减分类。轻量项目通常保留 `Added`、`Changed`、`Fixed` 即可。

### 2.4 管理规则

- 只记录 user-facing 或 release-relevant changes。
- 可以在版本区块标题中记录 release 时间，必要时精确到分钟。推荐格式：`## [version] - YYYY-MM-DD HH:MM`，跨时区项目可使用 ISO 8601。
- 不给每条变更记录分钟级操作时间；分钟级操作日志应放在 `SESSION_LOG.md`。
- 不记录 agent 的中间推理、尝试和临时修改。
- 如果只是内部实现调整，除非影响使用方式或维护判断，否则不要写入。
- 发布时，将 `[Unreleased]` 下的内容整理到带版本号和日期的区块中。
- 如果一天内可能有多次 release、需要审计发布顺序，或用户明确希望保留精确发布时间，可以使用分钟级 release 时间戳。

---

## 3. SESSION_LOG.md

### 3.1 定义

`SESSION_LOG.md` 是 agent 工作日志，用于记录会话级操作变化、文件级修改和未解决事项。它服务于上下文恢复、审计修改路径和跨会话交接。

适合记录：

- 本次 session 修改、新增、删除了哪些文件；
- 关键操作摘要；
- 本次没有解决但需要后续注意的问题；
- 对下一次继续工作的简短提示。

不适合记录：

- release note；
- 大段过程说明；
- 完整命令输出；
- 临时思考过程；
- 已解决的细碎中间步骤。

### 3.2 创建规则

`SESSION_LOG.md` 可以作为 workspace 初始化时的默认追踪文件创建，因为它直接服务于 agent 工作连续性。

第一，同一时间戳下允许多条更改。这样可以把一次连续操作聚合起来，避免产生很多碎片记录。

第二，bugfix 场景需要记录踩坑点。这个很有价值，因为 session log 的核心用途之一就是“下次不要重复踩同一个坑”。但也要限制为“有复用价值的踩坑点”，不能把所有无效尝试都写进去。

如果项目已有其他同类文件，例如 `WORKLOG.md`、`.agent/log.md`、`.claude/session-log.md`，则不要重复创建，应沿用已有约定。

### 3.3 模板

```md
# Session Log

<!--
Agent-facing operational log.Append concise entries after sessions that changed files or left unresolved issues.

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

中文项目可使用：

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

---

## 4. TODO.md

### 4.1 定义

`TODO.md` 是项目级 backlog，主要给人看，也允许 agent 在用户授权下辅助维护。它应记录重要、持久、可行动的待办事项，而不是当前 session 的临时执行步骤。

适合记录：

- 暂时搁置但后续应处理的重要事项；
- 尚未完成的项目级任务；
- 需要用户确认后才能继续的事项；
- 已完成的重要任务摘要。

不适合记录：

- agent 当前执行计划中的临时步骤；
- 已在同一 session 中解决的过程性 todo；
- 低价值提醒；
- 模型为了组织自己思路而生成的内部检查项；
- 与项目长期进展无关的细碎事项。

### 4.2 是否需要“进行中”区块

一般不建议保留 `进行中` 区块。

原因：

- `进行中` 状态变化快，容易诱导 agent 频繁编辑；
- 当前 session 的执行计划应留在对话或 plan 中；
- 长期 `TODO.md` 更适合只表达“待完成”和“已完成”；
- 减少模型读写和维护负担。

建议结构为：

- `待完成`
- `已完成`

如确有需要，可以在最终回复中建议用户新增条目，而不是由 agent 自动写入。

### 4.3 模板

```md
# TODO

<!--
Project-level backlog for important pending and completed work.
User-governed and agent-assisted. Agents may suggest updates and edit this file after user approval or an explicit request.
-->

## 待完成

- [ ] 重要待办事项

## 已完成

### YYYY-MM-DD

- [x] 已完成事项
```

如果项目偏英文，可使用：

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

### 4.4 管理规则

- `TODO.md` 是 user-governed、agent-assisted 的项目 backlog。AI 可以维护，但必须由用户授权触发。
- agent 默认不读取，也默认不编辑。
- 当用户要求“继续之前的待办”“看看还有什么没做”“根据 backlog 继续”等场景时，agent 才读取。
- agent 不应写入临时实现步骤。
- agent 不应把同一 session 内已经解决的过程性事项写入 TODO。
- 如果任务结束后出现重要但暂时搁置的事项，agent 应在最终回复中建议可加入 `TODO.md` 的条目，并询问是否代为写入。
- 如果本轮任务完成了 `TODO.md` 中已有事项，agent 可以提示用户是否将对应条目标记为完成；用户同意后再修改。
- 当用户明确要求更新 TODO，或明确同意 agent 代为写入 / 勾选 / 移动条目时，agent 可以编辑 `TODO.md`。
- agent 更新 TODO 时，应只做用户同意范围内的最小修改：新增重要待办、勾选已完成项、移动到已完成区，或删除用户明确要求删除的项。

建议 agent 在最终回复中这样提示：

```md
建议加入 TODO.md：

- [ ] 确认是否需要创建 release-facing CHANGELOG.md
- [ ] 后续为 SESSION_LOG.md 增加归档策略

本轮任务似乎也完成了 TODO.md 中的以下事项：

- [x] 将会话日志与 release changelog 分离

是否要我帮你更新 TODO.md？
```

---

## 5. 在 CLAUDE.md / AGENTS.md 中的简短说明

这些规则不应在 `CLAUDE.md` 或 `AGENTS.md` 中写成长篇说明。主规则文件只需要告诉 agent：文件存在、用途是什么、什么时候读、什么时候写。

### 5.1 推荐最短版本

```md
- `SESSION_LOG.md`: append concise session-level notes after file changes or unresolved issues. One timestamp may group related changes. For bugfixes, record reusable debugging context: symptom, root cause, pitfall, and final fix.
- `TODO.md`: user-governed, agent-assisted backlog for important pending/completed work; do not read or edit by default, but suggest updates and apply them after user approval.
- `CHANGELOG.md`: optional release-facing changelog; update only for user-facing or release-relevant changes.
```

### 5.2 推荐中文版本

```md
- `SESSION_LOG.md`：会话级操作日志；仅在修改文件或留下未解决事项后追加简短记录。同一时间戳可聚合多条相关更改；修 bug 时记录有复用价值的现象、根因、踩坑点和最终修复。
- `TODO.md`：用户授权下由 AI 辅助维护的项目级待办；默认不读取、不编辑，必要时建议新增或勾选条目，并在用户同意后更新。
- `CHANGELOG.md`：可选的 release 变更日志；只记录用户可见或发布相关变化。
```

### 5.3 如果只想放一条极简规则

```md
- Tracking files: use `SESSION_LOG.md` for session-level operational notes, `TODO.md` for user-governed agent-assisted backlog, and `CHANGELOG.md` only for release-facing changes; do not read or edit them by default unless relevant to the task or approved by the user.
```

中文：

```md
- 追踪文件：`SESSION_LOG.md` 记录会话级操作，`TODO.md` 记录用户授权下由 AI 辅助维护的项目级待办，`CHANGELOG.md` 仅记录 release 变化；默认不读取或编辑，除非与当前任务相关或用户同意。
```

---

## 6. 推荐 workspace-init 行为

初始化 skill 可以采用以下策略：

1. 默认创建 `SESSION_LOG.md`，除非已有同类工作日志文件。
2. 默认创建 `TODO.md`，但明确其为 user-governed、agent-assisted backlog。
3. 不默认创建 `CHANGELOG.md`，除非项目已有发布语义或用户明确要求。
4. 如果已有 `CHANGELOG.md`，不要覆盖；只在规则中说明它是 release-facing changelog。
5. 如果已有 `TODO.md`，不要覆盖；不要自动改写为 agent task list。
6. 如果已有 `SESSION_LOG.md`，不要覆盖；仅追加，不重排历史。
7. 在 `CLAUDE.md` / `AGENTS.md` 中只注入极短说明，不展开长篇规则。

推荐 skill 规则片段：

```md
## Tracking files

- Create `SESSION_LOG.md` if no equivalent work/session log exists.
- Create `TODO.md` if missing; it is a user-governed, agent-assisted project backlog, not an agent scratchpad.
- Do not create `CHANGELOG.md` unless the user asks or the project has clear release/versioning semantics.
- Never overwrite existing tracking files.
- Do not read or edit tracking files by default; use them only when relevant to the task.
```

---

## 7. 判断清单

### 7.1 一条内容应该写入 CHANGELOG.md 吗？

只有当答案多半为“是”时才写入：

- 用户或外部使用者是否需要知道？
- 是否影响功能、行为、兼容性、安全性或发布说明？
- 是否在未来查看版本历史时仍有价值？

### 7.2 一条内容应该写入 SESSION_LOG.md 吗？

只有当答案多半为“是”时才写入：

- 是否有助于恢复上次 session 的上下文？
- 是否说明了文件级修改或关键操作？
- 是否留下了未解决事项或后续注意点？

### 7.3 一条内容应该写入 TODO.md 吗？

只有当答案多半为“是”时才建议写入：

- 是否是项目级、持久、重要的待办？
- 是否不是当前 session 的临时步骤？
- 是否需要人类后续记住或决策？
- 是否不会在同一 session 内马上解决？

---

## 8. 最终推荐

默认组合：

```text
SESSION_LOG.md  # 记录会话级操作
TODO.md         # 用户授权下由 AI 辅助维护的项目 backlog
CHANGELOG.md    # release-facing changelog
```

默认读取策略：

```text
不要在每次 session start 自动读取这三个文件。
仅在当前任务需要历史上下文、backlog、release notes 或用户明确要求时读取。
```

默认写入策略：

```text
SESSION_LOG.md：会话结束后，有实际文件变化或未解决事项时追加。
TODO.md：默认不写；建议新增、勾选或移动条目，用户明确同意后再写。
CHANGELOG.md：默认不写；仅记录 release / 用户可见变化。
```

