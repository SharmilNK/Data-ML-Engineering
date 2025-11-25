"""
Data Loader - Downloads and loads data from GCS
"""
import os
import pandas as pd
import yaml
from google.cloud import storage

def setup_credentials():
    """Setup GCS credentials from file or environment variable."""
    
    # Check if GOOGLE_APPLICATION_CREDENTIALS is already set
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if os.path.exists(cred_path):
            print(f"✓ Using credentials from environment: {cred_path}")
            return True
    
    # Build absolute path to credentials file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_file = os.path.join(project_root, 'data', 'gcs-credentials.json')
    
    # Check if credentials file exists
    if os.path.exists(cred_file):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_file
        print(f"✓ Using credentials from: {cred_file}")
        return True
    
    # Check if credentials are in environment variable
    creds_json = os.environ.get("GCS_CREDENTIALS_JSON")
    if creds_json:
        # Write to temp file
        temp_cred_file = "/tmp/gcs-credentials.json"
        with open(temp_cred_file, "w") as f:
            f.write(creds_json)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_cred_file
        print(f"✓ Using credentials from environment variable, written to: {temp_cred_file}")
        return True
    
    # If no credentials found, show warning
    print("⚠ Warning: No GCS credentials found!")
    print("  Please either:")
    print("  1. Place gcs-credentials.json in data/ folder")
    print("  2. Set GCS_CREDENTIALS_JSON environment variable")
    return False



def load_config(config_path=None):
    """Load configuration from YAML file."""
    # Build the config path if not provided
    if config_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
    
    print(f"Loading config from: {config_path}")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    return config


def download_from_gcs(bucket_name, source_blob, destination):
    """Download a single file from GCS."""
    # Setup credentials before accessing GCS
    setup_credentials()
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Download the file
    blob.download_to_filename(destination)
    print(f"✓ Downloaded {source_blob}")


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
