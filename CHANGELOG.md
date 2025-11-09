# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
