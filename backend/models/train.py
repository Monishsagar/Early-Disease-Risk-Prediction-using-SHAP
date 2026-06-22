"""
Model training pipeline for all 4 diseases.
Trains Random Forest classifiers and saves them as .pkl files.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
import joblib
import json

from utils.preprocess import (
    download_dataset, clean_dataset, encode_categorical_features,
    normalize_features, augment_dataset_to_minimum, save_preprocessing_artifacts
)
from models.datasets_config import DATASETS_CONFIG

# Get absolute path for models directory
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "saved")
os.makedirs(MODELS_DIR, exist_ok=True)


def train_model_for_disease(disease, force_retrain=False):
    """
    Train Random Forest model for specified disease.
    
    Steps:
    1. Download dataset
    2. Clean dataset
    3. Encode categoricals
    4. Normalize numericals
    5. Augment to minimum 10,000 samples if needed
    6. Train Random Forest (n_estimators=100, random_state=42)
    7. Evaluate on test set
    8. Save model, encoders, scaler, and metadata
    
    Returns:
        dict with training_info (accuracy, auc, f1, augmentation_note)
    """
    
    config = DATASETS_CONFIG[disease]
    model_path = os.path.join(MODELS_DIR, f"{disease}_model.pkl")
    metadata_path = os.path.join(MODELS_DIR, f"{disease}_metadata.json")
    
    # Check if model already exists
    if os.path.exists(model_path) and not force_retrain:
        print(f"✓ Model already exists for {disease}, loading from cache")
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return metadata
    
    print(f"\n{'='*60}")
    print(f"🔄 TRAINING MODEL FOR {disease.upper()}")
    print(f"{'='*60}")
    
    # Step 1: Download dataset
    url = config["url"]
    df = download_dataset(disease, url)
    
    # Step 2: Clean dataset
    df = clean_dataset(df, disease)
    
    # Step 3: Prepare features and target
    target_col = config["target"]
    feature_cols = [col for col in config["features"] if col in df.columns]
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    # Sample to max size if needed (for diabetes dataset)
    if disease == "diabetes" and len(X) > config.get("sample_size", 50000):
        indices = np.random.choice(len(X), size=config.get("sample_size", 50000), replace=False)
        X = X.iloc[indices].reset_index(drop=True)
        y = y.iloc[indices].reset_index(drop=True)
        print(f"  - Sampled {len(X)} rows from dataset")
    
    # Step 4: Encode categoricals
    X, encoders_dict = encode_categorical_features(X, disease, fit_encoders=True)
    print(f"  - Encoded {len(encoders_dict)} categorical features")
    
    # Step 5: Normalize numericals (fit scaler)
    X, scaler = normalize_features(X, disease, fit_scaler=True, scaler=None)
    print(f"  - Normalized numerical features")
    
    # Step 6: Augment dataset if needed
    X, y, augmentation_note = augment_dataset_to_minimum(X, y, disease, min_samples=10000)
    
    # Step 7: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  - Train set: {len(X_train)} samples")
    print(f"  - Test set: {len(X_test)} samples")
    
    # Step 8: Train Random Forest
    print(f"  - Training Random Forest (n_estimators=100)...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        max_depth=15
    )
    rf_model.fit(X_train, y_train)
    
    # Step 9: Evaluate model
    y_pred = rf_model.predict(X_test)
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\n  📊 MODEL EVALUATION:")
    print(f"     Accuracy: {accuracy:.4f}")
    print(f"     ROC-AUC:  {auc:.4f}")
    print(f"     F1-Score: {f1:.4f}")
    
    # Step 10: Save artifacts
    model_pkl_path = os.path.join(MODELS_DIR, f"{disease}_model.pkl")
    joblib.dump(rf_model, model_pkl_path)
    print(f"  ✓ Saved model to {model_pkl_path}")
    
    # Save encoders and scaler
    save_preprocessing_artifacts(disease, encoders_dict, scaler)
    
    # Save metadata
    training_info = {
        "disease": disease,
        "dataset_name": config["name"],
        "total_samples": len(X),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_count": len(feature_cols),
        "positive_cases": int(y.sum()),
        "accuracy": float(accuracy),
        "auc_score": float(auc),
        "f1_score": float(f1),
        "augmentation_note": augmentation_note
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(training_info, f, indent=2)
    
    print(f"  ✓ Saved metadata to {metadata_path}")
    print(f"{'='*60}\n")
    
    return training_info


def load_or_train_all_models(force_retrain=False):
    """
    Load all 4 models from disk or train if not cached.
    Returns dict of {disease: model, metadata: {}}
    """
    models = {}
    metadata_all = {}
    
    for disease in ["heart", "diabetes", "liver", "kidney"]:
        try:
            info = train_model_for_disease(disease, force_retrain=force_retrain)
            metadata_all[disease] = info
            
            # Load the model
            model_path = f"{MODELS_DIR}/{disease}_model.pkl"
            models[disease] = joblib.load(model_path)
            
        except Exception as e:
            print(f"✗ Error training model for {disease}: {e}")
            raise
    
    print("\n✓ All models loaded successfully!\n")
    return models, metadata_all


def get_disease_model(disease):
    """
    Load a single disease model from disk.
    """
    model_path = f"{MODELS_DIR}/{disease}_model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found for {disease}")
    
    return joblib.load(model_path)


def get_disease_metadata(disease):
    """
    Load metadata for a disease model.
    """
    metadata_path = f"{MODELS_DIR}/{disease}_metadata.json"
    if not os.path.exists(metadata_path):
        return None
    
    import json
    with open(metadata_path, 'r') as f:
        return json.load(f)
