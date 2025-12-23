"""// ZeaZDev [Database Utilities] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 //
// Author: ZeaZDev Meta-Intelligence //
// --- DO NOT EDIT HEADER --- //"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Callable, Dict, TypeVar

from prisma import Prisma

T = TypeVar("T")


@asynccontextmanager
async def get_db_connection():
    """
    Context manager for database connections

    Ensures proper connection and disconnection

    Usage:
        async with get_db_connection() as db:
            result = await db.user.count()
    """
    prisma = Prisma()
    await prisma.connect()
    try:
        yield prisma
    finally:
        await prisma.disconnect()


async def time_database_operation(operation: Callable[[], Any]) -> Dict[str, Any]:
    """
    Time a database operation and return the result with timing info

    Args:
        operation: Async callable that performs the database operation

    Returns:
        Dict with 'result' and 'responseTime' (in milliseconds)
    """
    start_time = datetime.utcnow()
    result = await operation()
    end_time = datetime.utcnow()

    response_time = (end_time - start_time).total_seconds() * 1000

    return {"result": result, "responseTime": round(response_time, 2)}
