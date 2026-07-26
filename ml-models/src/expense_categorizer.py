import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
from typing import Tuple, Dict
import os

class ExpenseCategorizer:
    """
    AI model for automatic expense categorization using Random Forest
    """
    
    CATEGORIES = [
        'Groceries', 'Transportation', 'Utilities', 'Entertainment',
        'Healthcare', 'Shopping', 'Dining', 'Subscriptions',
        'Insurance', 'Rent', 'Education', 'Other'
    ]
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.model_path = 'models/expense_classifier.pkl'
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the expense categorizer model
        
        Args:
            X_train: Training features
            y_train: Training labels (category names)
        """
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y_train)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_encoded)
        
        print("✅ Expense categorizer trained successfully")
    
    def predict(self, X: np.ndarray) -> Dict:
        """
        Predict expense categories
        
        Args:
            X: Feature array
            
        Returns:
            Dictionary with prediction and confidence
        """
        if self.model is None:
            raise ValueError("Model not trained. Train first.")
        
        prediction = self.model.predict(X.reshape(1, -1))[0]
        probabilities = self.model.predict_proba(X.reshape(1, -1))[0]
        confidence = np.max(probabilities)
        
        category = self.label_encoder.inverse_transform([prediction])[0]
        
        return {
            'category': category,
            'confidence': float(confidence),
            'probabilities': {
                cat: float(prob) 
                for cat, prob in zip(self.CATEGORIES, probabilities)
            }
        }
    
    def predict_batch(self, X: np.ndarray) -> list:
        """
        Predict categories for multiple transactions
        
        Args:
            X: Feature array with shape (n_samples, n_features)
            
        Returns:
            List of predictions
        """
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        results = []
        for pred, probs in zip(predictions, probabilities):
            category = self.label_encoder.inverse_transform([pred])[0]
            confidence = np.max(probs)
            results.append({
                'category': category,
                'confidence': float(confidence)
            })
        
        return results
    
    def save_model(self):
        """Save model to disk"""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.label_encoder, 'models/label_encoder.pkl')
        print(f"✅ Model saved to {self.model_path}")
    
    def load_model(self):
        """Load model from disk"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.label_encoder = joblib.load('models/label_encoder.pkl')
            print(f"✅ Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the model"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        features = ['amount', 'day_of_week', 'month', 'day', 'desc_length', 'desc_words']
        importance = self.model.feature_importances_
        
        return {feat: float(imp) for feat, imp in zip(features, importance)}
