# ML Models Directory

This directory contains all machine learning models for the Finance PWA.

## Models

1. **Expense Categorizer** - Random Forest classifier for transaction categorization
2. **Cash Flow Forecaster** - LSTM & Prophet for spending predictions
3. **Fraud Detector** - Isolation Forest for anomaly detection
4. **Budget Optimizer** - Recommendation system for optimal budgets

## Training

```bash
python src/model_trainer.py
```

## Inference API

```bash
python -m uvicorn src.main:app --reload
```
