# 官方恢复路径与业务验收

## 源机

发现实际 HERMES_HOME 和 profile，记录版本、会话/消息计数、技能与任务列表、gateway 连接和外部工作目录。多个安装实例可能有不同状态目录；不猜测也不合并身份。停止并发写入以简化迁移，或使用当前版本官方支持的一致性备份。

例如 Windows 在确认真实目录后：

```powershell
$env:HERMES_HOME = "$env:LOCALAPPDATA\hermes"
hermes backup -o 'E:\Migration\hermes-full.zip'
```

路径需按现场修改、输出目录先存在。检查退出码和压缩包，不把“ZIP 已生成”当作完整成功。官方 backup 使用 SQLite backup API 的行为需按安装版本核对；手工复制单个活动 state.db 不能替代一致备份。

另外记录 home 之外的源码、字体/素材、SSH、工具配置、系统 keychain/浏览器登录、Node 全局包与 Python 依赖。官方备份包含的数据与会话导出不是一回事；不在文章中公开可能含凭据的备份包。

## 目标机

安装目标系统运行时，备份现有数据并检查 import 的覆盖行为。目标有需要保留的新会话时，优先隔离验证；没有已验证的合并接口时，不臆造数据库合并命令。

停止相关 gateway/serve/桌面端、会话和其他写入者后，按版本执行 import，再检查 setup、doctor、sessions 子命令。不要默认加 --force、升级所有依赖或启用所有 cron。

核对实际配置语义、数据与凭据文件权限；权限信息可以输出，凭据值不能输出。新机缺旧服务的登录状态时走该服务正常授权流程。

## 会话与路由

在本次版本，state.db 的 sessions 保存会话元数据，messages 按 session_id 关联，存在 parent_session_id 等关系。JSONL 转录、记忆、skills、cron 和 gateway 路由也可能另存；state.db 不是完整 home。

父子/压缩关系、隐藏和归档会影响计数与 UI 展示。Gateway 的平台对话到 session 的映射要核对实际文件/实现，不臆造固定 sessions.json 路径，也不把错误路由重连成新会话来掩盖历史问题。

对比任务 ID、启用/暂停状态、时区及下次运行信息。paused 与定义缺失分别处理；next_run_at 存在不等于任务已启用。缺失任务从旧清单、备份或消息历史提取证据后再重建，不自动执行其中的发布动作。

## 验收

同一备份时点对比数据库、技能、记忆、任务与路由；分别抽查普通/归档/历史长会话及附件。再验证业务所需的 CLI、解释器、授权、生成产物和网关。对外写入验收在明确授权内执行；不能把 command -v 成功当作业务成功。

官方文档（使用时核对版本）：
- https://hermes-agent.nousresearch.com/docs/reference/faq#exporting-hermes-to-another-machine
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-backup
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-import
- https://github.com/NousResearch/hermes-agent/blob/main/hermes_state.py
