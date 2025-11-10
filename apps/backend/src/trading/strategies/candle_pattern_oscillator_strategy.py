"""// ZeaZDev [Backend Strategy Candle Pattern Oscillator] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 6 Integration) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
from typing import Dict, Any
import pandas as pd
import pandas_ta as ta
import numpy as np
from src.trading.strategy_interface import Strategy, StrategyRegistry

class CandlePatternOscillatorStrategy(Strategy):
    name = "CANDLE_PATTERN_OSCILLATOR"

    def __init__(
        self, 
        oscillator_type: str = "RSI",  # "RSI", "MFI", "CCI", "STOCH"
        pattern_avg_period: int = 12,
        osc_period: int = 37,
        stoch_k: int = 47,
        stoch_d: int = 9,
        stoch_slow: int = 13,
        buy_confirm_level: float = 40.0,
        sell_confirm_level: float = 60.0
    ):
        """
        Combines "Three White Soldiers / Three Black Crows" patterns with
        an oscillator confirmation (RSI, MFI, CCI, or Stochastic).
        Based on MQL5 EAs (BlackCrows WhiteSoldiers).
        
        Args:
            oscillator_type: Confirmation oscillator ("RSI", "MFI", "CCI", "STOCH")
            pattern_avg_period: Period to calculate average candle body size [cite: 78]
            osc_period: Period for the main oscillator [cite: 78, 255, 645]
            stoch_k: Stochastic %K period [cite: 499]
            stoch_d: Stochastic %D period [cite: 500]
            stoch_slow: Stochastic slowing period [cite: 501]
            buy_confirm_level: Oscillator level to confirm BUY (e.g., < 40) [cite: 205, 382, 630, 772]
            sell_confirm_level: Oscillator level to confirm SELL (e.g., > 60) [cite: 206, 383, 631, 773]
        """
        self.osc_type = oscillator_type.upper()
        self.pattern_avg_period = pattern_avg_period
        self.osc_period = osc_period
        self.stoch_k = stoch_k
        self.stoch_d = stoch_d
        self.stoch_slow = stoch_slow
        self.buy_level = buy_confirm_level
        self.sell_level = sell_confirm_level
        self.last_signal = "HOLD"

    def execute(self, ticker_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute strategy logic
        """
        # We need OHLCV data
        opens = ticker_data.get("opens")
        highs = ticker_data.get("highs")
        lows = ticker_data.get("lows")
        closes = ticker_data.get("closes")
        volumes = ticker_data.get("volumes")
        
        min_data_len = max(self.pattern_avg_period, self.osc_period, self.stoch_k) + 10

        if not all([opens, highs, lows, closes, volumes]) or len(closes) < min_data_len:
            return {"signal": "HOLD", "confidence": 0.0, "meta": {"reason": f"Insufficient data: need {min_data_len}, got {len(closes)}"}}

        try:
            df = pd.DataFrame({
                'open': pd.to_numeric(opens),
                'high': pd.to_numeric(highs),
                'low': pd.to_numeric(lows),
                'close': pd.to_numeric(closes),
                'volume': pd.to_numeric(volumes)
            })

            # 1. Calculate Average Body Size [cite: 194, 371, 619, 761]
            body_size = (df['open'] - df['close']).abs()
            avg_body = body_size.rolling(window=self.pattern_avg_period).mean()
            df['avg_body'] = avg_body

            # 2. Calculate Confirmation Oscillator
            osc_value = 0.0
            if self.osc_type == "RSI":
                df['oscillator'] = ta.rsi(df['close'], length=self.osc_period)
                osc_value = df['oscillator'].iloc[-2] # Check last completed bar [cite: 202]
            elif self.osc_type == "MFI":
                df['oscillator'] = ta.mfi(df['high'], df['low'], df['close'], df['volume'], length=self.osc_period)
                osc_value = df['oscillator'].iloc[-2] # Check last completed bar [cite: 379]
            elif self.osc_type == "CCI":
                df['oscillator'] = ta.cci(df['high'], df['low'], df['close'], length=self.osc_period)
                osc_value = df['oscillator'].iloc[-2] # Check last completed bar [cite: 769]
            elif self.osc_type == "STOCH":
                stoch = ta.stoch(df['high'], df['low'], df['close'], k=self.stoch_k, d=self.stoch_d, smooth_k=self.stoch_slow)
                df['oscillator'] = stoch[stoch.columns[1]] # Use Signal line (%D) [cite: 637]
                osc_value = df['oscillator'].iloc[-2] # Check last completed bar [cite: 627]
            else:
                return {"signal": "HOLD", "confidence": 0.0, "meta": {"reason": f"Invalid oscillator type: {self.osc_type}"}}
            
            if pd.isna(osc_value) or pd.isna(df['avg_body'].iloc[-2]):
                return {"signal": "HOLD", "confidence": 0.0, "meta": {"reason": "NaN value in calculations"}}

            # 3. Check for Patterns (uses last 3 *completed* bars)
            # MQL5(3) = iloc[-4], MQL5(2) = iloc[-3], MQL5(1) = iloc[-2]
            bar1, bar2, bar3 = df.iloc[-2], df.iloc[-3], df.iloc[-4]
            avg_body_check = df['avg_body'].iloc[-2] # AvgBody(1) in MQL5 [cite: 197]

            signal = "HOLD"
            reason = "No pattern detected"
            pattern = "None"

            # Check 3 White Soldiers 
            is_soldier_1 = (bar1['close'] - bar1['open']) > avg_body_check
            is_soldier_2 = (bar2['close'] - bar2['open']) > avg_body_check
            is_soldier_3 = (bar3['close'] - bar3['open']) > avg_body_check
            is_higher_mids = ((bar1['high'] + bar1['low']) / 2) > ((bar2['high'] + bar2['low']) / 2) > ((bar3['high'] + bar3['low']) / 2)

            if is_soldier_1 and is_soldier_2 and is_soldier_3 and is_higher_mids:
                pattern = "3_WHITE_SOLDIERS"
                # Check confirmation [cite: 204, 381, 629, 771]
                if osc_value < self.buy_level:
                    if self.last_signal != "BUY":
                        signal = "BUY"
                        reason = f"3 White Soldiers confirmed by {self.osc_type} < {self.buy_level} ({osc_value:.2f})"
                        self.last_signal = "BUY"
                    else:
                        reason = "3 White Soldiers confirmed, but already in BUY"
                else:
                    reason = f"3 White Soldiers detected, but {self.osc_type} ({osc_value:.2f}) not below {self.buy_level}"

            # Check 3 Black Crows 
            is_crow_1 = (bar1['open'] - bar1['close']) > avg_body_check
            is_crow_2 = (bar2['open'] - bar2['close']) > avg_body_check
            is_crow_3 = (bar3['open'] - bar3['close']) > avg_body_check
            is_lower_mids = ((bar1['high'] + bar1['low']) / 2) < ((bar2['high'] + bar2['low']) / 2) < ((bar3['high'] + bar3['low']) / 2)

            if is_crow_1 and is_crow_2 and is_crow_3 and is_lower_mids:
                pattern = "3_BLACK_CROWS"
                # Check confirmation [cite: 206, 383, 631, 773]
                if osc_value > self.sell_level:
                    if self.last_signal != "SELL":
                        signal = "SELL"
                        reason = f"3 Black Crows confirmed by {self.osc_type} > {self.sell_level} ({osc_value:.2f})"
                        self.last_signal = "SELL"
                    else:
                        reason = "3 Black Crows confirmed, but already in SELL"
                else:
                    reason = f"3 Black Crows detected, but {self.osc_type} ({osc_value:.2f}) not above {self.sell_level}"

            # 4. Confidence
            confidence = 0.5
            if signal != "HOLD":
                # Confidence based on how deep in the zone the oscillator is
                if signal == "BUY":
                    confidence = max(0.5, 1.0 - (osc_value / self.buy_level)) # e.g. 30/40 = 0.75 -> 1-0.75 = 0.25 -> 0.5
                elif signal == "SELL":
                    confidence = max(0.5, (osc_value - self.sell_level) / (100 - self.sell_level)) # e.g. (70-60)/(100-60) = 10/40 = 0.25 -> 0.5
            
            return {
                "signal": signal,
                "confidence": round(float(min(confidence, 1.0)), 3),
                "meta": {
                    "reason": reason,
                    "pattern": pattern,
                    "oscillator_type": self.osc_type,
                    "oscillator_value": round(float(osc_value), 2)
                }
            }

        except Exception as e:
            return {
                "signal": "HOLD",
                "confidence": 0.0,
                "meta": {"reason": f"Calculation error: {str(e)}"}
            }

# Register the strategy
StrategyRegistry.register(CandlePatternOscillatorStrategy)