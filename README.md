# Skills

这个仓库用于集中存放个人常用的 Codex / Agent skills，方便在不同环境中复用、同步和维护。

## 目录结构

所有 skill 均放在仓库根目录的 `skill/` 文件夹下：

```text
skill/
├── ai-agent-daily-mentor/
├── code-development-standards/
├── drawio-mermaid/
├── learning-companion/
├── project-interrogator/
├── server-ops-deploy/
└── shushu-internship-tool/
```

每个子目录都是一个完整 skill，至少包含 `SKILL.md`；部分 skill 还包含 `agents/`、`references/`、`scripts/` 等配套资源。

## Skill 索引

| Skill | 用途 | 来源 |
| --- | --- | --- |
| `project-interrogator` | 中文项目拷问官：基于简历进行项目深挖、模拟面试、追问和面试复盘报告。 | 个人自有 / 本地沉淀 |
| `shushu-internship-tool` | 鼠鼠实习妙妙工具：围绕目标 JD 找项目、审代码、设计改造、生成简历 STAR 和面试材料。 | 来源于 GitHub 项目整理 |
| `code-development-standards` | 代码开发规范：在开发、重构、排障、测试和技术文档中统一中文注释、日志和文档风格。 | 个人自有 / 本地沉淀 |
| `drawio-mermaid` | draw.io / diagrams.net 转换工具：覆盖 Mermaid -> draw.io、draw.io XML/.drawio -> PNG/SVG/PDF 官方导出，以及 draw.io XML -> 语义化 Mermaid。 | 个人自有 / 本地沉淀 |
| `server-ops-deploy` | 个人服务器部署运维：覆盖 Git 同步、Docker Compose、nginx、HTTPS、静态站发布、回滚和验证。 | 个人自有 / 本地沉淀 |
| `ai-agent-daily-mentor` | 中文 AI Agent 实习冲刺导师：生成 8 周学习路线、每日任务、反馈调整和 Obsidian 双链知识点。 | 来源于 GitHub 项目整理 |
| `learning-companion` | 通用学习陪练：学语言/读论文/啃开源项目/跟进技术方向，有状态工作区+一手引用+自测闪卡+Obsidian 双链，含快速拆解轻模式。 | 个人自有 / 本地沉淀 |

## 来源说明

- `ai-agent-daily-mentor` 来源于 GitHub 项目整理，保留其子目录内原始 `README.md` 和配套参考资料。
- 其余 skill 为个人自有或本地沉淀内容，用于日常开发、面试辅导、实习项目准备和服务器部署等场景。

## 使用方式

将需要的 skill 目录复制或同步到目标环境的 skills 目录中，并确保保留完整目录结构，例如 `SKILL.md`、`references/`、`scripts/` 和 `agents/`。
