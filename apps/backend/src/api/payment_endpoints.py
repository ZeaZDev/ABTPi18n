"""// ZeaZDev [Payment API Endpoints] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 4) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
from src.services.promptpay_service import PromptPayService

router = APIRouter()
promptpay_service = PromptPayService()


class TopupRequest(BaseModel):
    amount: float
    currency: str = "THB"
    description: str = "Account Top-up"


class WebhookPayload(BaseModel):
    reference_id: str
    status: str
    metadata: Optional[dict] = None


@router.post("/promptpay/create")
async def create_promptpay_payment(
    request: TopupRequest,
    user_id: int = 1  # TODO: Get from auth token
):
    """Generate PromptPay QR code for payment"""
    try:
        result = await promptpay_service.create_payment_intent(
            user_id=user_id,
            amount=request.amount,
            currency=request.currency,
            description=request.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/promptpay")
async def promptpay_webhook(
    payload: WebhookPayload,
    x_webhook_signature: Optional[str] = Header(None)
):
    """Handle PromptPay payment webhook callbacks"""
    try:
        # Verify webhook signature
        if x_webhook_signature:
            # In production, verify the signature
            # is_valid = promptpay_service.verify_webhook_signature(...)
            pass
        
        result = await promptpay_service.process_payment_callback(
            reference_id=payload.reference_id,
            status=payload.status,
            metadata=payload.metadata
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wallet")
async def get_wallet_balance(
    user_id: int = 1  # TODO: Get from auth token
):
    """Get user wallet balance"""
    try:
        balance = await promptpay_service.get_wallet_balance(user_id)
        return balance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions")
async def get_transaction_history(
    user_id: int = 1,  # TODO: Get from auth token
    limit: int = 50,
    offset: int = 0
):
    """Get transaction history"""
    try:
        transactions = await promptpay_service.get_transaction_history(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        return {"transactions": transactions, "count": len(transactions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
