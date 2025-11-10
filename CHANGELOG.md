# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-11-10

### Updated
- Updated all Python backend dependencies to latest stable versions
  - cryptography: 44.0.1 → 46.0.3 (security update)
  - pillow: 10.3.0 → 11.3.0 (security update)
  - fastapi: 0.110.1 → 0.121.1
  - uvicorn: 0.29.0 → 0.34.0
  - celery: 5.3.6 → 5.4.0
  - redis: 5.0.1 → 5.2.1
  - ccxt: 4.3.74 → 4.4.48
  - pydantic: 2.6.4 → 2.10.6
  - numpy: 1.26.4 → 2.2.2
  - pandas: 2.2.1 → 2.2.3
  - scikit-learn: 1.5.0 → 1.6.1
  - scipy: 1.11.4 → 1.15.1
  - psycopg2-binary: 2.9.9 → 2.9.10
  - httpx: 0.25.2 → 0.28.1
  - tenacity: 8.2.3 → 9.0.0
  - prometheus-client: 0.20.0 → 0.21.1
  - google-auth: 2.27.0 → 2.37.0
  - google-auth-oauthlib: 1.2.0 → 1.2.1
  - python-telegram-bot: 20.7 → 21.10
  - qrcode: 7.4.2 → 8.0
  - pluggy: 1.3.0 → 1.6.0
  - importlib-metadata: 6.8.0 → 7.1.0
  - bandit: 1.7.5 → 1.8.0
  - semgrep: 1.45.0 → 1.101.0
  - python-json-logger: 2.0.7 → 3.2.1
  - psutil: 5.9.6 → 6.1.1
  - gdown: 5.1.0 → 5.2.0
  - pyyaml: 6.0.1 → 6.0.2
- Updated all Node.js frontend dependencies to latest compatible versions
  - react: 18.2.0 → 18.3.1
  - react-dom: 18.2.0 → 18.3.1
  - react-i18next: 13.2.2 → 16.2.4
  - i18next: 23.7.6 → 25.6.1
  - i18next-browser-languagedetector: 7.0.1 → 8.2.0
  - typescript: 5.3.3 → 5.7.3
  - next-themes: 0.2.1 → 0.4.6
  - @types/react: 18.2.0 → 18.3.18
  - @types/react-dom: 18.2.0 → 18.3.5
  - @types/node: 20.10.0 → 22.10.5
- Updated Prisma to 5.22.0

### Security
- Fixed security vulnerabilities in cryptography and pillow packages
- Updated all packages with known security issues to patched versions

### Verified
- All backend Python syntax validated
- All critical package imports tested successfully
- Frontend build tested and working correctly
- Verification script passes all checks

## [1.0.0] - 2025-11-09

### Added
- Initial release of Auto Bot Trader Pro i18n platform
- FastAPI Backend with Celery Worker Loop
- Next.js Frontend with App Router and react-i18next
- API Key encryption using AES-GCM
- Strategy Engine with plug-in architecture (RSI Cross strategy)
- Prisma Schema for PostgreSQL
- Rental Contract system
- PromptPay payment integration
- Module Registration system
- Google OAuth Authentication
- Telegram Notifications
- Dynamic Theme system
- Multi-language Support (Thai, English, Chinese, Japanese)
- PromptPay Top-up Flow
- Rental Expiry Enforcement
- Plugin Loader system
- Portfolio Aggregation
- Backtester and Paper Trading
- Audit Trail System
- Static Code Scanning (Bandit/Semgrep)
- Secret Rotation Flow
- DR/Failover Strategy
- ML Signal Quality Scoring
- Reinforcement Learning Strategy Tuning
- Predictive Volatility Estimation

### Phase Completions
- ✅ Phase 1: Foundation
- ✅ Phase 2: Strategy Engine
- ✅ Phase 3: i18n & Authentication
- ✅ Phase 4: Monetization & Advanced Features
- ✅ Phase 5: Security & Compliance
- ✅ Phase 6: ML & Intelligence

### Security
- AES-GCM encryption for API keys
- Google OAuth 2.0 authentication
- Security scanning with CodeQL, Bandit, and Semgrep
- Audit logging system
- Secret rotation mechanism

### Infrastructure
- Docker Compose orchestration
- PostgreSQL database
- Redis for caching and queuing
- Prometheus and Grafana monitoring
- Multi-container architecture (frontend, backend, worker, monitoring)
