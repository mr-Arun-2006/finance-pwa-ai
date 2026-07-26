import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, List
import os

class FraudDetector:
    """
    AI model for detecting fraudulent transactions using Isolation Forest
    """
    
    def __init__(self, contamination: float = 0.1):
        """
        Initialize fraud detector
        
        Args:
            contamination: Expected proportion of anomalies
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.model_path = 'models/fraud_detector.pkl'
    
    def train(self, X: np.ndarray):
        """
        Train the fraud detector
        
        Args:
            X: Training features (normal transactions)
        """
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model.fit(X_scaled)
        
        print("✅ Fraud detector trained successfully")
    
    def predict(self, X: np.ndarray) -> Dict:
        """
        Predict if transaction is fraudulent
        
        Args:
            X: Feature array
            
        Returns:
            Dictionary with fraud prediction and score
        """
        X_scaled = self.scaler.transform(X.reshape(1, -1))
        
        # Predict: -1 for anomaly, 1 for normal
        prediction = self.model.predict(X_scaled)[0]
        
        # Get anomaly score
        score = self.model.score_samples(X_scaled)[0]
        
        # Normalize score to 0-1 (higher = more likely fraud)
        anomaly_score = 1 / (1 + np.exp(-score))
        
        return {
            'is_fraud': bool(prediction == -1),
            'fraud_score': float(anomaly_score),
            'risk_level': self._get_risk_level(anomaly_score)
        }
    
    def predict_batch(self, X: np.ndarray) -> List[Dict]:
        """
        Detect fraud for multiple transactions
        
        Args:
            X: Feature array with shape (n_samples, n_features)
            
        Returns:
            List of fraud predictions
        """
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        results = []
        for pred, score in zip(predictions, scores):
            # Normalize score
            anomaly_score = 1 / (1 + np.exp(-score))
            results.append({
                'is_fraud': bool(pred == -1),
                'fraud_score': float(anomaly_score),
                'risk_level': self._get_risk_level(anomaly_score)
            })
        
        return results
    
    @staticmethod
    def _get_risk_level(score: float) -> str:
        """Get risk level from anomaly score"""
        if score > 0.8:
            return 'CRITICAL'
        elif score > 0.6:
            return 'HIGH'
        elif score > 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def save_model(self):
        """Save model to disk"""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, 'models/fraud_scaler.pkl')
        print(f"✅ Fraud detector saved to {self.model_path}")
    
    def load_model(self):
        """Load model from disk"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load('models/fraud_scaler.pkl')
            print(f"✅ Fraud detector loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
