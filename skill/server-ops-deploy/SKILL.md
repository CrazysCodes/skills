---
name: server-ops-deploy
description: 在处理个人服务器 tencent-service 上的部署、更新线上、Git 同步、Docker Compose、nginx、HTTPS 证书、域名绑定、静态站发布、容器管理、回滚和部署验证时使用。要求先检查真实环境，遵循 /srv/services 目录、release/current、compose 集中管理、nginx 统一入口和部署后验证规范。
metadata:
  short-description: 个人服务器部署与运维规范
---

# 个人服务器部署与运维规范

## 触发场景

当用户提到以下任务时使用本 skill：部署项目、更新线上、重新发布、服务器环境、域名映射、HTTPS 证书、nginx、Docker Compose、容器重启、静态站、release/current、Git 拉取/推送、回滚、验证线上状态。

## 先查真实环境

每次部署前先做非破坏性检查，不凭会话记忆直接操作：

- 确认目标项目类型：纯静态、前端应用、后端服务、前后端组合、内容型站点。
- 确认远程仓库、分支、最新 commit，以及服务器当前 `current` 指向或容器镜像状态。
- 检查 nginx 当前 `server_name`、证书、端口转发、Docker Compose 服务名。
- 需要服务器拓扑时读取 `references/server-layout.md`。
- 需要流程细节时读取 `references/workflows.md`。

## 硬规则

- 不把服务器临时修改当作长期状态；代码修复优先在本地项目仓库 commit/push，再让服务器拉远程。
- 不直接修改静态站 release 内的仓库文件来解决缓存或配置问题；缓存策略放 nginx。
- 所有公网入口经 nginx/HTTPS；容器端口只绑定 `127.0.0.1`。
- 敏感 env、token、密码、证书私钥不写入 skill、仓库或最终回答。
- Docker Compose 统一放在 `/srv/services/compose`，不要用临时功能分支名命名整体 compose/nginx 配置。
- 部署后必须验证：HTTP/HTTPS、关键静态资源或健康接口、容器状态、nginx 配置。

## 决策规则

- 纯静态站：优先 nginx `root` + `/srv/services/apps/<app>/releases/<timestamp>` + `current` 软链，不使用 Docker。
- Next.js、后端服务或前后端组合：优先 Docker Compose，构建上下文指向 `/srv/services/apps/<app>/current`。
- 内容型站点：内容目录使用服务器 bind mount，容器内只读挂载，例如 `/srv/services/apps/proofline/content:/app/content:ro`。
- 文件服务或上传类服务：必须明确鉴权、上传大小、反代超时和是否只监听本机。
- 静态资源文件名不带 hash 时，JS/CSS 默认使用 nginx `no-store/no-cache`，不要通过改 HTML 加 `?v=` 临时绕过。

## 常用脚本

脚本位于本 skill 的 `scripts/` 目录。执行前先读脚本参数和当前环境，确认不会覆盖错误目标。

- `deploy_static_site.sh`：发布纯静态 GitHub 仓库到服务器 release/current。
- `verify_site.sh`：验证域名 HTTPS、HTTP 跳转、资源状态和 nginx 配置。
- `inspect_server_app.sh`：查看服务器 app 当前 release、revision、nginx 和 compose 状态。

## 输出习惯

- 更新用户时说明正在检查什么事实，而不是只说“部署中”。
- 最终回答包含：发布 commit、release/current 路径、关键验证结果、是否重启容器、是否改过 nginx。
- 如果发现线上文件和 GitHub 不一致，先说明风险，再恢复或给出修复方案。
