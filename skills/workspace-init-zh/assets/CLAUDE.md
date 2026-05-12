# CLAUDE.md

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

## 仓库地图

- `<dir>/`：`<purpose>`
- `<dir>/`：`<purpose>`
- `<dir>/`：`<purpose>`
- `<dir>/`：生成代码；不要直接编辑。
- `<dir>/`：测试与 fixtures。

## 常用命令

- 安装依赖：`<command>`
- 启动开发服务器：`<command>`
- 运行 lint：`<command>`
- 运行 typecheck：`<command>`
- 运行单元测试：`<command>`
- 运行单个测试：`<command example>`
- 构建：`<command>`
- 数据库迁移：`<command>`

迭代时偏好聚焦测试。定型大范围改动前运行 `<final-verification-command>`。

## 工作规则

- 先探索：编辑前阅读相关文件与已有测试。
- 优先沿用已有模式，不引入新抽象。
- 改动范围限于请求的任务。
- 不要修改 `<generated-dir>` 中的生成文件；改动 `<source-of-truth>`。
- 新增生产依赖前需确认。
- 行为变更需新增或更新测试。
- UI 改动尽量附截图或人工验证记录。
- 实现类任务以以下内容收尾：变更文件、变更内容、已运行的验证命令、待跟进事项。

## 代码约定

- 格式化由 `<formatter>` 处理。
- Lint 由 `<linter>` 处理。
- `<files/components/functions>` 使用 `<naming convention>`。
- 遵循 `<project-specific convention that is not obvious from defaults>`。
- 避免 `<anti-pattern specific to this repo>`。

## 架构约束

- `<module/service>` 负责 `<responsibility>`。
- `<module/service>` 不得 import `<forbidden layer>`。
- `<clients/users>` 关心公共 API 兼容性。
- 鉴权/授权逻辑位于 `<path>`。
- Feature flag 定义于 `<path>`。

## 测试与验证

- 新行为应在 `<test location convention>` 附近补充测试。
- 修复 bug 时尽量补充回归测试。
- 不要在未说明原因的情况下跳过失败的测试。
- 若本地无法运行验证，说明原因并提供用户应运行的具体命令。

## 安全与凭据

- 不得提交 secrets、凭据、私钥或真实客户数据。
- 本地环境变量以 `<example env file>` 为模板。
- 将 `<security-sensitive-paths>` 下的改动视作安全敏感。
- 修改鉴权、权限、加密、计费、部署配置前需确认。

## 日期与文档头

- 时间戳一律用 shell（`date`、`Get-Date`）获取，禁止凭记忆编造；评估 / 方案 / 报告等独立文档在顶部加 `> 创建于：YYYY-MM-DD HH:MM` 一行。

## 跟踪文件

- `SESSION_LOG.md`：在文件变更或留下未解决事项后追加简短的会话级条目；同一时间戳可聚合多条相关更改。
- `TODO.md`：用户主导的 backlog；默认不读取或编辑，除非另有要求。
- `CHANGELOG.md`：面向发布的变更日志；仅在用户可见或发布相关变更时更新。

## 已知坑点

- `<gotcha 1>`
- `<gotcha 2>`
- `<gotcha 3>`
