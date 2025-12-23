# API Reference - UltimatePro Advance Enterprise

Complete API documentation for ABTPro UltimatePro Advance Enterprise Edition.

## Base URL

```
Production: https://api.abtpro.com/v1
Development: http://localhost:8000/v1
```

## Authentication

All API requests require authentication using JWT tokens.

### Obtaining an Access Token

```bash
POST /auth/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Using the Access Token

Include the token in the Authorization header:

```bash
Authorization: Bearer <your_access_token>
```

### Refreshing Tokens

```bash
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Rate Limiting

Enterprise tier rate limits:
- **Per Minute**: 1000 requests
- **Per Hour**: 10,000 requests
- **Per Day**: 100,000 requests

Rate limit headers in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Bot Management API

### List All Bots

```bash
GET /bots
```

**Query Parameters:**
- `status` (optional): Filter by status (`active`, `paused`, `stopped`)
- `strategy` (optional): Filter by strategy name
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "bots": [
    {
      "id": "bot_123abc",
      "name": "BTC RSI Bot",
      "status": "active",
      "strategy": "RSI_CROSS",
      "exchange": "binance",
      "symbol": "BTC/USDT",
      "created_at": "2024-01-15T10:30:00Z",
      "performance": {
        "total_pnl": 1234.56,
        "total_trades": 45,
        "win_rate": 0.64
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

### Get Bot Details

```bash
GET /bots/{bot_id}
```

**Response:**
```json
{
  "id": "bot_123abc",
  "name": "BTC RSI Bot",
  "status": "active",
  "strategy": "RSI_CROSS",
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "parameters": {
    "rsi_period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "risk_management": {
    "stop_loss_percent": 2.0,
    "take_profit_percent": 5.0,
    "max_position_size": 0.1
  },
  "performance": {
    "total_pnl": 1234.56,
    "total_trades": 45,
    "win_rate": 0.64,
    "sharpe_ratio": 1.8,
    "max_drawdown": 0.12
  },
  "current_position": {
    "side": "long",
    "size": 0.05,
    "entry_price": 45000,
    "current_price": 46500,
    "unrealized_pnl": 75.0
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:22:00Z"
}
```

### Create Bot

```bash
POST /bots
Content-Type: application/json

{
  "name": "My Trading Bot",
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "strategy": "RSI_CROSS",
  "parameters": {
    "rsi_period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "risk_management": {
    "stop_loss_percent": 2.0,
    "take_profit_percent": 5.0,
    "max_position_size": 0.1
  },
  "mode": "paper"
}
```

**Response:**
```json
{
  "id": "bot_456def",
  "name": "My Trading Bot",
  "status": "stopped",
  "message": "Bot created successfully. Use /bots/{id}/start to begin trading."
}
```

### Start Bot

```bash
POST /bots/{bot_id}/start
```

**Response:**
```json
{
  "id": "bot_123abc",
  "status": "active",
  "message": "Bot started successfully"
}
```

### Stop Bot

```bash
POST /bots/{bot_id}/stop
```

**Query Parameters:**
- `close_positions` (optional): Boolean, close all positions when stopping (default: false)

**Response:**
```json
{
  "id": "bot_123abc",
  "status": "stopped",
  "message": "Bot stopped successfully"
}
```

### Update Bot

```bash
PATCH /bots/{bot_id}
Content-Type: application/json

{
  "parameters": {
    "rsi_period": 12,
    "oversold": 28
  }
}
```

**Response:**
```json
{
  "id": "bot_123abc",
  "message": "Bot updated successfully",
  "changes_applied": ["parameters"]
}
```

### Delete Bot

```bash
DELETE /bots/{bot_id}
```

**Response:**
```json
{
  "message": "Bot deleted successfully"
}
```

## Strategy Management API

### List Available Strategies

```bash
GET /strategies
```

**Response:**
```json
{
  "strategies": [
    {
      "id": "RSI_CROSS",
      "name": "RSI Crossover",
      "description": "Classic RSI oversold/overbought strategy",
      "version": "2.0.0",
      "parameters": [
        {
          "name": "rsi_period",
          "type": "integer",
          "default": 14,
          "min": 7,
          "max": 28,
          "description": "Period for RSI calculation"
        },
        {
          "name": "oversold",
          "type": "integer",
          "default": 30,
          "min": 10,
          "max": 40,
          "description": "Oversold threshold"
        },
        {
          "name": "overbought",
          "type": "integer",
          "default": 70,
          "min": 60,
          "max": 90,
          "description": "Overbought threshold"
        }
      ],
      "supported_exchanges": ["binance", "kraken", "coinbase"],
      "backtest_results": {
        "sharpe_ratio": 1.8,
        "max_drawdown": 0.15,
        "win_rate": 0.62
      }
    }
  ]
}
```

### Get Strategy Details

```bash
GET /strategies/{strategy_id}
```

### Deploy Custom Strategy

```bash
POST /strategies/deploy
Content-Type: multipart/form-data

{
  "file": <strategy.zip>,
  "name": "my_custom_strategy",
  "version": "1.0.0",
  "description": "My custom trading strategy"
}
```

**Response:**
```json
{
  "id": "custom_789ghi",
  "name": "my_custom_strategy",
  "status": "validating",
  "message": "Strategy uploaded. Validation in progress."
}
```

## Trade History API

### Get Trades

```bash
GET /trades
```

**Query Parameters:**
- `bot_id` (optional): Filter by bot
- `symbol` (optional): Filter by trading pair
- `start_date` (optional): ISO 8601 format
- `end_date` (optional): ISO 8601 format
- `page`, `per_page`: Pagination

**Response:**
```json
{
  "trades": [
    {
      "id": "trade_101",
      "bot_id": "bot_123abc",
      "symbol": "BTC/USDT",
      "side": "buy",
      "order_type": "limit",
      "price": 45000,
      "quantity": 0.05,
      "commission": 2.25,
      "commission_asset": "USDT",
      "pnl": 75.0,
      "pnl_percent": 3.33,
      "timestamp": "2024-01-20T14:30:00Z"
    }
  ],
  "summary": {
    "total_trades": 150,
    "total_pnl": 5432.10,
    "win_rate": 0.64,
    "total_commission": 125.50
  }
}
```

### Get Trade Details

```bash
GET /trades/{trade_id}
```

## Portfolio API

### Get Portfolio Summary

```bash
GET /portfolio/summary
```

**Response:**
```json
{
  "total_balance_usd": 125000.50,
  "total_pnl_usd": 15432.10,
  "total_pnl_percent": 14.08,
  "accounts": [
    {
      "exchange": "binance",
      "account_id": "binance_main",
      "balance_usd": 75000.30,
      "pnl_usd": 10234.50,
      "allocation_percent": 60.0
    },
    {
      "exchange": "kraken",
      "account_id": "kraken_main",
      "balance_usd": 50000.20,
      "pnl_usd": 5197.60,
      "allocation_percent": 40.0
    }
  ],
  "positions": {
    "total": 15,
    "long": 8,
    "short": 7
  },
  "updated_at": "2024-01-20T15:00:00Z"
}
```

### Get Account Balances

```bash
GET /portfolio/balances
```

**Query Parameters:**
- `exchange` (optional): Filter by exchange

**Response:**
```json
{
  "balances": [
    {
      "exchange": "binance",
      "asset": "USDT",
      "free": 25000.50,
      "locked": 5000.00,
      "total": 30000.50
    },
    {
      "exchange": "binance",
      "asset": "BTC",
      "free": 0.5,
      "locked": 0.1,
      "total": 0.6
    }
  ]
}
```

### Get Portfolio Performance

```bash
GET /portfolio/performance
```

**Query Parameters:**
- `period`: `1d`, `7d`, `30d`, `90d`, `1y`, `all`

**Response:**
```json
{
  "period": "30d",
  "metrics": {
    "total_return": 0.1234,
    "sharpe_ratio": 2.1,
    "max_drawdown": 0.08,
    "volatility": 0.15,
    "alpha": 0.05,
    "beta": 0.8
  },
  "daily_returns": [
    {"date": "2024-01-01", "return": 0.012},
    {"date": "2024-01-02", "return": -0.005}
  ]
}
```

## Backtesting API

### Run Backtest

```bash
POST /backtest/run
Content-Type: application/json

{
  "strategy": "RSI_CROSS",
  "symbol": "BTC/USDT",
  "exchange": "binance",
  "start_date": "2023-01-01",
  "end_date": "2024-01-01",
  "initial_balance": 10000,
  "parameters": {
    "rsi_period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "commission": 0.001
}
```

**Response:**
```json
{
  "backtest_id": "bt_202401",
  "status": "running",
  "message": "Backtest started. Check /backtest/{id} for results."
}
```

### Get Backtest Results

```bash
GET /backtest/{backtest_id}
```

**Response:**
```json
{
  "backtest_id": "bt_202401",
  "status": "completed",
  "results": {
    "initial_balance": 10000,
    "final_balance": 12345.67,
    "total_return": 0.2346,
    "total_trades": 123,
    "win_rate": 0.63,
    "profit_factor": 1.85,
    "sharpe_ratio": 2.1,
    "max_drawdown": 0.12,
    "avg_win": 125.50,
    "avg_loss": -67.80,
    "best_trade": 456.30,
    "worst_trade": -123.45
  },
  "trades": [...],
  "equity_curve": [...]
}
```

## Machine Learning API

### Score Signal

```bash
POST /ml/score-signal
Content-Type: application/json

{
  "signal": {
    "action": "buy",
    "price": 45000,
    "indicators": {
      "rsi": 28,
      "macd": 0.5,
      "volume": 1500000
    }
  },
  "model_version": "v2.0"
}
```

**Response:**
```json
{
  "quality": "high",
  "confidence": 0.85,
  "predicted_success_rate": 0.72,
  "recommended_action": "execute",
  "risk_score": 0.3
}
```

### Optimize Strategy

```bash
POST /ml/optimize
Content-Type: application/json

{
  "strategy": "RSI_CROSS",
  "symbol": "BTC/USDT",
  "optimization_method": "reinforcement_learning",
  "objective": "sharpe_ratio",
  "constraints": {
    "max_drawdown": 0.15,
    "min_win_rate": 0.55
  },
  "episodes": 1000
}
```

**Response:**
```json
{
  "optimization_id": "opt_301",
  "status": "running",
  "estimated_completion": "2024-01-20T18:00:00Z"
}
```

### Get Optimization Results

```bash
GET /ml/optimize/{optimization_id}
```

**Response:**
```json
{
  "optimization_id": "opt_301",
  "status": "completed",
  "optimal_parameters": {
    "rsi_period": 11,
    "oversold": 28,
    "overbought": 73
  },
  "performance": {
    "sharpe_ratio": 2.3,
    "max_drawdown": 0.11,
    "win_rate": 0.67
  },
  "improvement_over_default": 0.28
}
```

## Webhook API

### Register Webhook

```bash
POST /webhooks
Content-Type: application/json

{
  "url": "https://your-server.com/webhook",
  "events": ["trade.executed", "bot.started", "bot.stopped"],
  "secret": "your-webhook-secret"
}
```

**Response:**
```json
{
  "webhook_id": "wh_401",
  "url": "https://your-server.com/webhook",
  "events": ["trade.executed", "bot.started", "bot.stopped"],
  "created_at": "2024-01-20T15:00:00Z"
}
```

### Webhook Payload Example

When an event occurs, ABTPro will send a POST request to your webhook URL:

```json
{
  "event": "trade.executed",
  "timestamp": "2024-01-20T15:30:00Z",
  "data": {
    "trade_id": "trade_501",
    "bot_id": "bot_123abc",
    "symbol": "BTC/USDT",
    "side": "buy",
    "price": 45000,
    "quantity": 0.05,
    "pnl": 75.0
  },
  "signature": "sha256_signature_here"
}
```

## Market Data API

### Get Current Price

```bash
GET /market/price/{symbol}
```

**Example:** `GET /market/price/BTC/USDT`

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "price": 45123.45,
  "timestamp": "2024-01-20T15:35:00Z"
}
```

### Get OHLCV Data

```bash
GET /market/ohlcv/{symbol}
```

**Query Parameters:**
- `timeframe`: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- `limit`: Number of candles (max: 1000)
- `since`: Unix timestamp

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "data": [
    {
      "timestamp": 1640995200000,
      "open": 45000.00,
      "high": 45500.00,
      "low": 44800.00,
      "close": 45200.00,
      "volume": 1234.56
    }
  ]
}
```

## WebSocket API

### Connect to WebSocket

```javascript
const ws = new WebSocket('wss://api.abtpro.com/v1/ws');

// Authenticate
ws.send(JSON.stringify({
  type: 'auth',
  token: 'your_access_token'
}));

// Subscribe to channels
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['trades', 'portfolio', 'market.BTC/USDT']
}));

// Listen for messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Available Channels

- `trades` - Real-time trade executions
- `portfolio` - Portfolio balance updates
- `bots` - Bot status changes
- `market.{symbol}` - Market data for specific pair
- `alerts` - System and user alerts

## Error Handling

All errors follow a consistent format:

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "The 'rsi_period' parameter must be between 7 and 28",
    "details": {
      "parameter": "rsi_period",
      "provided": 5,
      "min": 7,
      "max": 28
    }
  }
}
```

### Common Error Codes

- `UNAUTHORIZED` (401) - Invalid or expired token
- `FORBIDDEN` (403) - Insufficient permissions
- `NOT_FOUND` (404) - Resource not found
- `INVALID_PARAMETER` (400) - Invalid request parameter
- `RATE_LIMIT_EXCEEDED` (429) - Too many requests
- `INTERNAL_ERROR` (500) - Server error

## SDKs and Libraries

Official SDKs available:

- **Python**: `pip install abtpro-sdk`
- **JavaScript/Node.js**: `npm install abtpro-sdk`
- **Go**: `go get github.com/abtpro/abtpro-go`
- **Java**: Maven/Gradle packages available

---

*Next: [Troubleshooting Guide](TROUBLESHOOTING.en.md)*
