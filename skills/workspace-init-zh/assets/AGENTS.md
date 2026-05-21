# Repository Guidelines

## 项目概述

本仓库为 `<project-name>`，`<one-sentence purpose>`。
主要用户为 `<user/customer/system>`。
主要产品形态为 `<web-app/api/cli/mobile/etc>`。

## 技术栈

- 语言/运行时：`<language and version>`
- 框架：`<frameworks>`
- 包管理器：`<npm/pnpm/yarn/bun/poetry/uv/cargo/go/etc>`
- 数据库/存储：`<database/storage>`
- 测试栈：`<test frameworks>`
- 部署/运行环境：`<deployment target>`

IMPORTANT：依赖操作使用 `<package-manager>`，不要使用 `<disallowed-package-manager>`。

## 项目结构与模块组织

- 源代码位于 `<src-or-app-dir>/`。
- 测试位于 `<test-dir>/`，遵循 `<naming-pattern>` 命名约定。
- 公共工具位于 `<shared-dir>/`。
- 配置与部署文件位于 `<config-or-infra-dir>/`。
- 不要修改生成目录，例如 `<generated-dir>/`。

## 构建、测试与开发命令

- `<install-command>`：安装依赖。
- `<dev-command>`：启动本地开发服务器。
- `<build-command>`：创建生产构建。
- `<lint-command>`：运行 lint 检查。
- `<typecheck-command>`：运行类型检查。
- `<test-command>`：运行标准测试套件。
- `<single-test-command example>`：开发期间运行单个测试。
- `<migration-command>`：数据库迁移。

## 代码风格与命名约定

- 使用 `<formatter-or-linter>` 格式化；不要手动格式化大段 diff。
- 遵循 `<language/framework-specific project convention>`。
- 使用 `<naming-pattern>` 命名 `<components/functions/files>`。
- 优先沿用项目已有模式，避免引入新抽象。
- 避免 `<anti-pattern specific to this repo>`。

## 架构约束

- `<module/service>` 负责 `<responsibility>`。
- `<module/service>` 不得 import `<forbidden layer>`。
- `<clients/users>` 关心公共 API 兼容性。
- 鉴权/授权逻辑位于 `<path>`。
- Feature flag 定义于 `<path>`。

## 工作规则

- 先探索：编辑前阅读相关文件与已有测试。
- 改动范围限于请求的任务。
- 新增生产依赖前需确认。
- 实现类任务以以下内容收尾：变更文件、变更内容、已运行的验证命令、待跟进事项。

## 测试规范

- 行为变更需在 `<test location convention>` 附近新增或更新测试。
- 开发期间偏好聚焦测试；定型大范围改动前运行 `<full-verification-command>`。
- 修复 bug 时尽量补充回归测试。
- 不要在未说明原因的情况下跳过失败的测试。
- 若本地无法运行验证，说明原因并提供用户应运行的具体命令。

## 完成标准

一个会话或修改任务被视为“完成”需满足以下条件：
- **需求闭环**：用户的原始请求都已完全实现，没有遗漏。
- **范围最小化**：已审查 Diff，变更范围严格限制在目标内，无不相关的文件改动或意外的代码格式化。
- **验证通过**：相关测试、Lint 与类型检查通过；若无法通过或环境受限，阻塞原因与修复计划已显式记录。
- **风险评估**：关键修改的潜在副作用或影响范围已被评估并告知用户。
- **构建成功**：项目能够成功构建，或已知破坏已被确认并跟踪。

## 提交与 Pull Request 规范

- Commit message 遵循 `<commit-style>`。
- PR 需包含：摘要、测试证据、关联 issue，UI 改动需附截图。
- 保持 diff 聚焦；避免无关重构。

## 安全与配置

- 不得提交 secrets、token、私钥或真实客户数据。
- 本地配置使用 `<env-file-example>` 为模板。
- 将 `<security-sensitive-paths>` 下的改动视作安全敏感。
- 修改鉴权、权限、加密、计费、部署配置前需确认。

## 日期与文档头

- 时间戳一律用 shell（`date`、`Get-Date`）获取，禁止凭记忆编造；评估 / 方案 / 报告等独立文档在顶部加 `> 创建于：YYYY-MM-DD HH:MM` 一行。

## 跟踪文件

- `SESSION_LOG.md`：在文件变更或留下未解决事项后追加简短的会话级条目；同一时间戳可聚合多条相关更改；修复 bug 时如有复用价值，记录现象、根因、踩坑点与最终修复。
- `TODO.md`：用户主导、agent 辅助的 backlog；默认不读取或编辑；如果会话结束有待解决的遗留事项可建议用户更新TODO，由用户批准后再应用。
- `CHANGELOG.md`：面向发布的变更日志；仅在用户可见或发布相关变更时更新。

## 已知坑点

- `<gotcha 1>`
- `<gotcha 2>`
- `<gotcha 3>`
