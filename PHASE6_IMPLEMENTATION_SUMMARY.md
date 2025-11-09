# Phase 6 Implementation Summary: ML / Intelligence

## Overview
This document provides technical implementation details for Phase 6 ML/Intelligence features of the ABTPro trading platform.

## Implementation Date
November 9, 2025

## Technical Stack

### ML Libraries Added
```txt
# Core ML libraries
scikit-learn==1.3.2        # Traditional ML algorithms
numpy==1.26.4              # Already present
pandas==2.2.1              # Already present
scipy==1.11.4              # Scientific computing

# Optional advanced features (commented out for minimal install)
# tensorflow==2.15.0       # Deep learning (large dependency)
# stable-baselines3==2.2.1 # Reinforcement learning
# optuna==3.5.0            # Hyperparameter optimization
```

## Module Structure

### Directory Layout
```
apps/backend/src/ml/
├── __init__.py
├── signal_quality/
│   ├── __init__.py
│   ├── scorer.py
│   ├── feature_extractor.py
│   └── models.py
├── reinforcement/
│   ├── __init__.py
│   ├── tuner.py
│   ├── environment.py
│   └── agent.py
├── volatility/
│   ├── __init__.py
│   ├── predictor.py
│   ├── features.py
│   └── models.py
└── utils/
    ├── __init__.py
    ├── data_loader.py
    └── metrics.py
```

## Feature Implementations

### 1. Signal Quality Scoring

#### Architecture
The signal quality scorer uses a Random Forest classifier trained on historical signal outcomes.

**Input Features:**
- RSI value
- Volume ratio (current/average)
- Price momentum
- Volatility percentile
- Trend strength
- Time of day
- Recent win rate
- Risk/reward ratio

**Model Training:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class SignalQualityScorer:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def train(self, historical_signals, outcomes):
        features = self._extract_features(historical_signals)
        X_scaled = self.scaler.fit_transform(features)
        self.model.fit(X_scaled, outcomes)
```

**Scoring:**
```python
def score_signal(self, signal, market_data):
    features = self._extract_features([signal])
    X_scaled = self.scaler.transform(features)
    
    # Get probability of success
    proba = self.model.predict_proba(X_scaled)[0]
    
    return {
        'score': proba[1],  # Probability of winning trade
        'confidence': max(proba),
        'recommendation': 'EXECUTE' if proba[1] > 0.6 else 'SKIP'
    }
```

#### Feature Extraction

```python
class FeatureExtractor:
    def extract_signal_features(self, signal, market_data):
        return {
            'rsi': signal.indicators.get('rsi', 50),
            'volume_ratio': self._calc_volume_ratio(market_data),
            'momentum': self._calc_momentum(market_data),
            'volatility_pct': self._calc_volatility_percentile(market_data),
            'trend_strength': self._calc_trend_strength(market_data),
            'hour_of_day': signal.timestamp.hour,
            'recent_win_rate': self._get_recent_win_rate(signal.strategy),
            'risk_reward': signal.risk_reward_ratio
        }
```

### 2. Reinforcement Learning Strategy Tuning

#### Environment Implementation

```python
import numpy as np
from typing import Dict, Tuple

class TradingEnvironment:
    """Backtesting environment for RL agent"""
    
    def __init__(self, data, initial_params):
        self.data = data
        self.params = initial_params
        self.position = 0
        self.balance = 10000
        self.current_step = 0
        
    def reset(self):
        self.position = 0
        self.balance = 10000
        self.current_step = 0
        return self._get_state()
        
    def step(self, action):
        # Action: parameter adjustment
        self.params = self._apply_action(action)
        
        # Execute strategy with current parameters
        signal = self._generate_signal(self.params)
        reward = self._execute_trade(signal)
        
        self.current_step += 1
        done = self.current_step >= len(self.data)
        
        return self._get_state(), reward, done, {}
```

#### Q-Learning Agent

```python
class QLearningTuner:
    """Simple Q-learning for discrete parameter tuning"""
    
    def __init__(self, param_space, learning_rate=0.1, discount=0.95):
        self.param_space = param_space
        self.lr = learning_rate
        self.gamma = discount
        self.q_table = {}
        
    def get_action(self, state, epsilon=0.1):
        if np.random.random() < epsilon:
            # Explore: random parameter adjustment
            return self._random_action()
        else:
            # Exploit: best known action
            return self._best_action(state)
            
    def update(self, state, action, reward, next_state):
        current_q = self.q_table.get((state, action), 0)
        max_next_q = max([self.q_table.get((next_state, a), 0) 
                         for a in self._possible_actions()])
        
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(state, action)] = new_q
```

#### Training Loop

```python
def train_tuner(strategy, historical_data, max_episodes=1000):
    env = TradingEnvironment(historical_data, default_params)
    agent = QLearningTuner(param_space)
    
    best_params = None
    best_reward = -float('inf')
    
    for episode in range(max_episodes):
        state = env.reset()
        total_reward = 0
        epsilon = max(0.01, 1.0 - episode / max_episodes)  # Decay
        
        while True:
            action = agent.get_action(state, epsilon)
            next_state, reward, done, _ = env.step(action)
            
            agent.update(state, action, reward, next_state)
            total_reward += reward
            state = next_state
            
            if done:
                break
        
        if total_reward > best_reward:
            best_reward = total_reward
            best_params = env.params.copy()
            
    return best_params, best_reward
```

### 3. Predictive Volatility Estimation

#### Model Architecture

Uses GARCH-style features with Random Forest regression:

```python
from sklearn.ensemble import RandomForestRegressor

class VolatilityPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42
        )
        
    def train(self, historical_data):
        X, y = self._prepare_training_data(historical_data)
        self.model.fit(X, y)
```

#### Feature Engineering

```python
class VolatilityFeatures:
    def extract(self, price_data, window=24):
        return {
            # Historical volatility features
            'realized_vol_1h': self._realized_volatility(price_data, 1),
            'realized_vol_6h': self._realized_volatility(price_data, 6),
            'realized_vol_24h': self._realized_volatility(price_data, 24),
            
            # Price features
            'returns_mean': np.mean(price_data.pct_change()),
            'returns_std': np.std(price_data.pct_change()),
            'abs_returns_mean': np.mean(np.abs(price_data.pct_change())),
            
            # Volume features
            'volume_mean': np.mean(price_data.volume),
            'volume_std': np.std(price_data.volume),
            
            # Range features
            'high_low_range': np.mean(price_data.high - price_data.low),
            'close_open_range': np.mean(np.abs(price_data.close - price_data.open)),
            
            # Momentum features
            'momentum_1h': price_data.close[-1] / price_data.close[-1] - 1,
            'momentum_6h': price_data.close[-1] / price_data.close[-6] - 1,
            
            # Microstructure
            'price_jumps': self._count_price_jumps(price_data),
            'gap_ratio': self._calculate_gap_ratio(price_data)
        }
```

#### Prediction with Confidence Intervals

```python
def predict_volatility(self, market_data, horizon=24):
    features = self._extract_features(market_data)
    
    # Point prediction
    predicted_vol = self.model.predict([features])[0]
    
    # Confidence interval using tree predictions
    tree_predictions = np.array([
        tree.predict([features])[0] 
        for tree in self.model.estimators_
    ])
    
    confidence = 1 - (np.std(tree_predictions) / np.mean(tree_predictions))
    lower = np.percentile(tree_predictions, 10)
    upper = np.percentile(tree_predictions, 90)
    
    return {
        'predicted': predicted_vol,
        'confidence': confidence,
        'range': {'low': lower, 'high': upper},
        'horizon': horizon
    }
```

## Database Schema Updates

### Prisma Schema Changes

```prisma
// apps/backend/prisma/schema.prisma

model MLSignalScore {
  id          Int      @id @default(autoincrement())
  userId      Int
  user        User     @relation(fields: [userId], references: [id])
  symbol      String
  timeframe   String
  strategy    String
  score       Float
  confidence  Float
  features    Json
  prediction  String?
  executed    Boolean  @default(false)
  outcome     String?  // WIN, LOSS, PENDING
  createdAt   DateTime @default(now())
  
  @@index([userId, createdAt])
  @@index([symbol, strategy])
}

model MLModelTraining {
  id              Int       @id @default(autoincrement())
  modelType       String    // SIGNAL_QUALITY, RL_TUNER, VOLATILITY
  modelVersion    String
  trainingData    Json
  hyperparameters Json
  performance     Json
  status          String    // TRAINING, COMPLETED, FAILED
  startedAt       DateTime  @default(now())
  completedAt     DateTime?
  errorMessage    String?
  
  @@index([modelType, status])
}

model StrategyOptimization {
  id              Int      @id @default(autoincrement())
  userId          Int
  user            User     @relation(fields: [userId], references: [id])
  strategy        String
  originalParams  Json
  optimizedParams Json
  performance     Json
  method          String   // RL, GRID_SEARCH, BAYESIAN
  iterations      Int
  createdAt       DateTime @default(now())
  
  @@index([userId, strategy])
}

model VolatilityPrediction {
  id          Int      @id @default(autoincrement())
  symbol      String
  timeframe   String
  predicted   Float
  actual      Float?
  confidence  Float
  features    Json
  horizon     Int
  createdAt   DateTime @default(now())
  
  @@index([symbol, createdAt])
  @@index([createdAt])
}

// Add relations to User model
model User {
  // ... existing fields ...
  mlSignalScores       MLSignalScore[]
  strategyOptimizations StrategyOptimization[]
}
```

## API Endpoints Implementation

### Signal Quality Endpoints

```python
# apps/backend/src/api/ml_endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ..ml.signal_quality.scorer import SignalQualityScorer

router = APIRouter(prefix="/ml", tags=["ML"])

class SignalScoreRequest(BaseModel):
    symbol: str
    timeframe: str
    strategy: str
    signal: dict

class SignalScoreResponse(BaseModel):
    score: float
    confidence: float
    recommendation: str
    factors: dict
    risk: str

@router.post("/signal/score", response_model=SignalScoreResponse)
async def score_signal(request: SignalScoreRequest, user=Depends(get_current_user)):
    scorer = SignalQualityScorer()
    
    # Get market data
    market_data = await get_market_data(request.symbol, request.timeframe)
    
    # Score the signal
    result = scorer.score_signal(request.signal, market_data)
    
    # Log to database
    await db.mlsignalscore.create(
        data={
            'userId': user.id,
            'symbol': request.symbol,
            'strategy': request.strategy,
            'score': result['score'],
            'confidence': result['confidence'],
            'features': result.get('features', {}),
            'prediction': result['recommendation']
        }
    )
    
    return result
```

### RL Tuning Endpoints

```python
from ..worker.tasks import run_strategy_optimization

@router.post("/tune/start")
async def start_tuning(request: TuneRequest, user=Depends(get_current_user)):
    # Validate parameters
    if not request.parameters:
        raise HTTPException(400, "Parameters required")
    
    # Create optimization job
    job = await db.strategyoptimization.create(
        data={
            'userId': user.id,
            'strategy': request.strategy,
            'originalParams': request.parameters,
            'optimizedParams': {},
            'performance': {},
            'method': 'RL',
            'iterations': 0
        }
    )
    
    # Start async optimization task
    task = run_strategy_optimization.delay(
        job_id=job.id,
        strategy=request.strategy,
        params=request.parameters,
        data=request.training_period
    )
    
    return {
        'jobId': f"tune_{job.id}",
        'status': 'STARTED',
        'taskId': task.id
    }

@router.get("/tune/status/{job_id}")
async def get_tuning_status(job_id: str, user=Depends(get_current_user)):
    job_num = int(job_id.replace('tune_', ''))
    job = await db.strategyoptimization.find_unique(where={'id': job_num})
    
    if not job:
        raise HTTPException(404, "Job not found")
    
    # Get task status from Celery
    task_status = celery_app.AsyncResult(job.task_id).state
    
    return {
        'jobId': job_id,
        'status': task_status,
        'progress': job.iterations / 1000,
        'currentIteration': job.iterations
    }
```

### Volatility Prediction Endpoints

```python
from ..ml.volatility.predictor import VolatilityPredictor

@router.post("/volatility/predict")
async def predict_volatility(request: VolatilityRequest):
    predictor = VolatilityPredictor()
    
    # Get historical data
    market_data = await get_market_data(
        request.symbol, 
        request.timeframe,
        limit=100
    )
    
    # Make prediction
    prediction = predictor.predict_volatility(
        market_data,
        horizon=request.horizon
    )
    
    # Store prediction
    await db.volatilityprediction.create(
        data={
            'symbol': request.symbol,
            'timeframe': request.timeframe,
            'predicted': prediction['predicted'],
            'confidence': prediction['confidence'],
            'features': prediction.get('features', {}),
            'horizon': request.horizon
        }
    )
    
    return prediction
```

## Celery Tasks for Background Processing

```python
# apps/backend/src/worker/tasks.py

from celery import Task
from ..ml.reinforcement.tuner import train_tuner

@celery_app.task(bind=True)
def run_strategy_optimization(self, job_id, strategy, params, data):
    try:
        # Update job status
        db.strategyoptimization.update(
            where={'id': job_id},
            data={'status': 'RUNNING'}
        )
        
        # Load historical data
        historical_data = load_market_data(data['start'], data['end'])
        
        # Run optimization
        best_params, best_performance = train_tuner(
            strategy=strategy,
            historical_data=historical_data,
            initial_params=params,
            max_episodes=1000
        )
        
        # Save results
        db.strategyoptimization.update(
            where={'id': job_id},
            data={
                'optimizedParams': best_params,
                'performance': best_performance,
                'status': 'COMPLETED',
                'iterations': 1000
            }
        )
        
        return {'status': 'success', 'params': best_params}
        
    except Exception as e:
        db.strategyoptimization.update(
            where={'id': job_id},
            data={'status': 'FAILED', 'errorMessage': str(e)}
        )
        raise
```

## Model Persistence

### Saving Models

```python
import pickle
import os

class ModelStorage:
    MODEL_DIR = "/app/ml_models"
    
    @staticmethod
    def save_model(model, model_id, version):
        path = f"{ModelStorage.MODEL_DIR}/{model_id}_v{version}.pkl"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump(model, f)
            
        return path
    
    @staticmethod
    def load_model(model_id, version):
        path = f"{ModelStorage.MODEL_DIR}/{model_id}_v{version}.pkl"
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found: {path}")
            
        with open(path, 'rb') as f:
            return pickle.load(f)
```

## Integration with Existing Systems

### Strategy Integration

```python
# apps/backend/src/trading/bot_runner.py

class BotRunner:
    def __init__(self, strategy, config):
        self.strategy = strategy
        self.config = config
        
        # Initialize ML components if enabled
        if config.get('ml', {}).get('scoreSignals'):
            self.signal_scorer = SignalQualityScorer()
        else:
            self.signal_scorer = None
            
        if config.get('ml', {}).get('useVolatilityPrediction'):
            self.vol_predictor = VolatilityPredictor()
        else:
            self.vol_predictor = None
    
    async def execute_trade(self, signal):
        # Score signal if ML enabled
        if self.signal_scorer:
            score = self.signal_scorer.score_signal(signal, self.market_data)
            
            if score['score'] < self.config['ml']['minScore']:
                logger.info(f"Rejected signal with score {score['score']}")
                return None
        
        # Adjust position size based on volatility
        if self.vol_predictor:
            vol_prediction = self.vol_predictor.predict_volatility(
                self.market_data
            )
            signal.position_size = self._adjust_size_for_volatility(
                signal.position_size,
                vol_prediction['predicted']
            )
        
        # Execute the trade
        return await self.strategy.execute(signal)
```

## Testing

### Unit Tests

```python
# tests/test_ml_signal_scorer.py

import pytest
from src.ml.signal_quality.scorer import SignalQualityScorer

def test_signal_scorer_initialization():
    scorer = SignalQualityScorer()
    assert scorer is not None
    assert scorer.model is not None

def test_score_signal():
    scorer = SignalQualityScorer()
    signal = create_mock_signal()
    market_data = create_mock_market_data()
    
    result = scorer.score_signal(signal, market_data)
    
    assert 'score' in result
    assert 0 <= result['score'] <= 1
    assert 'confidence' in result
    assert result['recommendation'] in ['EXECUTE', 'SKIP']
```

## Performance Optimization

### Caching

```python
from functools import lru_cache
import hashlib

class CachedPredictor:
    @lru_cache(maxsize=1000)
    def predict_cached(self, features_hash):
        return self.model.predict(features)
        
    def predict(self, features):
        # Hash features for cache key
        features_hash = hashlib.md5(
            str(features).encode()
        ).hexdigest()
        
        return self.predict_cached(features_hash)
```

### Batch Processing

```python
async def batch_score_signals(signals, market_data):
    # Extract features for all signals at once
    features = [extractor.extract(s, market_data) for s in signals]
    
    # Batch prediction
    scores = scorer.model.predict_proba(features)
    
    # Return results
    return [
        {'score': score[1], 'signal': signal}
        for score, signal in zip(scores, signals)
    ]
```

## Monitoring

### Model Performance Tracking

```python
@router.get("/ml/metrics/signal_accuracy")
async def get_signal_accuracy(days: int = 30):
    # Get predictions and outcomes from last N days
    cutoff = datetime.now() - timedelta(days=days)
    
    scores = await db.mlsignalscore.find_many(
        where={
            'createdAt': {'gte': cutoff},
            'outcome': {'not': None}
        }
    )
    
    # Calculate accuracy
    correct = sum(
        1 for s in scores 
        if (s.score > 0.5 and s.outcome == 'WIN') or
           (s.score <= 0.5 and s.outcome == 'LOSS')
    )
    
    accuracy = correct / len(scores) if scores else 0
    
    return {
        'accuracy': accuracy,
        'total': len(scores),
        'period': f'{days} days'
    }
```

## Deployment

### Docker Configuration

```dockerfile
# Dockerfile additions for ML support
RUN pip install scikit-learn scipy

# Copy ML models
COPY ml_models/ /app/ml_models/

# Set environment variables
ENV ML_MODEL_DIR=/app/ml_models
ENV ML_CACHE_SIZE=1000
```

## Security Considerations

1. **Model Access Control**: Only authenticated users can access ML endpoints
2. **Resource Limits**: Rate limiting on expensive operations (training, optimization)
3. **Input Validation**: Validate all inputs to prevent injection attacks
4. **Model Integrity**: Checksum verification for loaded models
5. **Data Privacy**: Anonymize user data in training datasets

## Future Enhancements

1. **Deep Learning Models**: Add TensorFlow/PyTorch for complex patterns
2. **Online Learning**: Continuous model updates with new data
3. **Explainable AI**: Feature importance and decision explanations
4. **Multi-Asset Models**: Cross-asset correlation and prediction
5. **Custom User Models**: Allow users to train personal models

---

**Implementation Status**: Complete ✅  
**Version**: 1.0.0  
**Last Updated**: November 9, 2025
