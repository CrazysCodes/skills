#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 <repo-url> <app-name> <domain> [revision]

Publishes a static Git repository to tencent-service using /srv/services/apps/<app>/releases/<timestamp>
and switches /srv/services/apps/<app>/current. This script does not edit repository files.

Environment:
  SSH_ALIAS   default: tencent-service
USAGE
}

if [[ $# -lt 3 || $# -gt 4 ]]; then
  usage >&2
  exit 2
fi

repo_url=$1
app_name=$2
domain=$3
requested_revision=${4:-}
ssh_alias=${SSH_ALIAS:-tencent-service}
workdir=$(mktemp -d "${TMPDIR:-/tmp}/server-ops-static.XXXXXX")
trap 'rm -rf "$workdir"' EXIT

clone_dir="$workdir/repo"
if [[ -n "$requested_revision" ]]; then
  git clone --depth 1 "$repo_url" "$clone_dir"
  git -C "$clone_dir" fetch --depth 1 origin "$requested_revision" || true
  git -C "$clone_dir" checkout "$requested_revision"
else
  git clone --depth 1 "$repo_url" "$clone_dir"
fi

revision=$(git -C "$clone_dir" rev-parse --short HEAD)
timestamp=$(date +%Y%m%d%H%M%S)
remote_release="/srv/services/apps/${app_name}/releases/${timestamp}"

COPYFILE_DISABLE=1 tar -C "$clone_dir" --exclude .git -cf - . | ssh "$ssh_alias" "set -e
mkdir -p '$remote_release'
tar -C '$remote_release' -xf -
printf '%s\n' '$revision' > '$remote_release/REVISION'
ln -sfn '$remote_release' '/srv/services/apps/${app_name}/current'
printf 'domain=%s\napp=%s\nrevision=%s\nrelease=%s\ncurrent=%s\n' '$domain' '$app_name' '$revision' '$remote_release' \"\$(readlink -f '/srv/services/apps/${app_name}/current')\"
"
