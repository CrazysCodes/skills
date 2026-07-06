# 服务器布局参考

## 基本信息

- SSH alias：`tencent-service`
- 服务器公网 IP：`139.199.202.137`
- 应用根目录：`/srv/services/apps/<app>/`
- 代码发布目录：`/srv/services/apps/<app>/releases/<timestamp>`
- 当前版本软链：`/srv/services/apps/<app>/current`
- Compose 根目录：`/srv/services/compose/`
- Public apps compose：`/srv/services/compose/apps/docker-compose.apps.yml`
- Public apps compose project：`public-apps`
- nginx sites：`/etc/nginx/sites-available`、`/etc/nginx/sites-enabled`
- Docker 外部网络：`server-net`

## 当前 public apps

- Proofline
  - 主域名：`adong.org.cn`
  - 子域名：`proofline.adong.org.cn`
  - 容器：`proofline`
  - 本机端口：`127.0.0.1:3010 -> 3000`
  - 内容挂载：`/srv/services/apps/proofline/content:/app/content:ro`
  - env：`/srv/services/compose/apps/proofline.env`

- ShipReadme
  - 域名：`shipreadme.adong.org.cn`
  - 容器：`shipreadme`
  - 本机端口：`127.0.0.1:3011 -> 3000`

- NoteHealth
  - 域名：`notehealth.adong.org.cn`
  - 容器：`notehealth`
  - 本机端口：`127.0.0.1:3012 -> 3002`

- Academic Research Agent
  - 域名：`academic.adong.org.cn`
  - 前端容器：`academic-research-agent-frontend`，本机端口 `127.0.0.1:3013 -> 3000`
  - 后端容器：`academic-research-agent-backend`，本机端口 `127.0.0.1:8013 -> 8000`
  - env：`/srv/services/compose/apps/academic.env`

## 当前静态站和工具

- AirNote
  - 域名：`airnote.adong.org.cn`
  - 静态根：`/srv/services/apps/airnote/current`
  - 发布结构：`/srv/services/apps/airnote/releases/<timestamp>` + `current` 软链
  - 不使用 Docker
  - JS/CSS 缓存策略由 nginx 控制，不修改 HTML 加版本参数

- dufs
  - 域名：`file.adong.org.cn`
  - 容器：`dufs`
  - 本机端口：`127.0.0.1:8002 -> 5000`
  - nginx 反代，支持大文件和长连接

## nginx 现状提醒

- 历史 public apps 配置文件名仍可能是 `phase2-apps.conf`，不要因为文件名不理想就在部署任务中顺手重命名。
- 新增独立静态站建议使用单独文件：`/etc/nginx/sites-available/<domain>.conf`。
- Certbot 可能会直接改写 nginx vhost；签证后必须 `nginx -t` 并 reload/验证。
