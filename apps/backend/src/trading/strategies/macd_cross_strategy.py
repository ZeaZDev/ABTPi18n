"""// ZeaZDev [Backend Trading Strategies Package Init] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

# Import all strategies to register them
from .rsi_cross_strategy import RSICrossStrategy
from .mean_reversion_strategy import MeanReversionStrategy
from .breakout_strategy import BreakoutStrategy
from .vwap_strategy import VWAPStrategy
from .macd_cross_strategy import MACDCrossStrategy  # <-- ADD THIS LINE

__all__ = [
    "RSICrossStrategy",
    "MeanReversionStrategy", 
    "BreakoutStrategy",
    "VWAPStrategy",
    "MACDCrossStrategy"  # <-- ADD THIS LINE
]