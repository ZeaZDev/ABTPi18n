# คู่มือการกำหนดค่า - UltimatePro Advance Enterprise

คู่มือนี้ให้ตัวเลือกการกำหนดค่าโดยละเอียดสำหรับ ABTPro UltimatePro Advance Enterprise

## สารบัญ

1. [การกำหนดค่าสภาพแวดล้อม](#การกำหนดค่าสภาพแวดล้อม)
2. [การกำหนดค่าฐานข้อมูล](#การกำหนดค่าฐานข้อมูล)
3. [การกำหนดค่าความปลอดภัย](#การกำหนดค่าความปลอดภัย)
4. [การกำหนดค่าตลาด](#การกำหนดค่าตลาด)
5. [การกำหนดค่ากลยุทธ์](#การกำหนดค่ากลยุทธ์)
6. [การกำหนดค่าการจัดการความเสี่ยง](#การกำหนดค่าการจัดการความเสี่ยง)
7. [การกำหนดค่าการแจ้งเตือน](#การกำหนดค่าการแจ้งเตือน)
8. [การกำหนดค่าการตรวจสอบ](#การกำหนดค่าการตรวจสอบ)
9. [การกำหนดค่าความพร้อมใช้งานสูง](#การกำหนดค่าความพร้อมใช้งานสูง)
10. [การปรับแต่งประสิทธิภาพ](#การปรับแต่งประสิทธิภาพ)

## การกำหนดค่าสภาพแวดล้อม

### ตัวแปรสภาพแวดล้อม Production

การกำหนดค่า `.env` แบบสมบูรณ์สำหรับ production:

```env
# แอปพลิเคชัน
NODE_ENV=production
PYTHON_ENV=production
LOG_LEVEL=info
APP_NAME="ABTPro Enterprise"

# ใบอนุญาต Enterprise
ENTERPRISE_LICENSE_KEY="ent-xxxx-xxxx-xxxx-xxxx"
ENTERPRISE_TIER="ultimate_pro_advance"

# ฐานข้อมูล
DATABASE_URL="postgresql://abtpro:secure_password@db-primary:5432/abtpro_enterprise"
DATABASE_REPLICA_URL="postgresql://abtpro:secure_password@db-replica:5432/abtpro_enterprise"
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30

# Redis
REDIS_URL="redis://:redis_password@redis-primary:6379/0"
REDIS_SENTINEL_URL="redis-sentinel://sentinel1:26379,sentinel2:26379,sentinel3:26379"
REDIS_MASTER_NAME="abtpro-master"

# ความปลอดภัย
SECRET_KEY="your-secret-key-minimum-32-characters-long"
ENCRYPTION_KEY="base64-encoded-32-byte-key"
JWT_ALGORITHM="HS256"
JWT_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth
GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="your-client-secret"
OAUTH_REDIRECT_URI="https://yourdomain.com/api/auth/callback/google"

# CORS
ALLOWED_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"

# การจำกัดอัตรา
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# Celery Worker
CELERY_BROKER_URL="redis://:redis_password@redis-primary:6379/1"
CELERY_RESULT_BACKEND="redis://:redis_password@redis-primary:6379/2"
CELERY_TASK_ALWAYS_EAGER=false
CELERY_WORKER_CONCURRENCY=8
CELERY_WORKER_PREFETCH_MULTIPLIER=4

# การซื้อขาย
MAX_CONCURRENT_BOTS=unlimited
DEFAULT_POSITION_SIZE=0.01
MAX_POSITION_SIZE=10.0
TRADING_FEE_PERCENTAGE=0.1

# Telegram
TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
TELEGRAM_WEBHOOK_URL="https://yourdomain.com/api/telegram/webhook"

# PromptPay (การชำระเงินไทย)
PROMPTPAY_ENABLED=true
PROMPTPAY_MERCHANT_ID="your-merchant-id"
PROMPTPAY_WEBHOOK_SECRET="your-webhook-secret"
PROMPTPAY_CALLBACK_URL="https://yourdomain.com/api/payment/callback"

# การตรวจสอบ
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090
GRAFANA_ENABLED=true
GRAFANA_PORT=3001

# การบันทึกล็อก
LOG_FORMAT=json
LOG_FILE_PATH=/var/log/abtpro/app.log
LOG_MAX_SIZE=100MB
LOG_RETENTION_DAYS=30

# การสำรองข้อมูล
BACKUP_ENABLED=true
BACKUP_SCHEDULE="0 2 * * *"  # รายวันเวลา 2 AM
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET="abtpro-backups"
BACKUP_S3_REGION="ap-southeast-1"

# Feature Flags
ENABLE_ML_FEATURES=true
ENABLE_PAPER_TRADING=true
ENABLE_BACKTESTING=true
ENABLE_CUSTOM_PLUGINS=true
ENABLE_API_ACCESS=true
ENABLE_WHITE_LABEL=true
```

## การกำหนดค่าฐานข้อมูล

### การกำหนดค่า PostgreSQL

**การตั้งค่าฐานข้อมูลหลัก** (`postgresql.conf`):

```conf
# การตั้งค่าการเชื่อมต่อ
max_connections = 200
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB

# การจำลองแบบ
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
hot_standby = on
```

### Connection Pooling ด้วย PgBouncer

```ini
[databases]
abtpro_enterprise = host=db-primary port=5432 dbname=abtpro_enterprise

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
reserve_pool_timeout = 3
```

### การย้ายข้อมูลฐานข้อมูล

```bash
# รันการย้ายข้อมูล
cd apps/backend
python -m prisma migrate deploy

# ย้อนกลับการย้ายข้อมูล
python -m prisma migrate rollback

# ตรวจสอบสถานะการย้ายข้อมูล
python -m prisma migrate status
```

## การกำหนดค่าความปลอดภัย

### การเข้ารหัสคีย์ API

กำหนดค่าการเข้ารหัส AES-GCM สำหรับคีย์ API ของตลาด:

```python
# ใน src/security/encryption.py
ENCRYPTION_CONFIG = {
    "algorithm": "AES-GCM",
    "key_size": 256,
    "nonce_size": 96,
    "tag_size": 128,
    "key_rotation_days": 90
}
```

### การหมุนเวียนข้อมูลลับ

กำหนดค่าการหมุนเวียนข้อมูลลับอัตโนมัติ:

```env
SECRET_ROTATION_ENABLED=true
SECRET_ROTATION_SCHEDULE="0 0 1 * *"  # รายเดือน
SECRET_ROTATION_GRACE_PERIOD_DAYS=7
SECRET_ROTATION_NOTIFICATION_DAYS=14
```

### การบันทึกการตรวจสอบ

```env
AUDIT_ENABLED=true
AUDIT_LOG_PATH=/var/log/abtpro/audit.log
AUDIT_LOG_LEVEL=info
AUDIT_RETENTION_DAYS=365
AUDIT_EVENTS=login,logout,api_key_create,api_key_delete,trade_execute,config_change
```

## การกำหนดค่าตลาด

### ตลาดที่รองรับ

กำหนดค่าตลาดหลายแห่ง:

```json
{
  "exchanges": [
    {
      "id": "binance",
      "name": "Binance",
      "enabled": true,
      "testnet": false,
      "rate_limit": 1200,
      "api_version": "v3",
      "sandbox_mode": false
    },
    {
      "id": "kraken",
      "name": "Kraken",
      "enabled": true,
      "testnet": false,
      "rate_limit": 15,
      "api_version": "v1",
      "sandbox_mode": false
    },
    {
      "id": "coinbase",
      "name": "Coinbase Pro",
      "enabled": true,
      "testnet": false,
      "rate_limit": 10,
      "api_version": "v2",
      "sandbox_mode": false
    }
  ]
}
```

### การตั้งค่าเฉพาะของตลาด

**การกำหนดค่า Binance:**
```env
BINANCE_TESTNET=false
BINANCE_RATE_LIMIT=1200
BINANCE_RECV_WINDOW=5000
BINANCE_WS_ENABLED=true
```

**การกำหนดค่า Kraken:**
```env
KRAKEN_RATE_LIMIT=15
KRAKEN_TIER=4  # Pro tier
KRAKEN_2FA_ENABLED=true
```

## การกำหนดค่ากลยุทธ์

### การตั้งค่ากลยุทธ์ทั่วโลก

```json
{
  "strategies": {
    "default_parameters": {
      "timeframe": "1h",
      "lookback_period": 100,
      "max_positions": 5,
      "position_sizing": "fixed"
    },
    "risk_limits": {
      "max_drawdown_percent": 20,
      "max_daily_loss_percent": 5,
      "max_position_size_percent": 10
    }
  }
}
```

### การกำหนดค่ากลยุทธ์แบบกำหนดเอง

เปิดใช้งานการพัฒนากลยุทธ์แบบกำหนดเอง:

```env
CUSTOM_STRATEGIES_ENABLED=true
CUSTOM_STRATEGIES_PATH=/app/custom_strategies
STRATEGY_PLUGIN_DIR=/app/plugins/strategies
STRATEGY_VALIDATION_STRICT=true
```

### พารามิเตอร์กลยุทธ์

ตัวอย่างการกำหนดค่ากลยุทธ์ RSI Cross:

```json
{
  "strategy_id": "rsi_cross_v2",
  "parameters": {
    "rsi_period": 14,
    "oversold_threshold": 30,
    "overbought_threshold": 70,
    "ma_period": 20,
    "ma_type": "EMA",
    "signal_confirmation": true,
    "min_volume": 1000000
  }
}
```

## การกำหนดค่าการจัดการความเสี่ยง

### พารามิเตอร์ความเสี่ยงทั่วโลก

```json
{
  "risk_management": {
    "global": {
      "max_portfolio_risk": 0.02,
      "max_correlation": 0.7,
      "max_leverage": 3,
      "margin_call_threshold": 0.8
    },
    "position_sizing": {
      "method": "kelly_criterion",
      "kelly_fraction": 0.25,
      "max_position_risk": 0.01,
      "min_position_size_usd": 10
    },
    "stop_loss": {
      "enabled": true,
      "type": "trailing",
      "initial_stop_percent": 2,
      "trailing_distance_percent": 1.5,
      "break_even_trigger_percent": 3
    },
    "take_profit": {
      "enabled": true,
      "targets": [
        {"percent": 3, "size_percent": 33},
        {"percent": 5, "size_percent": 33},
        {"percent": 8, "size_percent": 34}
      ]
    }
  }
}
```

### Circuit Breakers

```json
{
  "circuit_breakers": {
    "daily_loss_limit": {
      "enabled": true,
      "threshold_percent": 5,
      "action": "pause_all_trading",
      "cooldown_hours": 24
    },
    "drawdown_limit": {
      "enabled": true,
      "threshold_percent": 15,
      "action": "reduce_position_sizes",
      "reduction_factor": 0.5
    },
    "consecutive_losses": {
      "enabled": true,
      "max_consecutive": 5,
      "action": "pause_strategy",
      "review_required": true
    }
  }
}
```

## การกำหนดค่าการแจ้งเตือน

### การแจ้งเตือน Telegram

```json
{
  "telegram": {
    "enabled": true,
    "notifications": {
      "trade_executed": {
        "enabled": true,
        "min_value_usd": 100
      },
      "profit_target_hit": {
        "enabled": true
      },
      "stop_loss_triggered": {
        "enabled": true
      },
      "daily_summary": {
        "enabled": true,
        "time": "23:00"
      },
      "error_alerts": {
        "enabled": true,
        "severity": ["error", "critical"]
      },
      "system_status": {
        "enabled": true,
        "interval_hours": 24
      }
    }
  }
}
```

### การแจ้งเตือนอีเมล

```env
EMAIL_ENABLED=true
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@abtpro.com
```

## การกำหนดค่าการตรวจสอบ

### เมตริก Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'abtpro-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'abtpro-worker'
    static_configs:
      - targets: ['worker:9100']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### แดชบอร์ด Grafana

แดชบอร์ดที่กำหนดค่าไว้ล่วงหน้ารวมถึง:
- ประสิทธิภาพการซื้อขาย
- สุขภาพระบบ
- เมตริกฐานข้อมูล
- ประสิทธิภาพ API
- เมตริกความเสี่ยง

## การกำหนดค่าความพร้อมใช้งานสูง

### การปรับใช้หลายภูมิภาค

```yaml
# docker-compose.ha.yml
version: '3.8'

services:
  backend:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3

  worker:
    deploy:
      replicas: 5
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Load Balancing

**การกำหนดค่า Nginx:**

```nginx
upstream backend {
    least_conn;
    server backend1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server backend3:8000 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## การปรับแต่งประสิทธิภาพ

### ประสิทธิภาพ Backend

```env
# Uvicorn Workers
UVICORN_WORKERS=4
UVICORN_WORKER_CLASS=uvicorn.workers.UvicornWorker
UVICORN_TIMEOUT=60
UVICORN_KEEPALIVE=5

# ขีดจำกัดคำขอ
MAX_REQUEST_SIZE=10MB
MAX_UPLOAD_SIZE=50MB
REQUEST_TIMEOUT=30
```

### ประสิทธิภาพ Celery

```python
# celery_config.py
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# ประสิทธิภาพ
CELERY_WORKER_PREFETCH_MULTIPLIER = 4
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_DISABLE_RATE_LIMITS = False

# เส้นทางงาน
CELERY_TASK_ROUTES = {
    'src.trading.tasks.*': {'queue': 'trading'},
    'src.ml.tasks.*': {'queue': 'ml'},
    'src.backtest.tasks.*': {'queue': 'backtest'},
}
```

### กลยุทธ์แคช

```env
CACHE_ENABLED=true
CACHE_TYPE=redis
CACHE_DEFAULT_TIMEOUT=300
CACHE_KEY_PREFIX=abtpro:

# แคชข้อมูลเฉพาะ
CACHE_MARKET_DATA_TTL=60
CACHE_USER_SETTINGS_TTL=3600
CACHE_STRATEGY_CONFIG_TTL=1800
```

---

*ถัดไป: [เอกสารฟีเจอร์](FEATURES.th.md)*
