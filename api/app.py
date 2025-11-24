from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import ModelService

app = FastAPI(
    title="From Air to Care API",
    description="Predict hospital admissions based on environmental factors",
    version="1.0"
)

# Initialize model service
model_service = None

@app.on_event("startup")
def load_model():
    global model_service
    try:
        model_service = ModelService()
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        raise

class PredictionRequest(BaseModel):
    """Request model for prediction."""
    # Weather features
    Temp_Max_C: Optional[float] = None
    Temp_Min_C: Optional[float] = None
    Humidity_Avg: Optional[float] = None
    Precip_mm: Optional[float] = None
    WindSpeed_mps: Optional[float] = None
    
    # Air quality features (if available)
    AQ_PM2_5: Optional[float] = None
    AQ_Ozone: Optional[float] = None
    AQ_NO2: Optional[float] = None
    
    # Temporal features
    month: Optional[int] = None
    day: Optional[int] = None
    day_of_week: Optional[int] = None
    quarter: Optional[int] = None
    season: Optional[int] = None
    
    # Borough (will be one-hot encoded)
    borough: Optional[str] = None  # "brooklyn", "bronx", "manhattan", "queens", "staten island"
    
    # Lag features (if available)
    Total_Hospitalization_lag7: Optional[float] = None
    Temp_Max_C_lag7: Optional[float] = None
    Humidity_Avg_lag7: Optional[float] = None
    
    # Rolling features
    Total_Hospitalization_roll7: Optional[float] = None
    Temp_Max_C_roll7: Optional[float] = None

@app.get("/")
def read_root():
    return {
        "message": "Welcome to From Air to Care API",
        "endpoints": {
            "/predict": "POST - Make predictions",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    if model_service is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Predict hospital admissions.
    
    Returns both classification (high-risk day) and regression (admission count).
    """
    if not model_service:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert Pydantic model to dict (Pydantic v2 compatible)
        input_dict = request.model_dump(exclude_none=True)
        
        # Handle borough one-hot encoding
        if 'borough' in input_dict:
            borough = input_dict['borough'].lower().strip()
            valid_boroughs = ['brooklyn', 'bronx', 'manhattan', 'queens', 'staten island']
            if borough in valid_boroughs:
                # Add one-hot encoded borough columns
                for b in valid_boroughs:
                    input_dict[f'borough_{b.replace(" ", "_")}'] = 1 if b == borough else 0
            del input_dict['borough']
        
        # Make predictions
        result = model_service.predict(input_dict)
        
        return {
            "success": True,
            "predictions": {
                "classification": {
                    "is_high_risk": result['classification']['is_high_risk'],
                    "probability": result['classification']['probability']
                },
                "regression": {
                    "predicted_admissions": result['regression']['predicted_count'],
                    "predicted_admissions_rounded": result['regression']['prediction']
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")