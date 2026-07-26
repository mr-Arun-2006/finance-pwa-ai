from fastapi import FastAPI, HTTPException, File, UploadFile, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

from expense_categorizer import ExpenseCategorizer
from fraud_detector import FraudDetector
from cash_flow_forecaster import CashFlowForecaster
from data_processor import DataProcessor

load_dotenv()

app = FastAPI(
    title="Finance PWA ML API",
    description="Machine Learning API for financial analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
categorizer = ExpenseCategorizer()
fraud_detector = FraudDetector()
forecaster = CashFlowForecaster()

# Load models if they exist
try:
    categorizer.load_model()
except:
    print("⚠️ Categorizer model not found. Will use random predictions.")

try:
    fraud_detector.load_model()
except:
    print("⚠️ Fraud detector model not found. Will use random predictions.")

try:
    forecaster.load_model()
except:
    print("⚠️ Forecaster model not found.")

# Pydantic models
class Transaction(BaseModel):
    date: str
    amount: float
    description: str
    merchant: str

class CategorizationRequest(BaseModel):
    transactions: List[Transaction]

class FraudCheckRequest(BaseModel):
    transactions: List[Transaction]

class ForecastRequest(BaseModel):
    transactions: List[Transaction]
    periods: int = 30

# Routes
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models": {
            "categorizer": "loaded" if categorizer.model else "not_loaded",
            "fraud_detector": "loaded" if fraud_detector.model else "not_loaded",
            "forecaster": "loaded" if forecaster.model else "not_loaded"
        }
    }

@app.post("/api/categorize")
def categorize_transactions(request: CategorizationRequest):
    """
    Categorize expenses using AI
    """
    try:
        processor = DataProcessor()
        results = []
        
        for transaction in request.transactions:
            # Extract features
            features = processor.extract_features(transaction.dict())
            
            # Categorize
            if categorizer.model:
                prediction = categorizer.predict(features)
            else:
                # Fallback: random category
                prediction = {
                    'category': 'Other',
                    'confidence': 0.5
                }
            
            results.append({
                'transaction_id': transaction.description[:20],
                'amount': transaction.amount,
                'category': prediction['category'],
                'confidence': prediction['confidence']
            })
        
        return {"categorizations": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect-fraud")
def detect_fraud(request: FraudCheckRequest):
    """
    Detect fraudulent transactions
    """
    try:
        processor = DataProcessor()
        results = []
        
        for transaction in request.transactions:
            features = processor.extract_features(transaction.dict())
            
            if fraud_detector.model:
                prediction = fraud_detector.predict(features)
            else:
                prediction = {
                    'is_fraud': False,
                    'fraud_score': 0.1,
                    'risk_level': 'LOW'
                }
            
            results.append({
                'transaction_id': transaction.description[:20],
                'amount': transaction.amount,
                'is_fraud': prediction['is_fraud'],
                'fraud_score': prediction['fraud_score'],
                'risk_level': prediction['risk_level']
            })
        
        return {"fraud_checks": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/forecast")
def forecast_spending(request: ForecastRequest):
    """
    Forecast future spending
    """
    try:
        processor = DataProcessor()
        
        # Prepare time series data
        df = processor.preprocess_transactions([t.dict() for t in request.transactions])
        ts_data = df.groupby('date')['amount'].sum().reset_index()
        ts_data.columns = ['ds', 'y']
        
        if forecaster.model:
            forecaster.forecast_periods = request.periods
            forecast_result = forecaster.forecast()
        else:
            forecast_result = {
                'forecast': [],
                'trend': 'stable',
                'average': 0,
                'min': 0,
                'max': 0
            }
        
        return forecast_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feature-importance")
def get_feature_importance():
    """
    Get feature importance from categorizer
    """
    try:
        if categorizer.model:
            importance = categorizer.get_feature_importance()
            return {"feature_importance": importance}
        else:
            raise HTTPException(status_code=400, detail="Model not trained yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
