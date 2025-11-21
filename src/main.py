"""
Main Pipeline - Run full training pipeline
"""
import yaml
from data_loader import load_config, load_data
from preprocessing import preprocess_data
from feature_engineering import create_features, create_target
from train import prepare_splits, train_classifier, train_regressor, save_models


def run_pipeline(config_path="../config/config.yaml"):
    """Run the complete ML pipeline."""
    print("=" * 70)
    print("FROM AIR TO CARE - ML PIPELINE")
    print("=" * 70)
    
    # Load config
    config = load_config(config_path)
    print(f"✓ Config loaded from {config_path}")
    
    # Step 1: Load data
    df_weather, df_resp, df_asthma, df_airq = load_data(config)
    
    # Step 2: Preprocess
    df_processed = preprocess_data(df_weather, df_resp, df_asthma, df_airq, config)
    
    # Step 3: Feature engineering
    df_featured = create_features(df_processed, config)
    df_final = create_target(df_featured, config)
    
    # Step 4: Prepare splits
    splits = prepare_splits(df_final, config)
    
    # Step 5: Train models
    classifier, class_metrics = train_classifier(splits, config)
    regressor, reg_metrics = train_regressor(splits, config)
    
    # Step 6: Save models
    save_models(classifier, regressor, splits['scaler'], splits['feature_cols'], config)
    
    print("\n" + "=" * 70)
    print("✓ PIPELINE COMPLETE!")
    print("=" * 70)
    
    return {
        'classifier': classifier,
        'regressor': regressor,
        'class_metrics': class_metrics,
        'reg_metrics': reg_metrics
    }


if __name__ == "__main__":
    results = run_pipeline()
