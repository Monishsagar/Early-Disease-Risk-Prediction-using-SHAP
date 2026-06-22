"""
Prediction logic for all disease models.
Handles input validation, preprocessing, and prediction with SHAP explanations.
"""

import numpy as np
from utils.preprocess import (
    preprocess_input_features, load_preprocessing_artifacts
)
from utils.explainability import get_shap_explanations, format_shap_explanation
from models.datasets_config import DATASETS_CONFIG, RISK_THRESHOLDS, CLINICAL_RECOMMENDATIONS
from models.train import get_disease_model
import pandas as pd


def validate_prediction_input(input_dict, disease):
    """
    Validate prediction input against clinical ranges.
    Raises ValueError if any feature is out of range or missing.
    """
    config = DATASETS_CONFIG[disease]
    
    for feature_name in config["features"]:
        if feature_name not in input_dict:
            raise ValueError(f"Missing required feature: {feature_name}")
        
        value = input_dict[feature_name]
        
        # Validate range
        if feature_name in config["feature_ranges"]:
            min_val, max_val = config["feature_ranges"][feature_name]
            if value < min_val or value > max_val:
                raise ValueError(
                    f"Feature '{feature_name}' value {value} is out of valid range [{min_val}, {max_val}]"
                )
    
    return True


def predict_disease_risk(input_dict, disease, model, X_background_sample=None):
    """
    Predict disease risk for a single patient.
    
    Args:
        input_dict: dict with feature values
        disease: disease name (heart, diabetes, liver, kidney)
        model: trained Random Forest model
        X_background_sample: background data for SHAP (optional, uses training data if not provided)
    
    Returns:
        dict with:
        - risk_score (0-100)
        - risk_level (Low/Moderate/High)
        - confidence (raw probability)
        - top_risk_factors (list of top 3 SHAP features)
        - recommendations (list of 3 clinical recommendations)
    """
    
    # Validate input
    validate_prediction_input(input_dict, disease)
    
    config = DATASETS_CONFIG[disease]
    
    # Load preprocessing artifacts
    encoders_dict, scaler = load_preprocessing_artifacts(disease)
    if encoders_dict is None or scaler is None:
        raise RuntimeError(f"Preprocessing artifacts not found for {disease}")
    
    # Preprocess input
    X_preprocessed = preprocess_input_features(input_dict, disease, encoders_dict, scaler)
    
    # Make prediction
    prediction_proba = model.predict_proba(X_preprocessed.reshape(1, -1))[0]
    risk_probability = prediction_proba[1]  # Probability of disease (positive class)
    risk_score = int(risk_probability * 100)
    
    # Determine risk level
    if risk_score < RISK_THRESHOLDS["low"]:
        risk_level = "Low"
    elif risk_score < RISK_THRESHOLDS["moderate"]:
        risk_level = "Moderate"
    else:
        risk_level = "High"
    
    # Get SHAP explanations
    feature_names = config["features"]
    
    # Create background sample if not provided (use random samples from preprocessed training data)
    if X_background_sample is None:
        X_background_sample = np.random.randn(100, len(config["features"])) * 0.1
    
    top_features = get_shap_explanations(
        model, X_preprocessed, X_background_sample, feature_names, top_k=3
    )
    
    # Format SHAP explanations for response
    top_risk_factors = format_shap_explanation(top_features, risk_score)
    
    # Generate clinical recommendations based on risk level and top factors
    recommendations = generate_recommendations(disease, risk_level, top_risk_factors)
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "confidence": float(risk_probability),
        "top_risk_factors": top_risk_factors,
        "recommendations": recommendations
    }


def generate_recommendations(disease, risk_level, top_risk_factors):
    """
    Generate clinical recommendations based on disease, risk level, and top risk factors.
    """
    base_recommendations = CLINICAL_RECOMMENDATIONS[disease][risk_level.lower()]
    
    # Enhance recommendations with top risk factors
    enhanced_recs = []
    for i, rec in enumerate(base_recommendations):
        if i < 2 and top_risk_factors:
            factor = top_risk_factors[i % len(top_risk_factors)]
            enhanced_recs.append(rec)
        else:
            enhanced_recs.append(rec)
    
    return enhanced_recs[:3]
