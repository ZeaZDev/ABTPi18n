# STRATEGY DEVELOPMENT GUIDE

## 1. Interface
กลยุทธ์ต้องสืบทอดจาก `Strategy` และกำหนด:
- name (string ไม่ซ้ำ)
- execute(ticker_data, context) -> dict

ตัวอย่างโครงสร้างใน `rsi_cross_strategy.py`:
```python
class RSICrossStrategy(Strategy):
    name = "RSI_CROSS"
    def execute(self, ticker_data, context):
        ...
```

## 2. การลงทะเบียน
หลังประกาศคลาส เรียก:
```python
StrategyRegistry.register(RSICrossStrategy)
```

## กลยุทธ์ในเฟส 2 (Cross-Reference)
เฟส 2 ได้เพิ่มกลยุทธ์ใหม่ 3 แบบ:
- **Mean Reversion Strategy** (`MEAN_REVERSION`) - ใช้แนวคิด Bollinger Bands ตรวจหาสถานะ overbought/oversold
- **Breakout Strategy** (`BREAKOUT`) - ตรวจจับการทะลุราคาสูง/ต่ำพร้อมการยืนยันด้วย volume
- **VWAP Strategy** (`VWAP`) - กลยุทธ์ Volume Weighted Average Price

รายละเอียดเพิ่มเติมดูที่ [PHASE2_SUMMARY.md](PHASE2_SUMMARY.md)

## Enhanced Risk Manager
เฟส 2 ได้เพิ่ม `EnhancedRiskManager` ที่รวม:
- **Max Drawdown Tracker** - ติดตามและหยุดการเทรดเมื่อ drawdown เกินที่กำหนด
- **Circuit Breaker** - หยุดการเทรดหลังขาดทุนติดต่อกัน และจำกัดจำนวนเทรดต่อชั่วโมง

ดูวิธีการใช้งานและตั้งค่าได้ที่ [PHASE2_GUIDE.md](PHASE2_GUIDE.md)

## 3. การเข้าถึงข้อมูล
`ticker_data`: ประกอบด้วย OHLCV / closes / volumes (ตามการเตรียมใน BotRunner)
`context`: มี symbol, timeframe, bot metadata (ขยายได้)

## 4. ผลลัพธ์
ส่ง dict:
```python
{
  "signal": "BUY|SELL|HOLD",
  "confidence": 0.0-1.0,
  "meta": {}
}
```

## 5. แนวคิดการเพิ่ม
- Mean Reversion: ตรวจ Z-score บน rolling window
- Momentum: ตรวจ EMA Cross + Strength
- Breakout: ตรวจ Donchian Channel
- VWAP Strategy: เทียบราคาเทียบกับ VWAP

## 6. การทดสอบ
แนะนำสร้างโมดูล backtest (Phase 4)
- โหลด historical OHLCV
- สร้าง loop เรียก execute
- วัด Sharpe, Max Drawdown

## 7. Sandbox (Hardening)
- จำกัดเวลา execute < 500ms
- จำกัด Memory
- แยก Process (Multiprocessing) สำหรับ Third-party

## 8. Logging
อย่า log sensitive data
- Log: signal, symbol, timeframe, latency