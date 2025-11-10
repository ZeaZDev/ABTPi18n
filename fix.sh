#!/usr/bin/env bash
# Fix build/runtime issues for Prisma (Python) + Docker in ABTPi18n
# - Installs prisma + Node runtime inside containers (pip nodejs-bin, fallback apt NodeSource)
# - Generates Prisma client and runs initial migrate
# - Prunes Docker when disk low (optional)
#
# Usage:
#   bash fix.sh
#   DEBUG=1 bash fix.sh        # verbose
#   PRUNE=1 bash fix.sh        # force prune docker caches/volumes
#   SKIP_MIGRATE=1 bash fix.sh
#   SKIP_WORKER=1 bash fix.sh
set -euo pipefail
[[ "${DEBUG:-0}" == "1" ]] && set -x

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$ROOT_DIR"

SCHEMA_LOCAL="${SCHEMA_LOCAL:-apps/backend/prisma/schema.prisma}"
SCHEMA_IN_CONTAINER="${PRISMA_SCHEMA_PATH:-/app/prisma/schema.prisma}"
BACKEND_SERVICE="${BACKEND_SERVICE:-backend}"
WORKER_SERVICE="${WORKER_SERVICE:-worker}"
DISK_THRESHOLD_MB="${DISK_THRESHOLD_MB:-2048}"

say(){ printf "\n[*] %s\n" "$*"; }
warn(){ printf "\n[!] %s\n" "$*" >&2; }
die(){ printf "\n[✗] %s\n" "$*" >&2; exit 1; }

ensure_schema(){
  say "Checking schema: $SCHEMA_LOCAL"
  [[ -f "$SCHEMA_LOCAL" ]] || die "Missing $SCHEMA_LOCAL"
}

low_space_prune(){
  local free_mb
  free_mb="$(df -Pm "$ROOT_DIR" | awk 'NR==2{print $4}')"
  say "Free space: ${free_mb} MB"
  if (( free_mb < DISK_THRESHOLD_MB )); then
    warn "Low disk space -> prune"
    docker system prune -af --volumes || true
    docker builder prune -af || true
  fi
}

build_up(){
  say "Building images..."
  docker compose build
  say "Starting services..."
  docker compose up -d
  say "Waiting 5s for DB..."
  sleep 5
}

install_prisma_runtime(){
  local svc="$1"
  say "Install prisma runtime in $svc"
  # Skip if already present
  if docker compose exec -T "$svc" sh -lc 'python - <<PY
import sys
from importlib import metadata
try:
  print(metadata.version("prisma"))
  sys.exit(0)
except:
  sys.exit(1)
PY'; then
    say "prisma already installed in $svc, skipping install."
    return 0
  fi

  docker compose exec -T "$svc" sh -lc 'python -m pip install --no-cache-dir --upgrade pip || true'
  # Timeout 180s for pip install
  if ! docker compose exec -T "$svc" sh -lc 'timeout 180s python -m pip install --no-cache-dir prisma nodejs-bin'; then
    warn "pip install prisma nodejs-bin failed or timed out, fallback to apt Node.js"
    docker compose exec -T "$svc" bash -lc 'set -e; \
      apt-get update; \
      apt-get install -y --no-install-recommends curl ca-certificates gnupg; \
      curl -fsSL https://deb.nodesource.com/setup_20.x | bash -; \
      apt-get install -y nodejs; \
      pip install --no-cache-dir prisma; \
      node --version; prisma --version || true; \
      apt-get purge -y --auto-remove curl gnupg || true; \
      rm -rf /var/lib/apt/lists/*'
  fi

  docker compose exec -T "$svc" sh -lc 'echo "Verification:"; node --version || echo "no-node"; prisma --version || echo "no-prisma"'
}

generate_client(){
  local svc="$1"
  say "Generate client in $svc"
  docker compose exec -T "$svc" sh -lc "[ -f '$SCHEMA_IN_CONTAINER' ] && prisma generate --schema '$SCHEMA_IN_CONTAINER' || prisma generate || true"
}

migrate_dev(){
  local svc="$1"
  [[ "${SKIP_MIGRATE:-0}" == "1" ]] && { say "Skip migrate"; return; }
  say "Migrate dev in $svc"
  docker compose exec -T "$svc" sh -lc "[ -f '$SCHEMA_IN_CONTAINER' ] && prisma migrate dev --name init --schema '$SCHEMA_IN_CONTAINER' || prisma migrate dev --name init || true"
}

main(){
  ensure_schema
  low_space_prune
  build_up
  install_prisma_runtime "$BACKEND_SERVICE"
  generate_client "$BACKEND_SERVICE"
  migrate_dev "$BACKEND_SERVICE"

  if [[ "${SKIP_WORKER:-0}" != "1" ]]; then
    install_prisma_runtime "$WORKER_SERVICE"
    generate_client "$WORKER_SERVICE"
  fi

  say "Check client files:"
  docker compose exec -T "$BACKEND_SERVICE" sh -lc "find /app/prisma -maxdepth 2 -type f | head || echo 'no files'"
  say "Endpoints:"
  echo "Frontend: https://app.abtpi18n.com:3000/en/dashboard"
  echo "Backend:  https://app.abtpi18n.com:8000/docs"
  say "Done."
}

main "$@"