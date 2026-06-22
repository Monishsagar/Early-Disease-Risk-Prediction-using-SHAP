"""
Dataset statistics API routes.
GET /api/dataset/stats/{disease} - Get dataset statistics and model performance
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.train import get_disease_metadata

router = APIRouter(prefix="/api", tags=["datasets"])


class DatasetStatsResponse(BaseModel):
    disease: str
    total_samples: int
    feature_count: int
    positive_cases: int
    accuracy: float
    auc_score: float
    augmentation_note: Optional[str] = None


@router.get("/dataset/stats/{disease}", response_model=DatasetStatsResponse)
async def get_dataset_stats(disease: str):
    """
    Get dataset statistics and model performance metrics.
    
    Returns:
        - total_samples: Total samples used for training
        - feature_count: Number of features
        - positive_cases: Number of positive cases (diseased)
        - accuracy: Model accuracy on test set
        - auc_score: ROC-AUC score on test set
        - augmentation_note: Note about dataset augmentation (if applied)
    """
    
    valid_diseases = ["heart", "diabetes", "liver", "kidney"]
    if disease not in valid_diseases:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid disease. Must be one of: {', '.join(valid_diseases)}"
        )
    
    try:
        metadata = get_disease_metadata(disease)
        
        if metadata is None:
            raise HTTPException(
                status_code=404,
                detail=f"Metadata not found for {disease}"
            )
        
        return DatasetStatsResponse(
            disease=disease,
            total_samples=metadata["total_samples"],
            feature_count=metadata["feature_count"],
            positive_cases=metadata["positive_cases"],
            accuracy=metadata["accuracy"],
            auc_score=metadata["auc_score"],
            augmentation_note=metadata.get("augmentation_note")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dataset stats: {str(e)}")
