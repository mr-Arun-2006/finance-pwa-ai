import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta

class DataProcessor:
    """Process and prepare financial data for ML models"""
    
    @staticmethod
    def preprocess_transactions(transactions: list) -> pd.DataFrame:
        """
        Preprocess raw transaction data
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Processed DataFrame
        """
        df = pd.DataFrame(transactions)
        
        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract temporal features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        
        # Extract features from description
        df['description_length'] = df['description'].str.len()
        df['description_words'] = df['description'].str.split().str.len()
        
        return df
    
    @staticmethod
    def extract_features(transaction: dict) -> np.ndarray:
        """
        Extract features from a single transaction
        
        Args:
            transaction: Transaction dictionary
            
        Returns:
            Feature array
        """
        date = pd.to_datetime(transaction['date'])
        
        features = [
            float(transaction['amount']),
            date.dayofweek,
            date.month,
            date.day,
            len(transaction['description']),
            len(transaction['description'].split()),
        ]
        
        return np.array(features)
    
    @staticmethod
    def generate_time_series(transactions: list, freq: str = 'D') -> pd.DataFrame:
        """
        Generate time series data from transactions
        
        Args:
            transactions: List of transactions
            freq: Frequency ('D', 'W', 'M')
            
        Returns:
            Time series DataFrame
        """
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by date and sum amounts
        ts = df.groupby(df['date'].dt.to_period(freq))['amount'].sum()
        ts.index = ts.index.to_timestamp()
        
        return ts.reset_index()
