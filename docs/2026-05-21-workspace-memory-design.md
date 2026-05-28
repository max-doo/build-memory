# 跨 Agent 项目记忆层优化设计方案

## 1. 目标与背景

现有 `build-memory` 通过 `AGENTS.md` / `CLAUDE.md` / `SESSION_LOG.md` / `TODO.md` / `CHANGELOG.md` 建立轻量项目记忆层。这个方向继续保留，但 `SESSION_LOG.md` 在长期、多 Agent 协作中暴露出两个主要问题：

- **并发写入风险**：多个 Claude Code / Codex session 同时结束并写入 `SESSION_LOG.md` 时，可能出现覆盖、冲突或重复整理。
- **上下文膨胀**：`SESSION_LOG.md` 持续累积后，Agent 为了恢复上下文可能读取大量低价值历史，增加 token 成本并干扰判断。

本方案的目标不是引入重型 memory framework，而是在保持 Markdown 可读性和五文件心智模型的前提下，增加一个轻量 Python 写入脚本，让日志写入、锁处理、历史归档和 lesson 候选提示自动化。

## 2. 设计原则

1. **保留单主入口**：`SESSION_LOG.md` 仍然是人和 Agent 查看最近协作上下文的主文件，不废弃、不拆散为默认多文件入口。
2. **脚本作为唯一推荐写入口**：Agent 不应手工追加 `SESSION_LOG.md`，而应调用脚本，由脚本统一处理时间、锁、归档和格式。
3. **读快写稳**：Agent 查看最近历史时直接读 `SESSION_LOG.md`；写入时才运行脚本。
4. **最近窗口优先**：`SESSION_LOG.md` 只保留最近 7 天记录；更早日期块自动迁移到归档文件。
5. **知识沉淀按需进行**：`KNOWLEDGE.md` 用于沉淀可复用经验、踩坑和长期决策，但不作为默认加载上下文。
6. **冲突明确处理**：写锁冲突时自动等待重试；超过等待上限后明确提示稍后重试，不引入额外待合并队列。

## 3. 文件结构

```text
 项目根目录/
  ├── AGENTS.md
  ├── CLAUDE.md
  ├── SESSION_LOG.md
  ├── TODO.md
  ├── CHANGELOG.md
  └── .memory/
        ├── session_log.py
        ├── SESSION_LOG.lock
        ├── KNOWLEDGE.md
        └── sessions/
              └── 2026-05-15.md
```

### 文件职责

- `SESSION_LOG.md`：最近 7 天的结构化协作日志。Agent 可直接读取。
- `.memory/session_log.py`：唯一推荐写入工具，负责追加、锁、自动归档和 lesson 候选提示。脚本放在记忆目录内，避免污染项目代码目录。
- `.memory/sessions/YYYY-MM-DD.md`：超过 7 天的每日历史归档。默认不读取，除非用户明确追溯历史。
- `.memory/KNOWLEDGE.md`：长期经验库，沉淀可复用 lesson、踩坑、架构决策和项目级约定。通过 `AGENTS.md` 挂载说明，但不全文内联；若 `CLAUDE.md` 已引用 `AGENTS.md`，则不需要重复写一份规则。

## 4. 写入脚本设计

只提供一个常用写入命令，脚本自动获取当前系统时间。

```bash
python .memory/session_log.py \
  --done "确定 workspace memory 采用单主日志和 Python 写入脚本" \
  --context "目标是在不增加 Agent 默认上下文负担的前提下，解决 SESSION_LOG.md 膨胀和并发写入问题。" \
  --decision "保留 SESSION_LOG.md 作为主入口；脚本写入时自动归档 7 天前日期块；Knowledge 只收录可复用 lesson，不默认加载。" \
  --modified "plans/2026-05-21-workspace-memory-design.md" \
  --lesson "按天分卷不能真正解决同日并发写冲突；锁写入比 merge-only 更稳。"
```

### 字段规范

- `done`：必填。本次完成了什么。
- `context`：可选。说明为什么做、当时问题背景和约束。
- `decision`：可选。本次形成的判断、取舍或后续应遵守的方向。
- `added`：可选。新增文件，可重复传入或用分隔符传入。
- `modified`：可选。修改文件，可重复传入或用分隔符传入。
- `removed`：可选。删除文件，可重复传入或用分隔符传入。
- `lesson`：可选。可复用经验、踩坑点、以后应避免的误判。
- `unresolved`：可选。遗留事项或后续需要用户确认的问题。

`done` 记录事实，`context` 记录事实背后的说明，`decision` 记录本次协作形成的结论。这样 `SESSION_LOG.md` 不只是文件改动流水账，也能保留后续恢复上下文时真正需要的判断依据。

### 写入格式

```md
## 2026-05-22

### 23:42 | codex

- done: 确定 workspace memory 采用单主日志和 Python 写入脚本
- context: 目标是在不增加 Agent 默认上下文负担的前提下，解决 SESSION_LOG.md 膨胀和并发写入问题。
- decision: 保留 SESSION_LOG.md 作为主入口；脚本写入时自动归档 7 天前日期块；Knowledge 只收录可复用 lesson，不默认加载。
- modified:
  - `plans/2026-05-21-workspace-memory-design.md`
- lesson: 按天分卷不能真正解决同日并发写冲突；锁写入比 merge-only 更稳。
```

脚本只识别 `## YYYY-MM-DD` 日期块，不尝试解析任意 Markdown 结构。这样可以降低脚本复杂度并提高迁移稳定性。

## 5. 锁与冲突处理

脚本写入时使用文件锁保护 `SESSION_LOG.md`。

```text
1. 尝试创建 `.memory/SESSION_LOG.lock`
2. 如果创建成功，进入写入流程
3. 如果锁已存在，最多等待约 10 秒并重试
4. 如果仍然失败，脚本退出并提示当前日志被占用，请稍后重试
5. 写入完成后删除锁
```

这意味着用户和 Agent 通常只需要运行同一个写入命令。短暂冲突由脚本自动等待处理；长时间冲突显式失败，避免引入后台队列、额外合并语义和不可见的 pending 状态。

## 6. 自动归档策略

每次运行写入脚本时，脚本先检查 `SESSION_LOG.md` 中的日期块：

- 最近 7 天日期块保留在 `SESSION_LOG.md`。
- 7 天前的日期块迁移到 `.memory/sessions/YYYY-MM-DD.md`。
- 如果目标归档文件已存在，则追加到该文件，避免覆盖历史。
- 归档完成后再写入本次 session 记录。

这样 `SESSION_LOG.md` 始终保持轻量，Agent 直接读取也不会承担过大的上下文负担。

## 7. Knowledge 与 lesson 沉淀

`.memory/KNOWLEDGE.md` 保留，但它不是第二个 `AGENTS.md` / `CLAUDE.md`。

它只记录长期可复用内容：

- 反复会遇到的调试经验
- 已确认的架构决策
- 项目级踩坑点
- 跨 session 仍然有效的操作约束

脚本不会自动总结或改写 `KNOWLEDGE.md`。脚本只做 lesson 候选提示：

```text
Lesson candidates detected:
- 2026-05-18: ...
- 2026-05-21: ...

Consider promoting stable lessons to `.memory/KNOWLEDGE.md`.
```

触发规则可以是：

- 最近 7 天内 `lesson` 条目超过 3 条；
- 或本次归档的旧日期块中包含 `lesson`；

是否写入 `KNOWLEDGE.md` 由 Agent 判断。Agent 只应提炼稳定、可复用、跨任务仍然有价值的内容，不把普通 session 过程搬进去。

## 8. AGENTS.md / CLAUDE.md 挂载规则

模板中只加入短规则，不全文内联 Knowledge。当前工作流允许 `CLAUDE.md` 引用 `AGENTS.md`：如果项目采用这种模式，记忆层规则只需要写入 `AGENTS.md`，`CLAUDE.md` 保持引用即可；如果某个环境要求 `CLAUDE.md` 自包含，再同步写入同一段短规则。

```md
## Tracking files

- `SESSION_LOG.md`: recent 7-day collaboration log. Read it directly when recent context is needed.
- Use `python .memory/session_log.py` to append session notes; do not edit `SESSION_LOG.md` manually.
- The script automatically handles time, file lock retries, and old-date archival. If the lock remains busy after retrying, rerun the command later.
- `.memory/KNOWLEDGE.md`: long-term reusable lessons and decisions. Read it only for recurring issues, debugging, architecture decisions, or when the current task likely depends on prior project experience.
- `.memory/sessions/`: archived daily session logs older than the recent window. Do not read by default unless tracing older history.
```

中文挂载示例：

```md
## 跟踪文件

- `SESSION_LOG.md`：最近 7 天协作日志；需要近期上下文时可直接读取。
- 使用 `python .memory/session_log.py` 追加 session 记录；不要手工编辑 `SESSION_LOG.md`。
- 脚本会自动处理当前时间、文件锁重试和旧日期归档；若重试后仍无法获得锁，稍后重新运行命令。
- `.memory/KNOWLEDGE.md`：长期可复用经验和决策；仅在处理反复问题、调试、架构决策或当前任务明显依赖项目历史经验时读取。
- `.memory/sessions/`：超过最近窗口的每日归档日志；默认不读取，除非需要追溯更早历史。
```

中文项目可生成对应中文规则。

## 9. 迁移策略

对于已经存在的旧 `SESSION_LOG.md`：

1. 保留文件，不废弃文件名。
2. 首次运行 `.memory/session_log.py` 时自动识别 `## YYYY-MM-DD` 日期块。
3. 最近 7 天保留在 `SESSION_LOG.md`。
4. 更早日期块迁移到 `.memory/sessions/YYYY-MM-DD.md`。
5. 如果旧文件格式无法可靠解析，脚本不应强行重写；应停止并提示 Agent 手动整理一次。

## 10. 推荐结论

最终方案为：

> 保留 `SESSION_LOG.md` 作为单一主日志入口；在 `.memory/` 中新增一个跨平台 Python 写入脚本；脚本负责锁、10 秒重试、自动归档 7 天前记录、结构化追加和 lesson 候选提示；`KNOWLEDGE.md` 作为按需读取的长期经验库，主要通过 `AGENTS.md` 挂载，`CLAUDE.md` 可引用 `AGENTS.md`，不默认加载 Knowledge 全文。

这个方案比“按天分卷 + 默认 Knowledge 加载”更轻，也比“多命令 CLI + 手动 merge”更容易执行。它把复杂度集中到一个脚本里，同时保留 Markdown 文件对人类和 Agent 的可读性。
