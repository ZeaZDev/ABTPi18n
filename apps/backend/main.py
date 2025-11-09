"""// ZeaZDev [Backend FastAPI Entrypoint] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime
from src.api.bot_endpoints import router as bot_router
from src.api.auth_endpoints import router as auth_router
from src.api.telegram_endpoints import router as telegram_router
from src.api.preferences_endpoints import router as preferences_router
from src.security.crypto_service import encrypt_data
from src.trading.strategy_interface import StrategyRegistry
from typing import Optional
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

DATABASE_URL = os.getenv("DATABASE_URL")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

app = FastAPI(title="ZeaZDev-ABTPro-i18n Backend", version="1.0.0")
prisma = Prisma()

origins = ["http://localhost:3000", os.getenv("FRONTEND_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
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
    await prisma.connect()
    # Initialize Prometheus instrumentation
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

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
    record = await prisma.exchangekey.create(data={
        "exchange": payload.exchange,
        "encrypted_key": enc_key,
        "iv_key": iv_key,
        "encrypted_secret": enc_secret,
        "iv_secret": iv_secret
    })
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
        "last_update": datetime.utcnow().isoformat()
    }

app.include_router(bot_router, prefix="/bot", tags=["Bot Control"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(telegram_router, prefix="/telegram", tags=["Telegram"])
app.include_router(preferences_router, prefix="/user", tags=["User Preferences"])