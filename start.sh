#!/bin/zsh
# Hairfall Lab - start Postgres, MinIO and the app, then open the browser.
#   ./start.sh            start whatever is not running yet (a running app is left alone)
#   ./start.sh --restart  restart the app server too (refused while a step is running)
set -u
cd "$(dirname "$0")/backend"
export PATH="$HOME/.orbstack/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MAC=0; [[ "$(uname)" == "Darwin" ]] && MAC=1
# On Linux system PostgreSQL clusters often own 5432-5434, so the lab's Postgres container uses 5455 there.
if (( ! MAC )); then export LAB_PG_PORT=5455 LAB_PG_DSN="postgresql://lab:lab@127.0.0.1:5455/lab"; fi
URL="http://127.0.0.1:8000"
RESTART=0; [[ "${1:-}" == "--restart" ]] && RESTART=1

fail() { print -P "%F{red}✗ $1%f"; exit 1; }
ok()   { print -P "%F{green}✓%f $1"; }
wait_for() {  # wait_for <seconds> <description> <command...>
  local secs=$1 what=$2; shift 2
  for _ in $(seq 1 $secs); do "$@" >/dev/null 2>&1 && return 0; sleep 1; done
  fail "$what did not start within ${secs}s"
}

# ---- checks ----
[[ -x .venv/bin/uvicorn ]] || fail "Python environment missing - see README (python3.12 -m venv .venv && pip install -r requirements.txt)"
if (( MAC )); then
  command -v docker >/dev/null || fail "Docker not found - install OrbStack (brew install --cask orbstack)"
  command -v minio  >/dev/null || fail "MinIO not found - brew install minio"
else
  command -v docker >/dev/null || fail "Docker not found - install Docker Engine (https://docs.docker.com/engine/install/)"
fi
[[ -f ../thesis_project/data/data.csv ]] || print -P "%F{yellow}!%f thesis_project/data/data.csv is missing - the Dataset tab will be empty"
[[ -f .env ]] || print -P "%F{yellow}!%f backend/.env is missing - TabPFN needs TABPFN_TOKEN (see .env.example)"
mkdir -p data/minio

# ---- Docker + Postgres ----
if ! docker info >/dev/null 2>&1; then
  if (( MAC )); then open -ga OrbStack 2>/dev/null; else sudo -n systemctl start docker 2>/dev/null; fi
  wait_for 90 "Docker" docker info
fi
ok "Docker"
compose_up() { docker compose up -d --no-recreate >>data/compose.log 2>&1 </dev/null; }
compose_up || { sleep 2; compose_up; } || fail "docker compose up failed - see backend/data/compose.log"
wait_for 60 "Postgres" docker compose exec -T postgres pg_isready -U lab
ok "Postgres"

# ---- MinIO (S3 storage) ----
# MinIO no longer ships Linux binaries/images, so on Linux RustFS (S3-compatible drop-in) runs in Docker
# with the same port and credentials.
if (( MAC )); then
  if ! pgrep -x minio >/dev/null; then
    MINIO_ROOT_USER=minioadmin MINIO_ROOT_PASSWORD=minioadmin \
      nohup minio server data/minio --address 127.0.0.1:9000 --console-address 127.0.0.1:9001 >> data/minio.log 2>&1 &
  fi
elif ! docker ps --format '{{.Names}}' | grep -qx hairfall-s3; then
  docker rm -f hairfall-s3 >/dev/null 2>&1
  docker run -d --name hairfall-s3 --restart unless-stopped --user "$(id -u):$(id -g)" \
    -p 127.0.0.1:9000:9000 -p 127.0.0.1:9001:9001 -v "$PWD/data/minio:/data" \
    -e RUSTFS_ACCESS_KEY=minioadmin -e RUSTFS_SECRET_KEY=minioadmin rustfs/rustfs:latest >/dev/null \
    || fail "could not start the S3 storage container (docker logs hairfall-s3)"
fi
wait_for 30 "MinIO" curl -s -o /dev/null 127.0.0.1:9000/minio/health/live

# ---- results from ~/Documents (Kaggle downloads): import any new/updated Step_*.zip ----
if [[ -d "$HOME/Documents" ]]; then
  .venv/bin/python import_kaggle_run.py --sync "$HOME/Documents" 2>&1 | tail -1
fi

# ---- app ----
if curl -sf "$URL/api/status" >/dev/null; then
  if (( RESTART )); then
    curl -s "$URL/api/status" | grep -q '"running":null' || fail "A step is running - wait for it (or stop it in the Notebook) before restarting"
    pkill -TERM -f "uvicorn app.main:app"
    for _ in $(seq 1 15); do pgrep -f "uvicorn app.main:app" >/dev/null || break; sleep 1; done
  else
    ok "App already running"
  fi
fi
if ! curl -sf "$URL/api/status" >/dev/null; then
  # caffeinate keeps the Mac awake while the server runs (long training)
  KEEPAWAKE=(); (( MAC )) && KEEPAWAKE=(caffeinate -i)
  nohup $KEEPAWAKE .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 >> data/api.log 2>&1 &
  wait_for 60 "The app" curl -sf "$URL/api/status"
  ok "App"
fi

echo ""
echo "  Hairfall Lab:   $URL"
echo "  Server log:     tail -f backend/data/api.log"
echo "  Stop:           ./stop.sh      Backup: ./backup.sh"
if (( MAC )); then open "$URL"; else xdg-open "$URL" >/dev/null 2>&1 || true; fi
