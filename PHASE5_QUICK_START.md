# Phase 5 Quick Start Guide

## What's New in Phase 5?

Phase 5 adds enterprise-level compliance, security, and disaster recovery features:

✅ **Audit Trail** - Complete logging of all API activities
✅ **Security Scanning** - Automated vulnerability detection  
✅ **Secret Rotation** - Systematic credential management
✅ **Disaster Recovery** - Backup and failover strategies

## Quick Test (5 minutes)

### 1. Check Health Status
```bash
curl http://localhost:8000/health/detailed
```

### 2. View Audit Logs
```bash
# This request will be logged automatically
curl http://localhost:8000/strategies

# View the audit log
curl http://localhost:8000/audit/logs?limit=5
```

### 3. Check Secret Rotation
```bash
curl http://localhost:8000/secrets/rotation/schedule
```

### 4. Run Security Scan
```bash
cd apps/backend
bandit -r src/ -ll  # Only high/medium severity
```

## Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Basic health check |
| `GET /health/detailed` | Full system status |
| `GET /audit/logs` | Query audit trail |
| `GET /audit/stats` | Audit statistics |
| `GET /secrets/rotation/schedule` | View rotation schedule |
| `POST /secrets/rotation/rotate` | Trigger rotation |

## Configuration

Edit `.env` to customize:

```env
# Audit log retention (days)
AUDIT_LOG_RETENTION_DAYS=90

# Secret rotation interval (days)
SECRET_ROTATION_POLICY_DAYS=90

# Backup retention (days)
BACKUP_RETENTION_DAYS=30
```

## Daily Operations

### View System Health
```bash
curl http://localhost:8000/health/detailed | jq
```

### Export Audit Logs (Last 7 Days)
```bash
curl "http://localhost:8000/audit/export?format=csv&startDate=$(date -d '7 days ago' -I)" -o audit_logs.csv
```

### Check Secrets Due for Rotation
```bash
curl http://localhost:8000/secrets/rotation/due?daysAhead=30 | jq
```

### Run Security Scan
```bash
cd apps/backend
bandit -r src/ -f json -o security_report.json
```

## Common Tasks

### Rotate a Secret
```bash
curl -X POST http://localhost:8000/secrets/rotation/rotate \
  -H "Content-Type: application/json" \
  -d '{
    "secretType": "DATABASE",
    "secretName": "postgres_password",
    "newValue": "new_secure_password",
    "userId": 1
  }'
```

### Search Audit Logs
```bash
# Find all CREATE actions by user 1
curl "http://localhost:8000/audit/logs?userId=1&action=CREATE"

# Find all failed requests (5xx status codes)
curl "http://localhost:8000/audit/logs" | jq '.logs[] | select(.statusCode >= 500)'
```

### Monitor Health
```bash
# Basic monitoring script
while true; do
  curl -s http://localhost:8000/health | jq
  sleep 30
done
```

## Documentation

- **Full Guide**: [PHASE5_GUIDE.md](PHASE5_GUIDE.md)
- **Technical Details**: [PHASE5_SUMMARY.md](PHASE5_SUMMARY.md)  
- **Implementation**: [PHASE5_IMPLEMENTATION_SUMMARY.md](PHASE5_IMPLEMENTATION_SUMMARY.md)
- **Migration**: [PHASE5_MIGRATION_GUIDE.md](PHASE5_MIGRATION_GUIDE.md)
- **DR Strategy**: [DR_FAILOVER_STRATEGY.md](DR_FAILOVER_STRATEGY.md)

## Security Best Practices

1. **Regular Scans**: Run security scans before each deployment
2. **Rotate Secrets**: Follow the 90-day rotation schedule
3. **Monitor Logs**: Review audit logs weekly
4. **Test DR**: Conduct monthly failover drills
5. **Update Dependencies**: Keep security tools up to date

## Troubleshooting

### Audit logs not appearing?
- Check `ENABLE_AUDIT_LOGGING=true` in `.env`
- Restart backend service: `docker-compose restart backend`

### Health check fails?
- Verify database: `docker-compose exec postgres psql -U abtuser -c "SELECT 1"`
- Verify Redis: `docker-compose exec redis redis-cli PING`

### Security scan errors?
- Install tools: `pip install bandit semgrep`
- Check configuration: `.bandit` and `.semgrep.yml`

## Next Steps

1. ✅ Set up monitoring alerts (Prometheus/Grafana)
2. ✅ Schedule regular DR drills
3. ✅ Configure CI/CD security scanning
4. ✅ Train team on audit log queries
5. ✅ Establish secret rotation schedule

---

**Phase 5 Status**: ✅ Complete
**Deployment Ready**: Yes
**Production Ready**: Yes (after migration testing)
