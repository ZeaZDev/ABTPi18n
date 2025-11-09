# GITHUB SETUP

## Secrets ที่ต้องมี
- ENCRYPTION_KEY (Base64 256-bit)
- DATABASE_URL (รูปแบบ: postgresql://user:pass@host:port/db)
- REDIS_URL (redis://host:port/0)

## Branch Rules
- main (Protected, ต้องผ่าน CI)
- develop (รวม feature ก่อน merge)
- feature/* (งานย่อย)
- hotfix/* (แก้ด่วน production)

## Actions (แนะนำ)
1. CI:
   - Install dependencies
   - Run prisma validate
   - Run mypy / flake8 / ruff
   - Run unit tests
2. Security:
   - Bandit scan
   - Dependabot updates
3. Build & Push Image (Option):
   - Docker build backend/frontend
   - Push to GHCR

## Pull Request Checklist
- Strategy ใหม่: มีเอกสารอธิบาย
- API ใหม่: Update README + SECURITY impact
- DB Schema: prisma migrate + regenerate
- Docs: อัปเดต/ตรวจทาน PHASE2_GUIDE.md และ PHASE2_SUMMARY.md

## Tagging
- v1.0.0 (Omega Scaffolding)
- v1.x (Features เพิ่มเติม)