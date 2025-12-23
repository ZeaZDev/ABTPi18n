# Getting Started with UltimatePro Advance Enterprise

This guide will help you set up and start using ABTPro UltimatePro Advance Enterprise edition.

## Prerequisites

### System Requirements

**Minimum Requirements:**
- **CPU**: 8 cores (Intel Xeon or AMD EPYC recommended)
- **RAM**: 16 GB
- **Storage**: 100 GB SSD
- **Network**: 100 Mbps dedicated connection
- **OS**: Ubuntu 20.04 LTS or later, CentOS 8, or Docker-compatible system

**Recommended for Production:**
- **CPU**: 16+ cores
- **RAM**: 32 GB or more
- **Storage**: 500 GB NVMe SSD with RAID 1
- **Network**: 1 Gbps dedicated connection with redundancy
- **OS**: Ubuntu 22.04 LTS

### Software Dependencies

- **Docker**: 24.0+ and Docker Compose 2.0+
- **Python**: 3.11 or later
- **Node.js**: 18 LTS or later
- **PostgreSQL**: 14 or later (15+ recommended)
- **Redis**: 7.0 or later
- **Git**: 2.30 or later

### Required Accounts and Keys

1. **Exchange API Keys**: From supported exchanges (Binance, Kraken, etc.)
2. **Google OAuth Credentials**: For authentication
3. **Telegram Bot Token**: For notifications (optional but recommended)
4. **PromptPay Merchant ID**: For payment processing (Thai customers)
5. **Enterprise License Key**: Provided upon purchase

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/ZeaZDev/ABTPi18n.git
cd ABTPi18n

# Checkout the enterprise branch (if separate)
git checkout enterprise
```

### Step 2: Set Up Environment Variables

```bash
# Copy the enterprise environment template
cp .env.enterprise.example .env

# Edit the environment file with your configuration
nano .env
```

**Required Environment Variables:**

```env
# Database Configuration
DATABASE_URL="postgresql://user:password@localhost:5432/abtpro_enterprise"
REDIS_URL="redis://localhost:6379"

# Enterprise License
ENTERPRISE_LICENSE_KEY="your-enterprise-license-key"

# Security
SECRET_KEY="your-secret-key-min-32-chars"
ENCRYPTION_KEY="your-encryption-key-32-bytes-base64"

# OAuth Configuration
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
OAUTH_REDIRECT_URI="http://localhost:3000/api/auth/callback/google"

# Exchange API Keys (will be encrypted)
# These can also be added via the UI after installation

# Telegram Configuration (Optional)
TELEGRAM_BOT_TOKEN="your-telegram-bot-token"

# PromptPay Configuration (Optional, for Thai payments)
PROMPTPAY_MERCHANT_ID="your-promptpay-merchant-id"
PROMPTPAY_WEBHOOK_SECRET="your-webhook-secret"

# Monitoring (Optional but recommended)
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true

# Production Settings
NODE_ENV=production
PYTHON_ENV=production
LOG_LEVEL=info
```

### Step 3: Run Installation Script

The enterprise edition includes an automated installation script:

```bash
# Make the script executable
chmod +x install.sh

# Run the installation
./install.sh --enterprise

# Or for production deployment
./install.sh --enterprise --production
```

The installation script will:
1. Validate system requirements
2. Install dependencies
3. Set up the database
4. Run migrations
5. Build frontend and backend
6. Configure monitoring
7. Validate the enterprise license

### Step 4: Initialize the Database

```bash
# Run database migrations
cd apps/backend
python -m prisma migrate deploy

# (Optional) Seed initial data
python scripts/seed_enterprise.py
```

### Step 5: Start the Services

**Development Mode:**
```bash
docker-compose -f docker-compose.enterprise.yml up -d
```

**Production Mode:**
```bash
docker-compose -f docker-compose.enterprise.prod.yml up -d
```

### Step 6: Verify Installation

1. **Check service health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Access the frontend:**
   - Navigate to: http://localhost:3000/en/dashboard
   - You should see the login page

3. **Check the API documentation:**
   - Navigate to: http://localhost:8000/docs
   - You should see the FastAPI Swagger UI

4. **Verify monitoring (if enabled):**
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (default credentials: admin/admin)

## Initial Configuration

### Step 1: Admin Account Setup

1. Navigate to http://localhost:3000/en/login
2. Sign in with Google (using the configured OAuth credentials)
3. The first user to sign in will automatically become the admin

### Step 2: Add Exchange API Keys

1. Go to **Settings** → **Exchange Keys**
2. Click **Add New Exchange**
3. Select your exchange (e.g., Binance)
4. Enter your API credentials:
   - API Key
   - API Secret
   - (Optional) Passphrase for some exchanges
5. Click **Save and Encrypt**

The system will automatically encrypt your API keys using AES-GCM before storing them.

### Step 3: Configure Telegram Notifications

1. Go to **Settings** → **Notifications**
2. Click **Connect Telegram**
3. Follow the instructions to link your Telegram account
4. Configure notification preferences:
   - Trade executions
   - Profit/loss alerts
   - System notifications
   - Error alerts

### Step 4: Set Up User Management (Enterprise Feature)

1. Go to **Admin** → **User Management**
2. Configure user roles and permissions:
   - **Admin**: Full access
   - **Trader**: Can create and manage bots
   - **Viewer**: Read-only access
3. Invite team members via email

### Step 5: Configure Risk Management

1. Go to **Settings** → **Risk Management**
2. Set global risk parameters:
   - Maximum daily loss limit
   - Maximum drawdown percentage
   - Position size limits
   - Stop-loss requirements
3. Save configuration

## First Trading Bot

### Create Your First Strategy

1. Navigate to **Dashboard** → **New Bot**
2. Configure basic settings:
   - **Name**: My First Bot
   - **Exchange**: Select configured exchange
   - **Trading Pair**: BTC/USDT
   - **Strategy**: RSI Cross (or any available strategy)

3. Configure strategy parameters:
   ```json
   {
     "rsi_period": 14,
     "oversold": 30,
     "overbought": 70,
     "position_size": 0.01
   }
   ```

4. Set risk parameters:
   - Stop Loss: 2%
   - Take Profit: 5%
   - Max Position Size: 0.1 BTC

5. Choose execution mode:
   - **Paper Trading**: Test with simulated funds (recommended first)
   - **Live Trading**: Trade with real funds

6. Click **Create and Start Bot**

### Monitor Bot Performance

1. Go to **Dashboard** → **Active Bots**
2. Click on your bot to view:
   - Current positions
   - Trade history
   - P&L (Profit & Loss)
   - Performance metrics
3. Real-time updates via WebSocket

## Next Steps

1. **Explore Advanced Features**:
   - [Custom Strategy Development](FEATURES.en.md#custom-strategies)
   - [ML Signal Scoring](FEATURES.en.md#ml-features)
   - [Portfolio Aggregation](FEATURES.en.md#portfolio-management)

2. **Set Up Monitoring**:
   - Configure Grafana dashboards
   - Set up alerts
   - Review metrics

3. **Production Deployment**:
   - Follow the [Deployment Guide](DEPLOYMENT.en.md)
   - Set up disaster recovery
   - Configure backups

4. **API Integration**:
   - Review [API Reference](API_REFERENCE.en.md)
   - Generate API tokens
   - Integrate with your systems

## Common Issues

For troubleshooting help, see the [Troubleshooting Guide](TROUBLESHOOTING.en.md).

## Support

- **Email**: enterprise@abtpro.com
- **Priority Hotline**: Available 24/7
- **Documentation**: Full documentation in `/docs/enterprise/`
- **API Support**: Direct access to engineering team

---

*Next: [Configuration Guide](CONFIGURATION.en.md)*
