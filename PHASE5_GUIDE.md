# Phase 5 User Guide: Compliance & Audit

## Overview
This guide explains how to use the compliance and audit features introduced in Phase 5 of the ABTPro trading platform.

## Table of Contents
1. [Audit Trail System](#audit-trail-system)
2. [Static Code Scanning](#static-code-scanning)
3. [Secret Rotation](#secret-rotation)
4. [Disaster Recovery](#disaster-recovery)

---

## Audit Trail System

### What is Audit Trail?
The audit trail system automatically logs all API activities, providing a complete history of actions performed on the platform for security, compliance, and debugging purposes.

### Viewing Audit Logs

#### Query All Audit Logs
```bash
GET /audit/logs
```

**Query Parameters:**
- `userId` - Filter by user ID
- `action` - Filter by action type (CREATE, READ, UPDATE, DELETE)
- `resource` - Filter by API endpoint
- `startDate` - Start date for log range (ISO 8601)
- `endDate` - End date for log range (ISO 8601)
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 50, max: 1000)

**Example:**
```bash
curl -X GET "http://localhost:8000/audit/logs?userId=1&action=CREATE&startDate=2025-11-01T00:00:00Z"
```

**Response:**
```json
{
  "logs": [
    {
      "id": 1,
      "userId": 1,
      "action": "CREATE",
      "resource": "/bot/start",
      "method": "POST",
      "statusCode": 200,
      "ipAddress": "192.168.1.100",
      "userAgent": "Mozilla/5.0...",
      "requestData": "{\"strategy\":\"RSI_CROSS\"}",
      "createdAt": "2025-11-09T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "pages": 3
}
```

#### Get Specific Audit Log
```bash
GET /audit/logs/{id}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/audit/logs/1"
```

#### Export Audit Logs
```bash
GET /audit/export
```

**Query Parameters:**
- `format` - Export format (csv, json) (default: csv)
- `startDate` - Start date for export
- `endDate` - End date for export
- `userId` - Filter by user ID

**Example:**
```bash
curl -X GET "http://localhost:8000/audit/export?format=csv&startDate=2025-11-01T00:00:00Z" -o audit_logs.csv
```

#### View Audit Statistics
```bash
GET /audit/stats
```

**Response:**
```json
{
  "totalLogs": 1500,
  "byAction": {
    "CREATE": 450,
    "READ": 800,
    "UPDATE": 200,
    "DELETE": 50
  },
  "byUser": {
    "1": 600,
    "2": 450,
    "3": 450
  },
  "topEndpoints": [
    {
      "resource": "/dashboard/pnl",
      "count": 500
    },
    {
      "resource": "/bot/start",
      "count": 300
    }
  ]
}
```

### What Gets Logged?
- All API requests and responses
- User authentication events (login, logout)
- Bot operations (start, stop)
- Configuration changes
- Payment transactions
- Secret rotations
- Administrative actions

### Data Retention
- Audit logs are retained for 90 days by default
- Logs older than retention period are automatically archived
- Archived logs can be retrieved from backup storage

---

## Static Code Scanning

### What is Static Code Scanning?
Automated security and code quality scanning to detect vulnerabilities before they reach production.

### Running Security Scans Locally

#### Bandit (Python Security Scanner)
```bash
# Run Bandit on backend code
cd apps/backend
bandit -r src/ -f json -o bandit-report.json

# View report
cat bandit-report.json
```

#### Semgrep (Code Analysis)
```bash
# Run Semgrep with auto configuration
cd apps/backend
semgrep --config=auto src/

# Run with specific rules
semgrep --config=p/security-audit src/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically scan code before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### CI/CD Integration

Security scans run automatically on every push and pull request through GitHub Actions.

**View Scan Results:**
1. Go to GitHub repository
2. Click on "Actions" tab
3. Select the workflow run
4. View "Security Scan" job results

### Understanding Scan Results

#### Severity Levels
- **CRITICAL**: Immediate security risk - fix immediately
- **HIGH**: Significant security issue - fix within 24 hours
- **MEDIUM**: Moderate security concern - fix within 1 week
- **LOW**: Minor issue - fix when convenient

#### Common Issues Detected
- SQL injection vulnerabilities
- Hard-coded secrets
- Weak cryptographic algorithms
- Insecure deserialization
- Command injection risks
- Path traversal vulnerabilities

### Fixing Security Issues

Example: Hard-coded secret detected
```python
# ❌ Bad - Hard-coded secret
API_KEY = "sk_live_123456789"

# ✅ Good - Use environment variables
API_KEY = os.getenv("API_KEY")
```

---

## Secret Rotation

### What is Secret Rotation?
Systematic process of regularly changing sensitive credentials to minimize security risks.

### Viewing Rotation Schedule

```bash
GET /secrets/rotation/schedule
```

**Response:**
```json
{
  "schedules": [
    {
      "secretType": "DATABASE",
      "secretName": "postgres_password",
      "lastRotated": "2025-10-09T00:00:00Z",
      "nextRotation": "2026-01-09T00:00:00Z",
      "daysUntilRotation": 60,
      "status": "ACTIVE"
    },
    {
      "secretType": "ENCRYPTION_KEY",
      "secretName": "master_encryption_key",
      "lastRotated": "2025-11-01T00:00:00Z",
      "nextRotation": "2026-02-01T00:00:00Z",
      "daysUntilRotation": 83,
      "status": "ACTIVE"
    }
  ]
}
```

### Manual Secret Rotation

#### Rotate a Specific Secret
```bash
POST /secrets/rotation/rotate
```

**Request:**
```json
{
  "secretType": "DATABASE",
  "secretName": "postgres_password",
  "newValue": "new_secure_password_here"
}
```

**Response:**
```json
{
  "status": "success",
  "secretType": "DATABASE",
  "secretName": "postgres_password",
  "rotatedAt": "2025-11-09T10:45:00Z",
  "nextRotation": "2026-02-09T00:00:00Z"
}
```

### Rotation History

```bash
GET /secrets/rotation/history?secretType=DATABASE&limit=10
```

**Response:**
```json
{
  "history": [
    {
      "id": 5,
      "secretType": "DATABASE",
      "secretName": "postgres_password",
      "rotatedAt": "2025-11-09T10:45:00Z",
      "rotatedBy": 1,
      "status": "ROTATED"
    },
    {
      "id": 4,
      "secretType": "DATABASE",
      "secretName": "postgres_password",
      "rotatedAt": "2025-08-09T00:00:00Z",
      "rotatedBy": null,
      "status": "DEPRECATED"
    }
  ]
}
```

### Update Rotation Policy

```bash
PUT /secrets/rotation/policy
```

**Request:**
```json
{
  "secretType": "API_KEY",
  "rotationIntervalDays": 60,
  "gracePeriodDays": 7,
  "autoRotate": false
}
```

### Rotation Best Practices

1. **Regular Rotation Schedule**
   - Database passwords: Every 90 days
   - Encryption keys: Every 180 days
   - API keys: Every 60 days
   - OAuth secrets: Every 90 days

2. **Zero-Downtime Rotation**
   - Always maintain old secret during grace period
   - Update all services before deprecating old secret
   - Verify new secret works before completing rotation

3. **Rotation Notifications**
   - System sends notifications 7 days before rotation due
   - Reminders sent 3 days and 1 day before expiry
   - Alerts sent if rotation is overdue

---

## Disaster Recovery

### Health Checks

The platform provides multiple health check endpoints for monitoring.

#### Basic Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T10:50:00Z"
}
```

#### Detailed Health Check
```bash
GET /health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T10:50:00Z",
  "components": {
    "database": {
      "status": "healthy",
      "responseTime": 15
    },
    "redis": {
      "status": "healthy",
      "responseTime": 5
    },
    "celery": {
      "status": "healthy",
      "activeWorkers": 3
    }
  },
  "metrics": {
    "cpuUsage": 45.2,
    "memoryUsage": 67.8,
    "diskUsage": 42.1
  }
}
```

#### Database Health Check
```bash
GET /health/database
```

#### Redis Health Check
```bash
GET /health/redis
```

### Database Backups

#### Backup Configuration

Backups are automatically created daily at 2 AM UTC.

**Environment Variables:**
```env
BACKUP_RETENTION_DAYS=30
BACKUP_STORAGE_PATH=/backups
ENABLE_AUTOMATED_BACKUPS=true
```

#### Manual Backup

```bash
# Create manual backup
docker-compose exec postgres pg_dump -U abtuser abtpro_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Restore from Backup

```bash
# Restore from backup file
docker-compose exec -T postgres psql -U abtuser abtpro_db < backup_20251109_105000.sql
```

### Failover Procedures

#### Primary Database Failure

1. **Detect Failure**
   - Health checks will report database as unhealthy
   - Prometheus alerts will trigger

2. **Promote Replica**
   ```bash
   # Promote replica to primary
   docker-compose exec postgres-replica pg_ctl promote
   ```

3. **Update Connection String**
   ```env
   # Update .env file
   DATABASE_URL=postgresql://user:pass@replica:5432/db
   ```

4. **Restart Services**
   ```bash
   docker-compose restart backend celery-worker
   ```

#### Redis Failure

1. **Switch to Backup Redis**
   ```env
   REDIS_URL=redis://redis-backup:6379/0
   ```

2. **Restart Celery Workers**
   ```bash
   docker-compose restart celery-worker celery-beat
   ```

### Multi-Region Deployment

For production environments, deploy across multiple regions for high availability.

#### Architecture
```
Primary Region (us-east-1)
├── Application Servers
├── Primary Database
└── Redis Primary

Secondary Region (us-west-2)
├── Application Servers (standby)
├── Database Replica
└── Redis Replica

Load Balancer
├── Health Checks
├── Geographic Routing
└── Automatic Failover
```

#### Failover Testing

Regular failover drills should be conducted:

1. **Monthly**: Test database failover
2. **Quarterly**: Full region failover test
3. **Annually**: Complete disaster recovery drill

### Recovery Objectives

- **RTO (Recovery Time Objective)**: < 15 minutes
- **RPO (Recovery Point Objective)**: < 5 minutes
- **Availability Target**: 99.9% uptime

### Monitoring & Alerts

#### Prometheus Metrics
Monitor these key metrics:
- `health_check_status` - System health
- `database_connection_errors` - DB issues
- `backup_success_rate` - Backup health
- `failover_events` - Failover occurrences

#### Alert Notifications
Configure alerts for:
- Database connection failures
- Health check failures (3 consecutive)
- Backup failures
- High error rates (> 5% of requests)

---

## Compliance Reporting

### Generating Compliance Reports

#### SOC 2 Audit Report
```bash
GET /audit/export?format=json&startDate=2025-01-01&endDate=2025-12-31
```

#### Access Control Report
```bash
GET /audit/logs?action=LOGIN&format=csv
```

#### Change Management Report
```bash
GET /audit/logs?action=UPDATE&resource=/user/preferences
```

### Compliance Checklist

✅ **Audit Trail**
- [ ] All API calls are logged
- [ ] Logs retained for 90+ days
- [ ] Sensitive data is sanitized

✅ **Security Scanning**
- [ ] Weekly automated scans
- [ ] No critical vulnerabilities
- [ ] All findings documented

✅ **Secret Management**
- [ ] Rotation schedule followed
- [ ] No hard-coded secrets
- [ ] Rotation history maintained

✅ **Disaster Recovery**
- [ ] Daily backups verified
- [ ] Failover tested monthly
- [ ] RTO/RPO targets met

---

## Troubleshooting

### Audit Logs Not Appearing

**Problem**: API calls not being logged

**Solution**:
1. Check middleware is enabled in `main.py`
2. Verify database connectivity
3. Check `AUDIT_LOG_LEVEL` environment variable
4. Review application logs for errors

### Security Scan Failures

**Problem**: CI/CD security scans failing

**Solution**:
1. Review scan output for specific issues
2. Check `.bandit` and `semgrep` configurations
3. Update scan rules if false positives
4. Fix legitimate security issues

### Failed Secret Rotation

**Problem**: Secret rotation fails

**Solution**:
1. Verify new secret is valid
2. Check grace period is sufficient
3. Ensure all services are updated
4. Review rotation logs for errors

### Health Check Failures

**Problem**: Health checks reporting unhealthy

**Solution**:
1. Check database connectivity
2. Verify Redis is running
3. Review system resources (CPU, memory)
4. Check application logs

---

## Best Practices

### Security
1. Review audit logs weekly
2. Run security scans before each release
3. Rotate secrets on schedule
4. Test failover procedures regularly

### Monitoring
1. Set up Prometheus alerts
2. Monitor health check endpoints
3. Track audit log growth
4. Review backup success rates

### Compliance
1. Export audit logs monthly
2. Document all security incidents
3. Maintain rotation history
4. Keep compliance documentation updated

---

## Support

For issues or questions about Phase 5 features:
1. Check application logs in `/var/log/abtpro/`
2. Review Prometheus metrics at `/metrics`
3. Consult PHASE5_SUMMARY.md for technical details
4. Contact support team for assistance

## Additional Resources

- [PHASE5_SUMMARY.md](PHASE5_SUMMARY.md) - Technical specifications
- [SECURITY.md](SECURITY.md) - Security guidelines
- [ROADMAP.md](ROADMAP.md) - Platform roadmap
- [Prometheus Documentation](https://prometheus.io/docs/)
- [PostgreSQL Backup Guide](https://www.postgresql.org/docs/current/backup.html)
