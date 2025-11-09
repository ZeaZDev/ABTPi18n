# คู่มือการใช้งาน เฟส 1 (Phase 1) Implementation Guide

## Overview
Phase 1 establishes the foundational architecture for the Auto Bot Trader Pro platform, including the monorepo structure, backend API, database, message queue, and security infrastructure for encrypted exchange keys.

### Quick Links
- [Phase 1 Summary](PHASE1_SUMMARY.md)
- [Phase 1 Implementation Summary](PHASE1_IMPLEMENTATION_SUMMARY.md)
- [Roadmap](../../guides/ROADMAP.md)
- [Strategy Guide](../../strategy/STRATEGY_GUIDE.md)

## Core Features

### 1. Monorepo Structure
The project uses a monorepo architecture to manage both frontend and backend codebases:

```
ABTPi18n/
├── apps/
│   ├── backend/          # FastAPI backend
│   └── frontend/         # Next.js frontend
├── docs/                 # Documentation
├── monitoring/           # Prometheus & Grafana configs
└── docker-compose.yml    # Multi-service orchestration
```

**Benefits**:
- Unified version control
- Shared tooling and dependencies
- Easier cross-service testing
- Simplified deployment

### 2. FastAPI Backend
The backend is built with FastAPI, a modern Python framework for building high-performance APIs.

#### Main Application
**File**: `apps/backend/main.py`

**Features**:
- RESTful API endpoints
- Automatic OpenAPI documentation
- CORS middleware for frontend integration
- Health check endpoints
- Asynchronous request handling

**Key Endpoints**:
```http
GET  /health              # Health check
GET  /docs                # Swagger UI documentation
POST /exchange/keys       # Add exchange API key
POST /bot/start           # Start trading bot
POST /bot/stop            # Stop trading bot
GET  /dashboard/pnl       # Get P&L data
```

#### Running the Backend
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Access the API at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 3. Prisma ORM + PostgreSQL
The platform uses Prisma as the ORM layer with PostgreSQL database.

#### Database Schema
**File**: `apps/backend/prisma/schema.prisma`

**Core Models**:
- `User` - User accounts and authentication
- `ExchangeKey` - Encrypted exchange API keys
- `Strategy` - Trading strategy definitions
- `BotRun` - Bot execution instances
- `TradeLog` - Trade execution records

#### Database Setup
```bash
cd apps/backend

# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev

# View database in Prisma Studio
npx prisma studio
```

**Environment Variable**:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/abtpro"
```

### 4. Celery Worker Loop
Asynchronous task processing using Celery with Redis as the message broker.

#### Worker Tasks
**File**: `apps/backend/src/worker/tasks.py`

**Features**:
- Asynchronous bot execution
- Periodic market data fetching
- Background strategy calculations
- Scheduled risk assessments

#### Starting the Worker
```bash
cd apps/backend
celery -A worker worker --loglevel=info
```

**Environment Variables**:
```bash
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

### 5. Encrypted Exchange Keys (AES-GCM)
Secure encryption service for protecting exchange API keys using AES-GCM encryption.

#### Crypto Service
**File**: `apps/backend/src/security/crypto_service.py`

**Implementation**:
- AES-GCM (Galois/Counter Mode) encryption
- 256-bit encryption key
- Unique IV (Initialization Vector) per encryption
- Base64 encoding for storage

**Security Features**:
- Authenticated encryption (prevents tampering)
- No key storage in database (only encrypted values)
- IV uniqueness guarantees
- FIPS 140-2 compliant algorithm

#### Usage Example
```python
from src.security.crypto_service import encrypt_data, decrypt_data

# Encrypt API key
api_key = "your-api-key-here"
api_secret = "your-api-secret-here"

encrypted_key, iv_key = encrypt_data(api_key)
encrypted_secret, iv_secret = encrypt_data(api_secret)

# Store in database
exchange_key = {
    "exchange": "binance",
    "encrypted_key": encrypted_key,
    "iv_key": iv_key,
    "encrypted_secret": encrypted_secret,
    "iv_secret": iv_secret
}

# Decrypt when needed
decrypted_key = decrypt_data(encrypted_key, iv_key)
decrypted_secret = decrypt_data(encrypted_secret, iv_secret)
```

#### Environment Setup
Generate a secure encryption key:
```bash
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

Add to `.env`:
```bash
ENCRYPTION_KEY="<base64-encoded-32-byte-key>"
```

### 6. Strategy Interface + RSI Cross Strategy
Pluggable strategy architecture with the first production strategy implementation.

#### Strategy Interface
**File**: `apps/backend/src/trading/strategies/__init__.py`

**Base Strategy Pattern**:
```python
class BaseStrategy:
    def execute(self, ticker_data: dict, context: dict) -> dict:
        """
        Execute strategy logic
        
        Args:
            ticker_data: Market data (OHLCV)
            context: Additional context (symbol, timeframe, etc.)
            
        Returns:
            dict: {
                "signal": "BUY" | "SELL" | "HOLD",
                "confidence": 0.0 to 1.0,
                "reason": "explanation"
            }
        """
        raise NotImplementedError
```

#### RSI Cross Strategy
**File**: `apps/backend/src/trading/strategies/rsi_cross_strategy.py`

**Description**: Momentum-based strategy using Relative Strength Index (RSI)

**Parameters**:
- `rsi_period`: RSI calculation period (default: 14)
- `oversold_threshold`: Buy signal threshold (default: 30)
- `overbought_threshold`: Sell signal threshold (default: 70)

**Signal Logic**:
- **BUY**: RSI crosses above oversold threshold (e.g., 30)
- **SELL**: RSI crosses below overbought threshold (e.g., 70)
- **HOLD**: RSI in neutral zone

**Usage Example**:
```python
from src.trading.strategies.rsi_cross_strategy import RSICrossStrategy

strategy = RSICrossStrategy(rsi_period=14, oversold=30, overbought=70)

ticker_data = {
    "closes": [100, 101, 102, 103, 104],  # Closing prices
    "symbol": "BTC/USDT"
}

result = strategy.execute(ticker_data, {})
print(result)
# {"signal": "BUY", "confidence": 0.8, "reason": "RSI crossed above 30"}
```

### 7. Exchange Integration (CCXT)
Integration with cryptocurrency exchanges using the CCXT library.

#### Exchange Service
**File**: `apps/backend/src/services/exchange_service.py`

**Features**:
- Multi-exchange support (Binance, Kraken, Coinbase, etc.)
- Unified API across exchanges
- Market data fetching (OHLCV, ticker, orderbook)
- Order execution (market, limit orders)
- Balance and position queries

**Supported Operations**:
```python
from src.services.exchange_service import ExchangeService

service = ExchangeService()

# Fetch market data
ohlcv = await service.fetch_ohlcv("binance", "BTC/USDT", "1h")

# Get ticker
ticker = await service.fetch_ticker("binance", "BTC/USDT")

# Place order
order = await service.create_order(
    exchange="binance",
    symbol="BTC/USDT",
    side="buy",
    type="market",
    amount=0.001
)
```

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start with Docker Compose

1. **Clone the repository**:
```bash
git clone https://github.com/ZeaZDev/ABTPi18n.git
cd ABTPi18n
```

2. **Create `.env` file**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Generate encryption key**:
```bash
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
# Add to .env as ENCRYPTION_KEY
```

4. **Start services**:
```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Celery Worker
- Frontend (port 3000)

5. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Installation

#### Backend Setup
```bash
cd apps/backend

# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev

# Start backend
uvicorn main:app --reload --port 8000
```

#### Celery Worker
```bash
cd apps/backend
celery -A worker worker --loglevel=info
```

#### Frontend Setup
```bash
cd apps/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/abtpro"

# Redis
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# Security
ENCRYPTION_KEY="<base64-encoded-32-byte-key>"

# API
CORS_ORIGINS="http://localhost:3000"
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

## API Reference

### Exchange Key Management

#### Add Exchange Key
```http
POST /exchange/keys
Content-Type: application/json

{
  "exchange": "binance",
  "api_key": "your-api-key",
  "api_secret": "your-api-secret",
  "user_id": 1
}
```

**Response**:
```json
{
  "id": 1,
  "exchange": "binance",
  "encrypted_key": "<encrypted>",
  "iv_key": "<iv>",
  "encrypted_secret": "<encrypted>",
  "iv_secret": "<iv>",
  "created_at": "2024-11-09T00:00:00Z"
}
```

### Bot Control

#### Start Bot
```http
POST /bot/start
Content-Type: application/json

{
  "user_id": 1,
  "strategy": "RSI_CROSS",
  "symbol": "BTC/USDT",
  "timeframe": "1h"
}
```

#### Stop Bot
```http
POST /bot/stop
Content-Type: application/json

{
  "bot_run_id": 1
}
```

### Dashboard

#### Get P&L
```http
GET /dashboard/pnl?user_id=1
```

**Response**:
```json
{
  "total_pnl": 1250.50,
  "trades": 45,
  "win_rate": 0.67,
  "recent_trades": [...]
}
```

## Testing

### Run Backend Tests
```bash
cd apps/backend
pytest
```

### Test Strategy
```python
from src.trading.strategies.rsi_cross_strategy import RSICrossStrategy

strategy = RSICrossStrategy()
ticker_data = {"closes": [100, 102, 101, 103, 105]}
result = strategy.execute(ticker_data, {})
assert result["signal"] in ["BUY", "SELL", "HOLD"]
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `docker ps` or `systemctl status postgresql`
- Check DATABASE_URL in `.env`
- Test connection: `psql <DATABASE_URL>`

### Encryption Key Errors
- Ensure ENCRYPTION_KEY is set in `.env`
- Verify it's base64-encoded 32 bytes
- Regenerate if needed: `python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"`

### Celery Worker Not Starting
- Check Redis is running: `redis-cli ping`
- Verify CELERY_BROKER_URL in `.env`
- Check worker logs: `docker logs abt_worker`

### CCXT Exchange Errors
- Verify API keys are correct
- Check exchange API status
- Ensure IP whitelisting (if required by exchange)
- Check rate limits

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Rotate encryption keys** periodically
3. **Use strong API keys** with minimal permissions
4. **Enable IP whitelisting** on exchanges
5. **Monitor access logs** regularly
6. **Keep dependencies updated**
7. **Use HTTPS** in production

## Next Steps (Phase 2)
- Additional trading strategies (Mean Reversion, Breakout, VWAP)
- Enhanced risk management (Max Drawdown Tracker, Circuit Breaker)
- Real-time WebSocket market data
- Prometheus metrics and Grafana dashboards

## Support

For questions or issues:
- Review the [Contributing Guide](../../guides/CONTRIBUTING.md)
- Check the [Security Model](../../guides/SECURITY.md)
- See the [Roadmap](../../guides/ROADMAP.md) for planned features
