"""
Model Training
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, roc_auc_score, recall_score, precision_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def prepare_splits(df, config):
    """Split data into train/val/test."""
    print("=" * 60)
    print("PREPARING DATA SPLITS")
    print("=" * 60)
    
    # Define feature columns (exclude targets and metadata)
    exclude_cols = [
        'Date', 'Total_Hospitalization', 'Respiratory_Count',
        'Asthma_Count', 'High_Risk', 'year'
    ]
    exclude_cols += [c for c in df.columns if 'year' in c.lower()]
    
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    
    X = df[feature_cols].fillna(0)
    y_class = df['High_Risk']
    y_reg = df['Total_Hospitalization']
    dates = df['Date']
    
    # Split by year
    years = dates.dt.year
    train_years = config["split"]["train_years"]
    val_year = config["split"]["val_year"]
    test_year = config["split"]["test_year"]
    
    train_mask = years.isin(train_years)
    val_mask = years == val_year
    test_mask = years == test_year
    
    # Create splits
    X_train, X_val, X_test = X[train_mask], X[val_mask], X[test_mask]
    y_class_train, y_class_val, y_class_test = y_class[train_mask], y_class[val_mask], y_class[test_mask]
    y_reg_train, y_reg_val, y_reg_test = y_reg[train_mask], y_reg[val_mask], y_reg[test_mask]
    
    print(f"✓ Train: {X_train.shape} ({train_years})")
    print(f"✓ Val: {X_val.shape} ({val_year})")
    print(f"✓ Test: {X_test.shape} ({test_year})")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    return {
        'X_train': X_train_scaled, 'X_val': X_val_scaled, 'X_test': X_test_scaled,
        'y_class_train': y_class_train, 'y_class_val': y_class_val, 'y_class_test': y_class_test,
        'y_reg_train': y_reg_train, 'y_reg_val': y_reg_val, 'y_reg_test': y_reg_test,
        'feature_cols': feature_cols, 'scaler': scaler
    }


def train_classifier(splits, config):
    """Train classification model."""
    print("\n" + "=" * 60)
    print("TRAINING CLASSIFICATION MODEL")
    print("=" * 60)
    
    params = config["classification"]["params"]
    model = GradientBoostingClassifier(**params)
    
    model.fit(splits['X_train'], splits['y_class_train'])
    
    # Evaluate
    y_pred = model.predict(splits['X_test'])
    y_proba = model.predict_proba(splits['X_test'])[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(splits['y_class_test'], y_pred),
        'auroc': roc_auc_score(splits['y_class_test'], y_proba),
        'recall': recall_score(splits['y_class_test'], y_pred),
        'precision': precision_score(splits['y_class_test'], y_pred)
    }
    
    print(f"✓ Accuracy: {metrics['accuracy']:.4f}")
    print(f"✓ AUROC: {metrics['auroc']:.4f}")
    print(f"✓ Recall: {metrics['recall']:.4f}")
    print(f"✓ Precision: {metrics['precision']:.4f}")
    
    return model, metrics


def train_regressor(splits, config):
    """Train regression model."""
    print("\n" + "=" * 60)
    print("TRAINING REGRESSION MODEL")
    print("=" * 60)
    
    params = config["regression"]["params"]
    model = GradientBoostingRegressor(**params)
    
    model.fit(splits['X_train'], splits['y_reg_train'])
    
    # Evaluate
    y_pred = model.predict(splits['X_test'])
    
    metrics = {
        'r2': r2_score(splits['y_reg_test'], y_pred),
        'mae': mean_absolute_error(splits['y_reg_test'], y_pred),
        'rmse': np.sqrt(mean_squared_error(splits['y_reg_test'], y_pred))
    }
    
    print(f"✓ R²: {metrics['r2']:.4f}")
    print(f"✓ MAE: {metrics['mae']:.2f}")
    print(f"✓ RMSE: {metrics['rmse']:.2f}")
    
    return model, metrics


def save_models(classifier, regressor, scaler, feature_cols, config):
    """Save trained models."""
    model_dir = config["output"]["model_dir"]
    os.makedirs(model_dir, exist_ok=True)
    
    artifacts = {
        'classifier': classifier,
        'regressor': regressor,
        'scaler': scaler,
        'feature_cols': feature_cols
    }
    
    with open(f"{model_dir}/models.pkl", 'wb') as f:
        pickle.dump(artifacts, f)
    
    print(f"\n✓ Models saved to {model_dir}/models.pkl")
