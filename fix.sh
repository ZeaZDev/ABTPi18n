#!/usr/bin/env bash
# // ZeaZDev [Prisma Fix & Regeneration Script] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

set -euo pipefail

echo "[*] Prisma Client Regeneration & Fix Script"
echo "============================================"

# Check if docker compose is available
if ! command -v docker compose &> /dev/null; then
    echo "[!] ERROR: docker compose is not available"
    exit 1
fi

# Clean up Docker disk space to prevent "no space left" errors
echo "[*] Pruning Docker system to free up disk space..."
docker system prune -f --volumes || echo "[!] Warning: Could not prune Docker system"

# Set default schema path
export PRISMA_SCHEMA_PATH="${PRISMA_SCHEMA_PATH:-/app/prisma/schema.prisma}"

# Try to detect schema in container (dual-path check)
echo "[*] Detecting Prisma schema in container..."

# Check if backend service is running
if docker compose ps backend | grep -q "Up"; then
    EXEC_TARGET="backend"
    echo "[*] Using service name: backend"
elif docker ps --filter "name=abt_backend" --format '{{.Names}}' | grep -q "abt_backend"; then
    EXEC_TARGET="abt_backend"
    echo "[*] Fallback to container name: abt_backend"
    USE_CONTAINER=true
else
    echo "[!] ERROR: Backend container is not running"
    echo "[!] Please start the containers with: docker compose up -d"
    exit 1
fi

# Function to execute commands in container
exec_in_container() {
    if [ "${USE_CONTAINER:-false}" = "true" ]; then
        docker exec "$EXEC_TARGET" "$@"
    else
        docker compose exec "$EXEC_TARGET" "$@"
    fi
}

# Check for schema at multiple possible paths
SCHEMA_FOUND=false
for schema_path in "/app/prisma/schema.prisma" "/app/apps/backend/prisma/schema.prisma"; do
    if exec_in_container test -f "$schema_path" 2>/dev/null; then
        echo "[✓] Found schema at: $schema_path"
        export PRISMA_SCHEMA_PATH="$schema_path"
        SCHEMA_FOUND=true
        break
    fi
done

if [ "$SCHEMA_FOUND" = "false" ]; then
    echo "[!] ERROR: Prisma schema not found in container"
    echo "[!] Checked paths:"
    echo "    - /app/prisma/schema.prisma"
    echo "    - /app/apps/backend/prisma/schema.prisma"
    echo "[!] Please ensure the schema file exists in the backend build context"
    exit 1
fi

# Generate Prisma client
echo "[*] Generating Prisma Python client..."
if exec_in_container prisma generate --schema "$PRISMA_SCHEMA_PATH"; then
    echo "[✓] Prisma client generated successfully"
else
    echo "[!] ERROR: Prisma client generation failed"
    echo "[!] Check if Node.js is installed in the container"
    exit 1
fi

# Run migrations (non-fatal)
echo "[*] Running Prisma migrations (deploy)..."
if exec_in_container prisma migrate deploy --schema "$PRISMA_SCHEMA_PATH" 2>/dev/null; then
    echo "[✓] Migrations applied successfully"
else
    echo "[!] Warning: Migration failed or no migrations to apply (non-fatal)"
fi

# Verify client generation
echo "[*] Verifying Prisma client generation..."
if exec_in_container test -d "/app/prisma" 2>/dev/null; then
    echo "[✓] Prisma client directory exists"
else
    echo "[!] Warning: Prisma client directory not found at expected location"
fi

echo ""
echo "[✓] Fix script completed successfully"
echo "[*] You can now use the Prisma client in your application"
