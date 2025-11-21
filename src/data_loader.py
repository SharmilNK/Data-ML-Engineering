"""
Data Loader - Downloads and loads data from GCS
"""
import os
import pandas as pd
import yaml
from google.cloud import storage


def load_config(config_path="../config/config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def download_from_gcs(bucket_name, source_blob, destination):
    """Download a single file from GCS."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../data/gcs-credentials.json"
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob)
    
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    blob.download_to_filename(destination)
    print(f" Downloaded {source_blob}")


def load_data(config):
    """Load all datasets from cloud storage."""
     
    print("LOADING DATA FROM CLOUD")
    
    
    bucket = config["data"]["bucket_name"]
    local_path = config["data"]["local_path"]
    files = config["data"]["files"]
    
    # Download files if not present locally
    for key, filename in files.items():
        local_file = f"{local_path}/{filename}"
        if not os.path.exists(local_file):
            download_from_gcs(bucket, filename, local_file)
        else:
            print(f"{filename} already exists locally")
    
    # Load into DataFrames
    print("\nLoading DataFrames...")
    
    df_weather = pd.read_csv(
        f"{local_path}/{files['weather']}", 
        index_col=1, 
        parse_dates=True
    )
    df_respiratory = pd.read_csv(
        f"{local_path}/{files['respiratory']}", 
        index_col=6, 
        parse_dates=True
    )
    df_asthma = pd.read_csv(
        f"{local_path}/{files['asthma']}", 
        index_col=6, 
        parse_dates=True
    )
    df_air_quality = pd.read_csv(
        f"{local_path}/{files['air_quality']}", 
        index_col=6, 
        parse_dates=True
    )
    
    print(f" Weather data: {df_weather.shape}")
    print(f" Respiratory data: {df_respiratory.shape}")
    print(f" Asthma data: {df_asthma.shape}")
    print(f" Air quality data: {df_air_quality.shape}")
    
    return df_weather, df_respiratory, df_asthma, df_air_quality


if __name__ == "__main__":
    config = load_config()
    load_data(config)
