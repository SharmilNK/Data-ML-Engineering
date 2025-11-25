"""
Main Pipeline - Run full training pipeline
"""
import yaml
import os
from data_loader import load_config, load_data
from preprocessing import preprocess_data
from feature_engineering import create_features, create_target
from train import prepare_splits, run_mlflow_experiment


def run_pipeline(config_path=None):
    """Run the complete ML pipeline."""
    
    print("FROM AIR TO CARE - ML PIPELINE")
    # Build the config path if not provided
    # Build the config path if not provided
    if config_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
    
    # Load config (only once!)
    config = load_config(config_path)
    print(f" Config loaded from {config_path}")
    
    # Step 1: Load data
    df_weather, df_resp, df_asthma, df_airq = load_data(config)
    
    # Step 2: Preprocess
    df_processed = preprocess_data(df_weather, df_resp, df_asthma, df_airq, config)
    
    # Step 3: Feature engineering
    df_featured = create_features(df_processed, config)
    df_final = create_target(df_featured, config)
    
    # Step 4: Prepare splits
    splits = prepare_splits(df_final, config)
    
    # Step 5: Train with MLFlow tracking
    classifier, regressor, class_metrics, reg_metrics = run_mlflow_experiment(splits, config)
    

    print(" PIPELINE COMPLETE!")

    
    return {
        'classifier': classifier,
        'regressor': regressor,
        'class_metrics': class_metrics,
        'reg_metrics': reg_metrics
    }


if __name__ == "__main__":
    results = run_pipeline()
