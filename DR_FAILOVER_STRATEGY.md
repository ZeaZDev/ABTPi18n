# Disaster Recovery & Failover Strategy

## Overview
This document outlines the disaster recovery (DR) and failover strategy for the ABTPro trading platform to ensure business continuity and minimize downtime in case of infrastructure failures.

## Recovery Objectives

### Recovery Time Objective (RTO)
**Target: < 15 minutes**
- Time to restore service after a failure
- Includes detection, failover, and verification

### Recovery Point Objective (RPO)
**Target: < 5 minutes**
- Maximum acceptable data loss
- Achieved through continuous replication

### Availability Target
**Target: 99.9% uptime**
- Allows ~8.76 hours of downtime per year
- Monthly uptime: ~43 minutes

## Architecture Components

### Primary Region (Production)
```
Primary Region (us-east-1)
├── Load Balancer (ELB/ALB)
├── Application Servers (2+ instances)
│   ├── FastAPI Backend
│   └── Celery Workers
├── Primary Database (PostgreSQL)
│   ├── Automated backups
│   └── WAL archiving
└── Redis Primary
    └── AOF persistence
```

### Secondary Region (Standby)
```
Secondary Region (us-west-2)
├── Load Balancer (standby)
├── Application Servers (standby)
├── Database Replica (read-only)
│   ├── Streaming replication
│   └── Point-in-time recovery
└── Redis Replica
    └── Replication from primary
```

## Backup Strategy

### Database Backups

#### Automated Daily Backups
- **Frequency**: Daily at 2:00 AM UTC
- **Retention**: 30 days
- **Storage**: AWS S3 or equivalent
- **Encryption**: AES-256

**Script**:
```bash
#!/bin/bash
# Automated database backup script
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="abtpro_backup_${BACKUP_DATE}.sql.gz"

# Create backup
docker-compose exec -T postgres pg_dump -U abtuser abtpro_db | gzip > "/backups/${BACKUP_FILE}"

# Upload to S3 (if configured)
if [ -n "$AWS_S3_BUCKET" ]; then
    aws s3 cp "/backups/${BACKUP_FILE}" "s3://${AWS_S3_BUCKET}/backups/"
fi

# Clean up old backups (keep 30 days)
find /backups -name "abtpro_backup_*.sql.gz" -mtime +30 -delete
```

#### Point-in-Time Recovery (PITR)
- **WAL archiving**: Continuous
- **Retention**: 7 days
- **Recovery granularity**: 1 second

**Configuration** (`postgresql.conf`):
```conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/wal_archive/%f'
max_wal_senders = 3
wal_keep_size = 1GB
```

### Application Data Backups

#### Configuration Backups
- **Files**: .env, docker-compose.yml, nginx configs
- **Frequency**: On change + daily
- **Storage**: Git repository + S3

#### User Data Backups
- **Encrypted API keys**: Included in database backup
- **User preferences**: Included in database backup
- **Trade logs**: Included in database backup

## Replication Setup

### PostgreSQL Streaming Replication

#### Primary Database Setup
```sql
-- Create replication user
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'secure_password';

-- Configure pg_hba.conf
host replication replicator replica_ip/32 md5
```

#### Replica Database Setup
```bash
# Initial base backup
pg_basebackup -h primary_host -D /var/lib/postgresql/data -U replicator -P -v

# Configure standby.signal
touch /var/lib/postgresql/data/standby.signal

# Configure postgresql.conf
primary_conninfo = 'host=primary_host port=5432 user=replicator password=secure_password'
```

### Redis Replication

**Primary Redis** (`redis.conf`):
```conf
bind 0.0.0.0
protected-mode yes
requirepass your_redis_password
appendonly yes
appendfsync everysec
```

**Replica Redis** (`redis.conf`):
```conf
replicaof primary_host 6379
masterauth your_redis_password
replica-read-only yes
```

## Failover Procedures

### Database Failover

#### Automatic Failover (with Patroni/pgpool)
1. Health check detects primary failure
2. Promote replica to primary
3. Update connection strings
4. Restart application servers
5. Verify new primary is accepting writes

#### Manual Failover
```bash
# 1. Check replica status
docker-compose exec postgres-replica psql -U abtuser -c "SELECT pg_is_in_recovery();"

# 2. Promote replica to primary
docker-compose exec postgres-replica pg_ctl promote

# 3. Update DATABASE_URL in .env
DATABASE_URL=postgresql://abtuser:password@replica:5432/abtpro_db

# 4. Restart backend services
docker-compose restart backend celery-worker celery-beat

# 5. Verify writes
docker-compose exec postgres psql -U abtuser -c "CREATE TABLE failover_test (id INT);"
docker-compose exec postgres psql -U abtuser -c "DROP TABLE failover_test;"
```

### Redis Failover

```bash
# 1. Check replica status
docker-compose exec redis-replica redis-cli INFO replication

# 2. Promote replica (disable replication)
docker-compose exec redis-replica redis-cli REPLICAOF NO ONE

# 3. Update REDIS_URL in .env
REDIS_URL=redis://redis-replica:6379/0

# 4. Restart Celery workers
docker-compose restart celery-worker celery-beat
```

### Application Failover

#### DNS-based Failover
```
1. Update DNS records to point to standby region
2. TTL: 60 seconds for faster propagation
3. Health checks verify new endpoint
```

#### Load Balancer Failover
```
1. Update load balancer target group
2. Drain connections from failed instances
3. Route traffic to healthy instances
```

## Monitoring & Alerting

### Health Check Endpoints
- `GET /health` - Basic health status
- `GET /health/detailed` - Component health
- `GET /health/database` - Database connectivity
- `GET /health/redis` - Redis connectivity

### Prometheus Alerts

**Database Connection Alert**:
```yaml
- alert: DatabaseConnectionFailed
  expr: health_check_database_status == 0
  for: 5m
  annotations:
    summary: "Database connection failed"
    description: "Primary database is unreachable"
```

**High Error Rate Alert**:
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  annotations:
    summary: "High error rate detected"
    description: "More than 5% of requests are failing"
```

### Notification Channels
- **PagerDuty**: Critical alerts (database down, high error rate)
- **Slack**: Warning alerts (high CPU, disk space)
- **Email**: Daily summary and non-urgent alerts

## Disaster Recovery Drills

### Monthly DR Test
**Objective**: Verify backup and restore procedures

1. Create manual backup
2. Restore to test environment
3. Verify data integrity
4. Document any issues

**Checklist**:
- [ ] Backup completes successfully
- [ ] Backup file is encrypted
- [ ] Restore completes within 15 minutes
- [ ] Data integrity verified
- [ ] No data loss detected

### Quarterly Failover Test
**Objective**: Test complete failover process

1. Schedule maintenance window
2. Simulate primary region failure
3. Execute failover procedures
4. Verify all services operational
5. Measure RTO/RPO
6. Failback to primary

**Checklist**:
- [ ] Failover completes within RTO (15 min)
- [ ] Data loss within RPO (5 min)
- [ ] All services functional
- [ ] Monitoring operational
- [ ] No critical errors

### Annual Full DR Drill
**Objective**: Test complete disaster recovery

1. Simulate catastrophic failure
2. Restore from backups
3. Deploy to new region
4. Verify complete functionality
5. Load testing
6. Security audit

## Recovery Procedures

### Scenario 1: Database Corruption

**Detection**: Database queries failing, data inconsistencies

**Recovery**:
```bash
# 1. Stop application
docker-compose stop backend celery-worker

# 2. Identify latest good backup
ls -lt /backups/

# 3. Restore from backup
gunzip < /backups/abtpro_backup_20251109_020000.sql.gz | \
  docker-compose exec -T postgres psql -U abtuser abtpro_db

# 4. Apply WAL files for PITR (if available)
# This recovers to a specific point in time

# 5. Restart services
docker-compose start backend celery-worker

# 6. Verify data integrity
```

**Estimated Recovery Time**: 10-20 minutes

### Scenario 2: Complete Region Failure

**Detection**: All health checks failing, region unavailable

**Recovery**:
```bash
# 1. Update DNS to point to secondary region
# TTL: 60 seconds

# 2. Promote secondary database to primary
ssh secondary-region "docker-compose exec postgres pg_ctl promote"

# 3. Promote secondary Redis
ssh secondary-region "docker-compose exec redis redis-cli REPLICAOF NO ONE"

# 4. Start application services in secondary region
ssh secondary-region "docker-compose up -d backend celery-worker"

# 5. Verify health checks
curl https://secondary-region.abtpro.com/health/detailed

# 6. Monitor error rates and performance
```

**Estimated Recovery Time**: 10-15 minutes

### Scenario 3: Data Center Outage

**Detection**: Network connectivity lost, all services unreachable

**Recovery**:
1. Verify extent of outage
2. Activate disaster recovery plan
3. Deploy to alternate region
4. Restore from latest backup
5. Update DNS records
6. Notify users of service restoration

**Estimated Recovery Time**: 30-60 minutes

## Data Integrity Verification

### Automated Checks
```bash
# Database consistency check
docker-compose exec postgres psql -U abtuser -c "
  SELECT COUNT(*) FROM pg_stat_activity;
  SELECT COUNT(*) FROM user;
  SELECT COUNT(*) FROM tradelog;
"

# Redis data verification
docker-compose exec redis redis-cli DBSIZE
docker-compose exec redis redis-cli INFO persistence
```

### Manual Verification
1. Check user count matches expected
2. Verify recent trades are present
3. Check system configuration
4. Test critical user flows

## Communication Plan

### Incident Communication

**Status Page**: status.abtpro.com
- Real-time status updates
- Scheduled maintenance notifications
- Incident reports

**Communication Channels**:
1. **Immediate** (< 5 min): Status page update
2. **Short-term** (< 30 min): Email to affected users
3. **Post-incident** (< 24 hours): Detailed incident report

**Template**:
```
Subject: [INCIDENT] Service Disruption - [DATE]

We are currently experiencing a service disruption affecting:
- [Component]
- [Impact]
- [Affected users]

Current Status: [INVESTIGATING/IDENTIFIED/MONITORING/RESOLVED]

Expected Resolution: [TIME]

We will provide updates every 30 minutes.

Thank you for your patience.
```

## Compliance & Documentation

### Audit Requirements
- All DR drills documented
- Backup logs retained for 1 year
- Incident reports for all outages
- RTO/RPO metrics tracked

### Required Documentation
- [ ] Current system architecture diagram
- [ ] Backup and restore procedures
- [ ] Failover runbooks
- [ ] Contact list (on-call rotation)
- [ ] Vendor support contacts
- [ ] Recovery time estimates

## Continuous Improvement

### Post-Incident Review
After any incident or DR drill:
1. Document what happened
2. Analyze root cause
3. Identify improvements
4. Update procedures
5. Train team on changes

### Metrics to Track
- Mean Time To Detect (MTTD)
- Mean Time To Resolve (MTTR)
- Backup success rate
- Restore success rate
- Actual vs. target RTO/RPO

## Contact Information

### Emergency Contacts
- **On-call Engineer**: [Phone]
- **Database Admin**: [Phone]
- **Infrastructure Lead**: [Phone]
- **CTO**: [Phone]

### Vendor Support
- **AWS Support**: [Support plan level]
- **Database Vendor**: [Support contact]
- **Monitoring Service**: [Support contact]

## Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-09 | 1.0 | ZeaZDev | Initial DR strategy for Phase 5 |

---

**Last Updated**: November 9, 2025
**Next Review Date**: December 9, 2025
**Document Owner**: Infrastructure Team
