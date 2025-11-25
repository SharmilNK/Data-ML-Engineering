# From Air to Care: Predicting Tomorrow's ER Strain Today

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)
![GCP](https://img.shields.io/badge/Google_Cloud-Deployed-red.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B.svg)

**Using alternative data (weather, air quality, health records) to forecast hospital admissions 3-7 days in advance.**

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Model Architecture and Evaluation](#model-architecture-and-evaluation)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Train the Model](#how-to-train-the-model)
- [How to Build and Test the API Locally](#how-to-build-and-test-the-api-locally)
- [How to Deploy to the Cloud](#how-to-deploy-to-the-cloud)
- [MLFlow Experiment Tracking](#mlflow-experiment-tracking)
- [Frontend Application](#frontend-application)
- [Cloud Services Used](#cloud-services-used)
- [Ethical Considerations & Limitations](#ethical-considerations--limitations)
- [Future Work](#future-work)
- [Acknowledgments](#acknowledgments)
- [AI Citation](#ai-citation)

---

## Project Overview

**From Air to Care** is a machine learning system that predicts hospital admission surges in NYC boroughs based on environmental factors. The system helps hospitals proactively allocate resources, reduce costs, and improve patient outcomes.

### Project Goals

- **Predictive Modeling:** Forecast hospital admissions 3-7 days in advance using environmental data
- **Resource Optimization:** Enable proactive resource allocation to reduce costs by 15-25%
- **Borough-Specific Insights:** Provide separate predictions for each NYC borough
- **Reproducible Pipeline:** Build a containerized, version-controlled ML pipeline

### Key Features

- **Regression:** Predicts actual expected patient admission count
- **Borough-specific:** Separate predictions for Brooklyn, Bronx, Manhattan, Queens, Staten Island
- **3-7 day forecasting:** Advance warning for hospital planning

### Summary

We built a predictive system that forecasts hospital admissions 3-7 days in advance by combining air pollution, weather, and health data. Our models achieve **91% accuracy** in identifying high-risk days and predict patient volumes with **R² = 0.92**, enabling hospitals to optimize staffing and reduce surge-related costs by 15-25%.

### 🚀 Live Links

- **Deployed Frontend:** [https://from-air-to-care.streamlit.app/](https://from-air-to-care.streamlit.app/)
- **Deployed API:** [https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app](https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app)
- **API Docs (Swagger UI):** [https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/docs](https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/docs)

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

| Source | Description | Time Period | Link |
| :--- | :--- | :--- | :--- |
| **NOAA** | Weather data (temperature, humidity, wind, precipitation) | 2017-2024 | [NOAA Climate Data](https://www.ncei.noaa.gov/) |
| **AQNCI** | Air quality data (PM2.5, Ozone, NO2) | 2017-2024 | [Air Quality Network](https://www.airnow.gov/) |
| **NYC DOHMH** | Respiratory and Asthma ER visits | 2017-2024 | [NYC Open Data](https://data.cityofnewyork.us/Health) |

### Data Storage

Data is stored in **Google Cloud Storage (GCS)** bucket: `from-air-to-care-data-1990`

- Weather data: `nyc_weather_by_borough_2017-2024.csv`
- Respiratory data: `Respiratory.csv`
- Asthma data: `Asthama.csv`
- Air quality data: `Air_Quality.csv`

The pipeline automatically downloads data from GCS using `src/data_loader.py`.

### Data Statistics

| Metric | Value |
| :--- | :--- |
| Total Hospitalizations | 5,133,904 |
| Asthma Cases | 814,962 |
| Respiratory Cases | 4,318,942 |
| Boroughs | 5 |
| Features (after engineering) | 42 |
| Time Period | 2017-2024 |

### Target Variables

1. **Regression Target:** `Total_Hospitalization` (continuous)
   - Actual count of daily admissions
   - Evaluation metric: R² Score, MAE, RMSE

---

## Model Architecture and Evaluation

### Model Architecture

We use **Gradient Boosting** models (from scikit-learn) for both classification and regression tasks:

#### Classification Model
- **Algorithm:** GradientBoostingClassifier
- **Purpose:** Predict if a day will be "high-risk" (top 25% admission volume)
- **Parameters:**
  - `n_estimators`: 100
  - `max_depth`: 5
  - `random_state`: 42
- **Threshold:** Top 25% of admission days (≥754 admissions) = High Risk

#### Regression Model
- **Algorithm:** GradientBoostingRegressor
- **Purpose:** Predict actual patient admission count
- **Parameters:**
  - `n_estimators`: 100
  - `max_depth`: 5
  - `random_state`: 42

### Feature Engineering

The pipeline creates 42 features including:
- **Weather features:** Temperature (max/min), humidity, precipitation, wind speed
- **Air quality features:** PM2.5, Ozone, NO₂ concentrations
- **Temporal features:** Month, day, day of week, quarter, season
- **Borough features:** One-hot encoded borough indicators
- **Lag features:** 7-day lag of hospitalizations, temperature, humidity
- **Rolling features:** 7-day rolling averages

### Model Performance

#### Classification Results (High-Risk Day Prediction)

| Model | Accuracy | AUROC | Recall | Precision | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting** | **91.8%** | **0.965** | 80.0% | **82.2%** | **0.811** |
| SVM | 89.5% | 0.949 | 78.5% | 75.0% | 0.767 |
| Random Forest | 88.5% | 0.937 | 83.2% | 70.2% | 0.762 |
| Logistic Regression | 87.3% | 0.943 | **85.4%** | 66.7% | 0.749 |

#### Regression Results (Patient Volume Prediction)

| Model | R² Score | MAE | RMSE | MAPE |
| :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting** | **0.919** | **±57.8** | **74.8** | 12.7% |
| Random Forest | 0.904 | ±57.8 | 81.5 | **10.9%** |
| Lasso Regression | 0.842 | ±80.8 | 104.5 | 17.2% |

### Train/Validation/Test Split

- **Training:** 2017-2019
- **Validation:** 2023
- **Test:** 2024

---

## Project Structure

```
Data-ML-Engineering
├── api
│   └── app.py
├── config
│   └── config.yaml
├── frontend
│   └── app_ui.py
├── src
│   ├── artifacts
│   │   ├── confusion_matrix.png
│   │   ├── predicted_vs_actual.png
│   │   └── roc_curve.png
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── main.py
│   ├── predict.py
│   ├── preprocessing.py
│   └── train.py
├── .dockerignore
├── .gcloudignore
├── .gitignore
├── Dockerfile
├── README.md
├── cloudbuild.yaml
├── entrypoint.py
├── requirements.txt
├── runtime.txt
└── test_api.py

```

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker Desktop (optional, for containerized runs)
- Google Cloud account (for data storage)
- Git

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

Edit `config/config.yaml` with your settings:

```yaml
data:
  bucket_name: "from-air-to-care-data-1990"
```

---

## How to Train the Model

### Option 1: Run Locally

```bash
# From project root
cd src
python main.py

# Or from project root
python -m src.main
```

### Option 2: Run with Docker

To ensure reproducibility, you can run the training pipeline inside a container:

```bash
# 1. Build the image
docker build -t from-air-to-care .

# 2. Run training (mounting local volumes for credentials and output)
# Note: For Windows PowerShell, use ${PWD}. For Command Prompt, use %cd%. For Mac/Linux use $(pwd).
docker run -e PYTHONPATH=/app \
  -v "${PWD}/data/gcs-credentials.json:/app/data/gcs-credentials.json" \
  -v "${PWD}/models:/app/models" \
  -v "${PWD}/src/mlruns:/app/src/mlruns" \
  from-air-to-care train
```

### Expected Output

```
======================================================================
STARTING TRAINING PIPELINE
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

## How to Build and Test the API Locally

### 1. Build and Run API Locally

#### Option A: Using Python directly

```bash
# Ensure models are trained first (models/models.pkl exists)
# Run the FastAPI server locally
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

#### Option B: Using Docker

```bash
# Build the image
docker build -t from-air-to-care .

# Run API server
docker run -p 8000:8000 \
  -v "${PWD}/models:/app/models" \
  -v "${PWD}/src/models:/app/src/models" \
  from-air-to-care serve
```

The API will be available at `http://localhost:8000`

### 2. Test API Endpoints

#### Using curl

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Root Endpoint:**
```bash
curl http://localhost:8000/
```

**Make a Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Temp_Max_C": 25.0,
    "Temp_Min_C": 15.0,
    "Humidity_Avg": 70.0,
    "month": 6,
    "day": 15,
    "day_of_week": 5,
    "quarter": 2,
    "season": 3,
    "borough": "brooklyn"
  }'
```

#### Using Python test script

We provide a test script for automated testing:

```bash
# Test local API
python test_api.py http://localhost:8000

# Test deployed API
python test_api.py https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app
```

#### Using Postman

1. Import the API collection from Swagger UI: `http://localhost:8000/docs`
2. Or manually create requests:
   - **GET** `http://localhost:8000/health`
   - **POST** `http://localhost:8000/predict` with JSON body

### 3. Interactive API Documentation

Once the API is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## How to Deploy to the Cloud

We deploy the API to **Google Cloud Run** for serverless hosting.

### Prerequisites

1. Google Cloud account with billing enabled
2. Google Cloud SDK installed (`gcloud`)
3. Docker installed (for local builds)

### Step 1: Set Up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Push Docker Image

#### Option A: Using Cloud Build (Recommended)

```bash
# Build and deploy in one command
gcloud builds submit --config cloudbuild.yaml
```

#### Option B: Manual Build and Push

```bash
# Build the image for amd64 platform (required for Cloud Run)
docker build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/from-air-to-care-api:latest .

# Configure Docker to use gcloud credentials
gcloud auth configure-docker

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/from-air-to-care-api:latest
```

### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy from-air-to-care-api \
  --image gcr.io/YOUR_PROJECT_ID/from-air-to-care-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars PYTHONUNBUFFERED=1
```

### Step 4: Get API URL

```bash
gcloud run services describe from-air-to-care-api \
  --region us-central1 \
  --format 'value(status.url)'
```

### Step 5: Test Deployed API

```bash
# Health check
curl https://YOUR_API_URL/health

# Make a prediction
curl -X POST "https://YOUR_API_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "month": 6,
    "day": 15,
    "day_of_week": 5,
    "quarter": 2,
    "season": 3,
    "borough": "brooklyn"
  }'
```

### Deployed API

**Production API:** https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app

**API Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Make predictions
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

---

## MLFlow Experiment Tracking

### View Experiments

After training, launch MLFlow UI:

```bash
mlflow ui
```

Then open: http://localhost:5000

### What's Tracked

- **Parameters:** model type, n_estimators, max_depth, threshold_percentile, train_years, test_year
- **Metrics:** accuracy, AUROC, recall, precision, F1-score, R², MAE, RMSE
- **Artifacts:** 
  - Trained models (`models.pkl`)
  - Confusion matrix plots (`confusion_matrix.png`)
  - ROC curves (`roc_curve.png`)
  - Predicted vs actual plots (`predicted_vs_actual.png`)

### Comparing Runs

MLFlow allows you to:
- Compare multiple experiment runs side-by-side
- Track model versioning
- Reproduce any previous experiment
- View parameter and metric history

### MLFlow Configuration

MLFlow is configured in `config/config.yaml`:

```yaml
mlflow:
  experiment_name: "from-air-to-care"
  tracking_uri: "mlruns"
```

---

## Frontend Application

### 🌐 Live Frontend Application

**Deployed Frontend:** [https://from-air-to-care.streamlit.app/](https://from-air-to-care.streamlit.app/)

The frontend application is now live and publicly accessible!

### Frontend Features

The frontend application provides an interactive web interface to:

- **Select a date** (between January 1, 2022 and December 31, 2024)
- **Select a NYC borough** (Brooklyn, Bronx, Manhattan, Queens, Staten Island)
- **Get real-time predictions** from the deployed API
- **View predicted hospital admission counts** with detailed information

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
- Results visualization with prominent display
- Responsive layout using Streamlit columns

### Frontend Requirements

The frontend requires:
- `streamlit>=1.26.0`
- `requests>=2.31.0`

These are already included in `requirements.txt`.

---

## Cloud Services Used

| Service | Purpose |
| :--- | :--- |
| **Google Cloud Storage (GCS)** | Store raw CSV data files |
| **MLFlow** | Experiment tracking and model versioning |
| **Docker** | Containerization for reproducibility |
| **Google Cloud Run** | Host API endpoint for model predictions |
| **Streamlit Cloud** | Host frontend application |

---

## Ethical Considerations & Limitations

As part of our commitment to responsible AI, we have identified the following considerations:

- **Data Bias:** Our training data relies on historical hospital admissions. If certain demographics have historically faced barriers to accessing healthcare, the model may under-predict demand in those communities, potentially perpetuating resource inequity.

- **Correlation vs. Causation:** While air quality is a strong predictor, the model does not prove causality. High pollution days often correlate with other factors (e.g., high traffic) that might also influence ER visits.

- **Privacy:** All data used is aggregated at the borough level. No individual patient health information (PHI) was accessed or processed, ensuring compliance with privacy standards.

- **Scope Limitation:** The model is currently trained only on NYC data. It should not be generalized to other cities without retraining on local environmental and health data.

- **Model Limitations:** The model predicts based on historical patterns and may not account for novel events (e.g., new diseases, extreme weather events not seen in training data).

---

## Future Work

- **Real-time Data Integration:** Integrate live weather and air quality APIs for real-time predictions
- **Multi-city Expansion:** Extend the model to other cities with similar data availability
- **Advanced Models:** Experiment with deep learning models (LSTM, Transformer) for time series forecasting
- **Dashboard Development:** Create an admin dashboard for hospital staff to monitor predictions
- **Alert System:** Implement automated alerting for high-risk days
- **Model Retraining Pipeline:** Set up automated retraining pipeline with new data
- **Feature Engineering:** Explore additional features (holidays, events, social factors)

---

## Acknowledgments

- NYC Department of Health and Mental Hygiene (DOHMH) for health data
- NOAA for weather data
- EPA for air quality data
- Google Cloud Platform for cloud infrastructure
- Streamlit for frontend framework

---

## AI Citation

For our project, the following AI tools were utilized to assist in development, analysis, and documentation:

- **Composer 1:** Used on November 24, 2025, for the UI design of the frontend application.

- **Claude Sonnet 4.5:** Used on November 21 and 24, 2025, to assist with code debugging and error correction.

- **Gemini 3 Pro:** Used on November 24, 2025, to assist with the revision, formatting, and completion of the README file.

- **ChatGPT 5.1:** Used on November 21, 2025, to provide guidance on cloud data deployment, Docker containerization strategies, and instructions for deploying the Front-End Interface.
