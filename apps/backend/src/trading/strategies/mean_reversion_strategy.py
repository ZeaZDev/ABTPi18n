"""// ZeaZDev [Backend Strategy Mean Reversion] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 2) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
from typing import Dict, Any
import pandas as pd
import numpy as np
from src.trading.strategy_interface import Strategy, StrategyRegistry

class MeanReversionStrategy(Strategy):
    name = "MEAN_REVERSION"

    def __init__(self, window: int = 20, std_dev_factor: float = 2.0):
        """
        Mean Reversion Strategy using Bollinger Bands concept.
        
        Args:
            window: Moving average window period
            std_dev_factor: Standard deviation multiplier for bands
        """
        self.window = window
        self.std_dev_factor = std_dev_factor
        self.last_signal = "HOLD"

    def execute(self, ticker_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        closes = ticker_data.get("closes")
        if not closes or len(closes) < self.window + 5:
            return {"signal": "HOLD", "reason": "Insufficient data"}

        series = pd.Series(closes)
        ma = series.rolling(window=self.window).mean()
        std = series.rolling(window=self.window).std()
        
        upper_band = ma + (std * self.std_dev_factor)
        lower_band = ma - (std * self.std_dev_factor)
        
        current_price = closes[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        current_ma = ma.iloc[-1]
        
        signal = "HOLD"
        # Price below lower band suggests oversold -> BUY
        if current_price < current_lower and self.last_signal != "BUY":
            signal = "BUY"
        # Price above upper band suggests overbought -> SELL
        elif current_price > current_upper and self.last_signal != "SELL":
            signal = "SELL"
        
        if signal != "HOLD":
            self.last_signal = signal
        
        # Confidence based on distance from mean relative to band width
        band_width = current_upper - current_lower
        distance_from_mean = abs(current_price - current_ma)
        confidence = min(distance_from_mean / (band_width / 2), 1.0) if band_width > 0 else 0.0
        
        return {
            "signal": signal,
            "current_price": round(float(current_price), 2),
            "moving_average": round(float(current_ma), 2),
            "upper_band": round(float(current_upper), 2),
            "lower_band": round(float(current_lower), 2),
            "confidence": round(float(confidence), 3),
            "meta": {
                "window": self.window,
                "std_dev_factor": self.std_dev_factor
            }
        }

StrategyRegistry.register(MeanReversionStrategy)
