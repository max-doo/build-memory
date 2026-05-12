# Changelog

本项目所有显著变更都会记录在此文件中。

<!--
面向发布的变更日志。仅记录用户可见或与发布相关的变更。

规则：
- 使用版本级时间戳（## [version] - YYYY-MM-DD），不在此处放置 commit 级别的分钟时间戳。
- 会话级操作记录请放入 SESSION_LOG.md，不要写在这里。
- 发布时将 [Unreleased] 中的条目移入对应版本号的小节（例如 ## [1.1.0] - 2026-05-04）。
- 留空的小节（Removed、Security 等）可删除。
-->

## [Unreleased]

### Added

- 空工作空间处理：检测到目录仅含 `.git` / README / dotfiles 时，skill 暂停并询问用户（跳过 / 描述项目 / 生成带 `TODO: empty workspace` 标记的最小骨架），不再静默铺满 `TODO: confirm` 占位符。
- `AGENTS.md` 与 `CLAUDE.md` 模板新增「日期与文档头」一节（单行规则）：时间戳一律用 shell 获取，评估 / 方案 / 报告类独立文档在顶部加 `Created:` 一行。

### Changed

- `SKILL.md` 顶部「非妥协规则」从两条扩展为三条，新增「真实时间」原则。
- `reference/rules-generation-guide.md` 同步更新嵌入模板与 §5.1 内容决策表。
- `workspace-init-zh` 中文版 skill 同步上述变更。

## [1.0.0] - 2026-05-04

首个公开发布版本，确立 `workspace-init` 的基本职责：为项目初始化一套与 AI Agent 协作的基准规则与跟踪文件。

### Added

- 受管文件体系：创建并维护 5 个职责分明的文件——`AGENTS.md`（通用编码规范）、`CLAUDE.md`（Claude 专属会话记忆）、`CHANGELOG.md`（版本级变更）、`SESSION_LOG.md`（会话级操作日志）、`TODO.md`（用户主导的待办清单）。
- 工作空间扫描：写入前先检查顶层目录、`package.json` / `pyproject.toml` / `Cargo.toml` 等构建文件、`Makefile` 与 CI 配置中的真实命令，以及是否已存在同义文件（如 `agent.md`、`WORKLOG.md`）。无法从仓库确认的字段一律以 `TODO: confirm` 标记保留，绝不编造命令或路径。
- 文件刷新策略：将差异分为「小问题」（措辞、过时命令、缺失记录）和「大问题」（文件角色错误、互相引用、长度超标两倍以上等）；前者直接修复，后者必须先征求用户同意。
- 两条铁律：
  - **独立性**——`AGENTS.md` 与 `CLAUDE.md` 互不引用，允许少量事实重复以保证各自自包含。
  - **无静默覆盖**——任何实质性改写必须先获得用户的明确批准。
- 多语言支持：模板以英文随 skill 分发，根据用户显式指令或输入语言在写入时翻译为目标语言；附带 `README.md` 与 `README-zh.md` 双语说明。
- 跨工具兼容：基于通用的 `SKILL.md` 标准，可在 Claude Code、OpenAI Codex、Cursor、Google Antigravity 中加载使用。
- `TODO.md` 设计：仅保留 `Pending` 与 `Done` 两种状态，不设 `In progress`，避免 Agent 频繁改写并保留用户对进度的主导权。
- 配套参考文档：
  - `reference/tracking-files-guide.md`——`CHANGELOG.md` / `SESSION_LOG.md` / `TODO.md` 的定义、模板、维护规则与决策清单。
  - `reference/rules-generation-guide.md`——`AGENTS.md` / `CLAUDE.md` 的差异化写法与内容归属表。
- 模板资产：`assets/` 目录提供 5 个受管文件的英文基准模板，便于一致化生成。
- MIT 许可证。
