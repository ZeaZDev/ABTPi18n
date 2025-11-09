# Phase 6 Quick Start Guide

## Overview
Phase 6 adds ML/Intelligence features to ABTPro. This quick start shows you how to use them.

## Quick Start

### 1. Signal Quality Scoring

Score a trading signal before execution:

```bash
curl -X POST http://localhost:8000/ml/signal/score \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "strategy": "RSI_CROSS",
    "signal": {
      "type": "BUY",
      "price": 45000,
      "indicators": {
        "rsi": 35,
        "volume": 1250000,
        "trend": "BULLISH"
      }
    }
  }'
```

**Response:**
```json
{
  "score": 0.82,
  "confidence": 0.91,
  "recommendation": "EXECUTE",
  "risk": "LOW"
}
```

**Interpretation:**
- Score > 0.7: Execute trade
- Score 0.5-0.7: Proceed with caution
- Score < 0.5: Skip trade

### 2. Volatility Prediction

Predict future volatility for risk management:

```bash
curl -X POST http://localhost:8000/ml/volatility/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "horizon": 24
  }'
```

**Response:**
```json
{
  "predicted": 0.028,
  "confidence": 0.85,
  "range": {"low": 0.024, "high": 0.032},
  "regime": "INCREASING_VOLATILITY",
  "risk": "MODERATE"
}
```

**Use Cases:**
- Adjust position size based on volatility
- Set dynamic stop-loss levels
- Choose strategies based on volatility regime

### 3. Strategy Parameter Optimization

Optimize your strategy parameters using RL:

```bash
curl -X POST http://localhost:8000/ml/tune/start \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "strategy": "RSI_CROSS",
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "optimizationGoal": "SHARPE_RATIO",
    "parameters": {
      "rsiPeriod": {"min": 10, "max": 20, "current": 14},
      "oversoldThreshold": {"min": 20, "max": 35, "current": 30},
      "overboughtThreshold": {"min": 65, "max": 80, "current": 70}
    },
    "maxIterations": 1000
  }'
```

**Response:**
```json
{
  "jobId": "tune_abc123",
  "status": "STARTED",
  "estimatedTime": "15-20 minutes"
}
```

Check status:
```bash
curl http://localhost:8000/ml/tune/status/tune_abc123
```

Get results:
```bash
curl http://localhost:8000/ml/tune/results/tune_abc123
```

## Integration with Trading

### Enable ML in Your Strategy

```python
# In your bot configuration
{
  "strategy": "RSI_CROSS",
  "mlEnhancements": {
    "signalQualityFilter": true,
    "minScore": 0.6,
    "useVolatilityPrediction": true,
    "dynamicStopLoss": true
  }
}
```

### ML-Enhanced Trading Flow

1. **Generate Signal**: Your strategy generates a trading signal
2. **Score Signal**: ML evaluates signal quality (score 0-1)
3. **Filter**: Only execute if score > threshold (e.g., 0.6)
4. **Predict Volatility**: Get volatility forecast
5. **Adjust Size**: Modify position size based on volatility
6. **Execute**: Trade with ML-optimized parameters

## Available Endpoints

### Signal Quality
- `POST /ml/signal/score` - Score a signal
- `GET /ml/signal/history` - View scoring history
- `GET /ml/signal/stats` - Get statistics

### Volatility
- `POST /ml/volatility/predict` - Predict volatility
- `GET /ml/volatility/history` - View predictions
- `GET /ml/volatility/accuracy` - Check accuracy

### Strategy Tuning
- `POST /ml/tune/start` - Start optimization
- `GET /ml/tune/status/{jobId}` - Check progress
- `GET /ml/tune/results/{jobId}` - Get results
- `POST /ml/tune/apply` - Apply optimized params

### Models
- `GET /ml/models/list` - List models
- `POST /ml/models/train` - Train new model
- `GET /ml/models/performance` - View metrics

## Best Practices

### Signal Scoring
1. **Start Conservative**: Use minScore=0.7 initially
2. **Monitor Performance**: Track score vs. actual outcomes
3. **Adjust Threshold**: Lower threshold if missing good trades
4. **Review Rejections**: Periodically check rejected signals

### Volatility Prediction
1. **Short Horizons**: More accurate for 1-6 hour predictions
2. **Combine Indicators**: Use with other risk metrics
3. **Update Frequently**: Predictions improve with fresh data
4. **Respect Regimes**: Different strategies for different regimes

### Parameter Optimization
1. **Use Historical Data**: Minimum 6 months recommended
2. **Validate**: Always use out-of-sample validation
3. **Don't Overfit**: Avoid optimizing on too little data
4. **Re-optimize**: Run monthly or when performance degrades
5. **Test First**: Paper trade optimized params before live

## Troubleshooting

### Low Signal Scores
- Check if market conditions match training data
- Verify indicator calculations
- Consider retraining model with recent data

### Poor Predictions
- Use shorter prediction horizons
- Check for market regime changes
- Ensure sufficient historical data

### Slow Optimization
- Reduce max iterations
- Use smaller parameter search space
- Run during off-peak hours

## Next Steps

1. **Read Full Guide**: See [PHASE6_GUIDE.md](PHASE6_GUIDE.md)
2. **Review Examples**: Check [PHASE6_IMPLEMENTATION_SUMMARY.md](PHASE6_IMPLEMENTATION_SUMMARY.md)
3. **Understand Architecture**: Read [PHASE6_SUMMARY.md](PHASE6_SUMMARY.md)

## Support

For questions or issues:
- Review documentation in `/docs`
- Check application logs
- Contact support team

---

**Version**: 1.0.0  
**Last Updated**: November 9, 2025
