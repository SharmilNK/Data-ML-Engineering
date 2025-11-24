"""
Model Service - Load and serve trained models
"""
import pickle
import os
import pandas as pd
import numpy as np
from pathlib import Path


class ModelService:
    """Service class to load models and make predictions."""
    
    def __init__(self, model_path=None):
        """
        Initialize model service.
        
        Args:
            model_path: Path to the saved models.pkl file
        """
        if model_path is None:
            # Try multiple possible paths (check both relative and absolute)
            possible_paths = [
                "models/models.pkl",  # Root models directory
                "src/models/models.pkl",  # Source models directory
                "../models/models.pkl",  # Parent models directory
                "/app/models/models.pkl",  # Docker path (root)
                "/app/src/models/models.pkl",  # Docker path (src)
                os.path.join(os.path.dirname(__file__), "models", "models.pkl"),  # Relative to this file
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "models.pkl"),  # Root models
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        # Load models
        with open(model_path, 'rb') as f:
            artifacts = pickle.load(f)
        
        self.classifier = artifacts['classifier']
        self.regressor = artifacts['regressor']
        self.scaler = artifacts['scaler']
        self.feature_cols = artifacts['feature_cols']
        
        print(f"✓ Models loaded from {model_path}")
        print(f"  Feature columns: {len(self.feature_cols)}")
    
    def _prepare_features(self, input_data):
        """
        Prepare input data for prediction.
        
        Args:
            input_data: dict with feature values or DataFrame
            
        Returns:
            numpy array of scaled features
        """
        # Convert dict to DataFrame if needed
        if isinstance(input_data, dict):
            # Create a DataFrame with all feature columns, fill missing with 0
            df = pd.DataFrame([input_data])
            
            # Ensure all required features are present
            for col in self.feature_cols:
                if col not in df.columns:
                    df[col] = 0
            
            # Select only the features used in training
            X = df[self.feature_cols].fillna(0)
        else:
            X = input_data[self.feature_cols].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        return X_scaled
    
    def predict_classification(self, input_data):
        """
        Predict if a day is high-risk (classification).
        
        Args:
            input_data: dict or DataFrame with feature values
            
        Returns:
            dict with prediction and probability
        """
        X = self._prepare_features(input_data)
        prediction = self.classifier.predict(X)[0]
        probability = self.classifier.predict_proba(X)[0]
        
        return {
            'prediction': int(prediction),
            'is_high_risk': bool(prediction),
            'probability': {
                'normal': float(probability[0]),
                'high_risk': float(probability[1])
            }
        }
    
    def predict_regression(self, input_data):
        """
        Predict total hospitalization count (regression).
        
        Args:
            input_data: dict or DataFrame with feature values
            
        Returns:
            dict with predicted count
        """
        X = self._prepare_features(input_data)
        prediction = self.regressor.predict(X)[0]
        
        return {
            'predicted_count': float(prediction),
            'prediction': int(round(prediction))
        }
    
    def predict(self, input_data):
        """
        Make both classification and regression predictions.
        
        Args:
            input_data: dict or DataFrame with feature values
            
        Returns:
            dict with both predictions
        """
        class_result = self.predict_classification(input_data)
        reg_result = self.predict_regression(input_data)
        
        return {
            'classification': class_result,
            'regression': reg_result
        }