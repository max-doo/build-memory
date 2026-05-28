---
name: build-memory
description: 初始化或完善 agent 工作空间的跟踪与规则文件。适用场景：(1) 用户运行 `/build-memory` 或要求初始化工作空间；(2) 创建或更新 AGENTS.md / CLAUDE.md / CHANGELOG.md / SESSION_LOG.md / TODO.md；(3) 审计已有的规则或跟踪文件以发现质量问题；(4) 为项目补齐缺失的受管文件；(5) 用户询问工作空间约定、会话日志、待办、变更日志相关问题。
---

# 工作空间初始化

在项目根目录创建或完善五个受管文件：`AGENTS.md`、`CLAUDE.md`、`CHANGELOG.md`、`SESSION_LOG.md`、`TODO.md`，并补充轻量 `.memory/` 支撑目录，用于稳定写入 session log 和沉淀长期经验。

四条不可妥协的规则：
- **单点事实来源 (Single Source of Truth)。** 所有通用的项目规则、命令、技术栈均写入 `AGENTS.md`。`CLAUDE.md` 仅作为一个极简的入口，强制要求通过 `@AGENTS.md` 引用它。禁止在 `CLAUDE.md` 中重复写具体命令。
- **脚本化写入 session 记录。** Agent 应优先使用 `python .memory/session_log.py` 追加 session 记录，而不是手工编辑 `SESSION_LOG.md`；脚本负责锁、7 天归档和结构化格式。
- **不静默改写。** 未经用户明确同意，不得覆盖或删除已有内容。
- **真实时间。** 写入任何受管文件中的时间戳之前，必须通过 shell 命令（`date`、`date -Iseconds`、`Get-Date` 等）获取系统真实时间。不得凭记忆编造时间戳。

模板仅以英文形式存放于 `assets/`，写入时按目标语言翻译。

## 工作流

### 1. 选择语言

对于**新建**文件：
- **明确指令**（“use English”、“用中文”、“create in Japanese”）→ 使用该语言。
- **实质性用户输入**（除单纯调用外，附带任意语言的指令或上下文）→ 检测该输入的语言。
- **空调用**（仅 `/build-memory`、“init workspace” 或类似无附加要求的调用）→ **询问用户**使用哪种语言，不要猜测。

对于**完善**已有文件，沿用文件原语言，不进行翻译。

### 2. 检查工作空间

任何写入前先收集事实：
- 顶层文件与目录
- 包管理器 / 语言 / 框架（`package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod` 等）
- 来自 `package.json` scripts、`Makefile`、CI 配置的真实命令
- 已存在的受管文件及可能的别名（`agent.md`、`WORKLOG.md`、`.agent/log.md` 等）

**空工作空间检测。** 若检查时未发现源码目录、未发现包管理清单（`package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod` 等）、未发现构建/测试配置（`Makefile`、`tsconfig.json` 等），也未发现 CI 配置——即目录仅含 `.git`、README、license 或 dotfiles——在写入任何受管文件之前先**停下并询问用户**：

1. 暂时跳过工作空间初始化。
2. 由用户简述拟开发的项目（语言、框架、目标），以便用合理的默认值填充。
3. 生成最小骨架文件，并在显著位置加 `TODO: empty workspace` 标记与说明，表明此时工作空间为空。

空工作空间不要自动填充占位符；铺满 `TODO: confirm` 反而比不写更糟。

不得编造命令或路径。若占位符无法从仓库中确认，留下 `TODO: confirm` 标记并告知用户。

### 3. 创建缺失文件和记忆支撑目录

对每个缺失文件：
1. 读取 `assets/<filename>` 处的英文模板。
2. 将固定文本（标题、注释、标签）翻译为目标语言。
3. 用第 2 步获得的事实替换占位符。
4. 写入项目根目录。

如果目标项目缺少 `.memory/`，还应将 `assets/.memory/` 复制到项目根目录作为 `.memory/`。未经用户明确批准，不要覆盖已有的 `.memory/session_log.py` 或 `.memory/KNOWLEDGE.md`。

| 文件 | 角色 | 目标 |
|------|------|------|
| `AGENTS.md` | 面向所有 code agent 的项目主仓库指南（含所有规则、栈与命令） | 200–400 词 |
| `CLAUDE.md` | Claude 极简入口；**必须**包含 `@AGENTS.md` 引用 | 1–3 行 |
| `CHANGELOG.md` | 面向发布；仅记录版本级条目 | — |
| `SESSION_LOG.md` | Agent 操作日志；按会话时间戳记录 | — |
| `TODO.md` | 用户主导的 backlog；仅 `Pending` / `Done`（无 `In progress`） | — |
| `.memory/session_log.py` | 推荐的 session log 写入脚本，包含锁重试、7 天归档和 lesson 候选提示 | — |
| `.memory/KNOWLEDGE.md` | 长期可复用经验和稳定决策；仅按需读取 | — |

### 4. 完善已有文件

对每个已存在的受管文件：

1. 完整阅读。
2. **必须严格**与规范对比。如果你尚未加载规范，**必须**读取以下相关参考章节（不可省略或凭记忆猜测）：
   - 对 `CHANGELOG.md`、`SESSION_LOG.md`、`TODO.md`：参见 `reference/tracking-files-guide.md`
     - §2 CHANGELOG 定义与规则
     - §3 SESSION_LOG 定义与规则
     - §4 TODO 定义与规则
     - §7 判断清单
   - 对 `AGENTS.md`、`CLAUDE.md`：参见 `reference/rules-generation-guide.md`
     - §1 AGENTS.md 生成指南
     - §2 CLAUDE.md 生成指南
     - §3 差异化写法（AGENTS.md 与 CLAUDE.md）
     - §6 附录：内容决策对照表
   - 如果存在 `.memory/KNOWLEDGE.md`，且正在创建或完善 `AGENTS.md` 的“已知坑点”，读取该文件并判断是否有经验值得提升。只有跨任务反复出现、误用代价高、无法从代码结构直接看出、可写成一句明确操作规则的经验才提升到 `AGENTS.md`；其余继续留在 `KNOWLEDGE.md`。
3. 分类差异（**强制严格审计，拒绝妥协**）：
   - **小问题** — 仅限于极轻微的措辞修订、明显过期的单行命令修正、无害的微小冗余。可以直接编辑。
   - **大问题** — 结构与规范不符（如 `AGENTS.md` 缺少必要的章节或规则违背单点事实来源）、文件角色错误（如 `CLAUDE.md` 包含具体命令而非只引用 `@AGENTS.md`）、文件长度超过推荐值的 2 倍、`TODO.md` 包含“进行中”区块，或 `CHANGELOG.md` 被用作日常日志。
4. **大问题需在编辑前征得用户同意。绝对禁止在不规范的结构上静默打补丁或强行融合。** 
   - 你必须向用户明确指出违反规范的地方，将其标记为“大问题”。
   - 提供问题说明与**重写建议**摘要。
   - 停下来等待用户的批准、跳过或逐项指示。

### 5. 报告

以简洁报告结束：**created**（已创建）、**refined**（已完善）、**left alone**（保持不变）、**pending decision**（待决定）。

## 资源与参考

- `assets/<filename>` — 五个受管文件的英文模板。
- `assets/.memory/` — 支撑脚本、长期知识模板和归档目录占位文件。
- `reference/tracking-files-guide.md` — `CHANGELOG.md`、`SESSION_LOG.md`、`TODO.md` 的完整规则。
  - §2 CHANGELOG：面向发布、版本级时间戳、何时创建
  - §3 SESSION_LOG：agent 操作日志、按会话条目、bugfix 上下文
  - §4 TODO：用户主导 backlog、仅 Pending/Done、不设 “In progress”
  - §7 判断清单：每个跟踪文件应写入的内容
- `reference/rules-generation-guide.md` — `AGENTS.md`、`CLAUDE.md` 的完整规则。
  - §1 AGENTS.md：Codex 风格仓库指南，200–400 词
  - §2 CLAUDE.md：Claude Code 极简入口，仅包含对 AGENTS.md 的引用
  - §3 主从引用模式：AGENTS.md 与 CLAUDE.md 的单点事实来源规则
  - §6 附录：内容决策对照表（哪类内容放哪里）

完善与模板有非平凡差异的文件前，应先阅读相关参考章节。
