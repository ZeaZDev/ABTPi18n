# Algorithms — Design, Complexity, and Test Fixtures

This document documents the canonical algorithm patterns used in MetaUltra example modules, their complexity, and test strategies.

Common algorithm categories
- Ranking & selection: score strategies and choose top-k for allocation.
- Signal generation: compute indicators (moving averages, z-score, momentum) and emit signals.
- Risk controls: compute drawdown, exposure, and enforce circuit breakers.
- Backtesting harnesses: deterministic replay of ticks with fixtures for regression tests.

Example — Ranking (O(n * m))
```py
def rank_strategies(strategies, weights):
    # strategies: List[Dict(metrics)]
    scores = []
    for s in strategies:
        score = 0.0
        for k, w in weights.items():
            score += w * s['metrics'].get(k, 0.0)
        scores.append((s['name'], score))
    return [name for name, _ in sorted(scores, key=lambda x: x[1], reverse=True)]
```
Complexity: O(n * m) where n = #strategies, m = #metrics evaluated per strategy.

Example — Signal Generation (stream-friendly)
- Normalize inputs using a rolling window.
- Apply smoothing (exponential moving average) — O(1) per tick with constant memory per indicator.
- Compute threshold crossings and output signals with confidence scores.

Pseudocode: Signal pipeline
```
for tick in stream:
  features = normalize_and_extract(tick)
  indicators = update_indicators(features)
  signal = evaluate_rules(indicators)
  if signal and signal.confidence >= threshold:
    emit(signal)
```

Testing & Determinism
- Use fixture streams (static CSV/JSON) that are checked into `tests/fixtures/`.
- Compute expected outputs and assert bit-for-bit equality for pure functions.
- For stochastic or randomized training modules, set fixed seeds and verify high-level metrics (e.g., AUC > X).

Auditability & Complexity Notes
- Document algorithmic complexity and memory assumptions at the top of each module.
- Prefer deterministic, auditable transformations in production strategies — avoid hidden randomness during evaluation.
