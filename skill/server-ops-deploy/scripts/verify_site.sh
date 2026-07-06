#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 <domain> <server-ip> [resource ...]

Verifies HTTPS, HTTP redirect, optional resources, and remote nginx syntax.
Environment:
  SSH_ALIAS   default: tencent-service
USAGE
}

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 2
fi

domain=$1
server_ip=$2
shift 2
ssh_alias=${SSH_ALIAS:-tencent-service}
resources=("$@")
if [[ ${#resources[@]} -eq 0 ]]; then
  resources=(/ /app.js /styles.css)
fi

printf '== HTTPS resources ==\n'
for resource in "${resources[@]}"; do
  curl --resolve "${domain}:443:${server_ip}" -sS -o /dev/null -w "${resource} %{http_code} ssl=%{ssl_verify_result}\n" "https://${domain}${resource}"
done

printf '\n== HTTP redirect ==\n'
curl --resolve "${domain}:80:${server_ip}" -sS -I "http://${domain}/" | sed -n '1,8p'

printf '\n== nginx syntax ==\n'
ssh "$ssh_alias" 'nginx -t'
