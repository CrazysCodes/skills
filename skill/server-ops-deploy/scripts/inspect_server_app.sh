#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 <app-name> [domain]

Inspects server app release/current, REVISION, nginx vhost snippets, and compose/container state.
Environment:
  SSH_ALIAS   default: tencent-service
USAGE
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage >&2
  exit 2
fi

app_name=$1
domain=${2:-}
ssh_alias=${SSH_ALIAS:-tencent-service}

ssh "$ssh_alias" "set -e
app_name='${app_name}'
domain='${domain}'
app_dir=\"/srv/services/apps/\${app_name}\"

echo '== app current =='
if [ -e \"\$app_dir/current\" ]; then
  current=\$(readlink -f \"\$app_dir/current\")
  echo \"\$current\"
  [ -f \"\$current/REVISION\" ] && cat \"\$current/REVISION\" || true
  find \"\$current\" -path \"\$current/.git\" -prune -o -maxdepth 2 -type f -printf '%P %s bytes\\n' | sort | head -80
else
  echo 'no current symlink found'
fi

echo
echo '== compose references =='
for file in /srv/services/compose/docker-compose*.yml /srv/services/compose/apps/docker-compose.apps.yml; do
  [ -f \"\$file\" ] || continue
  grep -n \"\$app_name\" \"\$file\" || true
done

echo
echo '== docker containers =='
docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}' | grep -i \"\$app_name\" || true

echo
echo '== nginx references =='
if [ -n \"\$domain\" ]; then
  escaped_domain=\$(printf '%s' \"\$domain\" | sed 's/[.[\\*^$()+?{}|]/\\\\&/g')
  grep -R -n -E \"server_name[[:space:]]+([^;[:space:]]+[[:space:]]+)*\$escaped_domain([[:space:];]|$)|root .*\$app_name|proxy_pass .*\$app_name\" /etc/nginx/sites-enabled /etc/nginx/sites-available 2>/dev/null || true
else
  grep -R -n \"\$app_name\" /etc/nginx/sites-enabled /etc/nginx/sites-available 2>/dev/null || true
fi
"
