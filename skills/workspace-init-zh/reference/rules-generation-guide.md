# 规则生成指南

本文件规定如何为项目生成 `AGENTS.md` 与 `CLAUDE.md`。两份文件面向不同的 Agent，遵循不同的约定，因此分别说明。第一节按 OpenAI Codex 官方指南撰写 `AGENTS.md`；第二节结合 Anthropic 官方文档与社区实践撰写 `CLAUDE.md`。

## 一、生成 `AGENTS.md`（OpenAI Codex 指南）

### 1.1 背景

按照 OpenAI Codex 官方文档，`AGENTS.md` 是 Codex 在开始工作前读取的持久项目指令文件。Codex 按层级合并指令：全局、仓库根目录及当前工作目录沿途的 `AGENTS.md`；越靠近当前目录的文件越晚出现，可覆盖前面的规则。系统同时支持 `AGENTS.override.md` 高优先级覆盖、可配置的 fallback 文件名，以及默认 32 KiB 的项目文档大小限制。([OpenAI Developers][1])

Codex `/init` 命令会在当前目录生成 `AGENTS.md` scaffold，需要人工 review 并按仓库约定调整。([OpenAI Developers][2]) Codex 仓库公开的 `/init` prompt 要求生成一份名为 “Repository Guidelines” 的贡献者指南，长度约 200–400 词，覆盖项目结构、构建/测试/开发命令、代码风格、测试规范、提交与 PR 规范，并可按需加入安全、配置、架构或 agent-specific 指令。([GitHub][3])

### 1.2 生成流程

**第一步——确定作用域。** 普通项目将 `AGENTS.md` 放在仓库根目录。Monorepo 或多服务仓库在根目录放通用规则，在 `services/payments/AGENTS.md` 或 `AGENTS.override.md` 放局部规则。不要将所有子项目规则集中至根文件。

**第二步——查看项目整体结构。** 通过 `tree -L 2` 或等价命令检查目录结构，排除 `node_modules`、`dist`、`.next`、`target`、`build`、`.venv` 等生成目录。目标是识别源码、测试、文档、脚本、配置、部署文件的位置。

**第三步——识别技术栈与命令来源。** 阅读 `package.json`、`pnpm-workspace.yaml`、`pyproject.toml`、`requirements.txt`、`Cargo.toml`、`go.mod`、`pom.xml`、`Makefile`、`justfile`、`Dockerfile`、`.github/workflows/*`、`README.md`。优先从项目已有脚本与 CI 中提取 build、test、lint、typecheck、dev 命令，而非根据技术栈推断。

**第四步——提取代码规范。** 读取格式化、lint、类型检查配置，例如 ESLint、Prettier、Biome、Ruff、Black、mypy、tsconfig、rustfmt、golangci-lint。仅记录“项目特有”或“易出错”的规范，不记录语言常识。

**第五步——识别测试约定。** 检查测试目录、命名模式、测试框架；判断是否偏好单测优先、是否有 e2e、是否要求覆盖率、是否有慢测试标签。明确指出“修改后应运行哪些验证命令”。

**第六步——查阅 Git 历史与 PR 习惯。** 通过最近若干条 commit 总结是否使用 Conventional Commits、scope、issue 编号、PR 描述、截图、变更日志。不得臆造团队流程。

**第七步——撰写短、明确、可执行的规则。** Codex `/init` prompt 推荐 200–400 词，适合根 `AGENTS.md`。复杂项目通过分层文件解决，避免单文件过长。([GitHub][3])

**第八步——人工审核。** 重点检查：命令是否真实存在、规则是否稳定、是否泄露 secret、是否存在过期路径、是否存在“写干净代码”一类无效规则。

### 1.3 内容指引

| 应写 | 不应写 |
|------|--------|
| 项目结构与关键目录 | 文件逐个解释 |
| build/test/lint/dev 命令 | 工具文档全文 |
| 项目特有代码风格 | 标准语言常识 |
| 测试框架、命名、验证要求 | “尽量多测试”一类空话 |
| 提交、PR、review 习惯 | 临时任务计划 |
| 安全与配置注意事项 | API key、密码、真实 token |
| 架构约束与常见坑 | 易变的路线图 |
| 子目录专属 override 规则 | 全部服务规则混入根文件 |

### 1.4 `AGENTS.md` 模板

```md
# Repository Guidelines

## Project Structure & Module Organization

- Source code lives in `<src-or-app-dir>/`.
- Tests live in `<test-dir>/` and follow the `<naming-pattern>` convention.
- Shared utilities are in `<shared-dir>/`.
- Configuration and deployment files are in `<config-or-infra-dir>/`.
- Do not edit generated directories such as `<generated-dir-1>/`, `<generated-dir-2>/`.

## Build, Test, and Development Commands

- `<install-command>`: install dependencies.
- `<dev-command>`: start the local development server.
- `<build-command>`: create a production build.
- `<lint-command>`: run lint checks.
- `<typecheck-command>`: run type checks.
- `<test-command>`: run the standard test suite.
- `<single-test-command example>`: run a targeted test while iterating.

## Coding Style & Naming Conventions

- Use `<formatter-or-linter>` for formatting; do not hand-format large diffs.
- Follow `<language/framework-specific project convention>`.
- Name `<components/functions/files>` using `<naming-pattern>`.
- Prefer existing project patterns over introducing new abstractions.

## Testing Guidelines

- Add or update tests for behavior changes.
- Prefer focused tests during development; run `<full-verification-command>` before finalizing broad changes.
- Place new tests near the code they cover unless the existing pattern says otherwise.
- For bug fixes, include a regression test when practical.

## Commit & Pull Request Guidelines

- Commit messages follow `<commit-style>`, for example `<example-commit>`.
- PRs should include: summary, test evidence, linked issue, and screenshots for UI changes.
- Keep diffs focused; avoid unrelated refactors.

## Security & Configuration

- Never commit secrets, tokens, private keys, or real credentials.
- Use `<env-file-example>` for local configuration.
- Ask before adding production dependencies or changing deployment/security-sensitive code.

## Dates & Document Headers

- Obtain timestamps from the shell (`date`, `Get-Date`); never invent them. Standalone documents (reports, plans, assessments) carry a `> Created: YYYY-MM-DD HH:MM (TZ)` line near the top.

## Agent-Specific Instructions

- Before editing, inspect the relevant files and existing patterns.
- After changes, run the smallest relevant verification command, then the broader suite when warranted.
- If a command fails, report the exact command and failure summary.
```

## 二、生成 `CLAUDE.md`（官方与社区实践）

### 2.1 背景

按 Anthropic 官方文档，`CLAUDE.md` 是 Claude Code 在每个 session 启动时读取的持久指令文件，用于项目级、个人级或组织级上下文，适合放置 build 命令、编码规范、工作流、项目架构等。文档强调 `CLAUDE.md` 是上下文而非强制配置：越具体、越简短，遵循越稳定。([Claude][4])

Claude `/init` 命令会分析代码库并生成初始 `CLAUDE.md`，包含 build commands、test instructions 与检测到的项目约定。若已存在 `CLAUDE.md`，`/init` 会建议改进而非覆盖。设置 `CLAUDE_CODE_NEW_INIT=1` 可启用交互式多阶段流程，配置 `CLAUDE.md`、skills、hooks。([Claude][4])

最佳实践指南更具规定性：`CLAUDE.md` 没有固定格式，但必须短、可读；只放每个 session 都广泛适用的信息。官方原则：若删除某一行不会导致 Claude 犯错，则应删除；偶尔相关的领域知识或工作流，应放入 skill，而不是污染每次会话。([Claude][5])

社区实践与官方方向一致，但更强调上下文工程。HumanLayer 将 `CLAUDE.md` 视作 Claude 的 onboarding 文档，覆盖 WHAT、WHY、HOW：项目是什么、为何如此组织、Claude 应如何构建与验证。少即是多，采用渐进披露，不要堆砌所有命令、规范、代码片段，应优先指向权威文件。([HumanLayer][6])

### 2.2 生成流程

**第一步——先做 repo onboarding，再写规则。** 阅读 `README.md`、`docs/`、架构说明、主要 package manifest、CI 配置与顶层目录。目标是让 Claude 了解“项目是什么、主要模块在哪里、如何验证修改”。

**第二步——识别技术栈。** 记录语言、框架、包管理器、数据库、测试框架、构建系统、部署方式。仅记录对 Claude 决策有影响的信息，例如“本项目使用 pnpm，不用 npm”“API schema 由 OpenAPI 生成，不要手改 generated client”。

**第三步——识别工作命令。** 5–8 条高价值命令即可：安装、开发、lint、typecheck、单测、e2e、build、数据库迁移。命令必须来自 package scripts、Makefile、CI 或官方文档。

**第四步——识别项目架构与边界。** 记录模块职责、数据流、重要不变量、不可破坏的兼容性要求。不要逐文件描述用途；Claude 可自行读取文件。

**第五步——识别 Claude 容易犯错之处。** 例如包管理器选择、生成代码、迁移流程、测试环境依赖、异步任务、权限模型、feature flag、monorepo workspace 边界。这些比泛泛的“写高质量代码”更有价值。

**第六步——将内容分散至其他位置。** 按 Claude 文档，`.claude/rules/` 支持 topic / path-scoped 规则，skills 支持可复用工作流，hooks 适合每次必须确定执行的动作；不要把所有内容塞进 `CLAUDE.md`。([Claude][7])

**第七步——通过 `@` 引用做渐进披露。** `CLAUDE.md` 支持 `@path/to/file` 引入其他文件。优先使用指针而非内联长内容，以避免过期与上下文膨胀。([Claude][5])

**第八步——控制长度并持续修剪。** 将 `CLAUDE.md` 视作代码维护：当 Claude 反复犯同一错误时增加规则；当规则不再影响行为时删除；当 Claude 忽略规则时，文件通常过长或措辞不清。([Claude][5]) `.claude` 目录文档建议长度控制在 200 行以内，更长的文件虽会加载，但遵循度下降。([Claude][8])

### 2.3 内容指引

| 应写 | 不应写 |
|------|--------|
| 项目目的与核心架构 | README 长篇复制 |
| Claude 每次都需要的稳定规则 | 仅与某个临时任务相关的信息 |
| 不易从代码推断的命令 | `package.json` 中已列脚本逐条复制 |
| 包管理器、测试策略、验证命令 | 通用语言教程 |
| 项目特有约束与常见坑 | “写 clean code” |
| 生成代码、迁移、安全边界 | secrets、真实账号、生产 token |
| 指向权威 docs 的 `@` 引用 | 大段 API 文档 |
| compact 时必须保留的信息 | 高频变化的路线图与排期 |

### 2.4 `CLAUDE.md` 模板

```md
# CLAUDE.md

## Project Overview

This repository is `<project-name>`, a `<one-sentence purpose>`.
The primary users are `<user/customer/system>`.
The main product surfaces are `<web-app/api/cli/mobile/etc>`.

For general setup and product context, read @README.md.
For deeper architecture, read @docs/architecture.md when relevant.

## Tech Stack

- Language/runtime: `<language and version>`
- Frameworks: `<frameworks>`
- Package manager: `<npm/pnpm/yarn/bun/poetry/uv/cargo/go/etc>`
- Database/storage: `<database/storage>`
- Test stack: `<test frameworks>`
- Deployment/runtime: `<deployment target>`

IMPORTANT: Use `<package-manager>` for dependency operations. Do not use `<disallowed-package-manager>`.

## Repository Map

- `<dir>/`: `<purpose>`
- `<dir>/`: `<purpose>`
- `<dir>/`: `<purpose>`
- `<dir>/`: generated code; do not edit directly.
- `<dir>/`: tests and fixtures.

For monorepo workspace details, read @<workspace-config-file>.

## Common Commands

- Install dependencies: `<command>`
- Start dev server: `<command>`
- Run lint: `<command>`
- Run typecheck: `<command>`
- Run unit tests: `<command>`
- Run a single test: `<command example>`
- Build: `<command>`
- Database migration: `<command>`

Prefer targeted tests while iterating. Before finalizing a broad code change, run `<final-verification-command>`.

## Working Rules

- Explore first: read the relevant files and existing tests before editing.
- Prefer existing patterns over new abstractions.
- Keep changes scoped to the requested task.
- Do not modify generated files in `<generated-dir>`; update `<source-of-truth>` instead.
- Ask before adding new production dependencies.
- For behavior changes, add or update tests.
- For UI changes, include screenshot or manual verification notes when possible.

## Code Conventions

- Formatting is handled by `<formatter>`.
- Linting is handled by `<linter>`.
- Use `<naming convention>` for `<files/components/functions>`.
- Follow `<project-specific convention that is not obvious from defaults>`.
- Avoid `<anti-pattern specific to this repo>`.

## Architecture Constraints

- `<module/service>` owns `<responsibility>`.
- `<module/service>` must not import from `<forbidden layer>`.
- Public API compatibility matters for `<clients/users>`.
- Authentication/authorization logic lives in `<path>`; do not duplicate it elsewhere.
- Feature flags are defined in `<path>`.

## Testing and Verification

- New behavior should have tests near `<test location convention>`.
- Bug fixes should include regression tests when practical.
- Do not skip failing tests without explaining the failure.
- If verification cannot be run locally, state why and provide the exact command the user should run.

## Security and Secrets

- Never commit secrets, credentials, private keys, or real customer data.
- Use `<example env file>` as the template for local environment variables.
- Treat changes under `<security-sensitive-paths>` as security-sensitive.
- Ask before changing auth, permissions, encryption, billing, or deployment configuration.

## Context Management

- Keep summaries of changed files and test commands when compacting.
- Use @docs/<specific-doc>.md for detailed procedures instead of copying them here.
- If a workflow is long or task-specific, propose moving it to `.claude/skills/` or `.claude/rules/`.

## Dates & Document Headers

- Obtain timestamps from the shell (`date`, `Get-Date`); never invent them. Standalone documents (reports, plans, assessments) carry a `> Created: YYYY-MM-DD HH:MM (TZ)` line near the top.

## Known Gotchas

- `<gotcha 1>`
- `<gotcha 2>`
- `<gotcha 3>`
```

### 2.5 可选小节

#### Claude Code 工作流

推荐写法：

```md
## Claude Code specific instructions

### Workflow

- For non-trivial changes, first inspect relevant files, then propose a short plan, then edit.
- Use Plan Mode for broad refactors, migrations, architecture changes, or tasks touching more than 5 files.
- Before editing, identify the smallest set of files required.
- Do not perform unrelated cleanup while implementing a requested change.
```

此小节适合放置 Claude Code 行为要求，但不应写入通用工程规则；通用规则放在 `AGENTS.md`。

#### Context management

用于减少盲目读文件、上下文浪费与输出过长：

```md
### Context management

- Prefer targeted file reads over scanning the whole repository.
- Summarize large files before making changes.
- Do not paste long command outputs into the final response; summarize key failures and fixes.
- When context is insufficient, inspect nearby files before asking for clarification.
```

#### Tool usage

说明项目内的工具使用策略：

```md
### Tool usage

- Use search tools before editing unfamiliar modules.
- Use project skills for repeated multi-step workflows.
- Use subagents for large read-heavy investigations, security review, or cross-module analysis.
- Do not use broad automated rewrites unless the task explicitly requires them.
```

不要将工具配置本身写入 `CLAUDE.md`，例如权限、hooks、MCP 服务器配置。这些应放入对应的配置文件。

#### Skills 与 subagents

若项目存在 Claude skills 或 subagents，可在 `CLAUDE.md` 中说明使用时机：

```md
### Skills and subagents

- Use the `pr-review` skill for pull request review tasks.
- Use the `migration-reviewer` subagent for database migration changes.
- Use the `security-reviewer` subagent for authentication, authorization, payment, and secret-handling changes.
```

不要将 skill 完整流程写入 `CLAUDE.md`。复杂流程应放入 `.claude/skills/<skill-name>/SKILL.md`。

#### 最终回复格式

规定 Claude Code 完成任务后的汇报格式：

```md
### Final response format

For implementation tasks, end with:

- Changed files
- What changed
- Validation commands run
- Known risks or follow-up items
```

固定格式可使输出更稳定，便于人工 review。

## 三、`AGENTS.md` 与 `CLAUDE.md` 的差异化写法

`AGENTS.md` 类似 Codex 的 repo-level contributor guide。按 OpenAI `/init` prompt，应短、结构化、面向贡献，重点是目录、命令、测试、风格、提交与 PR 规范。([GitHub][3])

`CLAUDE.md` 类似 Claude Code 的 session onboarding 与行为约束。除了告知 Claude 如何贡献代码，还需告知项目的 WHY、WHAT、HOW，以及哪些上下文应通过 `@`、rules、skills、hooks 渐进加载。Anthropic 明确建议 `CLAUDE.md` 仅放置广泛适用内容；偶尔相关的领域知识或工作流应改用 skills。([Claude][5])

同时支持 Codex 与 Claude Code 的项目，推荐结构：

```txt
repo/
  AGENTS.md              # 跨 agent 的核心仓库规则，偏贡献指南
  CLAUDE.md              # Claude Code 专用入口，可引用 AGENTS.md
  docs/
    architecture.md
    testing.md
    release.md
  .claude/
    rules/
      frontend.md
      backend.md
      migrations.md
    skills/
      fix-ci/
        SKILL.md
```

`CLAUDE.md` 引用示例：

```md
# CLAUDE.md

Read @AGENTS.md for shared repository guidelines.

Additional Claude Code instructions:

- Use `/clear` between unrelated tasks.
- When compacting, preserve the list of modified files, decisions, and verification commands.
- For long workflows, prefer relevant `.claude/skills/` or `.claude/rules/` files over expanding this file.
```

核心原则：根文件仅放“每次 agent 开工都必须知道”的稳定事实与规则；细节、教程、长流程、偶发任务放入 docs、rules、skills 或 hooks。这比把所有内容堆入单个 Markdown 文件更可靠。

## 四、独立维护（不互相引用）

`CLAUDE.md` 无需 `@AGENTS.md`，两套规则可保持完全独立。

更准确地：

- `AGENTS.md` 是给 Codex 与兼容 AGENTS.md 的 agent 读取的项目规则。
- `CLAUDE.md` 是给 Claude Code 读取的项目记忆文件。

Claude Code 不会天然要求 `AGENTS.md`。仅当 `CLAUDE.md` 中显式 `@AGENTS.md` 时才作为上下文引入。若希望两者解耦，省略 import 即可。

适合独立维护的场景：

| 场景 | 建议 |
|------|------|
| Codex 与 Claude 使用不同工作流 | 独立维护 |
| 两个工具的能力、偏好、命令习惯不同 | 独立维护 |
| 不希望 Claude 继承 Codex-specific 指令 | 不要 `@AGENTS.md` |
| 团队希望规则更可控、隐式上下文更少 | 独立维护 |
| 两份文件存在大量共同内容、维护成本高 | 考虑共享引用 |

需注意的风险：文件独立后易出现规则漂移。例如：

```txt
AGENTS.md: 使用 pnpm
CLAUDE.md: 使用 npm
```

```txt
AGENTS.md: 不要编辑 generated/
CLAUDE.md: 未提及 generated/，Claude 可能修改
```

独立维护时应采用“语义独立、结构对齐”：两份文件不互相引用，但 section 结构相近，便于人工同步。

推荐结构：

```txt
repo/
  AGENTS.md
  CLAUDE.md
```

`AGENTS.md`（偏 Codex）：

```md
# Repository Guidelines

## Project Structure
...

## Build, Test, and Development Commands
...

## Coding Style
...

## Testing Guidelines
...

## Commit and PR Guidelines
...

## Agent-Specific Instructions
...
```

`CLAUDE.md`（偏 Claude）：

```md
# CLAUDE.md

## Project Overview
...

## Tech Stack
...

## Repository Map
...

## Common Commands
...

## Working Rules
...

## Code Conventions
...

## Testing and Verification
...

## Known Gotchas
...
```

若希望工具隔离同时避免分叉，不要在 `CLAUDE.md` 中 `@AGENTS.md`，但应让两份文件共享同一组事实来源——`README.md`、`docs/architecture.md`、`package.json`、CI 配置——而非互相引用。这样规则独立，但不会长期偏离。

## 五、附录：内容决策对照表

### 5.1 应该写入的内容

| 类型 | 示例 | 推荐文件 |
|------|------|----------|
| 技术栈 | `Next.js + TypeScript + PostgreSQL` | `AGENTS.md` |
| 包管理器 | `Use pnpm, not npm or yarn` | `AGENTS.md` |
| 启动命令 | `pnpm dev` | `AGENTS.md` |
| 测试命令 | `pnpm test -- path/to/file.test.ts` | `AGENTS.md` |
| 架构边界 | `UI must not import database clients` | `AGENTS.md` |
| 高风险约束 | `Do not delete migrations without approval` | `AGENTS.md` |
| 完成标准 | `Relevant checks must pass or blockers documented` | `AGENTS.md` |
| 日期/时间纪律 | `时间须用 shell date 取；报告类文档头部需 Created:` | 同时写入 `AGENTS.md` 与 `CLAUDE.md` |
| Claude 工作方式 | `Use Plan Mode for broad refactors` | `CLAUDE.md` |
| Claude subagent 策略 | `Use security-reviewer for auth changes` | `CLAUDE.md` |
| Claude 输出格式 | `Changed files / Validation / Risks` | `CLAUDE.md` |

### 5.2 不应该写入的内容

| 类型 | 不推荐原因 | 应放位置 |
|------|------------|----------|
| 大段框架教程 | 浪费上下文，易过期 | `docs/` 或外部文档 |
| 临时需求 | 污染长期规则 | 当前任务 prompt |
| 个人偏好 | 不适合团队共享 | user-level 或 local 文件 |
| 密钥、token、账号密码 | 安全风险 | 不应写入仓库 |
| 权限配置 | 自然语言不具备硬约束 | settings / sandbox / hooks |
| 复杂流程 | 主文件过长，影响遵循 | `.claude/skills/` |
| 路径专属细则 | 每次加载浪费上下文 | `.claude/rules/` |
| Subagent 人设全文 | 主文件臃肿 | `.claude/agents/` 或 `.codex/agents/` |
| 重复规则 | 增加冲突概率 | 删除或合并 |
| 过期规则 | 误导 Agent | 定期清理 |

---

## 引用

[1]: https://developers.openai.com/codex/guides/agents-md "Custom instructions with AGENTS.md – Codex | OpenAI Developers"
[2]: https://developers.openai.com/codex/cli/slash-commands "Slash commands in Codex CLI | OpenAI Developers"
[3]: https://github.com/openai/codex/blob/main/codex-rs/tui/prompt_for_init_command.md "codex/codex-rs/tui/prompt_for_init_command.md at main · openai/codex · GitHub"
[4]: https://code.claude.com/docs/en/memory "How Claude remembers your project - Claude Code Docs"
[5]: https://code.claude.com/docs/en/best-practices "Best practices for Claude Code - Claude Code Docs"
[6]: https://www.humanlayer.dev/blog/writing-a-good-claude-md "Writing a good CLAUDE.md | HumanLayer Blog"
[7]: https://code.claude.com/docs/en/claude-directory "Explore the .claude directory - Claude Code Docs"
[8]: https://code.claude.com/docs/en/claude-directory "Explore the .claude directory - Claude Code Docs"
