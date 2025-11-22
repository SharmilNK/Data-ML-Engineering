"""
Model Training with MLFlow Tracking
"""
import pandas as pd
import numpy as np
import pickle
import os
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import (
    accuracy_score, roc_auc_score, recall_score, precision_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score,
    confusion_matrix, roc_curve
)


def prepare_splits(df, config):
    """Split data into train/val/test."""
    
    print("PREPARING DATA SPLITS")
    
    
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
    
    years = dates.dt.year
    train_years = config["split"]["train_years"]
    val_year = config["split"]["val_year"]
    test_year = config["split"]["test_year"]
    
    train_mask = years.isin(train_years)
    val_mask = years == val_year
    test_mask = years == test_year
    
    X_train, X_val, X_test = X[train_mask], X[val_mask], X[test_mask]
    y_class_train, y_class_val, y_class_test = y_class[train_mask], y_class[val_mask], y_class[test_mask]
    y_reg_train, y_reg_val, y_reg_test = y_reg[train_mask], y_reg[val_mask], y_reg[test_mask]
    
    print(f" Train: {X_train.shape}")
    print(f" Val: {X_val.shape}")
    print(f" Test: {X_test.shape}")
    
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


def plot_confusion_matrix(y_true, y_pred, save_path):
    """Create and save confusion matrix plot."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Normal', 'High Risk'],
                yticklabels=['Normal', 'High Risk'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    return save_path


def plot_roc_curve(y_true, y_proba, save_path):
    """Create and save ROC curve plot."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    return save_path


def plot_predictions(y_true, y_pred, save_path):
    """Create and save predicted vs actual plot."""
    plt.figure(figsize=(8, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Predicted vs Actual')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    return save_path


def train_classifier(splits, config):
    """Train classification model with MLFlow tracking."""
    
    print("TRAINING CLASSIFICATION MODEL")
    
    
    params = config["classification"]["params"]
    model = GradientBoostingClassifier(**params)
    
    # Train
    model.fit(splits['X_train'], splits['y_class_train'])
    
    # Predict
    y_pred = model.predict(splits['X_test'])
    y_proba = model.predict_proba(splits['X_test'])[:, 1]
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(splits['y_class_test'], y_pred),
        'auroc': roc_auc_score(splits['y_class_test'], y_proba),
        'recall': recall_score(splits['y_class_test'], y_pred),
        'precision': precision_score(splits['y_class_test'], y_pred),
        'f1': f1_score(splits['y_class_test'], y_pred)
    }
    
    print(f" Accuracy: {metrics['accuracy']:.4f}")
    print(f" AUROC: {metrics['auroc']:.4f}")
    print(f" Recall: {metrics['recall']:.4f}")
    print(f" Precision: {metrics['precision']:.4f}")
    print(f" F1: {metrics['f1']:.4f}")
    
    # Store predictions for plotting
    metrics['y_pred'] = y_pred
    metrics['y_proba'] = y_proba
    metrics['y_true'] = splits['y_class_test']
    
    return model, metrics


def train_regressor(splits, config):
    """Train regression model with MLFlow tracking."""
    
    print("TRAINING REGRESSION MODEL")
    
    
    params = config["regression"]["params"]
    model = GradientBoostingRegressor(**params)
    
    # Train
    model.fit(splits['X_train'], splits['y_reg_train'])
    
    # Predict
    y_pred = model.predict(splits['X_test'])
    
    # Calculate metrics
    metrics = {
        'r2': r2_score(splits['y_reg_test'], y_pred),
        'mae': mean_absolute_error(splits['y_reg_test'], y_pred),
        'rmse': np.sqrt(mean_squared_error(splits['y_reg_test'], y_pred))
    }
    
    print(f"R²: {metrics['r2']:.4f}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    
    # Store predictions for plotting
    metrics['y_pred'] = y_pred
    metrics['y_true'] = splits['y_reg_test']
    
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
    
    model_path = f"{model_dir}/models.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(artifacts, f)
    
    print(f"\n Models saved to {model_path}")
    return model_path


def run_mlflow_experiment(splits, config):
    """Run full training with MLFlow experiment tracking."""
    
    # Setup MLFlow
    mlflow_config = config["mlflow"]
    mlflow.set_tracking_uri(mlflow_config["tracking_uri"])
    mlflow.set_experiment(mlflow_config["experiment_name"])
    
   
    print(f"MLFLOW EXPERIMENT: {mlflow_config['experiment_name']}")
      
    # Start MLFlow run
    with mlflow.start_run(run_name="gradient_boosting_run"):
        
        # Log parameters
        print("\nLogging parameters...")
        mlflow.log_param("model_type_class", config["classification"]["model_type"])
        mlflow.log_param("model_type_reg", config["regression"]["model_type"])
        
        for key, value in config["classification"]["params"].items():
            mlflow.log_param(f"class_{key}", value)
        
        for key, value in config["regression"]["params"].items():
            mlflow.log_param(f"reg_{key}", value)
        
        mlflow.log_param("threshold_percentile", config["target"]["threshold_percentile"])
        mlflow.log_param("train_years", str(config["split"]["train_years"]))
        mlflow.log_param("test_year", config["split"]["test_year"])
        
        # Train classification model
        classifier, class_metrics = train_classifier(splits, config)
        
        # Log classification metrics
        print("\n Logging classification metrics...")
        mlflow.log_metric("accuracy", class_metrics['accuracy'])
        mlflow.log_metric("auroc", class_metrics['auroc'])
        mlflow.log_metric("recall", class_metrics['recall'])
        mlflow.log_metric("precision", class_metrics['precision'])
        mlflow.log_metric("f1", class_metrics['f1'])
        
        # Train regression model
        regressor, reg_metrics = train_regressor(splits, config)
        
        # Log regression metrics
        print("\n Logging regression metrics...")
        mlflow.log_metric("r2", reg_metrics['r2'])
        mlflow.log_metric("mae", reg_metrics['mae'])
        mlflow.log_metric("rmse", reg_metrics['rmse'])
        
        # Create and log artifacts (plots)
        print("\nCreating and logging artifacts...")
        os.makedirs("artifacts", exist_ok=True)
        
        # Confusion matrix
        cm_path = plot_confusion_matrix(
            class_metrics['y_true'], 
            class_metrics['y_pred'],
            "artifacts/confusion_matrix.png"
        )
        mlflow.log_artifact(cm_path)
        
        # ROC curve
        roc_path = plot_roc_curve(
            class_metrics['y_true'],
            class_metrics['y_proba'],
            "artifacts/roc_curve.png"
        )
        mlflow.log_artifact(roc_path)
        
        # Predicted vs Actual
        pred_path = plot_predictions(
            reg_metrics['y_true'],
            reg_metrics['y_pred'],
            "artifacts/predicted_vs_actual.png"
        )
        mlflow.log_artifact(pred_path)
        
        # Save and log models
        model_path = save_models(
            classifier, regressor, 
            splits['scaler'], splits['feature_cols'], 
            config
        )
        mlflow.log_artifact(model_path)
        
        # Log models to MLFlow model registry
        mlflow.sklearn.log_model(classifier, "classifier")
        mlflow.sklearn.log_model(regressor, "regressor")
        
        print("\n✓ MLFlow run complete!")
        print(f"  Run ID: {mlflow.active_run().info.run_id}")
        
        return classifier, regressor, class_metrics, reg_metrics