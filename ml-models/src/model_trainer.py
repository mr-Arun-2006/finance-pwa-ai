import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from expense_categorizer import ExpenseCategorizer
from fraud_detector import FraudDetector
from cash_flow_forecaster import CashFlowForecaster
from data_processor import DataProcessor

def generate_sample_data(n_samples: int = 1000):
    """
    Generate sample transaction data for training
    """
    np.random.seed(42)
    categories = ['Groceries', 'Transportation', 'Utilities', 'Entertainment',
                  'Healthcare', 'Shopping', 'Dining', 'Subscriptions',
                  'Insurance', 'Rent', 'Education', 'Other']
    
    merchants = ['Walmart', 'Amazon', 'Uber', 'Starbucks', 'Target', 'Apple',
                 'Netflix', 'Spotify', 'Google', 'Microsoft', 'GitHub', 'AWS']
    
    transactions = []
    for i in range(n_samples):
        date = datetime.now() - timedelta(days=np.random.randint(0, 365))
        amount = np.random.exponential(scale=50) + 5
        category = np.random.choice(categories)
        merchant = np.random.choice(merchants)
        
        transactions.append({
            'date': date.isoformat(),
            'amount': float(amount),
            'description': f"{merchant} - {category}",
            'merchant': merchant,
            'category': category
        })
    
    return transactions

def train_expense_categorizer():
    """
    Train the expense categorizer model
    """
    print("\n🚀 Training Expense Categorizer...")
    
    # Generate sample data
    transactions = generate_sample_data(1000)
    
    # Process data
    processor = DataProcessor()
    X_train = np.array([processor.extract_features(t) for t in transactions])
    y_train = np.array([t['category'] for t in transactions])
    
    # Train model
    categorizer = ExpenseCategorizer()
    categorizer.train(X_train, y_train)
    categorizer.save_model()
    
    # Print feature importance
    importance = categorizer.get_feature_importance()
    print("\n📊 Feature Importance:")
    for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {score:.4f}")

def train_fraud_detector():
    """
    Train the fraud detector model
    """
    print("\n🚀 Training Fraud Detector...")
    
    # Generate sample data (normal transactions)
    transactions = generate_sample_data(2000)
    
    # Process data
    processor = DataProcessor()
    X_train = np.array([processor.extract_features(t) for t in transactions])
    
    # Train model
    detector = FraudDetector(contamination=0.05)
    detector.train(X_train)
    detector.save_model()
    
    print("✅ Fraud detector trained successfully")

def train_cash_flow_forecaster():
    """
    Train the cash flow forecaster
    """
    print("\n🚀 Training Cash Flow Forecaster...")
    
    # Generate sample time series data
    dates = pd.date_range(end='today', periods=365)
    amounts = np.random.exponential(scale=100, size=365) + 50
    
    ts_data = pd.DataFrame({
        'ds': dates,
        'y': amounts
    })
    
    # Train model
    forecaster = CashFlowForecaster()
    forecaster.train(ts_data)
    forecaster.save_model()
    
    # Generate sample forecast
    forecast = forecaster.forecast()
    print(f"\n📈 Forecast Summary:")
    print(f"  Trend: {forecast['trend']}")
    print(f"  Average: ${forecast['average']:.2f}")
    print(f"  Min: ${forecast['min']:.2f}")
    print(f"  Max: ${forecast['max']:.2f}")

if __name__ == "__main__":
    print("="*60)
    print("🤖 Finance PWA - ML Model Training Pipeline")
    print("="*60)
    
    train_expense_categorizer()
    train_fraud_detector()
    train_cash_flow_forecaster()
    
    print("\n" + "="*60)
    print("✅ All models trained successfully!")
    print("="*60)
