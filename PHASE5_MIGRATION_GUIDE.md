# Phase 5 Migration Guide

## Prerequisites
- Phase 4 successfully deployed and running
- Database access with migration privileges
- Admin access to update environment variables
- Ability to restart services

## Migration Steps

### Step 1: Backup Current System
```bash
# 1. Create database backup
docker-compose exec postgres pg_dump -U abtuser abtpro_db > backup_pre_phase5_$(date +%Y%m%d).sql

# 2. Backup current .env file
cp .env .env.backup.$(date +%Y%m%d)

# 3. Note current git commit
git log -1 --oneline > migration_checkpoint.txt
```

### Step 2: Update Code
```bash
# 1. Pull latest changes
git fetch origin
git checkout copilot/start-phase-five

# 2. Verify files are updated
ls -la PHASE5*.md DR_FAILOVER_STRATEGY.md
```

### Step 3: Update Environment Variables
```bash
# Edit .env and add Phase 5 configuration
nano .env

# Add these variables:
cat >> .env << 'EOF'

# Phase 5: Audit Trail Configuration
AUDIT_LOG_RETENTION_DAYS=90
AUDIT_LOG_LEVEL=INFO
AUDIT_SENSITIVE_FIELDS=password,secret,token,api_key

# Phase 5: Security Scanning Configuration
BANDIT_CONFIG_PATH=.bandit
SEMGREP_CONFIG=auto
ENABLE_SECURITY_SCANNING=true

# Phase 5: Secret Rotation Configuration
SECRET_ROTATION_POLICY_DAYS=90
SECRET_ROTATION_GRACE_PERIOD_DAYS=7
ENABLE_AUTO_ROTATION_ALERTS=true

# Phase 5: DR/Failover Configuration
DATABASE_REPLICA_URL=postgresql://user:pass@replica:5432/db
ENABLE_HEALTH_CHECKS=true
HEALTH_CHECK_INTERVAL_SECONDS=30
BACKUP_RETENTION_DAYS=30
EOF
```

### Step 4: Install Dependencies
```bash
# 1. Install Python dependencies
cd apps/backend
pip install -r requirements.txt

# 2. Verify installations
pip list | grep -E "(bandit|semgrep|psutil|python-json-logger)"
```

### Step 5: Run Database Migration
```bash
# 1. Generate Prisma client
cd apps/backend
npx prisma generate

# 2. Create migration
npx prisma migrate dev --name add_phase5_models

# Expected output:
# - Creating migration...
# - Applying migration `add_phase5_models`
# - Running generate... (completed)

# 3. Verify migration
npx prisma migrate status
```

### Step 6: Restart Services
```bash
# 1. Stop services
docker-compose down

# 2. Start services with new configuration
docker-compose up -d

# 3. Check service health
docker-compose ps
docker-compose logs backend | tail -20
```

### Step 7: Verify Phase 5 Features

#### Test Health Checks
```bash
# Basic health check
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"..."}

# Detailed health check
curl http://localhost:8000/health/detailed
# Expected: Component health status with database, redis, metrics

# Database health
curl http://localhost:8000/health/database
# Expected: Database connectivity and metrics
```

#### Test Audit Logging
```bash
# Make a test request
curl http://localhost:8000/strategies

# Check if it was logged
curl http://localhost:8000/audit/logs?limit=10
# Expected: Recent audit log entries including the /strategies request

# Get audit statistics
curl http://localhost:8000/audit/stats
# Expected: Statistics about audit logs
```

#### Test Secret Rotation
```bash
# View rotation schedule (should be empty initially)
curl http://localhost:8000/secrets/rotation/schedule
# Expected: {"schedules":[],"total":0}

# Create a test rotation record
curl -X POST http://localhost:8000/secrets/rotation/rotate \
  -H "Content-Type: application/json" \
  -d '{
    "secretType": "API_KEY",
    "secretName": "test_key",
    "newValue": "test_secret_value_12345"
  }'
# Expected: Rotation record created

# View schedule again
curl http://localhost:8000/secrets/rotation/schedule
# Expected: One rotation record
```

### Step 8: Configure Security Scanning

#### Setup Pre-commit Hooks (Optional for Developers)
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

#### Test Security Scans
```bash
# Run Bandit scan
cd apps/backend
bandit -r src/ -f txt

# Run Semgrep scan
semgrep --config=auto src/
```

### Step 9: Configure Celery Beat Schedule

Edit your Celery beat configuration to include Phase 5 tasks:

```python
# In celery_app.py or beat schedule configuration
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Existing tasks...
    
    # Phase 5 tasks
    'check-secret-rotation-daily': {
        'task': 'check_secret_rotation',
        'schedule': crontab(hour=6, minute=0),  # 6 AM UTC daily
    },
    'cleanup-audit-logs-weekly': {
        'task': 'cleanup_audit_logs',
        'schedule': crontab(day_of_week=0, hour=3, minute=0),  # Sunday 3 AM UTC
    },
}
```

Restart Celery beat:
```bash
docker-compose restart celery-beat
```

### Step 10: Verify Celery Tasks
```bash
# Check Celery workers are running
docker-compose exec celery-worker celery -A src.worker.celery_app inspect active

# Check scheduled tasks
docker-compose exec celery-beat celery -A src.worker.celery_app beat inspect scheduled
```

### Step 11: Setup Monitoring (Optional but Recommended)

#### Configure Prometheus Alerts
```yaml
# Add to prometheus alerts configuration
groups:
  - name: phase5_alerts
    rules:
      - alert: DatabaseConnectionFailed
        expr: health_check_database_status == 0
        for: 5m
        annotations:
          summary: "Database connection failed"
          
      - alert: SecretsOverdue
        expr: secret_rotation_overdue > 0
        for: 1h
        annotations:
          summary: "Secrets overdue for rotation"
```

### Step 12: Test Disaster Recovery Procedures
```bash
# 1. Create a test backup
./scripts/backup_database.sh

# 2. Verify backup file exists
ls -lh /backups/

# 3. Review DR documentation
cat DR_FAILOVER_STRATEGY.md
```

## Post-Migration Checklist

- [ ] All services are running
- [ ] Health checks return healthy status
- [ ] Audit logs are being created
- [ ] Database migration completed successfully
- [ ] New API endpoints are accessible
- [ ] Celery tasks are scheduled
- [ ] Pre-commit hooks installed (dev environments)
- [ ] Security scans configured in CI/CD
- [ ] Backup procedures documented
- [ ] Team trained on new features

## Rollback Procedure

If issues occur during migration:

```bash
# 1. Stop services
docker-compose down

# 2. Restore previous .env
cp .env.backup.YYYYMMDD .env

# 3. Rollback database migration
cd apps/backend
npx prisma migrate resolve --rolled-back add_phase5_models

# 4. Restore database from backup (if needed)
cat backup_pre_phase5_YYYYMMDD.sql | docker-compose exec -T postgres psql -U abtuser abtpro_db

# 5. Checkout previous code
git checkout <previous-commit>

# 6. Restart services
docker-compose up -d
```

## Troubleshooting

### Issue: Migration fails with "column already exists"
**Solution**: The migration may have been partially applied. Check current schema:
```bash
npx prisma db pull
npx prisma migrate resolve --applied add_phase5_models
```

### Issue: Audit middleware causes errors
**Solution**: Disable middleware temporarily:
```bash
# In .env
ENABLE_AUDIT_LOGGING=false

# Restart services
docker-compose restart backend
```

### Issue: Health checks fail
**Solution**: Check database and Redis connectivity:
```bash
docker-compose exec postgres psql -U abtuser -c "SELECT 1"
docker-compose exec redis redis-cli PING
```

### Issue: Celery tasks not running
**Solution**: Check Celery worker logs:
```bash
docker-compose logs celery-worker
docker-compose logs celery-beat
```

## Performance Optimization

After migration, monitor these metrics:

1. **Audit Log Impact**
   - Monitor API response times
   - Check database write performance
   - Consider async logging if needed

2. **Database Size**
   - Monitor audit log table growth
   - Set up log rotation if needed
   - Consider partitioning for large datasets

3. **Health Check Load**
   - Monitor health endpoint response times
   - Add caching if needed
   - Consider rate limiting

## Support

For issues during migration:
1. Check logs: `docker-compose logs -f`
2. Review Phase 5 documentation: `PHASE5_GUIDE.md`
3. Consult implementation summary: `PHASE5_IMPLEMENTATION_SUMMARY.md`
4. Contact DevOps team

## Next Steps

After successful migration:
1. Schedule first DR drill
2. Configure monitoring alerts
3. Train team on audit log queries
4. Set up secret rotation schedules
5. Review and update security scan findings

---

**Migration Date**: _____________
**Migrated By**: _____________
**Verification**: _____________
**Sign-off**: _____________
