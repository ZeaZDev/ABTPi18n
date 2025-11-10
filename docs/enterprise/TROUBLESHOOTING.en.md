# Troubleshooting Guide - UltimatePro Advance Enterprise

Common issues and solutions for ABTPro UltimatePro Advance Enterprise Edition.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Connection Problems](#connection-problems)
3. [Trading Issues](#trading-issues)
4. [Performance Problems](#performance-problems)
5. [Database Issues](#database-issues)
6. [Security Concerns](#security-concerns)
7. [API Errors](#api-errors)
8. [Monitoring & Logging](#monitoring--logging)
9. [Getting Support](#getting-support)

## Installation Issues

### Problem: Installation Script Fails

**Symptoms:**
```bash
./install.sh --enterprise
Error: System requirements not met
```

**Solutions:**

1. **Check System Requirements:**
```bash
# Check Docker version
docker --version  # Should be 24.0+

# Check Python version
python3 --version  # Should be 3.11+

# Check Node version
node --version  # Should be 18+

# Check available disk space
df -h  # Should have 100GB+ free
```

2. **Install Missing Dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose python3.11 nodejs npm

# CentOS/RHEL
sudo yum install docker docker-compose python311 nodejs npm
```

3. **Check Logs:**
```bash
cat /var/log/abtpro/install.log
```

### Problem: Database Migration Fails

**Symptoms:**
```
Error: Could not connect to database
Migration failed: Connection timeout
```

**Solutions:**

1. **Verify Database is Running:**
```bash
docker ps | grep postgres
# Should show running container

# If not running:
docker-compose up -d postgres
```

2. **Check Database Credentials:**
```bash
# Verify .env file
grep DATABASE_URL .env

# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

3. **Reset Database (WARNING: Data Loss):**
```bash
docker-compose down -v
docker-compose up -d postgres
cd apps/backend
python -m prisma migrate deploy
```

### Problem: License Key Validation Fails

**Symptoms:**
```
Error: Invalid enterprise license key
License validation failed
```

**Solutions:**

1. **Verify License Key Format:**
```bash
# Should match: ent-xxxx-xxxx-xxxx-xxxx
grep ENTERPRISE_LICENSE_KEY .env
```

2. **Contact Support:**
- Email: enterprise@abtpro.com
- Provide order number and company name
- Request license key verification

## Connection Problems

### Problem: Cannot Connect to Exchange

**Symptoms:**
```
Error: Exchange connection failed
binance: Authentication failed
```

**Solutions:**

1. **Verify API Keys:**
```python
# Test API keys
from ccxt import binance

exchange = binance({
    'apiKey': 'your-api-key',
    'secret': 'your-secret'
})

try:
    balance = exchange.fetch_balance()
    print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
```

2. **Check IP Whitelist:**
- Log into exchange account
- Go to API Management
- Add server IP to whitelist

3. **Verify API Permissions:**
- Ensure API key has trading permissions enabled
- Check if withdrawal is disabled (recommended for security)

### Problem: WebSocket Connection Drops

**Symptoms:**
```
WebSocket connection closed
Reconnecting... (attempt 5/10)
```

**Solutions:**

1. **Check Network Stability:**
```bash
# Ping exchange
ping api.binance.com

# Check packet loss
mtr api.binance.com
```

2. **Adjust Reconnection Settings:**
```env
# In .env
WS_RECONNECT_DELAY=5000
WS_MAX_RECONNECT_ATTEMPTS=20
WS_PING_INTERVAL=30000
```

3. **Enable WebSocket Logging:**
```env
LOG_LEVEL=debug
WS_LOG_ENABLED=true
```

### Problem: Database Connection Pool Exhausted

**Symptoms:**
```
Error: Could not acquire connection from pool
Connection timeout after 30s
```

**Solutions:**

1. **Increase Pool Size:**
```env
# In .env
DATABASE_POOL_SIZE=30
DATABASE_MAX_OVERFLOW=20
```

2. **Check for Connection Leaks:**
```bash
# Monitor active connections
psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname='abtpro_enterprise';"
```

3. **Restart Application:**
```bash
docker-compose restart backend worker
```

## Trading Issues

### Problem: Bot Not Executing Trades

**Symptoms:**
- Bot shows as "active" but no trades executed
- Signal generated but no order placed

**Solutions:**

1. **Check Bot Logs:**
```bash
docker-compose logs -f worker | grep "bot_123abc"
```

2. **Verify Account Balance:**
```python
# Check if sufficient balance
GET /portfolio/balances
```

3. **Review Risk Parameters:**
```json
// Check if risk limits blocking trades
{
  "daily_loss_limit_reached": false,
  "max_drawdown_exceeded": false,
  "position_limit_reached": false
}
```

4. **Check Exchange Status:**
```bash
# Verify exchange is operational
curl https://api.binance.com/api/v3/ping
```

### Problem: Orders Not Filling

**Symptoms:**
- Orders placed but remain open
- Limit orders not executed

**Solutions:**

1. **Check Order Type:**
```json
// Use market orders for immediate execution
{
  "order_type": "market"
}

// Or use limit with better price
{
  "order_type": "limit",
  "price": "market_price * 1.001"  // Buy slightly above market
}
```

2. **Verify Minimum Order Size:**
```python
# Check exchange minimum
GET /market/info/BTC/USDT

# Response includes:
{
  "min_order_size": 0.00001,
  "min_order_value": 10
}
```

### Problem: Incorrect Position Sizing

**Symptoms:**
- Position sizes too large or too small
- Risk parameters not respected

**Solutions:**

1. **Review Position Sizing Configuration:**
```json
{
  "position_sizing": {
    "method": "percent_of_portfolio",
    "percent": 2.0,
    "max_position_size_usd": 10000
  }
}
```

2. **Check Account Balance:**
```bash
# Ensure sufficient balance for desired position
GET /portfolio/balances
```

3. **Verify Risk Calculations:**
```python
# Test position sizing calculation
position_size = (account_balance * risk_percent) / (entry_price - stop_loss_price)
```

## Performance Problems

### Problem: Slow API Response Times

**Symptoms:**
```
API response time: 5000ms (expected < 200ms)
Timeout errors on frontend
```

**Solutions:**

1. **Check System Resources:**
```bash
# CPU usage
top

# Memory usage
free -h

# Disk I/O
iostat -x 1
```

2. **Enable Caching:**
```env
CACHE_ENABLED=true
CACHE_TYPE=redis
CACHE_DEFAULT_TIMEOUT=300
```

3. **Scale Workers:**
```yaml
# docker-compose.yml
worker:
  deploy:
    replicas: 8
```

4. **Optimize Database Queries:**
```bash
# Check slow queries
psql -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

### Problem: High Memory Usage

**Symptoms:**
```
Memory usage: 95%
OOM killer activated
Container restarting
```

**Solutions:**

1. **Increase Memory Limits:**
```yaml
# docker-compose.yml
worker:
  deploy:
    resources:
      limits:
        memory: 8G
```

2. **Optimize Worker Configuration:**
```env
CELERY_WORKER_MAX_TASKS_PER_CHILD=100
CELERY_WORKER_PREFETCH_MULTIPLIER=2
```

3. **Monitor Memory Usage:**
```bash
docker stats
```

### Problem: Database Slow Queries

**Symptoms:**
```
Query execution time: 5000ms
Database CPU: 100%
```

**Solutions:**

1. **Add Missing Indexes:**
```sql
-- Check missing indexes
SELECT * FROM pg_stat_user_tables WHERE idx_scan = 0;

-- Add indexes
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
CREATE INDEX idx_bots_user_id ON bots(user_id);
```

2. **Optimize Queries:**
```sql
-- Use EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM trades WHERE timestamp > NOW() - INTERVAL '7 days';
```

3. **Vacuum Database:**
```bash
psql -c "VACUUM ANALYZE;"
```

## Database Issues

### Problem: Database Corruption

**Symptoms:**
```
Error: Invalid page header
Database integrity check failed
```

**Solutions:**

1. **Run Integrity Check:**
```sql
-- Check for corruption
SELECT * FROM pg_stat_database WHERE datname = 'abtpro_enterprise';
```

2. **Restore from Backup:**
```bash
# Stop application
docker-compose down

# Restore latest backup
./scripts/restore_backup.sh latest

# Start application
docker-compose up -d
```

### Problem: Out of Disk Space

**Symptoms:**
```
Error: No space left on device
Database write failed
```

**Solutions:**

1. **Check Disk Usage:**
```bash
df -h
du -sh /var/lib/docker/volumes/*
```

2. **Clean Up Logs:**
```bash
# Rotate logs
find /var/log/abtpro -name "*.log" -mtime +30 -delete

# Clean Docker logs
docker system prune -a
```

3. **Archive Old Data:**
```sql
-- Archive trades older than 6 months
INSERT INTO trades_archive SELECT * FROM trades WHERE timestamp < NOW() - INTERVAL '6 months';
DELETE FROM trades WHERE timestamp < NOW() - INTERVAL '6 months';
```

## Security Concerns

### Problem: Suspicious API Activity

**Symptoms:**
- Unusual trading activity
- API calls from unknown IPs
- Unauthorized access attempts

**Solutions:**

1. **Review Audit Logs:**
```bash
cat /var/log/abtpro/audit.log | grep "UNAUTHORIZED"
```

2. **Rotate API Keys:**
```bash
# Via API
POST /auth/rotate-keys

# Or manually in database
psql -c "UPDATE users SET api_key_rotation_required = true;"
```

3. **Enable IP Whitelisting:**
```env
IP_WHITELIST_ENABLED=true
ALLOWED_IPS=192.168.1.0/24,10.0.0.0/8
```

4. **Enable 2FA:**
```bash
# Enable for all users
psql -c "UPDATE users SET require_2fa = true;"
```

### Problem: API Key Compromised

**Symptoms:**
- Exchange reports suspicious activity
- Unauthorized trades executed

**Immediate Actions:**

1. **Disable All Bots:**
```bash
# Emergency stop all trading
POST /bots/emergency-stop-all
```

2. **Revoke Exchange API Keys:**
- Log into exchange immediately
- Delete compromised API keys
- Generate new keys with IP restrictions

3. **Rotate System Credentials:**
```bash
# Rotate encryption keys
./scripts/rotate_encryption_keys.sh

# Rotate JWT secrets
./scripts/rotate_jwt_secrets.sh
```

4. **Review All Transactions:**
```bash
# Export all trades for review
GET /trades?export=csv&start_date=<compromise_date>
```

## API Errors

### Problem: Rate Limit Exceeded

**Symptoms:**
```
Error 429: Too Many Requests
X-RateLimit-Remaining: 0
```

**Solutions:**

1. **Implement Backoff:**
```python
import time

def api_call_with_retry(endpoint, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = api.call(endpoint)
            return response
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise
```

2. **Request Rate Limit Increase:**
- Contact enterprise support
- Provide use case justification

### Problem: Authentication Errors

**Symptoms:**
```
Error 401: Unauthorized
Invalid or expired token
```

**Solutions:**

1. **Refresh Token:**
```bash
POST /auth/refresh
{
  "refresh_token": "your_refresh_token"
}
```

2. **Verify Token Expiration:**
```python
import jwt

def check_token_expiry(token):
    decoded = jwt.decode(token, options={"verify_signature": False})
    exp = decoded['exp']
    # Compare with current time
```

## Monitoring & Logging

### Accessing Logs

**Application Logs:**
```bash
# Backend logs
docker-compose logs -f backend

# Worker logs
docker-compose logs -f worker

# All logs
docker-compose logs -f
```

**System Logs:**
```bash
# View system logs
journalctl -u abtpro -f

# Filter by severity
journalctl -u abtpro -p err -f
```

### Log Locations

- **Application**: `/var/log/abtpro/app.log`
- **Audit**: `/var/log/abtpro/audit.log`
- **Trading**: `/var/log/abtpro/trading.log`
- **Errors**: `/var/log/abtpro/error.log`

### Monitoring Tools

**Prometheus Queries:**
```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Bot count
abtpro_active_bots
```

**Grafana Dashboards:**
- System Health: http://localhost:3001/d/system
- Trading Performance: http://localhost:3001/d/trading
- API Metrics: http://localhost:3001/d/api

## Getting Support

### Enterprise Support Channels

**Priority Hotline:**
- Available 24/7 for critical issues
- 1-hour response time SLA

**Email Support:**
- enterprise@abtpro.com
- Include:
  - License key
  - Error logs
  - Steps to reproduce
  - System information

**Slack Channel:**
- Direct access to engineering team
- Real-time assistance

### Information to Provide

When contacting support, include:

1. **System Information:**
```bash
# Generate system report
./scripts/generate_support_report.sh
```

2. **Error Logs:**
```bash
# Last 1000 lines of error logs
tail -n 1000 /var/log/abtpro/error.log > error_report.txt
```

3. **Configuration:**
```bash
# Sanitized configuration (secrets removed)
./scripts/export_config.sh --sanitize
```

### Emergency Procedures

**Critical Issue (Trading Stopped):**
1. Call priority hotline immediately
2. Stop all bots: `POST /bots/emergency-stop-all`
3. Preserve logs: `./scripts/preserve_logs.sh`
4. Wait for support team instructions

**Security Incident:**
1. Rotate all credentials immediately
2. Enable audit mode: `AUDIT_MODE=strict`
3. Contact security team: security@abtpro.com
4. Preserve evidence: Do not delete logs

---

*Next: [Deployment Guide](DEPLOYMENT.en.md)*
