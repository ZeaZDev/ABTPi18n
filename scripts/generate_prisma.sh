#!/usr/bin/env bash
# Helper to generate Prisma client inside a running container/service
# Usage:
#   scripts/generate_prisma.sh backend [/app/prisma/schema.prisma]
set -euo pipefail

SERVICE="${1:-backend}"
SCHEMA_PATH="${2:-/app/prisma/schema.prisma}"

echo "[*] Generating Prisma client in service: ${SERVICE}, schema: ${SCHEMA_PATH}"
docker compose exec -T "$SERVICE" sh -lc "if [ -f '${SCHEMA_PATH}' ]; then prisma generate --schema '${SCHEMA_PATH}'; else echo 'Schema not found at ${SCHEMA_PATH}'; exit 1; fi"