# Session Log

<!--
面向 Agent 的操作日志。仅在会话修改了文件或留下未解决事项时追加简短记录。
使用 `python .memory/session_log.py` 追加记录；不要手工编辑此文件。

规则：
- 此处仅保留最近 7 天窗口；脚本会将更早日期块归档到 `.memory/sessions/`。
- 记录应简短、可审计。
- `lesson` 仅用于可复用调试经验、踩坑点或长期决策，后续可按需沉淀到 `.memory/KNOWLEDGE.md`。
-->

## YYYY-MM-DD

### HH:MM | agent

- done: 本次完成内容摘要
- context: 相关背景或约束
- decision: 本次形成的判断或取舍
- modified:
  - `path/to/file`
- lesson: 可复用调试经验、踩坑点或长期决策
- unresolved: 简短遗留事项
