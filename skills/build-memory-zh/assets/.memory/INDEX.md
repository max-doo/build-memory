# 知识库索引与路由表 (Memory Index)

> **使用说明：** 开展复杂修改或调试前，根据当前任务关键词或修改路径匹配 triggers。若命中 L1 条目，仅切片读取 `.memory/KNOWLEDGE.md` 对应的 ### 章节。

## L0 级全局规则 (已注入 AGENTS.md，无需读取 KNOWLEDGE)
| id | 规则说明 | 所在位置 |
|---|---|---|
| `core-rules` | 核心工程底线与包管理器禁令 | `AGENTS.md` -> 技术栈/项目结构 |

## L1 级知识路由 (命中时切片读取 KNOWLEDGE.md)
| id | triggers (关键词 / 路径 Glob) | KNOWLEDGE 对应章节锚点 | 备注 |
|---|---|---|---|
| `example-api` | `api/, fetch, http, timeout` | `### 1. 接口请求与网络调优` | 示例路由（请根据项目替换） |
