# Repository Guidelines

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

## 代码风格与命名约定

- 使用 `<formatter-or-linter>` 格式化；不要手动格式化大段 diff。
- 遵循 `<language/framework-specific project convention>`。
- 使用 `<naming-pattern>` 命名 `<components/functions/files>`。
- 优先沿用项目已有模式，避免引入新抽象。

## 测试规范

- 行为变更需新增或更新测试。
- 开发期间偏好聚焦测试；定型大范围改动前运行 `<full-verification-command>`。
- 新增测试就近放在被测代码附近，除非已有约定另作规定。
- 修复 bug 时，可行情况下补充回归测试。

## 完成标准

修改完成需满足以下条件：
- 相关测试通过，或失败已记录并附计划。
- Lint 与 typecheck 通过，或阻塞项已显式说明。
- 构建成功，或破坏已被确认并跟踪。

## 提交与 Pull Request 规范

- Commit message 遵循 `<commit-style>`。
- PR 需包含：摘要、测试证据、关联 issue，UI 改动需附截图。
- 保持 diff 聚焦；避免无关重构。

## 安全与配置

- 不得提交 secrets、token、私钥或真实凭据。
- 本地配置使用 `<env-file-example>`。
- 新增生产依赖或修改部署/安全敏感代码前需确认。

## 日期与文档头

- 时间戳一律用 shell（`date`、`Get-Date`）获取，禁止凭记忆编造；评估 / 方案 / 报告等独立文档在顶部加 `> 创建于：YYYY-MM-DD HH:MM` 一行。

## 跟踪文件

- `SESSION_LOG.md`：在文件变更或留下未解决事项后追加简短的会话级条目；同一时间戳可聚合多条相关更改；修复 bug 时如有复用价值，记录现象、根因、踩坑点与最终修复。
- `TODO.md`：用户主导、agent 辅助的 backlog；默认不读取或编辑；建议更新由用户批准后再应用。
- `CHANGELOG.md`：面向发布的变更日志；仅在用户可见或发布相关变更时更新。
