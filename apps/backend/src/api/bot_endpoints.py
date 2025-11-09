"""// ZeaZDev [Backend API Bot Endpoints] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime
from src.worker.tasks import run_bot_loop

router = APIRouter()
prisma = Prisma()

class StartBotInput(BaseModel):
    strategy: str
    symbol: str
    timeframe: str

class StopBotInput(BaseModel):
    bot_id: int

@router.post("/start")
async def start_bot(data: StartBotInput):
    await prisma.connect()
    bot_run = await prisma.botrun.create(data={
        "userId": 1,
        "strategy": data.strategy,
        "symbol": data.symbol,
        "timeframe": data.timeframe,
        "status": "RUNNING"
    })
    task = run_bot_loop.delay(bot_run.id)
    await prisma.disconnect()
    return {"status": "BOT_STARTED", "bot_id": bot_run.id, "celery_task_id": task.id}

@router.post("/stop")
async def stop_bot(payload: StopBotInput):
    await prisma.connect()
    bot = await prisma.botrun.find_unique(where={"id": payload.bot_id})
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot.status != "RUNNING":
        raise HTTPException(status_code=400, detail="Bot not running")
    await prisma.botrun.update(where={"id": payload.bot_id}, data={
        "status": "STOPPED",
        "stoppedAt": datetime.utcnow()
    })
    await prisma.disconnect()
    return {"status": "BOT_STOPPED", "bot_id": payload.bot_id}