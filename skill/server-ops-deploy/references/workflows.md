# 部署工作流参考

## Git 规范

- 本地开发产生的代码修改，优先在对应项目仓库 commit/push。
- 服务器只拉远程已提交代码，避免服务器工作区长期 ahead 或有未提交补丁。
- 如果服务器无法推 GitHub，回到本机仓库使用本机 SSH/GitHub 凭据推送。
- 服务器更新前检查：`git status --short --branch`、`git log -1 --oneline`、目标远程分支最新 commit。
- 不把密钥、env、证书、token 写入提交。

## Docker Compose 应用规范

- Compose 集中管理在 `/srv/services/compose`，public apps 使用 `/srv/services/compose/apps/docker-compose.apps.yml`。
- 容器镜像名用项目名和稳定 tag，不使用临时分支名污染整体命名。
- 容器端口只暴露到本机，例如 `127.0.0.1:3010:3000`。
- 所有公网访问从 nginx 进入，再反代到本机端口。
- 生产 env 使用 `/srv/services/compose/apps/*.env`，不要写进仓库。
- 内容型目录使用只读 bind mount，降低 rebuild 频率和误写风险。
- 更新流程：拉代码 -> build 指定服务 -> `up -d <service>` -> 验证容器状态和域名。

## 静态站规范

- 纯 HTML/CSS/JS 项目不需要 Docker，使用 nginx 静态托管。
- 标准目录：`/srv/services/apps/<app>/releases/<timestamp>`，`/srv/services/apps/<app>/current` 指向当前 release。
- 每个 release 写入 `REVISION`，记录来源 commit。
- 不修改 release 内仓库文件；如果需要缓存、header、重定向、SPA fallback，到 nginx 配置处理。
- JS/CSS 文件名固定且无 hash 时，nginx 对 JS/CSS 使用 `no-store/no-cache`；图片等可长缓存。
- 发布后验证首页、JS、CSS、关键图片或资源，必要时用 `--resolve <domain>:443:<server-ip>` 绕过本地代理/DNS 干扰。

## nginx/HTTPS 规范

- 新域名单独建 vhost，先 HTTP 可访问，再用 Certbot 签 HTTPS。
- 证书命令通常使用：`certbot --nginx --non-interactive --agree-tos --register-unsafely-without-email --redirect -d <domain>`。
- 每次修改 nginx 后必须执行 `nginx -t`，通过后 reload。
- HTTP 应 301 到 HTTPS；HTTPS 应返回 200 或预期状态。
- 对 API/上传/文件服务设置必要的 `client_max_body_size`、buffering、timeout。

## 验证和回滚

- 验证至少包含：`nginx -t`、HTTPS 首页、HTTP 跳转、关键资源、容器状态或 current 软链。
- 静态站回滚：把 `current` 软链切回旧 release，再验证。
- Docker 应用回滚：优先回滚代码指针或镜像后重新 `docker compose up -d <service>`，不要破坏用户内容目录和 env。
- 如果发现线上行为异常，先查：实际 commit、浏览器/代理缓存、nginx 命中 vhost、容器端口、日志。
