#!/usr/bin/env bash
# // ZeaZDev [Installer Automation Script] //
# // Project: Auto Bot Trader i18n //
# // Version: 1.0.0 (Omega Scaffolding) //
# // Author: ZeaZDev Meta-Intelligence (Generated) //
# // --- DO NOT EDIT HEADER --- //

set -euo pipefail

echo "[*] ตรวจสอบ Dependencies..."

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1"; exit 1; }
}

for c in docker docker compose node pnpm python3 git; do
  need_cmd "$c"
done

echo "[*] สร้างไฟล์ .env หากยังไม่มี"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "[*] กำลังตรวจสอบ ENCRYPTION_KEY..."
  if grep -q "REPLACE_BASE64_32BYTE_KEY" .env; then
    KEY=$(openssl rand -base64 32)
    sed -i.bak "s|REPLACE_BASE64_32BYTE_KEY|$KEY|g" .env
    echo "[*] สร้าง ENCRYPTION_KEY ใหม่เรียบร้อย"
  fi
else
  echo "[*] พบ .env แล้ว"
fi

echo "[*] ติดตั้ง pnpm workspaces"
pnpm install

echo "[*] เรียก prisma generate (Python)"
if command -v prisma >/dev/null 2>&1; then
  pnpm prisma generate || true
else
  echo "[!] Prisma CLI ไม่พบ ข้าม generate (ให้รันด้วยตนเอง)"
fi

echo "[*] เปิด Docker Compose"
docker compose up -d --build

echo "[*] รอกำหนดค่า Postgres 5 วินาที..."
sleep 5

echo "[*] ตรวจสอบ migrate (ใช้ prisma python หากรองรับ)"
python3 - <<'PYEOF'
import os
print("NOTE: Prisma migrate dev สำหรับ Python ต้องเรียกผ่าน CLI แยก หากใช้ prisma-client-py ลอง 'prisma migrate dev'")
PYEOF

echo "[*] ระบบพร้อมใช้งาน:"
echo "Frontend: http://localhost:3000/en/dashboard"
echo "Backend:  http://localhost:8000/docs"

echo "[*] เสร็จสิ้น"