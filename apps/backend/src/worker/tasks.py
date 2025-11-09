"""// ZeaZDev [Backend Celery Tasks] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 4) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
import asyncio
import os
from src.worker.celery_app import celery_app
from prisma import Prisma
from src.trading.bot_runner import BotRunner
from src.services.rental_service import RentalService
from src.services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)
prisma = Prisma()

@celery_app.task(bind=True, name="run_bot_loop")
def run_bot_loop(self, bot_id: int):
    asyncio.run(run_bot_async(bot_id))

async def run_bot_async(bot_id: int):
    await prisma.connect()
    runner = BotRunner(prisma=prisma, bot_id=bot_id)
    await runner.run_loop()
    await prisma.disconnect()


# Phase 4: Contract expiry checking task
@celery_app.task(bind=True, name="check_contract_expiry")
def check_contract_expiry(self):
    """Check for expiring or expired rental contracts"""
    asyncio.run(check_contract_expiry_async())

async def check_contract_expiry_async():
    """Async implementation of contract expiry checking"""
    rental_service = RentalService()
    notification_service = NotificationService()
    
    try:
        logger.info("Starting contract expiry check...")
        
        # Check all contracts
        contracts_to_check = await rental_service.check_contract_expiry()
        
        for contract in contracts_to_check:
            logger.info(f"Processing contract {contract['contract_id']} for user {contract['user_id']}")
            
            # Send renewal reminder if needed
            if contract['should_send_reminder']:
                days = contract['days_until_expiry']
                message = f"Your subscription expires in {days} day(s). Please renew to continue using the service."
                
                # Send notification (email/telegram)
                try:
                    # This would send via telegram/email in production
                    logger.info(f"Sending renewal reminder to user {contract['user_id']}: {message}")
                except Exception as e:
                    logger.error(f"Failed to send renewal reminder: {e}")
            
            # Disable contract if expired and past grace period
            if contract['should_disable']:
                logger.warning(f"Expiring contract {contract['contract_id']} for user {contract['user_id']}")
                await rental_service.expire_contract(contract['contract_id'])
                
                # Send expiry notification
                message = "Your subscription has expired. Your bots have been stopped. Please renew to continue."
                logger.info(f"Sending expiry notification to user {contract['user_id']}: {message}")
        
        logger.info(f"Contract expiry check completed. Processed {len(contracts_to_check)} contracts.")
        
    except Exception as e:
        logger.error(f"Error during contract expiry check: {e}")
        raise