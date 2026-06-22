"""
Prediction API routes for disease risk prediction.
POST /api/predict/{disease} - Make predictions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from models.predict import predict_disease_risk
from models.train import get_disease_model
import traceback
import sys

router = APIRouter(prefix="/api", tags=["prediction"])

# Request/Response models
class PredictionRequest(BaseModel):
    """Base class for prediction requests - subclassed per disease"""
    pass


class RiskFactor(BaseModel):
    feature: str
    contribution: str
    shap_value: float
    feature_value: float


class PredictionResponse(BaseModel):
    risk_score: int
    risk_level: str
    confidence: float
    top_risk_factors: List[RiskFactor]
    recommendations: List[str]


@router.post("/predict/{disease}", response_model=PredictionResponse)
async def predict_disease(disease: str, data: Dict[str, Any]):
    """
    Predict disease risk for a patient.
    
    Accepts: JSON object with patient feature values
    Returns:
        - risk_score (0-100)
        - risk_level (Low/Moderate/High)
        - top_risk_factors (top 3 SHAP features)
        - confidence (raw probability)
        - recommendations (list of clinical recommendations)
    """
    
    # Validate disease
    valid_diseases = ["heart", "diabetes", "liver", "kidney"]
    if disease not in valid_diseases:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid disease. Must be one of: {', '.join(valid_diseases)}"
        )
    
    try:
        # Load model
        model = get_disease_model(disease)
        
        # Make prediction
        result = predict_disease_risk(data, disease, model)
        
        # Convert to response model
        response = PredictionResponse(
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            top_risk_factors=[RiskFactor(**factor) for factor in result["top_risk_factors"]],
            recommendations=result["recommendations"]
        )
        
        return response
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Print full traceback for debugging
        print(f"\n❌ ERROR in /api/predict/{disease}:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
