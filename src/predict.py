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
            # Build absolute path to model if not provided
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(project_root, 'models', 'best_model.pkl')
        
        print(f"Looking for model at: {model_path}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at {model_path}. "
                "Please train the model first by running the training pipeline."
            )
        
        print(f"✓ Loading model from: {model_path}")
        
        # Load models (use only ONE method - whichever was used to save)
        # If saved with joblib, use joblib.load:
        artifacts = joblib.load(model_path)
        
        # OR if saved with pickle, use pickle.load:
        # with open(model_path, 'rb') as f:
        #     artifacts = pickle.load(f)
        
        self.classifier = artifacts['classifier']
        self.regressor = artifacts['regressor']
        self.scaler = artifacts['scaler']
        self.feature_cols = artifacts['feature_cols']
        
        print(f"✓ Models loaded successfully")
        print(f"  Classifier: {type(self.classifier).__name__}")
        print(f"  Regressor: {type(self.regressor).__name__}")
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