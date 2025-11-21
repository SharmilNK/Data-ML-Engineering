"""
Download data from Google Cloud Storage
"""
import os
from google.cloud import storage

def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """Download a file from GCS bucket."""
    
    # Set credentials path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcs-credentials.json"
    
    # Initialize client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    # Download
    blob.download_to_filename(destination_file_name)
    print(f"✓ Downloaded {source_blob_name} to {destination_file_name}")


def download_all_data():
    """Download all required datasets."""
    
    BUCKET_NAME = "from-air-to-care-data-1990"  # Your bucket name
    
    files = [
        "nyc_weather_by_borough_2017-2024.csv",
        "Respiratory.csv",
        "Asthama.csv",
        "Air_Quality.csv"
    ]
    
    # Create data directory if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)
    
    for file in files:
        download_from_gcs(
            bucket_name=BUCKET_NAME,
            source_blob_name=file,
            destination_file_name=f"data/raw/{file}"
        )
    
    print("\n All data downloaded successfully!")


if __name__ == "__main__":
    download_all_data()
