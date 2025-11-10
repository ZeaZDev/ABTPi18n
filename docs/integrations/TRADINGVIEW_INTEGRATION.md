# TradingView Integration Guide

## Overview

The ABTPro i18n platform now supports integration with TradingView alerts through webhooks. This allows you to execute automated trades based on your TradingView strategies, indicators, and custom alerts.

## Features

- **Webhook Endpoint**: Receive real-time alerts from TradingView
- **Strategy Execution**: Automatically execute trades based on TradingView signals
- **Google Drive Integration**: Load strategy configurations from Google Drive folders
- **Alert History**: Track and audit all received TradingView alerts
- **Security**: Webhook authentication via secret tokens
- **Flexible Configuration**: Support for custom parameters and risk management

## Quick Start

### 1. Set Up Webhook Secret

Add the following to your `.env` file:

```bash
TRADINGVIEW_WEBHOOK_SECRET=your-secure-secret-key-here
API_BASE_URL=https://your-domain.com
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Configure TradingView Alert

1. Open TradingView and create an alert on your chart
2. In the alert settings:
   - **Webhook URL**: `https://your-domain.com/tradingview/webhook`
   - **Message**: Use JSON format (see example below)
3. Add a custom header in TradingView (if supported) or include secret in message

### 3. Alert Message Format

Use this JSON format in your TradingView alert message:

```json
{
  "ticker": "{{ticker}}",
  "action": "BUY",
  "price": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "strategy": "My TradingView Strategy",
  "volume": {{volume}}
}
```

#### Supported Actions
- `BUY` - Open long position
- `SELL` - Open short position or close long
- `CLOSE` - Close any open position
- `HOLD` - No action (informational only)

#### Available TradingView Placeholders
- `{{ticker}}` - Trading pair symbol
- `{{close}}` - Current close price
- `{{open}}` - Current open price
- `{{high}}` - Current high price
- `{{low}}` - Current low price
- `{{volume}}` - Current volume
- `{{time}}` - Alert timestamp
- `{{interval}}` - Chart timeframe
- `{{strategy.order.action}}` - Strategy order action

## API Endpoints

### POST /tradingview/webhook

Receive TradingView webhook alerts.

**Headers:**
```
X-Webhook-Secret: your-secret-key
Content-Type: application/json
```

**Request Body:**
```json
{
  "ticker": "BTCUSDT",
  "exchange": "binance",
  "action": "BUY",
  "price": 45000.50,
  "strategy": "RSI Divergence",
  "interval": "1h",
  "message": "RSI bullish divergence detected"
}
```

**Response:**
```json
{
  "status": "success",
  "alert_id": 123,
  "message": "Alert received: BUY BTCUSDT",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /tradingview/alerts

List recent TradingView alerts.

**Query Parameters:**
- `limit` (int, default: 50) - Maximum number of alerts to return
- `ticker` (string, optional) - Filter by ticker symbol
- `action` (string, optional) - Filter by action (BUY, SELL, CLOSE)

**Response:**
```json
{
  "alerts": [
    {
      "id": 123,
      "ticker": "BTCUSDT",
      "exchange": "binance",
      "action": "BUY",
      "price": 45000.50,
      "strategy": "RSI Divergence",
      "interval": "1h",
      "message": "RSI bullish divergence detected",
      "received_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

### GET /tradingview/config

Get webhook configuration instructions.

**Response:**
```json
{
  "webhook_url": "https://your-domain.com/tradingview/webhook",
  "setup_instructions": {
    "step_1": "Create an alert in TradingView",
    "step_2": "Set Webhook URL to: https://your-domain.com/tradingview/webhook",
    "step_3": "Add custom header: X-Webhook-Secret: your-secret-key",
    "step_4": "Configure alert message in JSON format"
  },
  "supported_actions": ["BUY", "SELL", "CLOSE", "HOLD"]
}
```

## Google Drive Integration

### Loading Strategies from Google Drive

The platform can automatically load TradingView strategy configurations from a Google Drive folder.

**Example Usage:**

```python
from src.services.gdrive_loader import load_tradingview_strategies_from_gdrive

# Load strategies from Google Drive folder
strategies = load_tradingview_strategies_from_gdrive(
    "https://drive.google.com/drive/folders/1YlCnoQSP8MlfJO6c1GySn32joXIzgz3G"
)

for strategy in strategies:
    print(f"Loaded: {strategy['name']}")
```

### Strategy Configuration Format

Create YAML or JSON files in your Google Drive folder:

**Example: `my_strategy.yaml`**

```yaml
name: "TradingView RSI Strategy"
description: "RSI-based strategy with TradingView alerts"
type: "TRADINGVIEW"

parameters:
  min_confidence: 0.7
  risk_per_trade: 1.0
  stop_loss_percent: 2.0
  take_profit_percent: 4.0

symbols:
  - "BTC/USDT"
  - "ETH/USDT"

timeframes:
  - "15m"
  - "1h"

webhook:
  auto_trade: false
  validate_price: true
  price_deviation_threshold: 5.0
```

## Using the TradingView Strategy

The `TRADINGVIEW` strategy is automatically registered and can be used in bot configurations:

```python
# Start a bot with TradingView strategy
POST /bot/start
{
  "strategy": "TRADINGVIEW",
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "parameters": {
    "min_confidence": 0.7
  }
}
```

The strategy will:
1. Listen for TradingView alerts for the specified symbol
2. Validate alerts against configured parameters
3. Execute trades if confidence threshold is met
4. Log all activity for audit purposes

## Security Best Practices

1. **Use Strong Secrets**: Generate cryptographically secure webhook secrets
2. **HTTPS Only**: Always use HTTPS for webhook URLs in production
3. **Validate Alerts**: Enable price validation to prevent erroneous trades
4. **Monitor Logs**: Regularly check audit logs for suspicious activity
5. **Rate Limiting**: Consider implementing rate limiting on webhook endpoint
6. **Test First**: Use paper trading mode before enabling auto-trading

## Troubleshooting

### Webhook Not Receiving Alerts

1. Check that `TRADINGVIEW_WEBHOOK_SECRET` is set in `.env`
2. Verify webhook URL is accessible from internet
3. Check firewall/security group settings
4. Review FastAPI logs for error messages
5. Test webhook with curl:

```bash
curl -X POST https://your-domain.com/tradingview/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your-secret-key" \
  -d '{
    "ticker": "BTCUSDT",
    "action": "BUY",
    "price": 45000
  }'
```

### Alerts Not Executing Trades

1. Check that `auto_trade` is enabled in strategy config
2. Verify confidence threshold is met
3. Check exchange API keys are configured
4. Review bot status (should be RUNNING)
5. Check risk management limits

### Google Drive Download Issues

1. Ensure folder/file is publicly shared
2. Check that `gdown` package is installed
3. Verify internet connectivity
4. Try downloading with direct file ID

## Example TradingView Script

Here's a simple Pine Script example that sends webhook alerts:

```pine
//@version=5
strategy("RSI Strategy with Webhook", overlay=true)

// Parameters
rsiLength = input.int(14, "RSI Length")
rsiOversold = input.int(30, "RSI Oversold")
rsiOverbought = input.int(70, "RSI Overbought")

// Calculate RSI
rsi = ta.rsi(close, rsiLength)

// Generate signals
longCondition = ta.crossover(rsi, rsiOversold)
shortCondition = ta.crossunder(rsi, rsiOverbought)

// Execute trades
if longCondition
    strategy.entry("Long", strategy.long, 
        alert_message='{"ticker": "' + syminfo.ticker + '", "action": "BUY", "price": ' + str.tostring(close) + ', "strategy": "RSI Strategy"}')

if shortCondition
    strategy.entry("Short", strategy.short,
        alert_message='{"ticker": "' + syminfo.ticker + '", "action": "SELL", "price": ' + str.tostring(close) + ', "strategy": "RSI Strategy"}')

// Plot
plot(rsi, "RSI", color=color.blue)
hline(rsiOverbought, "Overbought", color=color.red)
hline(rsiOversold, "Oversold", color=color.green)
```

## Advanced Configuration

### Custom Alert Processing

You can extend the webhook endpoint to add custom processing logic:

```python
# In tradingview_endpoints.py
async def process_alert(alert: TradingViewAlert):
    # Custom validation
    if alert.ticker not in ALLOWED_SYMBOLS:
        raise HTTPException(400, "Symbol not allowed")
    
    # Custom notifications
    await send_telegram_notification(
        f"TradingView Alert: {alert.action} {alert.ticker}"
    )
    
    # Custom trade execution
    if should_auto_trade(alert):
        await execute_trade(alert)
```

### Multi-Strategy Support

Configure different strategies for different symbols:

```yaml
strategies:
  - name: "BTC Strategy"
    symbols: ["BTC/USDT"]
    parameters:
      min_confidence: 0.8
  
  - name: "Altcoin Strategy"
    symbols: ["ETH/USDT", "BNB/USDT"]
    parameters:
      min_confidence: 0.7
```

## Support

For issues or questions:
- Check the [main documentation](../README.md)
- Review [API documentation](http://localhost:8000/docs)
- Open an issue on [GitHub](https://github.com/ZeaZDev/ABTPi18n/issues)

## References

- [TradingView Webhooks Documentation](https://www.tradingview.com/support/solutions/43000529348-about-webhooks/)
- [Pine Script Reference](https://www.tradingview.com/pine-script-reference/v5/)
- [CCXT Documentation](https://docs.ccxt.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
