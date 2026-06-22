"""
SHAP explainability module for feature importance computation.
Uses TreeExplainer for Random Forest models.
"""

import shap
import numpy as np


def get_shap_explanations(model, X_instance, X_background, feature_names, top_k=3):
    """
    Compute SHAP explanations for a single prediction.
    
    Args:
        model: Trained Random Forest model
        X_instance: Single instance (1D array or 2D array with 1 row)
        X_background: Background dataset for SHAP explainer
        feature_names: List of feature names
        top_k: Number of top features to return
    
    Returns:
        List of dicts: [
            {"feature": "age", "shap_value": 0.15, "feature_value": 65},
            ...
        ]
    """
    
    # Ensure X_instance is 2D
    if X_instance.ndim == 1:
        X_instance = X_instance.reshape(1, -1)
    
    # Create TreeExplainer
    explainer = shap.TreeExplainer(model)
    
    # Compute SHAP values
    shap_values = explainer.shap_values(X_instance)
    
    # For binary classification, shap_values is a list of 2 arrays (one per class)
    # Use the positive class (index 1)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    
    # Get the SHAP values for the single instance
    instance_shap = shap_values[0] if shap_values.ndim > 1 else shap_values
    
    # Create list of (feature_name, shap_value, feature_value) tuples
    feature_importance = []
    for i, fname in enumerate(feature_names):
        shap_val = instance_shap[i]
        # Ensure scalar value
        if hasattr(shap_val, '__len__'):
            shap_val = shap_val[0] if len(shap_val) > 0 else shap_val
        
        feature_importance.append({
            "feature": fname,
            "shap_value": float(shap_val),
            "feature_value": float(X_instance[0][i])
        })
    
    # Sort by absolute SHAP value (importance) and get top k
    feature_importance.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    top_features = feature_importance[:top_k]
    
    return top_features


def format_shap_explanation(top_features, risk_score):
    """
    Format SHAP explanations for API response.
    
    Returns list of dicts with feature, contribution (± format), and shap_value.
    """
    formatted = []
    for item in top_features:
        contribution = f"{'+' if item['shap_value'] > 0 else ''}{item['shap_value']:.4f}"
        formatted.append({
            "feature": item["feature"],
            "contribution": contribution,
            "shap_value": round(item["shap_value"], 4),
            "feature_value": round(item["feature_value"], 2)
        })
    
    return formatted
