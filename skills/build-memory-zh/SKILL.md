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

### 2. 阶段一：审查与提议 (Audit & Propose) - 强制门禁

在任何写入或修改之前，必须先收集事实：
- 顶层文件与目录
- 包管理器 / 语言 / 框架（`package.json`、`pyproject.toml` 等）
- 来自配置脚本的真实命令
- 完整读取工作区中已存在的所有规则受管文件（无论是标准的、 `AGENTS.md` 还是旧的 `CLAUDE.md`、`.cursor/rules` 等）。

**空工作空间检测。** 若检查时未发现源码、包清单、构建配置——即仅含 `.git`、README 等——在写入前先**停下并询问用户**：暂时跳过，或者简述项目生成骨架。不要盲目填充占位符。

对于非空工作空间，输出一份《重构计划清单》，明确列出：
1. 缺少哪些基础设施（如 `.memory/session_log.py` 需要物理拷贝）。
2. 发现了哪些现有的项目核心业务规则、评价原则等，并明确承诺这些内容将被**原封不动地保留**。
3. 计划如何重组 `AGENTS.md` 和 `CLAUDE.md`。

<HARD-GATE>
必须停下来等待用户的明确批准。在获得批准前，绝不能进行下一步实质性修改或写入。
</HARD-GATE>

### 3. 阶段二：物理基建强行挂载 (Infrastructure Scaffolding)

一旦获得用户批准，**第一步永远是物理复刻资产**。
- 无论项目中是否存在旧的或非标准的规则文件夹，你都**必须**将 Skill 中的 `assets/.memory/` 目录及其内部脚本完整复制到项目的根目录下。
- 绝不允许“借用旧框架”或“迎合非标准结构”。标准的 `.memory` 目录及 `session_log.py` 是不可动摇的基础设施。

### 4. 阶段三：差量融合与严格分区 (Differential Merging)

在创建缺失文件或完善已有文件时，必须遵循带有严格分区的“差量融合（Differential Merging）”原则。**整体结构必须强制对齐模板的骨架（Headings）**，但各区块内容的处理方式不同：

**绝对红线区 (Strict Zone)**：
- 对于 `AGENTS.md` 中的 `## Memory Layer` 这一小节，你**必须**一字不差地 100% 复制 `assets/AGENTS.md` 模板中的内容。绝对不允许任何自创、删减或改写，否则会导致记忆系统脚本失效。
- 确保 `CLAUDE.md` 被清理为仅仅保留一句 `@AGENTS.md` 的引用，杜绝在 `CLAUDE.md` 中冗余具体规则。

**通用基线区 (Baseline Zone)**：
- 对于 `## Working Rules` 和 `## Done Criteria` 这类通用的 Agent 工作规范，应当**完全保留模板中的标准表述**。
- 如果旧规则中存在针对该项目的“特殊完成标准”或“特定工作纪律”，你必须将它们**追加 (Append)** 到模板内容的末尾，绝不可用模板直接覆盖掉项目的个性化纪律。

**灵活保留区 (Flexible Zone)**：
- 现有的核心业务原则、架构约束等，必须根据具体情况填入对应的 Heading 下。**严禁以对齐模板的名义默默丢弃**。
- 如果旧规则实在难以归类到模板现有的 Heading 中，必须为它们创建专门的 Heading（如 `## 本地核心业务规则`）并原样保留。

针对具体的缺失文件创建：读取 `assets/` 模板，翻译标题，填充验证过的事实。
**冷启动播种**：如果工作区存在 `.git` 且你是首次创建 `SESSION_LOG.md`，你应当使用 `git log -n 5 --since="7 days ago" --oneline` 读取近期记录，将其归纳为简要的背景上下文，并立刻调用 `python .memory/session_log.py --done "从 Git 历史导入的近期背景: [你的归纳]"` 写入一条初始记录。
绝不编造命令或时间戳。未经批准绝不覆盖已有的 `.memory/KNOWLEDGE.md` 或手动篡改 `SESSION_LOG.md`（必须通过脚本）。

| 文件 | 角色 | 目标 |
|------|------|------|
| `AGENTS.md` | 面向所有 code agent 的项目主仓库指南（含所有规则、栈与命令） | 200–400 词 |
| `CLAUDE.md` | Claude 极简入口；**必须**包含 `@AGENTS.md` 引用 | 1–3 行 |
| `CHANGELOG.md` | 面向发布；仅记录版本级条目 | — |
| `SESSION_LOG.md` | Agent 操作日志；按会话时间戳记录 | — |
| `TODO.md` | 用户主导的 backlog；仅 `Pending` / `Done`（无 `In progress`） | — |
| `.memory/session_log.py` | 推荐的 session log 写入脚本，包含锁重试、7 天归档和 lesson 候选提示 | — |
| `.memory/KNOWLEDGE.md` | 长期可复用经验和稳定决策；仅按需读取 | — |

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
