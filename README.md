# From Air to Care

**Predicting Tomorrow's ER Strain Today**

Using alternative data (weather, air quality, health records) to forecast hospital admissions 3-7 days in advance.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Model Performance](#model-performance)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Train the Model](#how-to-train-the-model)
- [Docker](#docker)
- [MLFlow Experiment Tracking](#mlflow-experiment-tracking)
- [Cloud Services Used](#cloud-services-used)
- [API Deployment and Usage](#api-deployment-and-usage)
- [Frontend Application](#frontend-application)
- [Future Work](#future-work)

---

## Project Overview

**From Air to Care** is a machine learning system that predicts hospital admission surges in NYC boroughs based on environmental factors. The system helps hospitals proactively allocate resources, reduce costs, and improve patient outcomes.

### Key Features
- **Classification:** Predicts if a day will be "high-risk" (top 25% admission volume)
- **Regression:** Predicts actual patient admission count
- **Borough-specific:** Separate predictions for Brooklyn, Bronx, Manhattan, Queens, Staten Island
- **3-7 day forecasting:** Advance warning for hospital planning

### Summary
We built a predictive system that forecasts hospital admissions 3-7 days in advance by combining air pollution, weather, and health data. Our models achieve **91% accuracy** in identifying high-risk days and predict patient volumes with **R² = 0.92**, enabling hospitals to optimize staffing and reduce surge-related costs by 15-25%.

### 🚀 Live API
**Deployed API:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app  
**API Documentation:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/docs

---

## Problem Statement

### The Challenge
- Air pollution, extreme weather, and seasonal changes drive unexpected surges in ER visits
- Climate change is intensifying these health risks (wildfires, heatwaves, smog)
- Hospitals operate **reactively**, leading to overcrowding, stressed staff, and higher costs
- COVID-19 exposed the fragility of health systems

### Our Solution
- Predictive models using **alternative data** (weather + pollution + health)
- Forecast hospital strain **3-7 days in advance**
- Enable **proactive resource allocation**

### Impact
- 15-25% cost reduction through optimized resource allocation
- Better patient outcomes through preparation
- Data-driven capacity planning

---

## Dataset

### Data Sources

| Source | Description | Time Period |
|--------|-------------|-------------|
| **NOAA** | Weather data (temperature, humidity, wind, precipitation) | 2017-2024 |
| **AQNCI** | Air quality data (PM2.5, Ozone, NO2) | 2017-2024 |
| **NYC DOHMH** | Respiratory and Asthma ER visits | 2017-2024 |

### Data Statistics

| Metric | Value |
|--------|-------|
| Total Hospitalizations | 5,133,904 |
| Asthma Cases | 814,962 |
| Respiratory Cases | 4,318,942 |
| Boroughs | 5 |
| Features (after engineering) | 42 |

### Target Variables

1. **Classification Target:** `High_Risk` (binary)
   - 1 = Top 25% admission days (≥754 admissions)
   - 0 = Normal days

2. **Regression Target:** `Total_Hospitalization` (continuous)
   - Actual count of daily admissions

---

## Model Performance

### Classification Results (High-Risk Day Prediction)

| Model | Accuracy | AUROC | Recall | Precision | F1-Score |
|-------|----------|-------|--------|-----------|----------|
| **Gradient Boosting** | 91.8% | 0.965 | 80.0% | 82.2% | 0.811 |
| SVM | 89.5% | 0.949 | 78.5% | 75.0% | 0.767 |
| Random Forest | 88.5% | 0.937 | 83.2% | 70.2% | 0.762 |
| Logistic Regression | 87.3% | 0.943 | 85.4% | 66.7% | 0.749 |
| K-Nearest Neighbors | 88.3% | 0.919 | 74.3% | 73.2% | 0.738 |
| Decision Tree | 84.0% | 0.845 | 77.5% | 61.0% | 0.683 |

### Regression Results (Patient Volume Prediction)

| Model | R² Score | MAE | RMSE | MAPE |
|-------|----------|-----|------|------|
| **Gradient Boosting** | 0.919 | ±57.8 | 74.8 | 12.7% |
| Random Forest | 0.904 | ±57.8 | 81.5 | 10.9% |
| Lasso Regression | 0.842 | ±80.8 | 104.5 | 17.2% |
| Ridge Regression | 0.733 | ±111.4 | 136.0 | 28.3% |

### Environmental Impact Findings

| Factor | Impact on Admissions |
|--------|---------------------|
| Extreme Heat (>30°C) | +40% total, +57% asthma |
| High Humidity (>80%) | +17% asthma cases |
| High PM2.5 Days | +45% in Bronx, +38% in Brooklyn |

---

## Project Structure
```
from-air-to-care/
│
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition
├── .dockerignore               # Files to exclude from Docker
├── .gitignore                  # Files to exclude from Git
├── entrypoint.py               # Docker entry point script
|
│
├── config/
│   └── config.yaml             # Configuration file
│
├── data/
│   ├── gcs-credentials.json    # GCS credentials (gitignored)
│   └── raw/                    # Downloaded CSV files
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Load data from cloud
│   ├── preprocessing.py        # Clean and merge data
│   ├── feature_engineering.py  # Create features
│   └── train.py                # Train models with MLFlow
    ├── main.py                     # Main pipeline runner
|
│
├── models/                     # Saved trained models
│   └── models.pkl
│
├── artifacts/                  # Generated plots
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── predicted_vs_actual.png
│
└── mlruns/                     # MLFlow experiment tracking
```

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker Desktop
- Google Cloud account (for data storage)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/from-air-to-care.git
cd from-air-to-care
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Google Cloud Credentials

1. Create a GCS service account at https://console.cloud.google.com/iam-admin/serviceaccounts
2. Download the JSON key
3. Save it as `data/gcs-credentials.json`
4. This file is gitignored and must be created locally


### 5. Configure the Pipeline

Edit `config.yaml` with your settings:
```yaml
data:
  bucket_name: "from-air-to-care-data-1990"  
```

---

## How to Train the Model

### Option 1: Run Locally
```bash
python main.py
```

### Option 2: Run with Docker
```bash
# Build the image
docker build -t from-air-to-care .

# Run training (mount credentials)
docker run -v ${PWD}/data/gcs-credentials.json:/app/data/gcs-credentials.json from-air-to-care train
```

### Expected Output
```
======================================================================
FROM AIR TO CARE - ML PIPELINE WITH MLFLOW
======================================================================
✓ Config loaded from config.yaml
✓ Weather data: (9130, 9)
✓ Respiratory data: (12733, 6)
...
✓ Accuracy: 0.9175
✓ AUROC: 0.9651
✓ R²: 0.9191
✓ MAE: 57.82
...
✓ PIPELINE COMPLETE!
```

---

## Docker

### Build the Image
```bash
docker build -t from-air-to-care .
```

### Run Training
```bash
# Windows PowerShell
docker run -v ${PWD}/data/gcs-credentials.json:/app/data/gcs-credentials.json from-air-to-care train

# Mac/Linux
docker run -v $(pwd)/data/gcs-credentials.json:/app/data/gcs-credentials.json from-air-to-care train
```

### Run API Server
```bash
docker run -p 8000:8000 -v ${PWD}/data/gcs-credentials.json:/app/data/gcs-credentials.json from-air-to-care serve
```

### Docker Image Details

| Property | Value |
|----------|-------|
| Base Image | python:3.11-slim |
| Image Size | ~1.5GB |
| Exposed Port | 8000 |

---

## MLFlow Experiment Tracking

### View Experiments

After training, launch MLFlow UI:
```bash
mlflow ui
```

Then open: http://localhost:5000

### What's Tracked

- **Parameters:** model type, n_estimators, max_depth, threshold_percentile
- **Metrics:** accuracy, AUROC, recall, precision, R², MAE, RMSE
- **Artifacts:** confusion_matrix.png, roc_curve.png, models.pkl

### Comparing Runs

MLFlow allows you to:
- Compare multiple experiment runs side-by-side
- Track model versioning
- Reproduce any previous experiment

---

## Cloud Services Used

| Service | Purpose |
|---------|---------|
| **Google Cloud Storage** | Store raw CSV data files |
| **MLFlow** | Experiment tracking and model versioning |
| **Docker** | Containerization for reproducibility |
| **Google Cloud Run** | Host API endpoint for model predictions |

---

## API Deployment and Usage

### Local API Testing

Before deploying, test the API locally:

```bash
# Start the API server
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload

# Or using Docker
docker run -p 8000:8000 \
  -v $(pwd)/data/gcs-credentials.json:/app/data/gcs-credentials.json \
  from-air-to-care serve
```

### Test API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Make a Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Temp_Max_C": 25.0,
    "Temp_Min_C": 15.0,
    "Humidity_Avg": 70.0,
    "Precip_mm": 0.0,
    "month": 6,
    "day": 15,
    "day_of_week": 5,
    "quarter": 2,
    "season": 3,
    "borough": "brooklyn"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "predictions": {
    "classification": {
      "is_high_risk": false,
      "probability": {
        "normal": 0.85,
        "high_risk": 0.15
      }
    },
    "regression": {
      "predicted_admissions": 523.4,
      "predicted_admissions_rounded": 523
    }
  }
}
```

### Deploy to Google Cloud Run

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build and deploy
gcloud builds submit --config cloudbuild.yaml
```

**Get API URL:**
```bash
gcloud run services describe from-air-to-care-api \
  --region us-central1 \
  --format 'value(status.url)'
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Make predictions |

### API Request Format

The `/predict` endpoint accepts the following fields (all optional, missing values default to 0):

**Weather Features:**
- `Temp_Max_C`: Maximum temperature in Celsius
- `Temp_Min_C`: Minimum temperature in Celsius
- `Humidity_Avg`: Average humidity percentage
- `Precip_mm`: Precipitation in millimeters
- `WindSpeed_mps`: Wind speed in meters per second

**Air Quality Features:**
- `AQ_PM2_5`: PM2.5 concentration
- `AQ_Ozone`: Ozone concentration
- `AQ_NO2`: NO2 concentration

**Temporal Features:**
- `month`: Month (1-12)
- `day`: Day of month (1-31)
- `day_of_week`: Day of week (0=Monday, 6=Sunday)
- `quarter`: Quarter (1-4)
- `season`: Season (1=Winter, 2=Spring, 3=Summer, 4=Fall)

**Borough:**
- `borough`: One of "brooklyn", "bronx", "manhattan", "queens", "staten island"

**Lag Features (optional):**
- `Total_Hospitalization_lag7`: 7-day lag of total hospitalizations
- `Temp_Max_C_lag7`: 7-day lag of max temperature
- `Humidity_Avg_lag7`: 7-day lag of humidity

**Rolling Features (optional):**
- `Total_Hospitalization_roll7`: 7-day rolling average of hospitalizations
- `Temp_Max_C_roll7`: 7-day rolling average of temperature

### Deployed API URL

**Production API:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app

#### Test the Deployed API

**Health Check:**
```bash
curl https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/health
```

**Make a Prediction:**
```bash
curl -X POST "https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Temp_Max_C": 25.0,
    "Temp_Min_C": 15.0,
    "Humidity_Avg": 70.0,
    "Precip_mm": 0.0,
    "month": 6,
    "day": 15,
    "day_of_week": 5,
    "quarter": 2,
    "season": 3,
    "borough": "brooklyn"
  }'
```

**Using Python:**
```python
import requests

API_URL = "https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app"

# Health check
response = requests.get(f"{API_URL}/health")
print(response.json())

# Make prediction
prediction = requests.post(
    f"{API_URL}/predict",
    json={
        "Temp_Max_C": 25.0,
        "Temp_Min_C": 15.0,
        "Humidity_Avg": 70.0,
        "month": 6,
        "day": 15,
        "day_of_week": 5,
        "borough": "brooklyn"
    }
)
print(prediction.json())
```

**Interactive API Documentation:**
- Swagger UI: https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/docs
- ReDoc: https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/redoc

---

## Frontend Application

### 🌐 Live Frontend Application

**Deployed Frontend:** [Link will be added after deployment](#deploy-frontend-to-streamlit-cloud)

**Note:** After deploying to Streamlit Cloud, update this section with your live frontend URL.

The frontend application provides an interactive web interface to:
- Select a date (between January 1, 2022 and December 31, 2024)
- Select a NYC borough (Brooklyn, Bronx, Manhattan, Queens, Staten Island)
- Get real-time predictions from the deployed API
- View predicted hospital admission counts with detailed information

### Run Frontend Locally

**Prerequisites:**
- Python 3.8+
- Streamlit installed (`pip install streamlit`)

**Steps:**

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Run Streamlit app:**
   ```bash
   streamlit run app_ui.py
   ```

3. **Open in browser:**
   - The app will automatically open at `http://localhost:8501`
   - Or manually navigate to the URL shown in the terminal

4. **Configure API URL:**
   - The default API URL is set to the deployed production API
   - You can change it in the sidebar if testing with a local API

### Frontend Features

- **📅 Date Selection:** Simple date picker (January 1, 2022 - December 31, 2024)
  - Automatically extracts temporal features (month, day, day of week, quarter, season)
- **📍 Borough Selection:** Choose from 5 NYC boroughs (Brooklyn, Bronx, Manhattan, Queens, Staten Island)
- **📊 Results Display:**
  - Predicted hospital admission count (large, prominent display)
  - Exact prediction value
  - Date and borough information
  - Interpretation of the prediction

### Deploy Frontend to Streamlit Cloud

**Option 1: Streamlit Cloud (Recommended - Free)**

1. **Push your code to GitHub** (if not already done)

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure deployment:**
   - **Repository:** Select your GitHub repository
   - **Branch:** `main` (or your default branch)
   - **Main file path:** `frontend/app_ui.py`
   - **Python version:** 3.11

6. **Click "Deploy"**

7. **Your app will be live at:** `https://your-app-name.streamlit.app`

**Option 2: Other Platforms**

- **Hugging Face Spaces:** Upload to a Hugging Face Space with Streamlit
- **Vercel:** Deploy as a Python app (requires additional configuration)
- **Heroku:** Deploy using Procfile and requirements.txt

### Frontend Code Structure

```
frontend/
├── app_ui.py          # Main Streamlit application
```

**Key Components:**
- API health check (cached for 60 seconds)
- Form-based input collection
- Date picker with automatic feature extraction
- API request handling with error management
- Results visualization with color-coded risk indicators
- Responsive layout using Streamlit columns

### Frontend Requirements

The frontend requires:
- `streamlit>=1.26.0`
- `requests>=2.31.0`

These are already included in `requirements.txt`.

---

---

## Team




## Acknowledgments

- NYC Department of Health and Mental Hygiene (DOHMH)
- NOAA for weather data
- EPA for air quality data

