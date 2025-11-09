"""// ZeaZDev [PromptPay Service] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 4) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

import os
import qrcode
import io
import base64
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib
import hmac
import json
from prisma import Prisma

class PromptPayService:
    """Service for handling PromptPay QR code generation and payment processing"""
    
    def __init__(self):
        self.merchant_id = os.getenv("PROMPTPAY_MERCHANT_ID", "")
        self.webhook_secret = os.getenv("PROMPTPAY_WEBHOOK_SECRET", "")
        self.prisma = Prisma()
    
    def generate_qr_code(self, amount: float, reference_id: str) -> str:
        """
        Generate PromptPay QR code for payment
        
        Args:
            amount: Payment amount in THB
            reference_id: Unique reference ID for this transaction
            
        Returns:
            Base64 encoded QR code image
        """
        # PromptPay QR format (simplified version)
        # In production, use proper EMVCo QR format
        payload = f"PROMPTPAY|{self.merchant_id}|{amount:.2f}|{reference_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    async def create_payment_intent(
        self, 
        user_id: int, 
        amount: float, 
        currency: str = "THB",
        description: str = "Account Top-up"
    ) -> Dict[str, Any]:
        """
        Create a payment intent and generate QR code
        
        Args:
            user_id: User ID making the payment
            amount: Payment amount
            currency: Payment currency (default: THB)
            description: Payment description
            
        Returns:
            Dict with QR code and transaction details
        """
        await self.prisma.connect()
        
        try:
            # Create transaction record
            transaction = await self.prisma.transaction.create(data={
                "userId": user_id,
                "type": "TOP_UP",
                "amount": amount,
                "currency": currency,
                "status": "PENDING",
                "paymentMethod": "PROMPTPAY",
                "metadata": json.dumps({"description": description})
            })
            
            reference_id = f"TXN-{transaction.id}-{int(datetime.utcnow().timestamp())}"
            
            # Update transaction with reference ID
            await self.prisma.transaction.update(
                where={"id": transaction.id},
                data={"referenceId": reference_id}
            )
            
            # Generate QR code
            qr_code_url = self.generate_qr_code(amount, reference_id)
            
            return {
                "transaction_id": transaction.id,
                "reference_id": reference_id,
                "amount": amount,
                "currency": currency,
                "qr_code_url": qr_code_url,
                "status": "PENDING",
                "created_at": transaction.createdAt.isoformat()
            }
        finally:
            await self.prisma.disconnect()
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature from payment gateway
        
        Args:
            payload: Webhook payload
            signature: Signature from payment gateway
            
        Returns:
            True if signature is valid, False otherwise
        """
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    async def process_payment_callback(
        self, 
        reference_id: str, 
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process payment callback from payment gateway
        
        Args:
            reference_id: Transaction reference ID
            status: Payment status (SUCCESS, FAILED, PENDING)
            metadata: Additional metadata from gateway
            
        Returns:
            Dict with processing result
        """
        await self.prisma.connect()
        
        try:
            # Find transaction
            transaction = await self.prisma.transaction.find_first(
                where={"referenceId": reference_id}
            )
            
            if not transaction:
                return {
                    "success": False,
                    "error": "Transaction not found"
                }
            
            # Update transaction status
            updated_transaction = await self.prisma.transaction.update(
                where={"id": transaction.id},
                data={
                    "status": status,
                    "completedAt": datetime.utcnow() if status == "SUCCESS" else None,
                    "metadata": json.dumps({
                        **json.loads(transaction.metadata or "{}"),
                        "callback_metadata": metadata or {}
                    })
                }
            )
            
            # If successful, credit user wallet
            if status == "SUCCESS":
                await self._credit_wallet(transaction.userId, transaction.amount)
            
            return {
                "success": True,
                "transaction_id": transaction.id,
                "status": status,
                "amount": transaction.amount
            }
        finally:
            await self.prisma.disconnect()
    
    async def _credit_wallet(self, user_id: int, amount: float):
        """Credit amount to user wallet"""
        # Check if wallet exists
        wallet = await self.prisma.wallet.find_first(
            where={"userId": user_id}
        )
        
        if not wallet:
            # Create wallet if it doesn't exist
            wallet = await self.prisma.wallet.create(data={
                "userId": user_id,
                "balance": amount,
                "currency": "THB"
            })
        else:
            # Update existing wallet
            await self.prisma.wallet.update(
                where={"id": wallet.id},
                data={"balance": wallet.balance + amount}
            )
    
    async def get_wallet_balance(self, user_id: int) -> Dict[str, Any]:
        """Get user wallet balance"""
        await self.prisma.connect()
        
        try:
            wallet = await self.prisma.wallet.find_first(
                where={"userId": user_id}
            )
            
            if not wallet:
                # Create wallet with zero balance
                wallet = await self.prisma.wallet.create(data={
                    "userId": user_id,
                    "balance": 0.0,
                    "currency": "THB"
                })
            
            return {
                "balance": wallet.balance,
                "currency": wallet.currency,
                "last_updated": wallet.updatedAt.isoformat()
            }
        finally:
            await self.prisma.disconnect()
    
    async def get_transaction_history(
        self, 
        user_id: int, 
        limit: int = 50,
        offset: int = 0
    ) -> list:
        """Get user transaction history"""
        await self.prisma.connect()
        
        try:
            transactions = await self.prisma.transaction.find_many(
                where={"userId": user_id},
                order={"createdAt": "desc"},
                take=limit,
                skip=offset
            )
            
            return [
                {
                    "id": txn.id,
                    "type": txn.type,
                    "amount": txn.amount,
                    "currency": txn.currency,
                    "status": txn.status,
                    "payment_method": txn.paymentMethod,
                    "reference_id": txn.referenceId,
                    "created_at": txn.createdAt.isoformat(),
                    "completed_at": txn.completedAt.isoformat() if txn.completedAt else None
                }
                for txn in transactions
            ]
        finally:
            await self.prisma.disconnect()
