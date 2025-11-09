"""// ZeaZDev [Audit Service] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 5) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from prisma import Prisma

# Sensitive fields to sanitize from logs
SENSITIVE_FIELDS = os.getenv("AUDIT_SENSITIVE_FIELDS", "password,secret,token,api_key").split(",")

class AuditService:
    """Service for managing audit logs"""
    
    def __init__(self):
        self.prisma = Prisma()
        self.retention_days = int(os.getenv("AUDIT_LOG_RETENTION_DAYS", "90"))
    
    async def connect(self):
        """Connect to database"""
        if not self.prisma.is_connected():
            await self.prisma.connect()
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.prisma.is_connected():
            await self.prisma.disconnect()
    
    def sanitize_data(self, data: Any) -> str:
        """
        Sanitize sensitive data before logging
        
        Args:
            data: Data to sanitize (dict, list, or other)
            
        Returns:
            JSON string with sensitive fields redacted
        """
        if data is None:
            return None
        
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                # Check if key contains sensitive field name
                is_sensitive = any(field.lower() in key.lower() for field in SENSITIVE_FIELDS)
                if is_sensitive:
                    sanitized[key] = "***REDACTED***"
                elif isinstance(value, (dict, list)):
                    sanitized[key] = json.loads(self.sanitize_data(value))
                else:
                    sanitized[key] = value
            return json.dumps(sanitized)
        elif isinstance(data, list):
            return json.dumps([self.sanitize_data(item) for item in data])
        else:
            return json.dumps(data)
    
    async def log_api_call(
        self,
        user_id: Optional[int],
        action: str,
        resource: str,
        method: str,
        status_code: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log an API call to the audit trail
        
        Args:
            user_id: User ID making the request (None for unauthenticated)
            action: Action type (CREATE, READ, UPDATE, DELETE, LOGIN, LOGOUT)
            resource: API endpoint or resource identifier
            method: HTTP method (GET, POST, PUT, DELETE)
            status_code: HTTP status code
            ip_address: Client IP address
            user_agent: User agent string
            request_data: Request body/parameters
            metadata: Additional context
            
        Returns:
            Created audit log record
        """
        await self.connect()
        
        # Sanitize request data
        sanitized_request = self.sanitize_data(request_data) if request_data else None
        sanitized_metadata = self.sanitize_data(metadata) if metadata else None
        
        audit_log = await self.prisma.auditlog.create(
            data={
                "userId": user_id,
                "action": action,
                "resource": resource,
                "method": method,
                "statusCode": status_code,
                "ipAddress": ip_address,
                "userAgent": user_agent,
                "requestData": sanitized_request,
                "metadata": sanitized_metadata
            }
        )
        
        return {
            "id": audit_log.id,
            "userId": audit_log.userId,
            "action": audit_log.action,
            "resource": audit_log.resource,
            "createdAt": audit_log.createdAt.isoformat()
        }
    
    async def get_logs(
        self,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Query audit logs with filters
        
        Args:
            user_id: Filter by user ID
            action: Filter by action type
            resource: Filter by resource (supports partial match)
            start_date: Start of date range
            end_date: End of date range
            page: Page number (1-indexed)
            limit: Items per page (max 1000)
            
        Returns:
            Paginated audit logs
        """
        await self.connect()
        
        # Build where clause
        where = {}
        if user_id is not None:
            where["userId"] = user_id
        if action:
            where["action"] = action
        if resource:
            where["resource"] = {"contains": resource}
        
        # Date range filter
        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["gte"] = start_date
            if end_date:
                date_filter["lte"] = end_date
            where["createdAt"] = date_filter
        
        # Limit to max 1000 per page
        limit = min(limit, 1000)
        skip = (page - 1) * limit
        
        # Get logs and total count
        logs = await self.prisma.auditlog.find_many(
            where=where,
            skip=skip,
            take=limit,
            order={"createdAt": "desc"},
            include={"user": True}
        )
        
        total = await self.prisma.auditlog.count(where=where)
        
        return {
            "logs": [
                {
                    "id": log.id,
                    "userId": log.userId,
                    "userEmail": log.user.email if log.user else None,
                    "action": log.action,
                    "resource": log.resource,
                    "method": log.method,
                    "statusCode": log.statusCode,
                    "ipAddress": log.ipAddress,
                    "userAgent": log.userAgent,
                    "requestData": log.requestData,
                    "metadata": log.metadata,
                    "createdAt": log.createdAt.isoformat()
                }
                for log in logs
            ],
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }
    
    async def get_log_by_id(self, log_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific audit log by ID"""
        await self.connect()
        
        log = await self.prisma.auditlog.find_unique(
            where={"id": log_id},
            include={"user": True}
        )
        
        if not log:
            return None
        
        return {
            "id": log.id,
            "userId": log.userId,
            "userEmail": log.user.email if log.user else None,
            "action": log.action,
            "resource": log.resource,
            "method": log.method,
            "statusCode": log.statusCode,
            "ipAddress": log.ipAddress,
            "userAgent": log.userAgent,
            "requestData": log.requestData,
            "metadata": log.metadata,
            "createdAt": log.createdAt.isoformat()
        }
    
    async def get_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get audit log statistics
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            Statistics about audit logs
        """
        await self.connect()
        
        # Build where clause for date range
        where = {}
        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["gte"] = start_date
            if end_date:
                date_filter["lte"] = end_date
            where["createdAt"] = date_filter
        
        # Get total count
        total = await self.prisma.auditlog.count(where=where)
        
        # Get all logs for aggregation (could be optimized with raw SQL)
        logs = await self.prisma.auditlog.find_many(where=where)
        
        # Aggregate by action
        by_action = {}
        by_user = {}
        resource_counts = {}
        
        for log in logs:
            # Count by action
            by_action[log.action] = by_action.get(log.action, 0) + 1
            
            # Count by user
            if log.userId:
                by_user[str(log.userId)] = by_user.get(str(log.userId), 0) + 1
            
            # Count by resource
            resource_counts[log.resource] = resource_counts.get(log.resource, 0) + 1
        
        # Get top 10 endpoints
        top_endpoints = sorted(
            [{"resource": k, "count": v} for k, v in resource_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]
        
        return {
            "totalLogs": total,
            "byAction": by_action,
            "byUser": by_user,
            "topEndpoints": top_endpoints
        }
    
    async def cleanup_old_logs(self) -> int:
        """
        Delete audit logs older than retention period
        
        Returns:
            Number of logs deleted
        """
        await self.connect()
        
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
        
        result = await self.prisma.auditlog.delete_many(
            where={
                "createdAt": {
                    "lt": cutoff_date
                }
            }
        )
        
        return result
