"""// ZeaZDev [Backend Trading Bot Runner Core] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 2 Enhanced) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

import asyncio
from typing import Any, Dict

from prisma import Prisma
from tenacity import retry, stop_after_attempt, wait_fixed

from src.services.exchange_service import ExchangeConnector
from src.services.metrics_service import MetricsCollector
from src.trading.risk_manager import EnhancedRiskManager
from src.trading.strategy_interface import StrategyRegistry


# Legacy RiskManager for backward compatibility
class RiskManager:
    def __init__(self, max_drawdown: float = 0.25, max_position_fraction: float = 0.1):
        self.max_drawdown = max_drawdown
        self.max_position_fraction = max_position_fraction

    async def assess(
        self, context: Dict[str, Any], signal_payload: Dict[str, Any]
    ) -> bool:
        # Simplified risk: always allow if signal != HOLD
        if signal_payload.get("signal") == "HOLD":
            return False
        return True


class BotRunner:
    def __init__(self, prisma: Prisma, bot_id: int, use_enhanced_risk: bool = True):
        self.prisma = prisma
        self.bot_id = bot_id
        self._running = True
        # Use enhanced risk manager by default
        if use_enhanced_risk:
            self.risk = EnhancedRiskManager()
        else:
            self.risk = RiskManager()

    async def load_bot(self):
        bot = await self.prisma.botrun.find_unique(where={"id": self.bot_id})
        if not bot:
            raise ValueError("Bot not found")
        return bot

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    async def fetch_ohlcv(self, exchange, symbol: str, timeframe: str):
        return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=150)

    async def run_loop(self):
        bot = await self.load_bot()
        strategy = StrategyRegistry.create(bot.strategy)
        exchange = await ExchangeConnector.for_exchange("binance")  # Could map per bot
        symbol = bot.symbol
        timeframe = bot.timeframe

        # Update bot status metric
        MetricsCollector.update_bot_status(self.bot_id, bot.strategy, symbol, True)

        while self._running:
            bot_state = await self.prisma.botrun.find_unique(where={"id": self.bot_id})
            if bot_state.status != "RUNNING":
                break
            ohlcv = await asyncio.to_thread(
                self.fetch_ohlcv, exchange, symbol, timeframe
            )

            # Extract OHLCV data
            opens = [c[1] for c in ohlcv]
            highs = [c[2] for c in ohlcv]
            lows = [c[3] for c in ohlcv]
            closes = [c[4] for c in ohlcv]
            volumes = [c[5] for c in ohlcv]

            ticker_data = {
                "opens": opens,
                "highs": highs,
                "lows": lows,
                "closes": closes,
                "volumes": volumes,
            }
            context = {"symbol": symbol, "timeframe": timeframe}

            # Time strategy execution
            with MetricsCollector.time_strategy_execution(bot.strategy):
                decision = strategy.execute(ticker_data, context)

            # Record strategy signal
            signal = decision.get("signal", "HOLD")
            MetricsCollector.record_strategy_signal(bot.strategy, signal, symbol)

            # Enhanced risk assessment
            if isinstance(self.risk, EnhancedRiskManager):
                risk_result = await self.risk.assess(
                    context, decision, self.prisma, self.bot_id
                )
                allowed = risk_result["allowed"]
                MetricsCollector.record_risk_check(allowed)

                # Update risk metrics
                if allowed:
                    metrics = self.risk.get_metrics()
                    MetricsCollector.update_risk_metrics(self.bot_id, metrics)
            else:
                allowed = await self.risk.assess(context, decision)

            if allowed and decision["signal"] in ("BUY", "SELL"):
                qty = 0.001  # Fixed fraction (stub position sizing)
                await self.record_trade(decision["signal"], qty, closes[-1], decision)
            await asyncio.sleep(5)

        # Update bot status when stopped
        MetricsCollector.update_bot_status(self.bot_id, bot.strategy, symbol, False)

    async def record_trade(self, side: str, quantity: float, price: float, decision):
        pnl = 0.0  # For simplicity - could calculate based on previous trades

        # Get bot info for metrics
        bot = await self.prisma.botrun.find_unique(where={"id": self.bot_id})

        await self.prisma.tradelog.create(
            data={
                "botRunId": self.bot_id,
                "side": side,
                "quantity": quantity,
                "price": price,
                "pnl": pnl,
            }
        )

        # Record metrics
        MetricsCollector.record_trade(self.bot_id, bot.strategy, side, bot.symbol, pnl)

        # Record trade result in enhanced risk manager
        if isinstance(self.risk, EnhancedRiskManager):
            self.risk.record_trade_result(pnl)
            # Check if circuit breaker tripped
            if self.risk.circuit_breaker.is_tripped():
                MetricsCollector.record_circuit_breaker_trip()
