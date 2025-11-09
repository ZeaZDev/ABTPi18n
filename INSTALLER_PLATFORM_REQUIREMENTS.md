# PLATFORM REQUIREMENTS

## OS ที่รองรับ
- Ubuntu 22.04+
- macOS 13+
- Windows ผ่าน WSL2 (Ubuntu image)

## Core Software
- Docker 24+
- Docker Compose plugin
- Node.js 18+
- pnpm 8+
- Python 3.10+
- Git 2.40+

## Network
- เปิดพอร์ต: 3000 (Frontend), 8000 (Backend), 6379 (Redis), 5432 (Postgres)
- Phase 2: 9090 (Prometheus), 3001 (Grafana)
- Phase 3: HTTPS required สำหรับ OAuth callback และ Telegram webhook (Production)
- แนะนำเปิด Firewall จำกัด Access ภายนอกเฉพาะจำเป็น

## Performance (ขั้นต่ำ Dev)
- CPU: 2 Cores
- RAM: 4GB
- Storage: 10GB+

## Production (แนะนำ)
- CPU: 4+ Cores
- RAM: 16GB+
- Storage: NVMe 100GB+
- Monitoring: Enable Prometheus

## Security (แนะนำ)
- เปิด Automatic Security Updates
- ใช้ Fail2Ban / WAF (ถ้าเปิด public)
- แยก Volume สำหรับ DB พร้อม Backup Policy (Daily snapshot)
