# Phase 6 User Guide: ML / Intelligence

## Overview
This guide explains how to use the machine learning and intelligence features introduced in Phase 6 of the ABTPro trading platform.

## Table of Contents
1. [Signal Quality Scoring](#signal-quality-scoring)
2. [Reinforcement Learning Strategy Tuning](#reinforcement-learning-strategy-tuning)
3. [Predictive Volatility Estimation](#predictive-volatility-estimation)
4. [Model Management](#model-management)

---

## Signal Quality Scoring

### What is Signal Quality Scoring?
The signal quality scoring system uses machine learning to evaluate trading signals before execution, helping filter out low-quality signals and prioritize high-probability trades.

### Scoring a Trading Signal

#### Score Signal Before Trading
```bash
POST /ml/signal/score
```

**Request:**
```json
{
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
}
```

**Response:**
```json
{
  "score": 0.82,
  "confidence": 0.91,
  "recommendation": "EXECUTE",
  "factors": {
    "historicalWinRate": 0.78,
    "marketCondition": 0.85,
    "riskRewardRatio": 0.80,
    "volumeAlignment": 0.88
  },
  "risk": "LOW"
}
```

#### Understanding Score Values
- **0.0 - 0.3**: Poor signal, avoid trading
- **0.3 - 0.5**: Below average, proceed with caution
- **0.5 - 0.7**: Average signal, acceptable
- **0.7 - 0.9**: Good signal, recommended
- **0.9 - 1.0**: Excellent signal, high priority

### View Signal Scoring History

```bash
GET /ml/signal/history?userId=1&limit=50
```

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "symbol": "BTC/USDT",
      "timeframe": "1h",
      "strategy": "RSI_CROSS",
      "score": 0.82,
      "signalType": "BUY",
      "executed": true,
      "outcome": "WIN",
      "createdAt": "2025-11-09T10:30:00Z"
    }
  ],
  "stats": {
    "averageScore": 0.72,
    "totalScored": 150,
    "executionRate": 0.68
  }
}
```

### Signal Scoring Statistics

```bash
GET /ml/signal/stats?userId=1&days=30
```

**Response:**
```json
{
  "period": "30 days",
  "totalSignals": 450,
  "averageScore": 0.68,
  "scoreDistribution": {
    "excellent": 45,
    "good": 120,
    "average": 180,
    "poor": 105
  },
  "performanceByScore": {
    "0.0-0.3": {"winRate": 0.35, "count": 105},
    "0.3-0.5": {"winRate": 0.48, "count": 180},
    "0.5-0.7": {"winRate": 0.62, "count": 120},
    "0.7-1.0": {"winRate": 0.78, "count": 45}
  }
}
```

### Integrating with Trading Strategies

Signal quality scoring can be automatically integrated with your strategies:

**Enable in Bot Configuration:**
```json
{
  "strategy": "RSI_CROSS",
  "mlEnhancements": {
    "signalQualityFilter": true,
    "minScore": 0.6,
    "confidenceThreshold": 0.7
  }
}
```

When enabled:
- All signals are scored before execution
- Only signals above `minScore` are executed
- Confidence must exceed `confidenceThreshold`
- Rejected signals are logged for analysis

---

## Reinforcement Learning Strategy Tuning

### What is RL Strategy Tuning?
Automated optimization of strategy parameters using reinforcement learning to maximize returns and minimize risk.

### Start Parameter Optimization

```bash
POST /ml/tune/start
```

**Request:**
```json
{
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
  "trainingPeriod": {
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-10-31T23:59:59Z"
  },
  "validationSplit": 0.2,
  "maxIterations": 1000
}
```

**Response:**
```json
{
  "jobId": "tune_abc123",
  "status": "STARTED",
  "estimatedTime": "15-20 minutes",
  "message": "Optimization job started successfully"
}
```

### Check Tuning Status

```bash
GET /ml/tune/status/tune_abc123
```

**Response:**
```json
{
  "jobId": "tune_abc123",
  "status": "RUNNING",
  "progress": 0.65,
  "currentIteration": 650,
  "totalIterations": 1000,
  "bestPerformance": {
    "sharpeRatio": 1.85,
    "totalReturn": 0.42,
    "maxDrawdown": 0.15
  },
  "estimatedTimeRemaining": "5 minutes"
}
```

### Get Optimization Results

```bash
GET /ml/tune/results/tune_abc123
```

**Response:**
```json
{
  "jobId": "tune_abc123",
  "status": "COMPLETED",
  "originalParams": {
    "rsiPeriod": 14,
    "oversoldThreshold": 30,
    "overboughtThreshold": 70
  },
  "optimizedParams": {
    "rsiPeriod": 16,
    "oversoldThreshold": 28,
    "overboughtThreshold": 72
  },
  "performance": {
    "before": {
      "sharpeRatio": 1.45,
      "totalReturn": 0.32,
      "maxDrawdown": 0.22,
      "winRate": 0.58
    },
    "after": {
      "sharpeRatio": 1.85,
      "totalReturn": 0.42,
      "maxDrawdown": 0.15,
      "winRate": 0.64
    },
    "improvement": {
      "sharpeRatio": "+27.6%",
      "totalReturn": "+31.3%",
      "maxDrawdown": "-31.8%",
      "winRate": "+10.3%"
    }
  },
  "convergence": {
    "iterations": 872,
    "converged": true,
    "stability": 0.94
  }
}
```

### Apply Optimized Parameters

```bash
POST /ml/tune/apply
```

**Request:**
```json
{
  "jobId": "tune_abc123",
  "userId": 1,
  "strategy": "RSI_CROSS",
  "confirm": true
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Optimized parameters applied to RSI_CROSS strategy",
  "parameters": {
    "rsiPeriod": 16,
    "oversoldThreshold": 28,
    "overboughtThreshold": 72
  },
  "appliedAt": "2025-11-09T11:15:00Z"
}
```

### Optimization Best Practices

1. **Training Period**: Use at least 6 months of historical data
2. **Validation Split**: Keep 20% for validation to prevent overfitting
3. **Goal Selection**: Choose appropriate optimization goal:
   - `SHARPE_RATIO`: Best risk-adjusted returns
   - `TOTAL_RETURN`: Maximum profit (may increase risk)
   - `MAX_DRAWDOWN`: Minimize losses (may reduce returns)
   - `WIN_RATE`: Maximize winning trades
4. **Regular Retuning**: Re-optimize monthly or when performance degrades
5. **Market Conditions**: Consider different optimizations for bull/bear markets

---

## Predictive Volatility Estimation

### What is Volatility Prediction?
Machine learning-based forecasting of future market volatility to enable better risk management and position sizing.

### Predict Future Volatility

```bash
POST /ml/volatility/predict
```

**Request:**
```json
{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "horizon": 24,
  "includeFeatures": true
}
```

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "currentVolatility": 0.025,
  "predictions": [
    {
      "horizon": 1,
      "predicted": 0.028,
      "confidence": 0.92,
      "range": {"low": 0.024, "high": 0.032}
    },
    {
      "horizon": 6,
      "predicted": 0.032,
      "confidence": 0.85,
      "range": {"low": 0.027, "high": 0.037}
    },
    {
      "horizon": 24,
      "predicted": 0.035,
      "confidence": 0.78,
      "range": {"low": 0.028, "high": 0.042}
    }
  ],
  "regime": "INCREASING_VOLATILITY",
  "risk": "MODERATE"
}
```

### Volatility Prediction History

```bash
GET /ml/volatility/history?symbol=BTC/USDT&days=7
```

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "predictions": [
    {
      "predictedAt": "2025-11-09T10:00:00Z",
      "predicted": 0.028,
      "actual": 0.027,
      "error": 0.001,
      "horizon": 24
    }
  ],
  "averageError": 0.0015,
  "accuracy": 0.94
}
```

### Prediction Accuracy Metrics

```bash
GET /ml/volatility/accuracy?symbol=BTC/USDT&period=30d
```

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "period": "30 days",
  "metrics": {
    "mae": 0.0018,
    "rmse": 0.0024,
    "directionalAccuracy": 0.78,
    "coverage": 0.92
  },
  "byHorizon": {
    "1h": {"mae": 0.0008, "accuracy": 0.94},
    "6h": {"mae": 0.0015, "accuracy": 0.85},
    "24h": {"mae": 0.0024, "accuracy": 0.78}
  }
}
```

### Using Volatility Predictions

#### Dynamic Position Sizing
```python
# Get volatility prediction
volatility = await volatility_predictor.predict(symbol="BTC/USDT", horizon=24)

# Adjust position size inversely to volatility
base_size = 1000  # USD
volatility_adjusted_size = base_size * (0.02 / volatility.predicted)
```

#### Adaptive Stop-Loss
```python
# Set stop-loss based on predicted volatility
predicted_vol = volatility.predicted
stop_loss_pct = predicted_vol * 2  # 2x predicted volatility
```

#### Risk-Adjusted Strategy Selection
```python
# Choose strategy based on volatility regime
if volatility.regime == "LOW_VOLATILITY":
    strategy = "BREAKOUT"  # Works better in low vol
elif volatility.regime == "HIGH_VOLATILITY":
    strategy = "MEAN_REVERSION"  # Better in high vol
```

---

## Model Management

### List Available Models

```bash
GET /ml/models/list
```

**Response:**
```json
{
  "models": [
    {
      "id": "signal_quality_v1",
      "type": "SIGNAL_QUALITY",
      "version": "1.0.0",
      "status": "ACTIVE",
      "accuracy": 0.78,
      "trainedAt": "2025-11-01T00:00:00Z",
      "samples": 50000
    },
    {
      "id": "volatility_pred_v2",
      "type": "VOLATILITY",
      "version": "2.1.0",
      "status": "ACTIVE",
      "mae": 0.0018,
      "trainedAt": "2025-11-05T00:00:00Z",
      "samples": 100000
    }
  ]
}
```

### Train New Model

```bash
POST /ml/models/train
```

**Request:**
```json
{
  "modelType": "SIGNAL_QUALITY",
  "version": "1.1.0",
  "trainingData": {
    "startDate": "2024-01-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "symbols": ["BTC/USDT", "ETH/USDT"],
    "strategies": ["RSI_CROSS", "BREAKOUT"]
  },
  "hyperparameters": {
    "learningRate": 0.001,
    "epochs": 100,
    "batchSize": 32
  }
}
```

**Response:**
```json
{
  "trainingJobId": "train_xyz789",
  "status": "STARTED",
  "estimatedTime": "30-45 minutes"
}
```

### Model Performance Metrics

```bash
GET /ml/models/performance?modelId=signal_quality_v1
```

**Response:**
```json
{
  "modelId": "signal_quality_v1",
  "type": "SIGNAL_QUALITY",
  "performance": {
    "accuracy": 0.78,
    "precision": 0.82,
    "recall": 0.75,
    "f1Score": 0.78,
    "auc": 0.86
  },
  "confusionMatrix": {
    "truePositive": 3750,
    "trueNegative": 4200,
    "falsePositive": 900,
    "falseNegative": 1150
  },
  "calibration": {
    "brier": 0.15,
    "logLoss": 0.48
  }
}
```

---

## Configuration & Settings

### Global ML Settings

Update ML configuration in your user preferences:

```bash
PUT /user/preferences
```

**Request:**
```json
{
  "mlSettings": {
    "enableSignalScoring": true,
    "minSignalScore": 0.6,
    "enableAutoTuning": false,
    "tuningFrequency": "WEEKLY",
    "enableVolatilityPrediction": true,
    "positionSizingMode": "VOLATILITY_ADJUSTED"
  }
}
```

### Per-Strategy ML Configuration

```json
{
  "strategy": "RSI_CROSS",
  "config": {
    "ml": {
      "scoreSignals": true,
      "minScore": 0.65,
      "useVolatilityPrediction": true,
      "dynamicStopLoss": true,
      "autoTune": {
        "enabled": false,
        "frequency": "MONTHLY"
      }
    }
  }
}
```

---

## Monitoring & Alerts

### ML Performance Monitoring

The platform automatically monitors ML model performance:

- **Signal Score Accuracy**: Tracked against actual trade outcomes
- **Volatility Prediction Error**: Compared to realized volatility
- **RL Tuning Stability**: Monitor parameter convergence

### Alerts

Configure alerts for ML events:

```json
{
  "alerts": {
    "signalScoreAccuracyDrop": {
      "enabled": true,
      "threshold": 0.65,
      "notification": "TELEGRAM"
    },
    "volatilityPredictionError": {
      "enabled": true,
      "threshold": 0.05,
      "notification": "EMAIL"
    },
    "tuningCompleted": {
      "enabled": true,
      "notification": "TELEGRAM"
    }
  }
}
```

---

## Troubleshooting

### Low Signal Scores

**Problem**: Most signals scoring below 0.5

**Solutions**:
1. Review strategy parameters
2. Check market conditions
3. Verify indicator calculations
4. Consider retraining model with recent data

### Poor Volatility Predictions

**Problem**: High prediction errors

**Solutions**:
1. Check for market regime changes
2. Retrain model with recent data
3. Verify input features
4. Consider shorter prediction horizons

### Slow RL Tuning

**Problem**: Optimization taking too long

**Solutions**:
1. Reduce parameter search space
2. Decrease max iterations
3. Use shorter training period
4. Run during off-peak hours

### Model Training Failures

**Problem**: Model training not completing

**Solutions**:
1. Check data availability
2. Verify hyperparameters
3. Review training logs
4. Ensure sufficient compute resources

---

## Best Practices

### Signal Quality Scoring
1. Use scores as guidance, not absolute rules
2. Combine with your trading experience
3. Adjust thresholds based on strategy type
4. Review rejected signals periodically
5. Monitor score accuracy over time

### RL Strategy Tuning
1. Start with default parameters
2. Optimize one strategy at a time
3. Validate on out-of-sample data
4. Don't over-optimize (avoid overfitting)
5. Re-tune regularly (monthly/quarterly)

### Volatility Prediction
1. Use shorter horizons for better accuracy
2. Combine with other risk indicators
3. Update predictions frequently
4. Consider market regime
5. Validate predictions against realized volatility

### General ML Usage
1. Understand model limitations
2. Don't rely solely on ML predictions
3. Monitor model performance
4. Retrain models periodically
5. Keep training data up to date

---

## Support

For issues or questions about Phase 6 ML features:
1. Check model performance metrics
2. Review prediction accuracy
3. Consult PHASE6_SUMMARY.md for technical details
4. Contact support team for assistance

## Additional Resources

- [PHASE6_SUMMARY.md](PHASE6_SUMMARY.md) - Technical specifications
- [PHASE6_IMPLEMENTATION_SUMMARY.md](PHASE6_IMPLEMENTATION_SUMMARY.md) - Implementation details
- [ROADMAP.md](ROADMAP.md) - Platform roadmap
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Stable-Baselines3 Documentation](https://stable-baselines3.readthedocs.io/)
