"""
Preprocessing - Clean and merge datasets
"""
import pandas as pd
import numpy as np


def reset_date_index(df, date_col_name='Date'):
    """Reset index and ensure Date column exists."""
    if isinstance(df.index, pd.DatetimeIndex) and date_col_name not in df.columns:
        df = df.reset_index()
        df.columns = [date_col_name if 'DATE' in col.upper() or i == 0 
                      else col for i, col in enumerate(df.columns)]
    
    if date_col_name in df.columns:
        df[date_col_name] = pd.to_datetime(df[date_col_name], errors='coerce')
    
    return df


def prepare_weather_data(df_weather):
    """Clean and prepare weather data."""
    print("\nPreparing weather data...")
    
    df = reset_date_index(df_weather, 'Date')
    
    weather_cols = {
        'TMAX': 'Temp_Max_C', 'TMIN': 'Temp_Min_C',
        'PRCP': 'Precip_mm', 'AWND': 'WindSpeed_mps',
        'RHAV': 'Humidity_Avg', 'RHMX': 'Humidity_Max', 'RHMN': 'Humidity_Min'
    }
    df = df.rename(columns=weather_cols)
    
    keep_cols = ['Date', 'borough'] + [c for c in weather_cols.values() if c in df.columns]
    df = df[[c for c in keep_cols if c in df.columns]].copy()
    
    df['borough'] = df['borough'].astype(str).str.strip().str.lower()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df = df.groupby(['Date', 'borough'], as_index=False)[numeric_cols.tolist()].mean()
    
    print(f"✓ Weather data shape: {df.shape}")
    return df


def prepare_health_data(df_resp, df_asthma, config):
    """Prepare respiratory and asthma data."""
    print("\nPreparing health data...")
    
    df_resp = reset_date_index(df_resp, 'Date')
    df_asthma = reset_date_index(df_asthma, 'Date')
    
    df_resp = df_resp.rename(columns={'Dim1Value': 'borough'})
    df_asthma = df_asthma.rename(columns={'Dim1Value': 'borough'})
    
    df_resp['borough'] = df_resp['borough'].astype(str).str.strip().str.lower()
    df_asthma['borough'] = df_asthma['borough'].astype(str).str.strip().str.lower()
    
    df_resp['Count'] = pd.to_numeric(df_resp['Count'], errors='coerce')
    df_asthma['Count'] = pd.to_numeric(df_asthma['Count'], errors='coerce')
    
    resp_agg = df_resp.groupby(['Date', 'borough'], as_index=False)['Count'].sum()
    resp_agg = resp_agg.rename(columns={'Count': 'Respiratory_Count'})
    
    asth_agg = df_asthma.groupby(['Date', 'borough'], as_index=False)['Count'].sum()
    asth_agg = asth_agg.rename(columns={'Count': 'Asthma_Count'})
    
    df_health = pd.merge(resp_agg, asth_agg, on=['Date', 'borough'], how='outer')
    df_health = df_health.fillna(0)
    
    df_health['Total_Hospitalization'] = (
        df_health['Respiratory_Count'] + df_health['Asthma_Count']
    )
    
    # Filter years based on config
    train_years = config["split"]["train_years"]
    val_year = config["split"]["val_year"]
    test_year = config["split"]["test_year"]
    all_years = train_years + [val_year, test_year]
    
    df_health['year'] = df_health['Date'].dt.year
    df_health = df_health[df_health['year'].isin(all_years)].copy()
    
    print(f"✓ Health data shape: {df_health.shape}")
    return df_health


def prepare_air_quality_data(df_airq):
    """Clean and prepare air quality data."""
    print("\nPreparing air quality data...")
    
    df = reset_date_index(df_airq, 'Start_Date')
    df = df.rename(columns={'Start_Date': 'Date'})
    
    if 'Geo Place Name' in df.columns:
        df = df.rename(columns={'Geo Place Name': 'borough'})
    
    df['borough'] = df['borough'].astype(str).str.strip().str.lower()
    
    if 'Name' in df.columns and 'Data Value' in df.columns:
        df_pivot = df.pivot_table(
            index=['Date', 'borough'],
            columns='Name',
            values='Data Value',
            aggfunc='mean'
        ).reset_index()
        
        df_pivot.columns.name = None
        pollutant_cols = [c for c in df_pivot.columns if c not in ['Date', 'borough']]
        
        rename_map = {c: f"AQ_{c.replace(' ', '_')}" for c in pollutant_cols}
        df_pivot = df_pivot.rename(columns=rename_map)
        
        print(f"✓ Air quality data shape: {df_pivot.shape}")
        return df_pivot
    
    return df


def merge_all_data(df_weather, df_health, df_airq, config):
    """Merge all datasets."""
    print("\nMerging all datasets...")
    
    df = df_health.copy()
    df = pd.merge(df, df_weather, on=['Date', 'borough'], how='left')
    
    if len(df_airq) > 0:
        df = pd.merge(df, df_airq, on=['Date', 'borough'], how='left')
    
    valid_boroughs = config["preprocessing"]["valid_boroughs"]
    df = df[df['borough'].isin(valid_boroughs)]
    
    print(f"✓ Merged data shape: {df.shape}")
    return df


def impute_missing(df):
    """Impute missing values."""
    print("\nImputing missing values...")
    
    df = df.sort_values(['borough', 'Date']).reset_index(drop=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df.groupby('borough')[col].transform(lambda x: x.ffill().bfill())
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mean(), inplace=True)
    
    print(f"✓ Missing values imputed")
    return df


def preprocess_data(df_weather, df_resp, df_asthma, df_airq, config):
    """Full preprocessing pipeline."""
    print("=" * 60)
    print("PREPROCESSING DATA")
    print("=" * 60)
    
    weather_clean = prepare_weather_data(df_weather)
    health_clean = prepare_health_data(df_resp, df_asthma, config)
    airq_clean = prepare_air_quality_data(df_airq)
    
    df_merged = merge_all_data(weather_clean, health_clean, airq_clean, config)
    df_final = impute_missing(df_merged)
    
    print(f"\n✓ Final preprocessed shape: {df_final.shape}")
    return df_final
