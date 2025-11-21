"""
Feature Engineering - Create features for modeling
"""
import pandas as pd
import numpy as np


def create_features(df, config):
    """Create all features for modeling."""
    print("=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)
    
    df = df.copy()
    
    # Temporal features
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['quarter'] = df['Date'].dt.quarter
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['season'] = df['month'].map({
        12:1, 1:1, 2:1,   # Winter
        3:2, 4:2, 5:2,    # Spring
        6:3, 7:3, 8:3,    # Summer
        9:4, 10:4, 11:4   # Fall
    })
    
    print("✓ Temporal features created")
    
    # One-hot encode borough
    if 'borough' in df.columns:
        df = pd.get_dummies(df, columns=['borough'], prefix='borough')
        print("✓ Borough one-hot encoded")
    
    # Sort for lag features
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Lag features
    lag_days = config["features"]["lag_days"]
    lag_cols = ['Total_Hospitalization', 'Temp_Max_C', 'Humidity_Avg']
    
    for col in lag_cols:
        if col in df.columns:
            for lag in lag_days:
                df[f'{col}_lag{lag}'] = df[col].shift(lag)
    
    print(f"✓ Lag features created (lags: {lag_days})")
    
    # Rolling averages with shift
    rolling_window = config["features"]["rolling_window"]
    rolling_shift = config["features"]["rolling_shift"]
    
    for col in ['Total_Hospitalization', 'Temp_Max_C']:
        if col in df.columns:
            df[f'{col}_roll{rolling_window}'] = (
                df[col].rolling(window=rolling_window, min_periods=1).mean().shift(rolling_shift)
            )
    
    print(f"✓ Rolling features created (window: {rolling_window}, shift: {rolling_shift})")
    
    # Temperature range
    if 'Temp_Max_C' in df.columns and 'Temp_Min_C' in df.columns:
        df['Temp_Range'] = df['Temp_Max_C'] - df['Temp_Min_C']
    
    # Drop NaN in target
    df = df.dropna(subset=['Total_Hospitalization'])
    
    print(f"\n✓ Final feature set shape: {df.shape}")
    return df


def create_target(df, config):
    """Create binary target variable."""
    threshold_pct = config["target"]["threshold_percentile"]
    threshold = df['Total_Hospitalization'].quantile(threshold_pct / 100)
    
    df['High_Risk'] = (df['Total_Hospitalization'] >= threshold).astype(int)
    
    print(f"\n✓ Target created (threshold: {threshold:.0f} at {threshold_pct}th percentile)")
    print(f"  Class distribution: {df['High_Risk'].value_counts().to_dict()}")
    
    return df
