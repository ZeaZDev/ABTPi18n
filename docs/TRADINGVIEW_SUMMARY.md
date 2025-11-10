# TradingView Integration - Implementation Summary

## Overview

This implementation adds comprehensive TradingView integration to the ABTPro i18n platform, enabling users to:
- Receive webhook alerts from TradingView
- Execute automated trades based on TradingView signals
- Load strategy configurations from Google Drive
- Track and audit all webhook alerts

## What Was Implemented

### 1. TradingView Webhook API (`apps/backend/src/api/tradingview_endpoints.py`)

Three new endpoints were added:

- **POST /tradingview/webhook** - Receives webhook alerts from TradingView
  - Validates webhook secret via `X-Webhook-Secret` header
  - Stores all alerts in database for audit trail
  - Supports BUY, SELL, CLOSE, HOLD actions
  - Returns alert ID and status

- **GET /tradingview/alerts** - Lists recent alerts
  - Supports filtering by ticker and action
  - Configurable limit (default 50)
  - Returns alert history with timestamps

- **GET /tradingview/config** - Configuration instructions
  - Returns webhook URL and setup steps
  - Provides example alert message format
  - Lists supported actions

### 2. TradingView Strategy (`apps/backend/src/trading/strategies/tradingview_strategy.py`)

New `TRADINGVIEW` strategy that:
- Processes webhook alerts as trading signals
- Validates confidence thresholds (default 0.7)
- Performs price deviation checks for safety
- Converts CLOSE actions to SELL
- Follows the existing Strategy interface pattern
- Automatically registers with StrategyRegistry

### 3. Google Drive Integration (`apps/backend/src/services/gdrive_loader.py`)

Utility class for loading strategy configurations:
- Download files/folders from Google Drive using `gdown`
- Parse YAML and JSON configuration files
- Load multiple strategy configs from a folder
- Cache downloads in `/tmp/gdrive_cache`
- Supports the Google Drive URL from the issue

### 4. Database Schema (`apps/backend/prisma/schema.prisma`)

Added `TradingViewAlert` model:
```prisma
model TradingViewAlert {
  id         Int       @id @default(autoincrement())
  ticker     String
  exchange   String    @default("binance")
  action     String    // BUY, SELL, CLOSE, HOLD
  price      Float?
  strategy   String?
  interval   String?
  volume     Float?
  message    String?
  rawPayload String?   // JSON of complete payload
  receivedAt DateTime  @default(now())
  processed  Boolean   @default(false)
  
  @@index([ticker, receivedAt])
  @@index([action])
  @@index([receivedAt])
}
```

### 5. Documentation

- **TradingView Integration Guide** (`docs/integrations/TRADINGVIEW_INTEGRATION.md`)
  - Complete setup instructions
  - API endpoint documentation
  - Example Pine Script
  - Security best practices
  - Troubleshooting guide

- **Google Drive Loader Guide** (`docs/guides/GDRIVE_LOADER_GUIDE.md`)
  - CLI tool usage
  - Python API examples
  - Configuration file format
  - Sharing instructions

### 6. Tools & Examples

- **CLI Tool** (`tools/load_gdrive_strategies.py`)
  - Load strategies from Google Drive via command line
  - Support for custom output directory
  - Cache management
  - Verbose output option

- **Example Configuration** (`strategies/external/tradingview_example.yaml`)
  - Template for TradingView strategy configs
  - Demonstrates all configuration options
  - Ready to use as reference

- **Test Script** (`tools/test_tradingview_integration.py`)
  - Validates implementation without dependencies
  - Tests strategy logic
  - Checks file structure
  - All tests passing

### 7. Configuration Updates

- **Environment Variables** (`.env.example`)
  ```bash
  TRADINGVIEW_WEBHOOK_SECRET=your-webhook-secret
  API_BASE_URL=http://localhost:8000
  ```

- **Main Application** (`apps/backend/main.py`)
  - Registered TradingView router at `/tradingview` prefix
  - Added to tags for API documentation

- **Strategy Registry** (`apps/backend/src/trading/strategies/__init__.py`)
  - Imported and registered TradingViewStrategy
  - Available in strategy list

## How to Use

### 1. Configure Environment

```bash
# Generate secure webhook secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env file
TRADINGVIEW_WEBHOOK_SECRET=<generated-secret>
API_BASE_URL=https://your-domain.com
```

### 2. Run Database Migration

```bash
cd apps/backend
npx prisma migrate dev --name add_tradingview_alerts
```

### 3. Configure TradingView Alert

1. Create alert in TradingView
2. Set webhook URL: `https://your-domain.com/tradingview/webhook`
3. Add header: `X-Webhook-Secret: <your-secret>`
4. Use JSON message format:
   ```json
   {
     "ticker": "{{ticker}}",
     "action": "BUY",
     "price": {{close}},
     "time": "{{time}}",
     "strategy": "My Strategy"
   }
   ```

### 4. Load Strategies from Google Drive

```bash
# Using CLI tool
./tools/load_gdrive_strategies.py "https://drive.google.com/drive/folders/1YlCnoQSP8MlfJO6c1GySn32joXIzgz3G"

# Or in Python
from apps.backend.src.services.gdrive_loader import load_tradingview_strategies_from_gdrive

strategies = load_tradingview_strategies_from_gdrive(
    "https://drive.google.com/drive/folders/1YlCnoQSP8MlfJO6c1GySn32joXIzgz3G"
)
```

### 5. Start Trading Bot

```bash
# Via API
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

## Testing

Run the test suite:
```bash
python3 tools/test_tradingview_integration.py
```

All tests should pass:
- ✓ Pydantic Models
- ✓ Strategy Logic  
- ✓ YAML Configuration
- ✓ Google Drive Loader
- ✓ Endpoint Structure

## Security Considerations

1. **Webhook Authentication**: All webhooks require valid secret token
2. **Audit Trail**: All alerts stored in database with timestamps
3. **Price Validation**: Optional price deviation checks prevent erroneous trades
4. **Confidence Threshold**: Configurable minimum confidence level
5. **HTTPS Required**: Use HTTPS in production for webhook URLs

## Files Changed

### New Files (10)
1. `apps/backend/src/api/tradingview_endpoints.py`
2. `apps/backend/src/trading/strategies/tradingview_strategy.py`
3. `apps/backend/src/services/gdrive_loader.py`
4. `docs/integrations/TRADINGVIEW_INTEGRATION.md`
5. `docs/guides/GDRIVE_LOADER_GUIDE.md`
6. `strategies/external/tradingview_example.yaml`
7. `tools/load_gdrive_strategies.py`
8. `tools/test_tradingview_integration.py`

### Modified Files (4)
1. `apps/backend/prisma/schema.prisma` - Added TradingViewAlert model
2. `apps/backend/main.py` - Registered router
3. `apps/backend/src/trading/strategies/__init__.py` - Imported strategy
4. `.env.example` - Added configuration
5. `README.md` - Updated features

## Next Steps

After merging this PR:

1. Run database migration
2. Configure webhook secret in production
3. Set up TradingView alerts
4. Test with paper trading first
5. Monitor alert logs
6. Gradually enable auto-trading

## Support

- See [TradingView Integration Guide](docs/integrations/TRADINGVIEW_INTEGRATION.md)
- See [Google Drive Loader Guide](docs/guides/GDRIVE_LOADER_GUIDE.md)
- Check API docs at `/docs` endpoint
- Review test script for examples

## References

- Issue: "add TradingView and read https://drive.google.com/drive/u/0/folders/1YlCnoQSP8MlfJO6c1GySn32joXIzgz3G"
- TradingView Webhooks: https://www.tradingview.com/support/solutions/43000529348-about-webhooks/
- gdown library: https://github.com/wkentaro/gdown
- FastAPI: https://fastapi.tiangolo.com/
