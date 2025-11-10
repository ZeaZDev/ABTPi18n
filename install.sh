#!/usr/bin/env bash
# Simplified installer with correct service names and schema checks
set -euo pipefail

echo "[*] ตรวจสอบ Dependencies..."
command -v pnpm >/dev/null || npm i -g pnpm

echo "[*] สร้างไฟล์ .env หากยังไม่มี"
[ -f .env ] || cp .env.example .env

echo "[*] ติดตั้ง pnpm workspaces"
pnpm install

echo "[*] เปิด Docker Compose"
docker compose up -d --build

echo "[*] รอ Postgres 5 วินาที..."
sleep 5

SERVICE=backend
SCHEMA_IN_CONTAINER=${PRISMA_SCHEMA_PATH:-/app/prisma/schema.prisma}

if docker compose ps --services | grep -qx "$SERVICE"; then
  if [ -f apps/backend/prisma/schema.prisma ]; then
    if docker compose exec -T "$SERVICE" sh -lc "test -f '${SCHEMA_IN_CONTAINER}'"; then
      echo "[*] Generate Prisma client (python) inside container"
      docker compose exec -T "$SERVICE" sh -lc "prisma generate --schema '${SCHEMA_IN_CONTAINER}'" || echo "แจ้งเตือน: prisma generate ไม่สำเร็จ"
    else
      echo "(-) ข้าม generate เพราะไม่มี ${SCHEMA_IN_CONTAINER}"
    fi
  else
    echo "(-) ข้าม generate เพราะไม่มี apps/backend/prisma/schema.prisma"
  fi
else
  echo "(-) Service \"$SERVICE\" is not running"
fi

echo "[*] แจ้งเตือน migrate (Python prisma)"
echo "NOTE: หากใช้ prisma-client-py สำหรับ migrations ให้รัน 'prisma migrate dev' ด้วยตนเอง (CLI ยังไม่ถูกรวมในสคริปต์)"

echo "[*] ระบุมพร้อทใช้งาน:"
echo "Frontend: https://app.abtpi18n.com:3000/en/dashboard"
echo "Backend:  https://app.abtpi18n.com:8000/docs"
echo "[*] เสร็จสิ้น"