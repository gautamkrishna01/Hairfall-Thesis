#!/bin/zsh
# Hairfall Lab - stop the app, MinIO and Postgres cleanly. All saved data is kept.
#   ./stop.sh      asks first if a step is still running
#   ./stop.sh -y   stop without asking
set -u
cd "$(dirname "$0")/backend"
export PATH="$HOME/.orbstack/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

stop_proc() {  # stop_proc <name> <pgrep args...>: SIGTERM, wait up to 20 s for a clean exit
  local name=$1; shift
  pgrep "$@" >/dev/null || return 0
  pkill -TERM "$@"
  for _ in $(seq 1 20); do pgrep "$@" >/dev/null || { echo "✓ $name stopped"; return 0; }; sleep 1; done
  echo "! $name is still shutting down - check with: pgrep $*"
}

app_status=$(curl -s --max-time 3 http://127.0.0.1:8000/api/status 2>/dev/null)
if [[ "${1:-}" != "-y" && -n "$app_status" && "$app_status" != *'"running":null'* ]]; then
  read -q "?A step is still running and will be marked 'interrupted'. Stop anyway? [y/N] " || { echo "\nNothing stopped."; exit 0; }
  echo
fi

stop_proc "App" -f "uvicorn app.main:app"
stop_proc "MinIO" -x minio
docker stop -t 20 hairfall-s3 >/dev/null 2>&1 && echo "✓ S3 storage stopped"
if docker info >/dev/null 2>&1; then
  docker compose stop -t 30 >/dev/null 2>&1 && echo "✓ Postgres stopped"   # -t 30: time for a clean checkpoint
fi
