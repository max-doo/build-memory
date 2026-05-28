# 规则生成指南 (Rules Generation Guide)

本文件规定如何为项目生成高质量的、跨 Agent 通用的项目记忆层。

过去的实践往往将 OpenAI Codex 的偏好（极简、按目录层级、重命令）与 Anthropic Claude Code 的偏好（重上下文工程、WHY/WHAT/HOW、渐进披露）拆分为两套不同的哲学。在本项目中，我们将**集各家之长，融为一体**。

我们采用 **单点事实来源 (Single Source of Truth)** 架构：由一份统一的 `AGENTS.md` 承载所有的项目背景、规范和命令，同时兼具极高的结构化和丰富的上下文，让它成为任何 Agent 开工前的最强武器。而 `CLAUDE.md` 则退居为一个轻量级的引导桩（Stub）。

## 一、统一生成流程 (Unified Generation Procedure)

结合了 Codex 的严谨结构与 Claude 的上下文工程，我们提炼出以下 8 步生成法：

**第一步：代码库 Onboarding（明确 WHAT 与 WHY）**
阅读 `README.md`、`docs/`、架构说明与顶层目录。向 Agent 清晰定义项目目的、主要受众以及它解决的问题，避免 Agent 在没有大局观的情况下盲目改代码。

**第二步：识别技术栈与命令来源（从真实配置中提取）**
阅读 `package.json`、`pyproject.toml`、`Cargo.toml`、`Makefile`、CI 配置文件等。提取构建、测试、开发、Lint 的真实命令。**绝对不要凭空编造命令**。指出如“本项目使用 pnpm，禁止使用 npm”之类的硬性约束。

**第三步：提取项目目录结构与架构边界**
通过查看代码，记录核心源码、测试、公共工具和配置文件的位置。明确指出哪些是生成代码（如 `generated/`，不可手工编辑），以及关键模块的职责。

**第四步：提取代码规范与测试约定**
仅记录“项目特有”或“容易出错”的规范。检查测试框架、命名模式，明确指出“功能修改后必须运行哪些验证命令”。不要写“尽量多写测试”、“写干净代码”这种缺乏可执行性的废话。

**第五步：识别容易踩坑的模式（Failure Modes）**
记录 Agent 或新成员容易犯错的地方。例如：包管理器的错误选择、忘记更新 schema、破坏 monorepo 边界、漏掉 feature flag。防患于未然。
Agent 可以从 `.memory/KNOWLEDGE.md` 中判断哪些经验值得提升到 `AGENTS.md`，但必须满足四个条件：跨任务反复出现、误用代价高、无法从代码结构直接看出、可写成一句明确操作规则。不满足这些条件的经验应继续留在 `.memory/KNOWLEDGE.md`，不要扩大默认上下文。

**第六步：利用跟踪文件外化记忆**
配置 Agent 使用 `SESSION_LOG.md` 记录协作日记，使用 `TODO.md` 同步进度。这解决了多个会话间信息隔离的痛点。

**第七步：渐进式信息披露（Progressive Disclosure）**
长篇累牍的框架教程、冗长的复杂工作流、巨型 API 规范会严重浪费上下文窗口。使用 `@` 引用将这些细节分散到 `docs/` 或 `.claude/skills/`，按需加载，保持主规则文件精简。

**第八步：人工复核与持续修剪**
确保文件结构清晰。如果发现规则过时、命令报错、或者包含敏感的 Secret，必须进行清理。将规则文件视作代码一样进行维护。

## 二、内容指引

编写规则时，请遵循以下对照表：

| 应写 | 不应写 |
|------|--------|
| 项目目的与核心架构 (WHAT & WHY) | 把 README 原封不动复制过来 |
| 每次开工都需要的稳定事实与约束 | 只和某个临时任务相关的细节 |
| 无法直接从代码猜出的开发与测试命令 | 把 package.json 里所有脚本抄一遍 |
| 项目特有的架构限制与坑点 (Gotchas) | “请编写高质量且易于维护的代码” |
| 从 `KNOWLEDGE.md` 提升出的高频、高风险、可执行经验 | 普通调试流水、一次性事故复盘 |
| 对追踪文件（SESSION_LOG / TODO）的使用规定 | API Key、真实生产环境的 Token |
| 指向具体细则文档的链接引用（如 `@docs/testing.md`） | 冗长复杂的单任务流程、框架常识 |

## 三、模板结构

### 3.1 核心事实库：`AGENTS.md` 模板

所有的关键指令都在此文件中：

```md
# Repository Guidelines

## Project Overview
This repository is `<project-name>`, a `<one-sentence purpose>`.
The primary users are `<user/customer/system>`.
The main product surfaces are `<web-app/api/cli/mobile/etc>`.

## Tech Stack
- Language/runtime: `<language and version>`
- Frameworks: `<frameworks>`
- Package manager: `<package-manager>`
- Test stack: `<test frameworks>`
- Deployment/runtime: `<deployment target>`

IMPORTANT: Use `<package-manager>` for dependency operations. Do not use `<disallowed-package-manager>`.

## Project Structure & Module Organization
- Source code lives in `<src-or-app-dir>/`.
- Tests live in `<test-dir>/` and follow the `<naming-pattern>` convention.
- Shared utilities are in `<shared-dir>/`.
- Configuration and deployment files are in `<config-or-infra-dir>/`.
- Do not edit generated directories such as `<generated-dir>/`.

## Build, Test, and Development Commands
- `<install-command>`: install dependencies.
- `<dev-command>`: start the local development server.
- `<build-command>`: create a production build.
- `<lint-command>`: run lint checks.
- `<test-command>`: run the standard test suite.

## Coding Style & Naming Conventions
- Use `<formatter-or-linter>` for formatting; do not hand-format large diffs.
- Follow `<language/framework-specific project convention>`.
- Prefer existing project patterns over introducing new abstractions.

## Architecture Constraints
- `<module/service>` owns `<responsibility>`.
- `<module/service>` must not import from `<forbidden layer>`.
- Authentication/authorization logic lives in `<path>`.

## Working Rules & Testing Guidelines
- Explore first: read the relevant files and existing tests before editing.
- Add or update tests for behavior changes near `<test location convention>`.
- Do not skip failing tests without explaining the failure.
- End implementation tasks with: changed files, what changed, validation commands run, and any follow-up items.

## Tracking Files
- `SESSION_LOG.md`: append concise per-session entries after file changes or unresolved issues; record bug symptoms and root causes when reusable.
- `TODO.md`: user-governed, agent-assisted backlog; do not read or edit by default; suggest updates and apply them only after user approval.
- `CHANGELOG.md`: release-facing changelog; only update for release-relevant changes.

## Known Gotchas
- Keep only high-frequency gotchas that must be followed every session here, ideally 3-7 bullets.
- Agents may promote lessons from `.memory/KNOWLEDGE.md` into this section when they are recurring across tasks, costly when missed, not obvious from code structure, and expressible as one concrete operating rule.
```

### 3.2 极简入口：`CLAUDE.md` 模板

通过单向引用，确保信息同步：

```md
# CLAUDE.md

本项目的核心信息、目录结构、开发命令与规范，请统一读取 @AGENTS.md。

## Claude 专属补充说明

- 在不相关的任务之间使用 `/clear`。
- 处理重大变更时，先检查相关文件，提出简短计划，然后再编辑。
- 面对大范围重构、迁移、架构变更或涉及超过 5 个文件的任务时，请使用规划模式 (Plan Mode)。
```

## 四、避免冗余与死循环

千万不要在 `AGENTS.md` 里引用 `@CLAUDE.md`。引用必须是单向的（`CLAUDE.md` -> `AGENTS.md`）。
如果有需要让所有 Agent 都知道的注意事项，它就不应该出现在 `CLAUDE.md`，而应该转移到 `AGENTS.md` 中。这是保持记忆层健康的底线。
