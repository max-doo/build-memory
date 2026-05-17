# workspace-init SKILL

> **外化记忆。保留上下文。让 Agent 保持一致。**
>
> 这个 skill 为你的项目建立一个跨越会话、跨越 Agent 的共享工作记忆层。

---

## 问题：人机协作中的记忆断层

当你长期在一个项目中使用 Claude、Codex 或其他 AI 编程助手时，会反复遇到同样的摩擦：

- **每开一个新会话，都要重新交代一遍项目背景**——技术栈、命名习惯、关键目录结构。
- **上下文窗口有限。** Agent 记住了上一条建议，但跨会话就忘得一干二净。
- **多个 Agent，一个项目，却没有共享历史。** Codex 和 Claude 各自为战，一个学到的东西另一个不知道。
- **工作记录散落在聊天记录里。** 做过的决策、遇到的问题、探索过又放弃的路径——随着聊天记录翻页，全部丢失。

这些不是文件管理问题，而是**记忆问题**。

`workspace-init` 通过建立一套轻量、职责分明的文件外化上下文，建立持久的记忆层，每个 Agent 都基于同样的共享上下文工作。

---

## 原理：五个文件，一个共享记忆

Skill 会检查你的工作空间，生成或完善五个受管文件：

| 文件 | 在共享记忆中的角色 | 面向谁 |
|------|-------------------|--------|
| `AGENTS.md` | **通用项目规则**——目录约定、技术栈、测试规则、禁止事项 | Codex、Cursor 等 |
| `CLAUDE.md` | **Claude 的项目规则**——关键路径、常用命令、项目快捷方式 | Claude Code |
| `CHANGELOG.md` | **发布历史**——版本粒度的用户可见变更 | 开发者、用户 |
| `SESSION_LOG.md` | **协作日记**——做过的决策、遇到的问题、调试上下文 | 开发者、Agent |
| `TODO.md` | **用户主导的待办清单**——接下来做什么、已完成什么 | 开发者、Agent |

---

## 原则

### 先检查，再写入

Skill 不会凭空生成内容。它先检查你的项目：

- 顶层目录结构
- 构建文件（`package.json`、`pyproject.toml`、`Cargo.toml` 等）
- `Makefile`、CI 配置中的真实命令
- 是否已存在类似文件（如 `agent.md`、`WORKLOG.md`）

**绝不编造命令或路径。** 如果某项信息无法从仓库中确认，会留下 `TODO: confirm` 标记并提示你补充。

### 不静默覆盖

当文件已存在时，skill 会将其与规范对比：

- **小问题**（措辞、过时的命令、缺失的单行记录）→ 直接修复
- **大问题**（文件角色错误、文件间互相引用、长度超标两倍以上）→ **必须先获得你的明确批准，再修改**

### 独立性

`AGENTS.md` 和 `CLAUDE.md` 互不引用。两者间允许少量事实重复——这是为了各自自包含、面向不同读者。

---

## 对你的工作流意味着什么

### 降低会话启动成本

Agent 的上下文有限，而项目背景是无限的。把稳定的背景知识写进文件，每次会话只需加载这几百字，不必从零开始交代。

### 可追溯与可复盘

`SESSION_LOG.md` 和 `CHANGELOG.md` 不是为了替代 `git history`，而是为了补充**为什么**的记录——某个设计决策的上下文、某次调试的曲折过程，也便于项目复盘，沉淀经验和踩坑。这些是 `git log` 里不会写的东西。

---

## 安装位置

本 skill 采用跨工具通用的 `SKILL.md` 标准，同一份文件夹在 Claude Code、Codex、Cursor 和 Google Antigravity 中都可使用。将 `workspace-init/` 文件夹放入下方对应工具的 skills 目录即可。

### Claude Code

| 范围 | 路径 | 生效范围 |
|------|------|----------|
| 个人级（推荐） | `~/.claude/skills/workspace-init/` | 所有项目 |
| 项目级 | `<repo>/.claude/skills/workspace-init/` | 仅当前仓库 |

Windows 下 `~` 对应 `C:\Users\<用户名>`。

### OpenAI Codex（CLI / IDE）

| 范围 | 路径 | 生效范围 |
|------|------|----------|
| 全局 | `~/.codex/skills/workspace-init/` | 所有项目 |
| 项目级 | `<repo>/.agents/skills/workspace-init/` | 仅当前仓库 |

若设置了 `CODEX_HOME`，则该变量覆盖 `~/.codex`。新增 skill 后需重启 Codex。

### Cursor

| 范围 | 路径 | 生效范围 |
|------|------|----------|
| 项目级（推荐） | `<repo>/.cursor/skills/workspace-init/` | 仅当前仓库 |

Cursor 官方文档未提供全局 `~/.cursor/skills/` 路径，推荐使用项目级安装。新增 skill 后通过 `Cmd/Ctrl+Shift+P → Developer: Reload Window` 重新加载工作区。

### Google Antigravity

| 范围 | 路径 | 生效范围 |
|------|------|----------|
| 全局 | `~/.gemini/antigravity/skills/workspace-init/` | 所有项目 |
| 工作区 | `<workspace-root>/.agent/skills/workspace-init/` | 仅当前工作区 |

### 安装校验

正确放置后，目录结构应为：

```
<install-root>/workspace-init/
├── SKILL.md
├── README.md
├── assets/
└── reference/
```

`SKILL.md` 必须位于 `workspace-init/` 直接子级，不得再嵌套一层目录，否则 agent 无法识别该 skill。

---

## 使用方法

### 基本调用

在 Claude Code / Codex 中输入：

```
/workspace-init
```

Skill 会自动接管后续流程，只需回答它的几个确认问题即可。

### 首次初始化项目

当你在一个新项目中首次使用时，典型的流程如下：

**Step 1 — 选择语言**

Skill 会问你：文件用什么语言？

- 如果你想用中文，直接说"用中文"
- 如果你想用英文，直接说"use English"
- 如果你没指定，它会让你选，不会瞎猜

**Step 2 — 检查工作空间**

Skill 会扫描你的项目：
- 列出顶层目录
- 识别技术栈（从 `package.json`、`pyproject.toml` 等文件）
- 收集可用的脚本命令
- 检查是否已有类似文件

**Step 3 — 生成文件**

根据检查结果，它会创建缺失的 5 个文件。文件内容基于真实项目信息，不会编造命令。如果有不确定的地方，它会用 `TODO: confirm` 标记出来，让你后续补充。

例如，它可能会提示：

> 已创建 `CLAUDE.md`，但测试命令无法从仓库中自动确认，请在文件中找到 `TODO: confirm` 并替换为你的实际测试命令。

**Step 4 — 审阅结果**

最后会给出一个简洁的报告：
- 哪些文件**已创建**
- 哪些文件**已优化**
- 哪些文件**保持不变**
- 哪些修改**待你确认**

---

### 后续维护与优化

当你的项目结构变化时（比如换了测试框架、加了新的构建命令），重新运行 `/workspace-init`：

**它会对比现有文件与规范，分类处理：**

| 修改类型 | 处理方式 | 例子 |
|----------|----------|------|
| 小问题 | 直接修复，事后告知 | 改一个过时的命令、补一个缺失的状态标签 |
| 大问题 | 先问你，再动手 | 文件角色错误、`AGENTS.md` 引用了 `CLAUDE.md`、文件长度超标 |

**你随时可以说"跳过"或"保留现状"**——不强迫接受任何建议。

---

### 各文件的日常使用方式

这些文件创建后，不是摆设。它们会融入你的日常开发工作流：

**`AGENTS.md` + `CLAUDE.md`——项目规范**

Claude Code / Codex 会自动读取项目中的 `CLAUDE.md` 和 `AGENTS.md`，对齐项目项目规范。

**`TODO.md`——你的任务板**

`TODO.md` 是一个 Markdown 格式的简单看板：

```markdown
## Pending
- [ ] 重构用户认证模块
- [ ] 补充单元测试覆盖到 80%

## Done
- [x] 升级依赖到最新版本
```

你和 Agent 都可以维护它，但主动权在你。

**`SESSION_LOG.md`——写给人看的协作日记**

每次与 Agent 的重要会话后，skill 可以帮你追加一条记录：

```markdown
## 2026-05-04
- 决策：放弃使用 ORM，改为手写 SQL
  - 原因：项目查询太复杂，ORM 生成的 SQL 性能差
- 问题：Docker 构建在 Windows 上路径报错
  - 解决：将 `COPY` 指令中的反斜杠改为正斜杠
```

这些上下文是 `git log` 不会记录的东西，但三个月后你回来维护代码时会非常感谢自己写了这些。

**`CHANGELOG.md`——面向发布的版本历史**

只记录版本级别的变更，不是每个 commit 都写。适合开源项目或需要向用户交代变更的项目：

```markdown
## v1.2.0 — 2026-05-01
### Added
- 支持批量导入功能

### Fixed
- 修复导出时的编码问题
```

---

### 手动触发更新

如果你只想更新某一个文件，也可以直接对 Agent 说：

- "更新 AGENTS.md，加上新的 API 规范"
- "帮我把刚才的决策写进 SESSION_LOG"
- "TODO.md 里那项重构已经完成了，帮我标记一下"

Skill 会识别这些指令并调用对应的流程。

---

### 与版本控制配合

建议将生成的文件纳入 git 管理：

```bash
git add AGENTS.md CLAUDE.md CHANGELOG.md SESSION_LOG.md TODO.md
git commit -m "chore: init agent workspace tracking files"
```

这样团队成员可以共享同一套 Agent 协作规则，新成员加入项目时也能快速让 Agent 进入状态。

---

## 适用场景

- 刚开始在一个新项目中使用 Claude Code
- 发现 Agent 经常问重复的基础问题
- 团队中多人使用 AI 助手，需要一致的基准规范
- 项目已有一堆临时笔记（`notes.md`、`ai-context.md` 等），想整理成规范格式
- 想复盘过去与 Agent 的协作，但聊天记录已经刷过去

---

## 不适用场景

- 你想要一个全自动、无需确认的 Agent 管家——这个 skill 要求用户参与关键决策。
- 你的项目生命周期极短、一次性用完即弃——初始化文件本身也有成本。

---

## 文件规格速览

| 文件 | 长度建议 | 关键约束 |
|------|----------|----------|
| `AGENTS.md` | 200–400 词 | 通用、不引用其他规则文件 |
| `CLAUDE.md` | ≤150 行 | 自包含、面向 Claude Code 会话 |
| `CHANGELOG.md` | 随版本增长 | 只记版本级变更，不写日常提交 |
| `SESSION_LOG.md` | 持续追加 | 按会话时间戳条目，可记调试上下文 |
| `TODO.md` | 动态维护 | 仅 Pending / Done，无 In progress |

---

## 许可证

MIT
