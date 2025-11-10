"""// ZeaZDev [Backend Strategy MA Cross] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 6 Integration) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
from typing import Dict, Any
import pandas as pd
import numpy as np
from src.trading.strategy_interface import Strategy, StrategyRegistry

class MovingAverageCrossStrategy(Strategy):
    name = "MA_CROSS"

    def __init__(
        self, 
        ma_period: int = 12, 
        ma_shift: int = 6 
        # หมายเหตุ: MQL5 'shift' (6) [cite: 16] คือการเลื่อน indicator ไปข้างหน้า
        # ใน pandas การใช้ shift(6) จะเป็นการเลื่อนข้อมูลย้อนหลัง
        # การใช้งานจริงใน Python มักจะไม่ใช้ 'shift' หรือใช้เป็น 0
        # ในตัวอย่างนี้จะใช้ ma_shift = 0 เพื่อให้ตรงกับการใช้งานทั่วไป
    ):
        """
        Simple Moving Average (SMA) Price Crossover Strategy.
        Based on MQL5 ExpertMAMA / ExpertMAPSAR signal logic.
        
        Args:
            ma_period: Moving Average period (default: 12) [cite: 15, 88]
            ma_shift: Data shift (default: 0, MQL5 used 6) [cite: 16, 89]
        """
        self.ma_period = ma_period
        self.ma_shift = 0 # บังคับใช้ 0 เพื่อให้สอดคล้องกับการวิเคราะห์แบบ Real-time
        if ma_shift != 0:
            print(f"Warning: MA_CROSS Strategy loaded with MQL5 shift={ma_shift}, but overriding to 0 for Python implementation.")
            
        self.last_signal = "HOLD"

    def execute(self, ticker_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute MA Crossover strategy.
        
        Args:
            ticker_data: Dictionary containing 'closes'
            context: Dictionary with symbol, timeframe
            
        Returns:
            Dictionary with signal, confidence, and meta information
        """
        closes = ticker_data.get("closes")
        
        # 1. Data Validation
        if not closes or len(closes) < self.ma_period + 5:
            return {
                "signal": "HOLD",
                "confidence": 0.0,
                "meta": {
                    "reason": f"Insufficient data: need {self.ma_period + 5}, got {len(closes)}",
                    "ma_value": 0
                }
            }

        try:
            series = pd.Series(closes, dtype=float)

            # 2. Calculate Indicators
            sma = series.rolling(window=self.ma_period).mean()

            current_price = series.iloc[-1]
            prev_price = series.iloc[-2]
            current_sma = sma.iloc[-1]
            prev_sma = sma.iloc[-2]

            if pd.isna(current_sma) or pd.isna(prev_sma):
                 return {
                    "signal": "HOLD",
                    "confidence": 0.0,
                    "meta": {"reason": "Insufficient data for MA calculation (NaN)", "ma_value": 0}
                }

            # 3. Signal Generation
            signal = "HOLD"
            reason = "No crossover"

            # Bullish Crossover (Price crosses ABOVE MA)
            if prev_price < prev_sma and current_price >= current_sma and self.last_signal != "BUY":
                signal = "BUY"
                reason = f"Price crossed above SMA({self.ma_period})"
                self.last_signal = "BUY"
            
            # Bearish Crossover (Price crosses BELOW MA)
            elif prev_price > prev_sma and current_price <= current_sma and self.last_signal != "SELL":
                signal = "SELL"
                reason = f"Price crossed below SMA({self.ma_period})"
                self.last_signal = "SELL"
            
            # 4. Confidence Calculation
            # คำนวณความมั่นใจจากระยะห่างระหว่างราคาปัจจุบันกับเส้น SMA
            # (ยิ่งห่างมากหลังตัดกัน ยิ่งมั่นใจน้อยลงว่าเพิ่งตัด)
            price_std = series.iloc[-self.ma_period:].std()
            if price_std > 0:
                distance = abs(current_price - current_sma) / price_std
                confidence = max(0.5, 1.0 - (distance * 0.5)) # ลดความมั่นใจเมื่อราคาห่างจากเส้น MA
            else:
                confidence = 0.5
            
            if signal == "HOLD":
                confidence *= 0.3 # ลดความมั่นใจเมื่อ HOLD

            return {
                "signal": signal,
                "confidence": round(float(confidence), 3),
                "meta": {
                    "reason": reason,
                    "price": round(float(current_price), 4),
                    "ma_value": round(float(current_sma), 4),
                    "params": {
                        "period": self.ma_period,
                        "shift": self.ma_shift
                    }
                }
            }
        
        except Exception as e:
            return {
                "signal": "HOLD",
                "confidence": 0.0,
                "meta": {"reason": f"Calculation error: {str(e)}"}
            }

# Register the strategy
StrategyRegistry.register(MovingAverageCrossStrategy)