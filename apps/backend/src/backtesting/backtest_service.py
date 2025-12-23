"""// ZeaZDev [Backtest Service] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 4) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
from prisma import Prisma

logger = logging.getLogger(__name__)


class BacktestService:
    """Service for running backtests and paper trading sessions"""

    def __init__(self):
        self.prisma = Prisma()

    async def create_backtest(
        self,
        user_id: int,
        strategy_name: str,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime,
        initial_capital: float = 10000.0,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new backtest run"""
        await self.prisma.connect()

        try:
            backtest = await self.prisma.backtestrun.create(
                data={
                    "userId": user_id,
                    "strategyName": strategy_name,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "startDate": start_date,
                    "endDate": end_date,
                    "initialCapital": initial_capital,
                    "status": "PENDING",
                    "results": json.dumps({"parameters": parameters or {}}),
                }
            )

            return {
                "backtest_id": backtest.id,
                "status": backtest.status,
                "created_at": backtest.createdAt.isoformat(),
            }
        finally:
            await self.prisma.disconnect()

    async def run_backtest(self, backtest_id: int) -> Dict[str, Any]:
        """
        Execute a backtest (simplified version)
        In production, this would run in a Celery task
        """
        await self.prisma.connect()

        try:
            # Get backtest configuration
            backtest = await self.prisma.backtestrun.find_first(
                where={"id": backtest_id}
            )

            if not backtest:
                raise ValueError(f"Backtest {backtest_id} not found")

            # Update status to RUNNING
            await self.prisma.backtestrun.update(
                where={"id": backtest_id}, data={"status": "RUNNING"}
            )

            # Simulate backtest execution
            # In production, this would:
            # 1. Download historical data
            # 2. Initialize strategy with parameters
            # 3. Run strategy on historical data
            # 4. Calculate performance metrics

            # For now, generate mock results
            results = self._generate_mock_backtest_results(
                backtest.initialCapital, backtest.symbol
            )

            # Update backtest with results
            await self.prisma.backtestrun.update(
                where={"id": backtest_id},
                data={
                    "status": "COMPLETED",
                    "results": json.dumps(results),
                    "completedAt": datetime.utcnow(),
                },
            )

            return {
                "backtest_id": backtest_id,
                "status": "COMPLETED",
                "results": results,
            }
        except Exception as e:
            # Update status to FAILED
            await self.prisma.backtestrun.update(
                where={"id": backtest_id},
                data={"status": "FAILED", "results": json.dumps({"error": str(e)})},
            )
            raise
        finally:
            await self.prisma.disconnect()

    def _generate_mock_backtest_results(
        self, initial_capital: float, symbol: str
    ) -> Dict[str, Any]:
        """Generate mock backtest results for demonstration"""
        # Simulate some trades
        num_trades = np.random.randint(50, 200)
        win_rate = np.random.uniform(0.45, 0.65)

        winning_trades = int(num_trades * win_rate)
        losing_trades = num_trades - winning_trades

        # Calculate final capital (simple simulation)
        avg_win = initial_capital * 0.02  # 2% avg win
        avg_loss = initial_capital * 0.015  # 1.5% avg loss

        total_profit = (winning_trades * avg_win) - (losing_trades * avg_loss)
        final_capital = initial_capital + total_profit

        total_return = ((final_capital - initial_capital) / initial_capital) * 100

        # Calculate max drawdown (mock)
        max_drawdown = np.random.uniform(5, 25)

        # Calculate Sharpe ratio (mock)
        sharpe_ratio = np.random.uniform(0.5, 2.5)

        # Profit factor
        gross_profit = winning_trades * avg_win
        gross_loss = losing_trades * avg_loss
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        return {
            "initial_capital": initial_capital,
            "final_capital": round(final_capital, 2),
            "total_return": round(total_return, 2),
            "total_trades": num_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate * 100, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "profit_factor": round(profit_factor, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
        }

    async def get_backtest_results(self, backtest_id: int) -> Dict[str, Any]:
        """Get backtest results"""
        await self.prisma.connect()

        try:
            backtest = await self.prisma.backtestrun.find_first(
                where={"id": backtest_id}
            )

            if not backtest:
                raise ValueError(f"Backtest {backtest_id} not found")

            results = json.loads(backtest.results) if backtest.results else {}

            return {
                "backtest_id": backtest.id,
                "strategy_name": backtest.strategyName,
                "symbol": backtest.symbol,
                "timeframe": backtest.timeframe,
                "start_date": backtest.startDate.isoformat(),
                "end_date": backtest.endDate.isoformat(),
                "status": backtest.status,
                "created_at": backtest.createdAt.isoformat(),
                "completed_at": (
                    backtest.completedAt.isoformat() if backtest.completedAt else None
                ),
                "results": results,
            }
        finally:
            await self.prisma.disconnect()

    async def list_user_backtests(
        self, user_id: int, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List all backtests for a user"""
        await self.prisma.connect()

        try:
            backtests = await self.prisma.backtestrun.find_many(
                where={"userId": user_id}, order={"createdAt": "desc"}, take=limit
            )

            return [
                {
                    "backtest_id": bt.id,
                    "strategy_name": bt.strategyName,
                    "symbol": bt.symbol,
                    "timeframe": bt.timeframe,
                    "status": bt.status,
                    "created_at": bt.createdAt.isoformat(),
                }
                for bt in backtests
            ]
        finally:
            await self.prisma.disconnect()

    async def delete_backtest(self, backtest_id: int, user_id: int) -> Dict[str, Any]:
        """Delete a backtest"""
        await self.prisma.connect()

        try:
            # Verify backtest belongs to user
            backtest = await self.prisma.backtestrun.find_first(
                where={"id": backtest_id, "userId": user_id}
            )

            if not backtest:
                raise ValueError("Backtest not found or does not belong to user")

            await self.prisma.backtestrun.delete(where={"id": backtest_id})

            return {"success": True, "backtest_id": backtest_id}
        finally:
            await self.prisma.disconnect()

    # Paper Trading Methods

    async def start_paper_trading(
        self,
        user_id: int,
        strategy_name: str,
        symbol: str,
        timeframe: str,
        virtual_balance: float = 10000.0,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Start a paper trading session"""
        await self.prisma.connect()

        try:
            session = await self.prisma.papertradingsession.create(
                data={
                    "userId": user_id,
                    "strategyName": strategy_name,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "virtualBalance": virtual_balance,
                    "currentBalance": virtual_balance,
                    "status": "ACTIVE",
                }
            )

            return {
                "session_id": session.id,
                "strategy_name": strategy_name,
                "symbol": symbol,
                "virtual_balance": virtual_balance,
                "status": session.status,
                "started_at": session.startedAt.isoformat(),
            }
        finally:
            await self.prisma.disconnect()

    async def stop_paper_trading(self, session_id: int, user_id: int) -> Dict[str, Any]:
        """Stop a paper trading session"""
        await self.prisma.connect()

        try:
            # Verify session belongs to user
            session = await self.prisma.papertradingsession.find_first(
                where={"id": session_id, "userId": user_id}
            )

            if not session:
                raise ValueError(
                    "Paper trading session not found or does not belong to user"
                )

            # Update session
            updated_session = await self.prisma.papertradingsession.update(
                where={"id": session_id},
                data={"status": "STOPPED", "stoppedAt": datetime.utcnow()},
            )

            # Calculate final stats
            pnl = (
                updated_session.currentBalance or updated_session.virtualBalance
            ) - updated_session.virtualBalance
            return_pct = (pnl / updated_session.virtualBalance) * 100

            return {
                "session_id": session_id,
                "status": "STOPPED",
                "initial_balance": updated_session.virtualBalance,
                "final_balance": updated_session.currentBalance
                or updated_session.virtualBalance,
                "pnl": round(pnl, 2),
                "return_pct": round(return_pct, 2),
                "stopped_at": (
                    updated_session.stoppedAt.isoformat()
                    if updated_session.stoppedAt
                    else None
                ),
            }
        finally:
            await self.prisma.disconnect()

    async def get_paper_trading_status(self, session_id: int) -> Dict[str, Any]:
        """Get status of a paper trading session"""
        await self.prisma.connect()

        try:
            session = await self.prisma.papertradingsession.find_first(
                where={"id": session_id}
            )

            if not session:
                raise ValueError(f"Paper trading session {session_id} not found")

            pnl = (
                session.currentBalance or session.virtualBalance
            ) - session.virtualBalance
            return_pct = (pnl / session.virtualBalance) * 100

            return {
                "session_id": session.id,
                "strategy_name": session.strategyName,
                "symbol": session.symbol,
                "timeframe": session.timeframe,
                "status": session.status,
                "initial_balance": session.virtualBalance,
                "current_balance": session.currentBalance or session.virtualBalance,
                "pnl": round(pnl, 2),
                "return_pct": round(return_pct, 2),
                "started_at": session.startedAt.isoformat(),
                "stopped_at": (
                    session.stoppedAt.isoformat() if session.stoppedAt else None
                ),
            }
        finally:
            await self.prisma.disconnect()

    async def list_paper_trading_sessions(
        self, user_id: int, active_only: bool = False
    ) -> List[Dict[str, Any]]:
        """List paper trading sessions for a user"""
        await self.prisma.connect()

        try:
            where_clause = {"userId": user_id}
            if active_only:
                where_clause["status"] = "ACTIVE"

            sessions = await self.prisma.papertradingsession.find_many(
                where=where_clause, order={"startedAt": "desc"}
            )

            return [
                {
                    "session_id": s.id,
                    "strategy_name": s.strategyName,
                    "symbol": s.symbol,
                    "status": s.status,
                    "virtual_balance": s.virtualBalance,
                    "current_balance": s.currentBalance or s.virtualBalance,
                    "started_at": s.startedAt.isoformat(),
                }
                for s in sessions
            ]
        finally:
            await self.prisma.disconnect()
