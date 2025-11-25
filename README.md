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

- **Regression:** Predicts actual expected patient admission count
- **Borough-specific:** Separate predictions for Brooklyn, Bronx, Manhattan, Queens, Staten Island
- **3-7 day forecasting:** Advance warning for hospital planning

### Summary

We built a predictive system that forecasts hospital admissions 3-7 days in advance by combining air pollution, weather, and health data. Our models achieve **91% accuracy** in identifying high-risk days and predict patient volumes with **R² = 0.92**, enabling hospitals to optimize staffing and reduce surge-related costs by 15-25%.

### 🚀 Live API

**Deployed API:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app
**API Documentation:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/docs

### 🌐 Live Frontend

**Deployed Frontend:** https://from-air-to-care.streamlit.app/

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

| Source              | Description                                               | Time Period |
| ------------------- | --------------------------------------------------------- | ----------- |
| **NOAA**      | Weather data (temperature, humidity, wind, precipitation) | 2017-2024   |
| **AQNCI**     | Air quality data (PM2.5, Ozone, NO2)                      | 2017-2024   |
| **NYC DOHMH** | Respiratory and Asthma ER visits                          | 2017-2024   |

### Data Statistics

| Metric                       | Value     |
| ---------------------------- | --------- |
| Total Hospitalizations       | 5,133,904 |
| Asthma Cases                 | 814,962   |
| Respiratory Cases            | 4,318,942 |
| Boroughs                     | 5         |
| Features (after engineering) | 42        |

### Target Variables

1. **Regression Target:** `Total_Hospitalization` (continuous)
   - Actual count of daily admissions

---

## Model Performance

### Classification Results (High-Risk Day Prediction)

| Model                       | Accuracy | AUROC | Recall | Precision | F1-Score |
| --------------------------- | -------- | ----- | ------ | --------- | -------- |
| **Gradient Boosting** | 91.8%    | 0.965 | 80.0%  | 82.2%     | 0.811    |
| SVM                         | 89.5%    | 0.949 | 78.5%  | 75.0%     | 0.767    |
| Random Forest               | 88.5%    | 0.937 | 83.2%  | 70.2%     | 0.762    |
| Logistic Regression         | 87.3%    | 0.943 | 85.4%  | 66.7%     | 0.749    |
| K-Nearest Neighbors         | 88.3%    | 0.919 | 74.3%  | 73.2%     | 0.738    |
| Decision Tree               | 84.0%    | 0.845 | 77.5%  | 61.0%     | 0.683    |

### Regression Results (Patient Volume Prediction)

| Model                       | R² Score | MAE     | RMSE  | MAPE  |
| --------------------------- | --------- | ------- | ----- | ----- |
| **Gradient Boosting** | 0.919     | ±57.8  | 74.8  | 12.7% |
| Random Forest               | 0.904     | ±57.8  | 81.5  | 10.9% |
| Lasso Regression            | 0.842     | ±80.8  | 104.5 | 17.2% |
| Ridge Regression            | 0.733     | ±111.4 | 136.0 | 28.3% |

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

- Python 3.11
- Docker Desktop
- Google Cloud account (for data storage)

### 1. Clone the Repository

```bash
git clone https://github.com/SharmilNK/Data-ML-Engineering.git
cd Data-ML-Engineering
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

# Run training
docker run -e PYTHONPATH=/app/src -w /app `
  -v "C:\PWD\src:/app/src" `
  -v "C:\PWD\config:/app/config" `
  -v "C:\PWD\data\gcs-credentials.json:/app/data/gcs-credentials.json" `
  -v "C:\PWD\entrypoint.py:/app/entrypoint.py" `
  from-air-to-care
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

### Docker Image Details

| Property     | Value            |
| ------------ | ---------------- |
| Base Image   | python:3.11-slim |
| Image Size   | ~1.5GB           |
| Exposed Port | 8000             |

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

---

## Cloud Services Used

| Service                        | Purpose                                  |
| ------------------------------ | ---------------------------------------- |
| **Google Cloud Storage** | Store raw CSV data files                 |
| **MLFlow**               | Experiment tracking and model versioning |
| **Docker**               | Containerization for reproducibility     |
| **Google Cloud Run**     | Host API endpoint for model predictions  |

---

### Deployed API URL

**Production API:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app

## Frontend Application

### 🌐 Live Frontend Application

**Deployed Frontend:** https://from-air-to-care.streamlit.app/

The frontend application is now live and publicly accessible!

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

- **Date Selection:** Simple date picker (January 1, 2022 - December 31, 2024)
  - Automatically extracts temporal features (month, day, day of week, quarter, season)
- **Borough Selection:** Choose from 5 NYC boroughs (Brooklyn, Bronx, Manhattan, Queens, Staten Island)
- **Results Display:**
  - Predicted hospital admission count (large, prominent display)
  - Exact prediction value
  - Date and borough information
  - Interpretation of the prediction

### Frontend Code Structure

```
frontend/
├── app_ui.py          # Main Streamlit application
```

The frontend requires:

- `streamlit>=1.26.0`
- `requests>=2.31.0`

These are already included in `requirements.txt`.

---

## Acknowledgments

- NYC Department of Health and Mental Hygiene (DOHMH)
- NOAA for weather data
- EPA for air quality data
