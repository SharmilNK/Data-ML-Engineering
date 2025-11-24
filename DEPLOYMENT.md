# Deployment Guide

This guide explains how to deploy the From Air to Care API to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account**: Sign up at https://cloud.google.com/
2. **Google Cloud SDK**: Install from https://cloud.google.com/sdk/docs/install
3. **Docker**: Install Docker Desktop (for local testing)
4. **Trained Model**: Ensure `src/models/models.pkl` exists (run training first)

## Step 1: Set Up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create from-air-to-care --name="From Air to Care"

# Set as active project
gcloud config set project from-air-to-care

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

## Step 2: Set Up GCS Credentials (Secret Manager)

```bash
# Create secret for GCS credentials
gcloud secrets create gcs-credentials \
  --data-file=data/gcs-credentials.json \
  --replication-policy="automatic"

# Grant Cloud Run access to the secret
gcloud secrets add-iam-policy-binding gcs-credentials \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**Note**: Replace `PROJECT_NUMBER` with your actual project number (find it with `gcloud projects describe from-air-to-care --format="value(projectNumber)"`)

## Step 3: Build and Push Docker Image

### Option A: Using Cloud Build (Recommended)

```bash
# Build and deploy in one command
gcloud builds submit --config cloudbuild.yaml
```

### Option B: Manual Build and Push

```bash
# Build the image
docker build -t gcr.io/PROJECT_ID/from-air-to-care-api .

# Push to Container Registry
docker push gcr.io/PROJECT_ID/from-air-to-care-api
```

## Step 4: Deploy to Cloud Run

### Option A: Using Cloud Build (Already done if you used cloudbuild.yaml)

The `cloudbuild.yaml` file automatically deploys after building.

### Option B: Manual Deployment

```bash
gcloud run deploy from-air-to-care-api \
  --image gcr.io/PROJECT_ID/from-air-to-care-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-secrets /app/data/gcs-credentials.json=gcs-credentials:latest \
  --command python \
  --args "entrypoint.py,serve"
```

## Step 5: Get Your API URL

```bash
# Get the deployed URL
gcloud run services describe from-air-to-care-api \
  --region us-central1 \
  --format 'value(status.url)'
```

The output will be something like: `https://from-air-to-care-api-xxxxx-uc.a.run.app`

## Step 6: Test Your Deployed API

```bash
# Set your API URL
API_URL=$(gcloud run services describe from-air-to-care-api \
  --region us-central1 \
  --format 'value(status.url)')

# Test health endpoint
curl $API_URL/health

# Test prediction endpoint
curl -X POST "$API_URL/predict" \
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

## Local Testing Before Deployment

### Test API Locally

```bash
# Build Docker image locally
docker build -t from-air-to-care-api .

# Run API server locally
docker run -p 8000:8000 \
  -v $(pwd)/data/gcs-credentials.json:/app/data/gcs-credentials.json \
  from-air-to-care-api serve

# In another terminal, test the API
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Temp_Max_C": 25.0,
    "Temp_Min_C": 15.0,
    "Humidity_Avg": 70.0,
    "month": 6,
    "day": 15,
    "day_of_week": 5,
    "borough": "brooklyn"
  }'
```

## Troubleshooting

### Model Not Found Error

If you see `FileNotFoundError: Model file not found`, ensure:
1. Model file exists at `src/models/models.pkl`
2. Model file is included in Docker image (check `.dockerignore`)
3. Model file path is correct in `src/predict.py`

### GCS Credentials Error

If you see GCS authentication errors:
1. Ensure secret is created: `gcloud secrets list`
2. Check IAM permissions for Cloud Run service account
3. Verify secret path in deployment command

### API Timeout

If API requests timeout:
1. Increase timeout: `--timeout 300`
2. Check Cloud Run logs: `gcloud run services logs read from-air-to-care-api --region us-central1`

### Memory Issues

If you see out-of-memory errors:
1. Increase memory: `--memory 4Gi`
2. Check model size: `ls -lh src/models/models.pkl`

## Updating Deployment

To update your deployment after code changes:

```bash
# Rebuild and redeploy
gcloud builds submit --config cloudbuild.yaml
```

Or manually:

```bash
# Rebuild image
docker build -t gcr.io/PROJECT_ID/from-air-to-care-api .

# Push new image
docker push gcr.io/PROJECT_ID/from-air-to-care-api

# Update Cloud Run service
gcloud run deploy from-air-to-care-api \
  --image gcr.io/PROJECT_ID/from-air-to-care-api:latest \
  --region us-central1
```

## Cost Estimation

Cloud Run pricing (as of 2024):
- **Free tier**: 2 million requests/month, 360,000 GB-seconds memory
- **Pay-as-you-go**: ~$0.40 per million requests, ~$0.0000025 per GB-second

For this API:
- Estimated cost: **$0-5/month** for light usage
- Free tier should cover most academic/testing use cases

## Security Best Practices

1. **Use Secret Manager** for credentials (already configured)
2. **Enable authentication** for production: Remove `--allow-unauthenticated`
3. **Set up IAM** roles for least privilege access
4. **Enable Cloud Armor** for DDoS protection (optional)
5. **Use HTTPS** (automatically enabled by Cloud Run)

## Next Steps

1. Update frontend `app_ui.py` to use the deployed API URL
2. Deploy frontend to Streamlit Cloud or Vercel
3. Set up monitoring and alerts in Cloud Console
4. Configure custom domain (optional)

