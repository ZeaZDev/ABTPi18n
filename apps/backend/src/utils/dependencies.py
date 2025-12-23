"""// ZeaZDev [FastAPI Dependencies] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 //
// Author: ZeaZDev Meta-Intelligence //
// --- DO NOT EDIT HEADER --- //"""

from typing import Optional

from fastapi import Request


async def get_current_user_id(request: Request) -> int:
    """
    Dependency to extract user ID from session token

    In production, this would validate the session token from the cookie
    and look up the user in the database.

    For now, returns a default user ID of 1.

    Args:
        request: FastAPI Request object

    Returns:
        User ID

    Raises:
        HTTPException: If not authenticated
    """
    # Get session token from cookie
    _session_token = request.cookies.get("session_token")

    # In production, validate token and look up user
    # For now, return default user ID
    # TODO: Implement proper session validation
    return 1


async def get_optional_user_id(request: Request) -> Optional[int]:
    """
    Dependency to extract user ID from session token (optional)

    Returns None if not authenticated instead of raising an exception.

    Args:
        request: FastAPI Request object

    Returns:
        User ID or None
    """
    _session_token = request.cookies.get("session_token")

    if not _session_token:
        return None

    # In production, validate token and look up user
    # For now, return default user ID
    # TODO: Implement proper session validation
    return 1
