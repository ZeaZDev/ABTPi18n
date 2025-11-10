"""// ZeaZDev [Backend API Bot Endpoints] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from src.worker.tasks import run_bot_loop
from src.utils.database import get_db_connection
from src.utils.exceptions import raise_not_found, raise_bad_request

router = APIRouter()

class StartBotInput(BaseModel):
    strategy: str
    symbol: str
    timeframe: str

class StopBotInput(BaseModel):
    bot_id: int

@router.post("/start")
async def start_bot(data: StartBotInput):
    async with get_db_connection() as prisma:
        bot_run = await prisma.botrun.create(data={
            "userId": 1,
            "strategy": data.strategy,
            "symbol": data.symbol,
            "timeframe": data.timeframe,
            "status": "RUNNING"
        })
        task = run_bot_loop.delay(bot_run.id)
        return {"status": "BOT_STARTED", "bot_id": bot_run.id, "celery_task_id": task.id}

@router.post("/stop")
async def stop_bot(payload: StopBotInput):
    async with get_db_connection() as prisma:
        bot = await prisma.botrun.find_unique(where={"id": payload.bot_id})
        if not bot:
            raise_not_found("Bot not found")
        if bot.status != "RUNNING":
            raise_bad_request("Bot not running")
        await prisma.botrun.update(where={"id": payload.bot_id}, data={
            "status": "STOPPED",
            "stoppedAt": datetime.utcnow()
        })
        return {"status": "BOT_STOPPED", "bot_id": payload.bot_id}