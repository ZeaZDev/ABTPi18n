# คู่มือการใช้งาน เฟส 2 (Phase 2) Implementation Guide

## Overview
Phase 2 adds advanced trading strategies, enhanced risk management, streaming market data via WebSocket, and comprehensive monitoring with Prometheus and Grafana.

### Quick Links
- [Phase 2 Summary](PHASE2_SUMMARY.md)
- [Roadmap](ROADMAP.md)
- [Strategy Guide](STRATEGY_GUIDE.md)

## New Features

### 1. Trading Strategies
Three new strategies have been added:

#### Mean Reversion Strategy
- **Name**: `MEAN_REVERSION`
- **Description**: Uses Bollinger Bands concept to identify overbought/oversold conditions
- **Parameters**:
  - `window`: Moving average period (default: 20)
  - `std_dev_factor`: Standard deviation multiplier (default: 2.0)

#### Breakout Strategy
- **Name**: `BREAKOUT`
- **Description**: Identifies price breakouts from recent highs/lows with volume confirmation
- **Parameters**:
  - `lookback`: Number of periods for high/low (default: 20)
  - `volume_factor`: Volume multiplier for confirmation (default: 1.5)

#### VWAP Strategy
- **Name**: `VWAP`
- **Description**: Volume Weighted Average Price strategy
- **Parameters**:
  - `threshold`: Percentage deviation from VWAP to trigger signals (default: 0.02)

### 2. Enhanced Risk Management

#### Max Drawdown Tracker
- Monitors peak equity and current drawdown
- Halts trading when drawdown exceeds threshold
- Default threshold: 25%

#### Circuit Breaker
- Stops trading after consecutive losses
- Rate limits trades per hour
- Cooldown period after trip
- Default settings:
  - Max consecutive losses: 5
  - Cooldown: 60 minutes
  - Max trades per hour: 20

### 3. WebSocket Market Data
- Real-time streaming market data via CCXT Pro
- Subscribe to ticker and trade updates
- Supports multiple symbols simultaneously
- Auto-reconnection on disconnect

**Usage Example**:
```python
from src.services.websocket_service import get_websocket_instance

ws = get_websocket_instance("binance")
await ws.connect()

async def ticker_callback(ticker):
    print(f"New ticker: {ticker}")

await ws.subscribe_ticker("BTC/USDT", ticker_callback)
```

### 4. Prometheus Metrics & Grafana Dashboards

#### Metrics Available
- **Trading Metrics**:
  - `trading_trades_total`: Total trades executed
  - `trading_trade_pnl`: Profit/Loss histogram
  - `trading_strategy_signals_total`: Strategy signals count

- **Risk Metrics**:
  - `risk_checks_total`: Risk checks performed
  - `risk_circuit_breaker_trips_total`: Circuit breaker trips
  - `risk_max_drawdown`: Current max drawdown
  - `risk_current_equity`: Current equity value
  - `risk_consecutive_losses`: Consecutive loss count

- **Performance Metrics**:
  - `bot_status`: Bot running status
  - `strategy_execution_seconds`: Strategy execution time
  
- **WebSocket Metrics**:
  - `websocket_connections_active`: Active WebSocket connections
  - `websocket_messages_total`: Messages received
  - `websocket_errors_total`: WebSocket errors

- **Exchange API Metrics**:
  - `exchange_api_calls_total`: API calls count
  - `exchange_api_latency_seconds`: API latency histogram

#### Access Points
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3001](http://localhost:3001)
  - Username: `admin`
  - Password: `admin`

## Installation

1. Update dependencies:
```bash
cd apps/backend
pip install -r requirements.txt
```

2. Start services with Docker Compose:
```bash
docker-compose up -d
```

This will start:
- PostgreSQL
- Redis
- Backend API
- Celery Worker
- Frontend
- **Prometheus** (new)
- **Grafana** (new)

## Configuration

### Environment Variables
No new environment variables required for Phase 2 features. All configurations use sensible defaults.

### Risk Manager Configuration
To customize risk parameters when creating a bot:

```python
from src.trading.risk_manager import EnhancedRiskManager

risk_manager = EnhancedRiskManager(
    max_drawdown=0.20,  # 20% max drawdown
    max_position_fraction=0.1,
    max_consecutive_losses=3,
    cooldown_minutes=30,
    max_trades_per_hour=15
)
```

## Monitoring

### Viewing Metrics
1. Open Grafana at [http://localhost:3001](http://localhost:3001)
2. Login with admin/admin
3. Navigate to "ABTPi18n Trading Dashboard"
4. View real-time metrics including:
   - Trade volume
   - Strategy performance
   - Risk metrics
   - System health

### Custom Dashboards
Dashboard configuration is in `/monitoring/grafana/dashboards/abtpro-dashboard.json`. You can:
- Modify existing panels
- Add new metrics
- Create custom visualizations

## API Endpoints

### Metrics Endpoint
```http
GET /metrics
```
Returns Prometheus-formatted metrics for scraping.

## Testing Strategies

To test the new strategies:

```python
from src.trading.strategies.mean_reversion_strategy import MeanReversionStrategy
from src.trading.strategies.breakout_strategy import BreakoutStrategy
from src.trading.strategies.vwap_strategy import VWAPStrategy

# Example ticker data
ticker_data = {
    "closes": [...],  # List of closing prices
    "highs": [...],   # List of high prices
    "lows": [...],    # List of low prices
    "volumes": [...]  # List of volumes
}

strategy = MeanReversionStrategy(window=20, std_dev_factor=2.0)
result = strategy.execute(ticker_data, {"symbol": "BTC/USDT"})
print(result)  # {"signal": "BUY/SELL/HOLD", "confidence": 0.75, ...}
```

## Troubleshooting

### WebSocket Connection Issues
- Ensure CCXT Pro is installed: `pip install ccxt[async]`
- Check exchange API credentials
- Verify network connectivity to exchange

### Prometheus Not Scraping
- Check that backend is running on port 8000
- Verify prometheus.yml configuration
- Check Prometheus logs: `docker logs abt_prometheus`

### Grafana Dashboard Not Loading
- Ensure Prometheus datasource is configured
- Check datasource connection in Grafana settings
- Verify dashboard JSON is valid

## Next Steps (Phase 3)
- Google OAuth Integration
- Telegram notifications
- Dynamic theme configuration
- Additional language support (Chinese, Japanese)
