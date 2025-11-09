"""// ZeaZDev [Notification Service] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
from typing import Dict, Any, Optional
from prisma import Prisma
from .telegram_service import TelegramService

class NotificationService:
    """Service for sending notifications to users via various channels"""
    
    def __init__(self):
        self.telegram_service = TelegramService()
        self.prisma = Prisma()
    
    async def send_trade_notification(self, user_id: int, trade_data: Dict[str, Any]) -> bool:
        """Send trade execution notification"""
        await self.prisma.connect()
        
        # Check if user has enabled trade alerts
        prefs = await self.prisma.notificationpreference.find_first(
            where={"userId": user_id}
        )
        
        if not prefs or not prefs.tradeAlerts:
            await self.prisma.disconnect()
            return False
        
        # Get Telegram link
        telegram_link = await self.prisma.telegramlink.find_first(
            where={"userId": user_id}
        )
        
        await self.prisma.disconnect()
        
        if not telegram_link:
            return False
        
        # Format trade notification
        side = trade_data.get("side", "UNKNOWN")
        symbol = trade_data.get("symbol", "UNKNOWN")
        quantity = trade_data.get("quantity", 0)
        price = trade_data.get("price", 0)
        pnl = trade_data.get("pnl", 0)
        
        emoji = "🟢" if side == "BUY" else "🔴"
        message = f"""{emoji} Trade Executed

Symbol: {symbol}
Side: {side}
Quantity: {quantity}
Price: {price}
PnL: {pnl:.4f} USDT
"""
        
        return await self.telegram_service.send_message(telegram_link.chatId, message)
    
    async def send_risk_alert(self, user_id: int, alert_data: Dict[str, Any]) -> bool:
        """Send risk management alert"""
        await self.prisma.connect()
        
        # Check if user has enabled risk alerts
        prefs = await self.prisma.notificationpreference.find_first(
            where={"userId": user_id}
        )
        
        if not prefs or not prefs.riskAlerts:
            await self.prisma.disconnect()
            return False
        
        # Get Telegram link
        telegram_link = await self.prisma.telegramlink.find_first(
            where={"userId": user_id}
        )
        
        await self.prisma.disconnect()
        
        if not telegram_link:
            return False
        
        # Format risk alert
        alert_type = alert_data.get("type", "RISK_ALERT")
        message_text = alert_data.get("message", "Risk threshold exceeded")
        
        message = f"""⚠️ {alert_type}

{message_text}

Please review your trading strategy and risk settings.
"""
        
        return await self.telegram_service.send_message(telegram_link.chatId, message)
    
    async def send_system_notification(self, user_id: int, message_text: str) -> bool:
        """Send system notification"""
        await self.prisma.connect()
        
        # Check if user has enabled system alerts
        prefs = await self.prisma.notificationpreference.find_first(
            where={"userId": user_id}
        )
        
        if not prefs or not prefs.systemAlerts:
            await self.prisma.disconnect()
            return False
        
        # Get Telegram link
        telegram_link = await self.prisma.telegramlink.find_first(
            where={"userId": user_id}
        )
        
        await self.prisma.disconnect()
        
        if not telegram_link:
            return False
        
        message = f"""ℹ️ System Notification

{message_text}
"""
        
        return await self.telegram_service.send_message(telegram_link.chatId, message)
    
    async def send_daily_summary(self, user_id: int, summary_data: Dict[str, Any]) -> bool:
        """Send daily performance summary"""
        await self.prisma.connect()
        
        # Check if user has enabled daily summaries
        prefs = await self.prisma.notificationpreference.find_first(
            where={"userId": user_id}
        )
        
        if not prefs or not prefs.dailySummary:
            await self.prisma.disconnect()
            return False
        
        # Get Telegram link
        telegram_link = await self.prisma.telegramlink.find_first(
            where={"userId": user_id}
        )
        
        await self.prisma.disconnect()
        
        if not telegram_link:
            return False
        
        # Format daily summary
        total_pnl = summary_data.get("total_pnl", 0)
        trades_count = summary_data.get("trades_count", 0)
        win_rate = summary_data.get("win_rate", 0)
        
        pnl_emoji = "📈" if total_pnl >= 0 else "📉"
        message = f"""📊 Daily Summary

{pnl_emoji} Total PnL: {total_pnl:.4f} USDT
📝 Trades: {trades_count}
✅ Win Rate: {win_rate:.1f}%

Keep up the good work!
"""
        
        return await self.telegram_service.send_message(telegram_link.chatId, message)
