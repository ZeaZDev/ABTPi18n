# คู่มือการใช้งาน เฟส 4 (Phase 4) Implementation Guide

## Overview
Phase 4 focuses on monetization features, advanced portfolio management, and comprehensive backtesting capabilities for the ABTPro trading platform.

### Quick Links
- [Phase 4 Summary](PHASE4_SUMMARY.md)
- [Phase 3 Summary](PHASE3_SUMMARY.md)
- [Roadmap](ROADMAP.md)

## New Features

### 1. PromptPay Top-up Flow

Add credits to your account using Thai PromptPay QR codes for seamless payment processing.

#### Features
- Generate PromptPay QR codes for instant payment
- Support for multiple Thai banks
- Automatic balance credit upon payment confirmation
- Real-time payment status updates
- Complete transaction history

#### Configuration
```env
PROMPTPAY_MERCHANT_ID=your-merchant-id
PROMPTPAY_WEBHOOK_SECRET=your-webhook-secret
PAYMENT_GATEWAY_URL=https://payment-gateway.example.com
```

#### Usage

**Making a Top-up:**
1. Navigate to Wallet → Top-up
2. Enter amount in Thai Baht (THB)
3. Click "Generate QR Code"
4. Scan QR code with any Thai banking app
5. Complete payment in your banking app
6. Balance credited automatically (typically within 30 seconds)

**Transaction History:**
1. Go to Wallet → Transactions
2. View all top-ups, deductions, and refunds
3. Filter by date range or status
4. Export transaction report

**API Example:**
```python
# Generate PromptPay QR code
import requests

response = requests.post(
    "http://localhost:8000/payment/promptpay/create",
    json={
        "amount": 1000.00,
        "currency": "THB",
        "description": "Account Top-up"
    },
    headers={"Authorization": f"Bearer {token}"}
)

qr_code_url = response.json()["qr_code_url"]
reference_id = response.json()["reference_id"]
```

### 2. Rental Contract Expiry Enforcement

Automated subscription management with grace periods and auto-renewal options.

#### Features
- Automatic contract expiry checking (daily)
- Email and Telegram notifications before expiry
- Grace period support (configurable)
- Auto-disable bots on contract expiration
- Self-service renewal flow
- Multiple subscription tiers

#### Subscription Plans

**Basic Plan** (฿499/month)
- Up to 2 active bots
- Basic strategies only
- Email support
- Standard notifications

**Premium Plan** (฿1,499/month)
- Up to 10 active bots
- All strategies including advanced
- Priority support
- Real-time Telegram notifications
- Portfolio aggregation

**Enterprise Plan** (฿4,999/month)
- Unlimited bots
- Custom strategies
- Plugin support
- Dedicated support
- API access
- Multi-account portfolio

#### Managing Your Contract

**Viewing Contract Status:**
```bash
# Check current contract
curl -X GET http://localhost:8000/rental/contract \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Renewing Contract:**
1. Go to Settings → Subscription
2. View current plan and expiry date
3. Click "Renew Now" or "Upgrade Plan"
4. Complete payment via PromptPay
5. Contract extended immediately

**Notification Schedule:**
- 7 days before expiry: First reminder
- 3 days before expiry: Second reminder
- 1 day before expiry: Final reminder
- On expiry: All active bots stopped
- Grace period: 3 days (configurable by admin)

### 3. Module Plugin Loader

Extend ABTPro with custom plugins for strategies, indicators, and data sources.

#### Features
- Load custom strategies dynamically
- Add custom technical indicators
- Integrate alternative data sources
- Custom notification channels
- Plugin marketplace for sharing

#### Plugin Types

**Strategy Plugins**
- Custom trading logic
- Access to all platform APIs
- Position and risk management
- Event-driven architecture

**Indicator Plugins**
- Custom technical indicators
- Real-time calculation
- Integration with charting
- Backtesting support

**Data Source Plugins**
- Alternative market data feeds
- Custom websocket connections
- Historical data providers
- News and sentiment sources

**Notification Plugins**
- Custom alert channels (Discord, Slack, etc.)
- Advanced formatting
- Conditional routing
- Rate limiting

#### Creating a Plugin

**1. Define Plugin Structure:**
```python
# my_strategy_plugin.py
from src.plugins.plugin_interface import StrategyPlugin

class MyCustomStrategy(StrategyPlugin):
    name = "my_custom_strategy"
    version = "1.0.0"
    description = "My custom trading strategy"
    
    def __init__(self, config):
        super().__init__(config)
        self.param1 = config.get("param1", 10)
    
    def initialize(self):
        """Called when plugin is loaded"""
        self.logger.info(f"Initializing {self.name}")
    
    def on_candle(self, candle):
        """Called on each new candle"""
        # Your trading logic here
        if self.should_buy(candle):
            return {"action": "BUY", "quantity": 0.1}
        elif self.should_sell(candle):
            return {"action": "SELL", "quantity": 0.1}
        return None
    
    def should_buy(self, candle):
        # Custom buy logic
        return False
    
    def should_sell(self, candle):
        # Custom sell logic
        return False
```

**2. Create Plugin Package:**
```
my-strategy-plugin/
├── setup.py
├── my_strategy/
│   ├── __init__.py
│   └── strategy.py
└── README.md
```

**3. Setup Entry Point:**
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="my-strategy-plugin",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "abtpro.plugins.strategies": [
            "my_custom_strategy = my_strategy.strategy:MyCustomStrategy"
        ]
    }
)
```

**4. Install Plugin:**
```bash
# Via pip install
pip install my-strategy-plugin

# Or via UI
# Navigate to Plugins → Install → Upload ZIP
```

**5. Enable Plugin:**
```python
# API call to enable plugin
import requests

response = requests.post(
    "http://localhost:8000/plugins/install",
    json={
        "plugin_name": "my_custom_strategy",
        "config": {
            "param1": 20
        }
    },
    headers={"Authorization": f"Bearer {token}"}
)
```

#### Plugin Security

- All plugins run in sandboxed environment
- Resource limits enforced (CPU, memory)
- API access based on capability grants
- Code review required for marketplace
- Digital signatures for verification

### 4. Portfolio Aggregation / Multi-Account

Manage multiple trading accounts across different exchanges in one unified dashboard.

#### Features
- Add multiple accounts per exchange
- Consolidated portfolio view
- Cross-account P&L tracking
- Account grouping by strategy
- Real-time position sync
- Aggregate risk metrics

#### Setting Up Multi-Account

**Adding Accounts:**
1. Go to Settings → Accounts
2. Click "Add New Account"
3. Select exchange (Binance, Bybit, etc.)
4. Enter API credentials
5. Provide account label (e.g., "Main Trading", "Scalping Bot")
6. Optionally assign to group
7. Click "Add Account"

**Managing Accounts:**
```python
# API: Add account
import requests

response = requests.post(
    "http://localhost:8000/portfolio/accounts",
    json={
        "exchange": "binance",
        "api_key": "your_api_key",
        "api_secret": "your_api_secret",
        "label": "Main Trading Account",
        "group": "Long-term Strategies"
    },
    headers={"Authorization": f"Bearer {token}"}
)
```

**Viewing Portfolio:**
1. Navigate to Portfolio → Overview
2. See aggregated positions across all accounts
3. Filter by exchange, account, or group
4. View combined P&L and metrics
5. Drill down into individual accounts

#### Portfolio Metrics

**Aggregated Metrics:**
- Total Portfolio Value (in USD/THB)
- Combined P&L (Realized + Unrealized)
- Total Exposure (Long + Short)
- Risk Metrics (Value at Risk, Max Drawdown)
- Sharpe Ratio (portfolio level)
- Correlation between accounts

**Account-Level Metrics:**
- Individual account balance
- Account-specific P&L
- Active positions per account
- Account utilization (margin used)

**API Example:**
```python
# Get portfolio summary
response = requests.get(
    "http://localhost:8000/portfolio/summary",
    headers={"Authorization": f"Bearer {token}"}
)

portfolio = response.json()
print(f"Total Value: {portfolio['total_value']}")
print(f"Total PnL: {portfolio['total_pnl']}")
print(f"Number of Positions: {portfolio['position_count']}")
```

### 5. Backtester / Paper Trading Mode

Test strategies risk-free with historical data or live market simulation.

#### Features

**Backtesting:**
- Test on historical market data
- Realistic slippage and commission modeling
- Comprehensive performance metrics
- Parameter optimization
- Walk-forward analysis
- Visual equity curves

**Paper Trading:**
- Live market data with simulated execution
- Virtual balance (no real money)
- Real-time strategy validation
- Monitor performance before going live
- Seamless transition to live trading

#### Running a Backtest

**1. Prepare Backtest:**
```python
# API: Create backtest
import requests

response = requests.post(
    "http://localhost:8000/backtest/run",
    json={
        "strategy_name": "rsi_cross",
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_capital": 10000,
        "commission": 0.001,
        "slippage": 0.0005,
        "parameters": {
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70
        }
    },
    headers={"Authorization": f"Bearer {token}"}
)

backtest_id = response.json()["backtest_id"]
```

**2. Monitor Progress:**
```python
# Check backtest status
response = requests.get(
    f"http://localhost:8000/backtest/runs/{backtest_id}",
    headers={"Authorization": f"Bearer {token}"}
)

status = response.json()
print(f"Status: {status['status']}")
print(f"Progress: {status['progress']}%")
```

**3. View Results:**
1. Go to Backtesting → Results
2. Select completed backtest
3. View performance metrics:
   - Total Return
   - Sharpe Ratio
   - Maximum Drawdown
   - Win Rate
   - Profit Factor
   - Number of Trades
4. Analyze equity curve
5. Review trade-by-trade history
6. Export detailed report

#### Performance Metrics Explained

**Total Return:** Overall percentage gain/loss
```
Total Return = (Final Capital - Initial Capital) / Initial Capital × 100%
```

**Sharpe Ratio:** Risk-adjusted return
```
Sharpe Ratio = (Average Return - Risk-Free Rate) / Standard Deviation of Returns
```

**Maximum Drawdown:** Largest peak-to-trough decline
```
Max Drawdown = (Trough Value - Peak Value) / Peak Value × 100%
```

**Win Rate:** Percentage of profitable trades
```
Win Rate = (Winning Trades / Total Trades) × 100%
```

**Profit Factor:** Ratio of gross profit to gross loss
```
Profit Factor = Gross Profit / Gross Loss
```

#### Starting Paper Trading

**1. Create Paper Trading Session:**
```python
# API: Start paper trading
response = requests.post(
    "http://localhost:8000/backtest/paper/start",
    json={
        "strategy_name": "mean_reversion",
        "symbol": "ETH/USDT",
        "timeframe": "15m",
        "virtual_balance": 5000,
        "parameters": {
            "period": 20,
            "std_dev": 2
        }
    },
    headers={"Authorization": f"Bearer {token}"}
)

session_id = response.json()["session_id"]
```

**2. Monitor Performance:**
1. Go to Paper Trading → Active Sessions
2. View real-time performance
3. Check open positions
4. Monitor virtual balance
5. Review trade history

**3. Stop Session:**
```python
# Stop paper trading
requests.post(
    "http://localhost:8000/backtest/paper/stop",
    json={"session_id": session_id},
    headers={"Authorization": f"Bearer {token}"}
)
```

**4. Transition to Live:**
1. Review paper trading results
2. If satisfied, go to Bot Control
3. Start same strategy with live trading
4. Use proven parameters from paper trading

## Installation

### Prerequisites
- Phase 1, 2, and 3 completed
- Node.js 18+ and Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Docker and Docker Compose

### Setup Steps

**1. Update Dependencies**
```bash
# Backend
cd apps/backend
pip install -r requirements.txt

# Frontend
cd apps/frontend
npm install
```

**2. Configure Environment Variables**
```bash
# Add to .env file
PROMPTPAY_MERCHANT_ID=your-merchant-id
PROMPTPAY_WEBHOOK_SECRET=your-webhook-secret
PAYMENT_GATEWAY_URL=https://payment-gateway.example.com
PLUGIN_REGISTRY_URL=https://plugins.abtpro.com
ENABLE_PAPER_TRADING=true
```

**3. Run Database Migrations**
```bash
cd apps/backend
npx prisma migrate dev --name phase4_initial
```

**4. Start Services**
```bash
docker-compose up -d
```

**5. Initialize Default Data**
```bash
# Create default subscription plans
python scripts/init_rental_plans.py

# Load example plugins
python scripts/load_example_plugins.py
```

## Configuration

### Payment Gateway Setup

**PromptPay Configuration:**
1. Register for PromptPay merchant account
2. Obtain merchant ID and webhook secret
3. Configure webhook URL: `https://yourdomain.com/payment/webhook/promptpay`
4. Set up SSL certificate for webhooks
5. Test with sandbox environment first

### Subscription Plans Setup

**Creating Custom Plans:**
```python
# scripts/create_custom_plan.py
from prisma import Prisma

async def create_plan():
    prisma = Prisma()
    await prisma.connect()
    
    plan = await prisma.subscriptionplan.create(data={
        "name": "Custom Plan",
        "price": 2999,
        "currency": "THB",
        "duration_days": 30,
        "max_bots": 5,
        "features": json.dumps([
            "advanced_strategies",
            "telegram_notifications",
            "portfolio_aggregation"
        ])
    })
    
    await prisma.disconnect()
```

### Plugin Configuration

**Plugin Registry:**
```env
# .env
PLUGIN_REGISTRY_URL=https://plugins.abtpro.com
PLUGIN_VERIFY_SIGNATURES=true
PLUGIN_MAX_MEMORY_MB=512
PLUGIN_MAX_CPU_PERCENT=50
```

## API Endpoints

### Payment Endpoints
```http
# Generate PromptPay QR
POST /payment/promptpay/create
{
  "amount": 1000.00,
  "currency": "THB",
  "description": "Account Top-up"
}

# Get wallet balance
GET /payment/wallet

# Get transaction history
GET /payment/transactions?page=1&limit=20

# Webhook callback (internal)
POST /payment/webhook/promptpay
```

### Rental Endpoints
```http
# Get current contract
GET /rental/contract

# List available plans
GET /rental/plans

# Renew contract
POST /rental/renew
{
  "plan_id": 2,
  "payment_method": "promptpay"
}

# Get contract features
GET /rental/features
```

### Plugin Endpoints
```http
# List available plugins
GET /plugins/available?type=strategy

# Install plugin
POST /plugins/install
{
  "plugin_name": "my_custom_strategy",
  "config": {"param1": 20}
}

# Toggle plugin
POST /plugins/{plugin_id}/toggle
{
  "enabled": true
}

# Get plugin config
GET /plugins/{plugin_id}/config
```

### Portfolio Endpoints
```http
# Get portfolio summary
GET /portfolio/summary

# List accounts
GET /portfolio/accounts

# Add account
POST /portfolio/accounts
{
  "exchange": "binance",
  "api_key": "...",
  "api_secret": "...",
  "label": "Main Account",
  "group": "Long-term"
}

# Get all positions
GET /portfolio/positions

# Get performance metrics
GET /portfolio/performance?timeframe=30d
```

### Backtest Endpoints
```http
# Run backtest
POST /backtest/run
{
  "strategy_name": "rsi_cross",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_capital": 10000
}

# Get backtest results
GET /backtest/runs/{run_id}

# Start paper trading
POST /backtest/paper/start
{
  "strategy_name": "mean_reversion",
  "symbol": "ETH/USDT",
  "timeframe": "15m",
  "virtual_balance": 5000
}

# Stop paper trading
POST /backtest/paper/stop
{
  "session_id": "session-123"
}
```

## Testing

### Payment Testing
```bash
# Test PromptPay QR generation
pytest tests/test_promptpay.py -v

# Test webhook handling
pytest tests/test_payment_webhook.py -v

# Simulate payment callback
curl -X POST http://localhost:8000/payment/webhook/promptpay \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: test-signature" \
  -d '{"reference_id": "ref-123", "status": "SUCCESS"}'
```

### Rental Contract Testing
```bash
# Test expiry checking
pytest tests/test_rental_expiry.py -v

# Run expiry check task manually
python -m celery -A src.worker.celery_app call src.worker.tasks.check_contract_expiry
```

### Plugin Testing
```bash
# Test plugin loading
pytest tests/test_plugin_loader.py -v

# Test example plugin
pytest plugins/example_strategy/tests/ -v
```

### Backtesting Testing
```bash
# Test backtest engine
pytest tests/test_backtest_engine.py -v

# Run sample backtest
python scripts/run_sample_backtest.py
```

## Troubleshooting

### Payment Issues

**QR Code Not Generating:**
- Check PromptPay merchant ID is valid
- Verify payment gateway URL is accessible
- Check error logs: `docker-compose logs backend | grep payment`

**Webhook Not Received:**
- Verify webhook URL is publicly accessible (use ngrok for local testing)
- Check webhook secret matches configuration
- Ensure SSL certificate is valid
- Check firewall settings

**Balance Not Updated:**
- Check webhook signature validation
- Review transaction status in database
- Check Celery worker is processing payment tasks

### Rental Issues

**Contract Not Expiring:**
- Check Celery beat scheduler is running: `docker-compose ps celery-beat`
- Verify cron schedule in `src/worker/celery_app.py`
- Run expiry check manually for testing

**Grace Period Not Working:**
- Check `gracePeriodDays` value in database
- Review expiry logic in `src/services/rental_service.py`

### Plugin Issues

**Plugin Not Loading:**
- Verify plugin package is installed: `pip list | grep plugin-name`
- Check entry point configuration in `setup.py`
- Review plugin loader logs: `docker-compose logs backend | grep plugin`

**Plugin Execution Error:**
- Check plugin has required capabilities
- Verify plugin configuration is valid JSON
- Review resource limits (CPU, memory)
- Check plugin signature if verification enabled

### Portfolio Issues

**Positions Not Syncing:**
- Verify API keys are valid and have read permissions
- Check exchange API rate limits
- Review position sync task logs
- Ensure Redis is running for caching

**Incorrect Aggregation:**
- Check currency conversion rates are up to date
- Verify all accounts use same base currency
- Review aggregation logic for edge cases

### Backtest Issues

**Backtest Not Starting:**
- Check historical data is available for symbol/date range
- Verify strategy name exists
- Ensure no concurrent backtest limit reached
- Check Celery worker is running

**Incorrect Results:**
- Verify commission and slippage values
- Check data quality (gaps, anomalies)
- Review strategy logic for bugs
- Compare with known results for validation

## Security Considerations

### Payment Security
- All payment webhooks require signature validation
- Use HTTPS for all payment endpoints
- Implement idempotency keys for duplicate prevention
- Log all transactions for audit
- Rate limit payment endpoints (10 requests/minute)

### Plugin Security
- Plugins verified before marketplace listing
- Resource limits enforced (512MB RAM, 50% CPU)
- Sandboxed execution environment
- Capability-based API access
- Regular security audits of popular plugins

### Data Protection
- Encrypt wallet balances in database
- Secure multi-account API keys with AES-GCM
- Audit log for all financial operations
- Regular backups of transaction data
- GDPR compliance for user data

## Performance Optimization

### Payment Processing
- Queue webhook processing via Celery
- Cache QR codes for 5 minutes
- Use connection pooling for database
- Index transaction table by reference_id

### Portfolio Aggregation
- Cache aggregated results for 5 minutes
- Use database views for complex queries
- Implement pagination (50 items per page)
- Background sync every 30 seconds

### Backtesting
- Limit concurrent backtests to 3 per user
- Stream results for large datasets
- Cache historical data (1-hour TTL)
- Use progress tracking for long-running tests

## Best Practices

### Payment Best Practices
- Always provide transaction references to users
- Send email confirmation for successful top-ups
- Implement refund policy and process
- Keep transaction history for at least 7 years
- Regularly reconcile with payment gateway

### Contract Management
- Send renewal reminders well in advance
- Offer auto-renewal discount incentives
- Provide clear upgrade/downgrade paths
- Grace period should be clearly communicated
- Handle edge cases (timezone differences, holidays)

### Plugin Development
- Follow plugin naming conventions
- Provide comprehensive README
- Include example configurations
- Write unit tests for plugin logic
- Version plugins using semantic versioning

### Portfolio Management
- Regularly verify exchange balances
- Handle exchange maintenance windows
- Provide account labeling for organization
- Set up alerts for large position changes
- Regular reconciliation reports

### Backtesting
- Use sufficient historical data (at least 1 year)
- Test multiple market conditions (bull, bear, sideways)
- Validate results with out-of-sample data
- Document assumptions (commission, slippage)
- Use walk-forward analysis for robustness

## Next Steps (Phase 5)

According to the roadmap, Phase 5 includes:
- Audit Trail for all API calls
- Static Code Scan (Bandit, Semgrep)
- Secret Rotation Flow
- DR/Failover Strategy (Multi-region)

## Support

For issues or questions:
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Review [SECURITY.md](SECURITY.md) for security policies
- Check plugin marketplace for community plugins
- Open an issue on GitHub for bugs or feature requests
- Join our Discord community for discussions

## Appendix

### A. PromptPay QR Code Format
PromptPay uses EMVCo QR format with specific Thai payment tags.

### B. Subscription Plan Comparison
Detailed feature comparison table for all subscription tiers.

### C. Plugin API Reference
Complete API documentation for plugin developers.

### D. Backtest Metrics Glossary
Detailed explanations of all performance metrics.

### E. Sample Configurations
Example configurations for common use cases.
