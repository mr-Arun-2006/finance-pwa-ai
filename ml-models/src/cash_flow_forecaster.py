import numpy as np
import pandas as pd
from typing import Dict, Tuple
import joblib
import os
from datetime import datetime, timedelta

try:
    from fbprophet import Prophet
except:
    from prophet import Prophet

class CashFlowForecaster:
    """
    AI model for cash flow forecasting using Facebook Prophet and LSTM
    """
    
    def __init__(self, forecast_periods: int = 30):
        """
        Initialize forecaster
        
        Args:
            forecast_periods: Number of days to forecast ahead
        """
        self.forecast_periods = forecast_periods
        self.model = None
        self.model_path = 'models/forecasting_model.pkl'
    
    def train(self, ts_data: pd.DataFrame):
        """
        Train cash flow forecasting model
        
        Args:
            ts_data: DataFrame with columns 'ds' (date) and 'y' (amount)
        """
        # Ensure correct column names
        if 'date' in ts_data.columns:
            ts_data = ts_data.rename(columns={'date': 'ds', 'amount': 'y'})
        
        # Initialize Prophet
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            interval_width=0.95
        )
        
        # Fit model
        self.model.fit(ts_data)
        print("✅ Cash flow forecaster trained successfully")
    
    def forecast(self) -> Dict:
        """
        Generate forecast for next N periods
        
        Returns:
            Dictionary with forecast data
        """
        if self.model is None:
            raise ValueError("Model not trained. Train first.")
        
        # Generate future dataframe
        future = self.model.make_future_dataframe(periods=self.forecast_periods)
        forecast = self.model.predict(future)
        
        # Extract relevant columns
        forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(self.forecast_periods)
        
        return {
            'forecast': forecast_data.to_dict('records'),
            'trend': 'increasing' if forecast_data['yhat'].iloc[-1] > forecast_data['yhat'].iloc[0] else 'decreasing',
            'average': float(forecast_data['yhat'].mean()),
            'min': float(forecast_data['yhat'].min()),
            'max': float(forecast_data['yhat'].max())
        }
    
    def forecast_by_category(self, category_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        Generate forecasts for multiple expense categories
        
        Args:
            category_data: Dictionary with category names as keys and time series as values
            
        Returns:
            Dictionary with forecasts for each category
        """
        results = {}
        
        for category, ts_data in category_data.items():
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True, interval_width=0.95)
            model.fit(ts_data)
            
            future = model.make_future_dataframe(periods=self.forecast_periods)
            forecast = model.predict(future)
            
            forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(self.forecast_periods)
            
            results[category] = {
                'forecast': forecast_data.to_dict('records'),
                'average': float(forecast_data['yhat'].mean())
            }
        
        return results
    
    def get_anomalies(self, ts_data: pd.DataFrame, threshold: float = 2.0) -> list:
        """
        Detect anomalies in time series
        
        Args:
            ts_data: Time series data
            threshold: Standard deviation threshold for anomalies
            
        Returns:
            List of anomalies
        """
        if self.model is None:
            raise ValueError("Model not trained. Train first.")
        
        forecast = self.model.predict(ts_data[['ds']])
        
        # Calculate residuals
        residuals = ts_data['y'] - forecast['yhat']
        std = residuals.std()
        
        # Find anomalies
        anomalies = []
        for idx, (date, residual) in enumerate(zip(ts_data['ds'], residuals)):
            if abs(residual) > threshold * std:
                anomalies.append({
                    'date': date.isoformat(),
                    'residual': float(residual),
                    'severity': 'high' if abs(residual) > 3 * std else 'medium'
                })
        
        return anomalies
    
    def save_model(self):
        """Save model to disk"""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"✅ Forecasting model saved to {self.model_path}")
    
    def load_model(self):
        """Load model from disk"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"✅ Forecasting model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
