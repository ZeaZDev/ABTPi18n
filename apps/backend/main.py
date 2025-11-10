"""// ZeaZDev [Backend FastAPI Entrypoint] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 6) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

import os
from logging import getLogger
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime
from src.api.bot_endpoints import router as bot_router
from src.api.auth_endpoints import router as auth_router
from src.api.telegram_endpoints import router as telegram_router
from src.api.preferences_endpoints import router as preferences_router

# Phase 4 routers
from src.api.payment_endpoints import router as payment_router
from src.api.rental_endpoints import router as rental_router
from src.api.plugin_endpoints import router as plugin_router
from src.api.portfolio_endpoints import router as portfolio_router
from src.api.backtest_endpoints import router as backtest_router

# Phase 5 routers
from src.api.audit_endpoints import router as audit_router
from src.api.secret_rotation_endpoints import router as secrets_router
from src.api.health_endpoints import router as health_router

# Phase 6 routers
from src.api.ml_endpoints import router as ml_router

# TradingView integration
from src.api.tradingview_endpoints import router as tradingview_router

from src.security.crypto_service import encrypt_data
from src.trading.strategy_interface import StrategyRegistry

# Phase 5 middleware
from src.services.audit_middleware import AuditMiddleware
from typing import Optional
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

DATABASE_URL = os.getenv("DATABASE_URL")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

logger = getLogger(__name__)

app = FastAPI(title="ZeaZDev-ABTPro-i18n Backend", version="1.0.0")
prisma = Prisma()

origins = {
    "http://localhost:3000",
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.rstrip("/") for o in origins],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Phase 5: Add audit middleware
if os.getenv("ENABLE_AUDIT_LOGGING", "true").lower() == "true":
    app.add_middleware(AuditMiddleware)

# Initialize Prometheus instrumentation at module level (before startup)
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False,
)


class ExchangeKeyInput(BaseModel):
    exchange: str
    api_key: str
    api_secret: str


class LoginInput(BaseModel):
    email: str
    google_token: Optional[str] = None


@app.on_event("startup")
async def startup():
    """Startup handler with lazy DB connection retry"""
    try:
        await prisma.connect()
    except Exception as e:
        # Log error but don't crash - allow health endpoint to handle retries
        print(f"Warning: Database connection failed during startup: {e}")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown handler with safe disconnect"""
    try:
        if prisma.is_connected():
            await prisma.disconnect()
    except Exception as e:
        print(f"Warning: Error during database disconnect: {e}")


@app.get("/health", tags=["Health & Monitoring"])
async def health():
    """Health check endpoint with lazy DB connection"""
    if not prisma.is_connected():
        try:
            await prisma.connect()
        except Exception as e:
            logger.warning(
                f"DB connect failed in health check: {e.__class__.__name__}",
                extra={"component": "database", "event": "health_db_connect_failed"},
            )
            return {
                "status": "degraded",
                "component": "database",
                "code": "DB_CONNECT_FAILED",
            }
    return {"status": "ok"}


@app.post("/auth/login")
async def login(data: LoginInput):
    # Simplified login: In production integrate Google OAuth token validation
    user = await prisma.user.find_first(where={"email": data.email})
    if not user:
        user = await prisma.user.create(data={"email": data.email})
    return {"user_id": user.id, "email": user.email, "status": "LOGIN_OK"}


@app.post("/exchange/keys")
async def save_exchange_keys(payload: ExchangeKeyInput):
    if payload.exchange not in ["binance", "bybit"]:
        raise HTTPException(status_code=400, detail="Unsupported exchange")
    enc_key, iv_key = encrypt_data(payload.api_key)
    enc_secret, iv_secret = encrypt_data(payload.api_secret)
    record = await prisma.exchangekey.create(
        data={
            "exchange": payload.exchange,
            "encrypted_key": enc_key,
            "iv_key": iv_key,
            "encrypted_secret": enc_secret,
            "iv_secret": iv_secret,
        }
    )
    return {"status": "STORED_SECURE", "id": record.id}


@app.get("/strategies")
async def list_strategies():
    return {"strategies": StrategyRegistry.list_names()}


@app.get("/dashboard/pnl")
async def dashboard_pnl():
    # Aggregate from TradeLog & BotRun
    trades = await prisma.tradelog.find_many()
    pnl = sum([t.pnl for t in trades])
    open_bots = await prisma.botrun.count(where={"status": "RUNNING"})
    return {
        "total_pnl": round(pnl, 4),
        "currency": "USDT",
        "open_bots": open_bots,
        "last_update": datetime.utcnow().isoformat(),
    }


app.include_router(bot_router, prefix="/bot", tags=["Bot Control"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])
app.include_router(preferences_router, prefix="/user", tags=["User Preferences"])
# Phase 4 routes
app.include_router(payment_router, prefix="/payment", tags=["Payment & Wallet"])
app.include_router(rental_router, prefix="/rental", tags=["Rental Contracts"])
app.include_router(plugin_router, prefix="/plugins", tags=["Plugin System"])
app.include_router(portfolio_router, prefix="/portfolio", tags=["Portfolio Management"])
app.include_router(
    backtest_router, prefix="/backtest", tags=["Backtesting & Paper Trading"]
)
# Phase 5 routes
app.include_router(audit_router, prefix="/audit", tags=["Audit Trail"])
app.include_router(secrets_router, prefix="/secrets", tags=["Secret Rotation"])
# app.include_router(health_router, prefix="/health", tags=["Health & Monitoring"])  # optional alternative health router
# Phase 6 routes
app.include_router(ml_router, tags=["ML & Intelligence"])
# TradingView integration
app.include_router(tradingview_router, prefix="/tradingview", tags=["TradingView"])
