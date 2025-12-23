"""// ZeaZDev [Backend Service Exchange Connector] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

from typing import Optional

import ccxt
from prisma import Prisma

from src.security.crypto_service import decrypt_data

prisma = Prisma()


class ExchangeConnector:
    @staticmethod
    async def for_exchange(exchange_name: str, owner_id: Optional[int] = None):
        where_clause = {"exchange": exchange_name}
        if owner_id:
            where_clause["ownerId"] = owner_id
        key = await prisma.exchangekey.find_first(where=where_clause)
        if not key:
            raise ValueError("No exchange key stored")
        api_key = decrypt_data(key.encrypted_key, key.iv_key)
        api_secret = decrypt_data(key.encrypted_secret, key.iv_secret)
        cls = getattr(ccxt, exchange_name)
        return cls({"apiKey": api_key, "secret": api_secret, "enableRateLimit": True})
