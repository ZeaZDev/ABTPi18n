# ZeaZDev-ABTPro-i18n

แพลตฟอร์ม Auto Bot Trader ระดับ Production รองรับหลายภาษา (i18n) และหลายกลยุทธ์ (Multi-Strategy) บนหลาย Exchange (Multi-Exchange) พร้อมระบบความปลอดภัยสำหรับ API Key (AES-GCM) และส่วนขยายทางธุรกิจ (Rental, PromptPay Top-up, Module Plugin)

## คุณสมบัติหลัก
- FastAPI Backend + Celery Worker Loop
- Next.js Frontend (App Router) + react-i18next
- เข้ารหัส API Key ทันที (AES-GCM)
- Strategy Engine แบบ Plug-in (RSI Cross ตัวอย่าง Production)
- Prisma Schema สำหรับ Postgres
- ระบบเช่า (Rental Contract), เติมเงิน (PromptPay), โมดูล (ModuleRegistration)
- **Phase 3 (DONE ✅):** Google OAuth Authentication, Telegram Notifications, Dynamic Themes, Multi-language Support (Thai, English, Chinese, Japanese)
- **Phase 4 (DONE ✅):** PromptPay Top-up Flow, Rental Expiry Enforcement, Plugin Loader, Portfolio Aggregation, Backtester & Paper Trading
- **Phase 5 (DONE ✅):** Audit Trail System, Static Code Scanning (Bandit/Semgrep), Secret Rotation Flow, DR/Failover Strategy

## สถาปัตยกรรม
```mermaid
flowchart LR
    FE[Frontend: Next.js i18n] --> API[FastAPI Backend]
    API --> SEC[Security Service: AES-GCM]
    SEC --> DB[(Postgres)]
    API --> CELERY[Celery Dispatcher]
    CELERY --> WORKER[Worker Loop]
    WORKER --> STRAT[Strategy Engine]
    STRAT --> RISK[Risk Manager]
    RISK --> CCXT[CCXT Adapter]
    CCXT --> EXCH[(Exchange APIs)]
    STRAT --> LOGS[TradeLog → DB]
    API --> RENTAL[Rental Module]
    API --> PAYMENT[PromptPay]
    API --> TELE[Telegram Hook]
```

## Tech Stack
- Frontend: Next.js + react-i18next + Theme System
- Backend: FastAPI + Prisma Client (Python) + CCXT
- DB: Postgres
- Queue: Celery + Redis
- Security: AES-GCM encryption service
- Authentication: Google OAuth 2.0
- Notifications: Telegram Bot API
- Deployment: Docker Compose

## การติดตั้ง (ย่อ)
1. สร้างไฟล์ `.env` (หรือใช้ `install.sh`)
2. รัน `./install.sh`
3. เข้าใช้งาน Frontend: http://localhost:3000/en/dashboard

## การใช้งานเบื้องต้น
- เข้าสู่ระบบ: http://localhost:3000/en/login → Sign in with Google
- เพิ่ม API Key: หน้า Settings → บันทึก → ส่งไปที่ `/exchange/keys`
- เชื่อมต่อ Telegram: Settings → Telegram Integration → Link Account
- ปรับแต่งธีม: Settings → Theme Customizer → เลือกสี/โหมด
- เปลี่ยนภาษา: ใช้ Language Selector (🇬🇧 🇹🇭 🇨🇳 🇯🇵)
- เริ่มบอท: Dashboard → Start Bot (เรียก `/bot/start`)
- ดู PnL: Dashboard ดึง `/dashboard/pnl`

## ความปลอดภัย
ดูไฟล์ [SECURITY.md](SECURITY.md)

## กลยุทธ์
เพิ่มไฟล์ใหม่ใน `src/trading/strategies/` แล้ว `StrategyRegistry.register(YourStrategyClass)`

## เอกสาร (Documentation)
- [PHASE5_IMPLEMENTATION_SUMMARY.md](PHASE5_IMPLEMENTATION_SUMMARY.md) — สรุปการสร้างเฟส 5 (เสร็จแล้ว ✅)
- [PHASE5_SUMMARY.md](PHASE5_SUMMARY.md) — สรุปแผนงานเฟส 5 (เสร็จแล้ว ✅)
- [PHASE5_GUIDE.md](PHASE5_GUIDE.md) — คู่มือการใช้งานฟีเจอร์เฟส 5
- [DR_FAILOVER_STRATEGY.md](DR_FAILOVER_STRATEGY.md) — กลยุทธ์การกู้คืนจากภัยพิบัติ
- [PHASE4_IMPLEMENTATION_SUMMARY.md](PHASE4_IMPLEMENTATION_SUMMARY.md) — สรุปการสร้างเฟส 4 (เสร็จแล้ว ✅)
- [PHASE4_SUMMARY.md](PHASE4_SUMMARY.md) — สรุปแผนงานเฟส 4 (เสร็จแล้ว ✅)
- [PHASE4_GUIDE.md](PHASE4_GUIDE.md) — คู่มือการใช้งานฟีเจอร์เฟส 4
- [PHASE3_SUMMARY.md](PHASE3_SUMMARY.md) — สรุปแผนงานเฟส 3 (เสร็จแล้ว ✅)
- [PHASE3_GUIDE.md](PHASE3_GUIDE.md) — คู่มือการใช้งานฟีเจอร์เฟส 3
- [PHASE2_SUMMARY.md](PHASE2_SUMMARY.md) — สรุปสิ่งที่ทำในเฟส 2
- [PHASE2_GUIDE.md](PHASE2_GUIDE.md) — คู่มือการใช้งานฟีเจอร์เฟส 2
- [ROADMAP.md](ROADMAP.md) — สถานะและแผนงาน
- [STRATEGY_GUIDE.md](STRATEGY_GUIDE.md) — คู่มือการพัฒนากลยุทธ์

## Roadmap
ดูไฟล์ [ROADMAP.md](ROADMAP.md)

## การตั้งค่า GitHub
ดูไฟล์ [GITHUB-SETUP.md](GITHUB-SETUP.md)

## Installer
ดูไฟล์ `install.sh` และเอกสารระบบปฏิบัติการใน `INSTALLER_PLATFORM_REQUIREMENTS.md`
