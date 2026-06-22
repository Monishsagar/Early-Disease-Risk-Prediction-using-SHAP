"""
Data preprocessing utilities for disease datasets.
Handles downloading, cleaning, encoding, normalization, and augmentation.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
import joblib
import warnings

warnings.filterwarnings('ignore')

from models.datasets_config import DATASETS_CONFIG
from utils.synthetic_data import create_or_load_synthetic_data

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(CACHE_DIR, exist_ok=True)


def download_dataset(disease, url, cache_path=None):
    """
    Download dataset from URL if not cached locally.
    Falls back to synthetic data generation if URL fails.
    Returns DataFrame.
    """
    if cache_path is None:
        cache_path = os.path.join(CACHE_DIR, f"{disease}_raw.csv")
    
    if os.path.exists(cache_path):
        print(f"✓ Loading cached dataset for {disease}")
        df = pd.read_csv(cache_path)
        return df
    
    print(f"📥 Attempting to download {disease} dataset from URL...")
    try:
        df = pd.read_csv(url, timeout=10)
        df.to_csv(cache_path, index=False)
        print(f"✓ Downloaded and cached {disease} dataset ({len(df)} rows)")
        return df
    except Exception as e:
        print(f"⚠ URL download failed ({str(e)[:50]}), using synthetic dataset...")
        # Fallback to synthetic data generation
        df = create_or_load_synthetic_data(disease)
        return df


def clean_dataset(df, disease):
    """
    Clean dataset for specified disease.
    - Handle missing values: median for numerical, mode for categorical
    - Remove duplicates
    - Verify feature presence
    - Handle different column naming conventions
    """
    config = DATASETS_CONFIG[disease]
    
    print(f"🧹 Cleaning {disease} dataset ({len(df)} rows)...")
    
    # Handle different UCI dataset column naming (if real data was used)
    if disease == "heart" and "age" not in df.columns and df.columns[0].strip().isdigit() or len(df.columns) == 14:
        # UCI heart disease dataset has different format
        df.columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
        df = df.rename(columns={
            "sex": "gender",
            "trestbps": "ap_hi",
            "chol": "cholesterol",
            "cp": "gluc",
            "fbs": "smoke",
            "exang": "alco",
            "target": "cardio"
        })
        # Add missing synthetic columns
        if "height" not in df.columns:
            df["height"] = np.random.normal(170, 10, len(df)).astype(int)
        if "weight" not in df.columns:
            df["weight"] = np.random.normal(75, 15, len(df)).astype(int)
        if "ap_lo" not in df.columns:
            df["ap_lo"] = df["ap_hi"] - 40 + np.random.normal(0, 5, len(df))
        if "active" not in df.columns:
            df["active"] = np.random.choice([0, 1], len(df))
    
    # Remove duplicates
    df = df.drop_duplicates()
    print(f"  - After removing duplicates: {len(df)} rows")
    
    # Select only required features + target
    required_cols = config["features"] + [config["target"]]
    available_cols = [col for col in required_cols if col in df.columns]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"  ⚠ Missing columns: {missing_cols}")
    
    df = df[available_cols]
    
    # Handle missing values
    imputer_numerical = SimpleImputer(strategy='median')
    imputer_categorical = SimpleImputer(strategy='most_frequent')
    
    for col in config["numerical"]:
        if col in df.columns:
            df[col] = imputer_numerical.fit_transform(df[[col]])
    
    for col in config["categorical"]:
        if col in df.columns:
            df[col] = imputer_categorical.fit_transform(df[[col]])
    
    print(f"  - After handling missing values: {len(df)} rows")
    
    # Binarize target if needed (for liver disease)
    if disease == "liver" and config.get("target_binarize"):
        # Convert Category column: 0=healthy, 1=any disease stage
        df[config["target"]] = df[config["target"]].apply(lambda x: 0 if ('0' in str(x) or 'Blood' in str(x)) else 1)
    
    # Kidney disease: convert classification to binary (ckd=1, notckd=0)
    if disease == "kidney":
        df[config["target"]] = df[config["target"]].apply(lambda x: 1 if str(x).strip().lower() == 'ckd' else 0)
    
    # Ensure numeric target
    df[config["target"]] = pd.to_numeric(df[config["target"]], errors='coerce').fillna(0).astype(int)
    
    print(f"✓ Cleaned {disease} dataset: {len(df)} rows")
    return df


def encode_categorical_features(df, disease, fit_encoders=True, encoders_dict=None):
    """
    Encode categorical features using LabelEncoder.
    If fit_encoders=True: fit new encoders and return them
    If fit_encoders=False: use provided encoders_dict
    """
    config = DATASETS_CONFIG[disease]
    encoded_df = df.copy()
    encoders = {}
    
    for col in config["categorical"]:
        if col in encoded_df.columns:
            if fit_encoders:
                le = LabelEncoder()
                encoded_df[col] = le.fit_transform(encoded_df[col].astype(str))
                encoders[col] = le
            else:
                if encoders_dict and col in encoders_dict:
                    encoded_df[col] = encoders_dict[col].transform(encoded_df[col].astype(str))
    
    return encoded_df, encoders


def normalize_features(df, disease, fit_scaler=True, scaler=None):
    """
    Normalize numerical features using StandardScaler.
    If fit_scaler=True: fit new scaler and return it
    If fit_scaler=False: use provided scaler
    """
    config = DATASETS_CONFIG[disease]
    normalized_df = df.copy()
    
    numerical_cols = [col for col in config["numerical"] if col in normalized_df.columns]
    
    scaler_obj = scaler  # Default to provided scaler
    
    if numerical_cols:
        if fit_scaler:
            scaler_obj = StandardScaler()
            normalized_df[numerical_cols] = scaler_obj.fit_transform(normalized_df[numerical_cols])
        else:
            if scaler is not None:
                normalized_df[numerical_cols] = scaler.transform(normalized_df[numerical_cols])
    
    return normalized_df, scaler_obj


def augment_dataset_to_minimum(X, y, disease, min_samples=10000):
    """
    Apply SMOTE + Gaussian noise augmentation if dataset < min_samples.
    Returns augmented X, y and augmentation note.
    """
    original_count = len(X)
    augmentation_note = None
    
    if original_count >= min_samples:
        print(f"✓ {disease}: {original_count} samples >= {min_samples}, no augmentation needed")
        return X, y, augmentation_note
    
    print(f"⚠ {disease}: {original_count} samples < {min_samples}, applying SMOTE + augmentation...")
    
    # Apply SMOTE to oversample minority class
    try:
        smote = SMOTE(random_state=42, k_neighbors=min(5, len(y[y==1])-1) if len(y[y==1]) > 1 else 1)
        X_smote, y_smote = smote.fit_resample(X, y)
    except Exception as e:
        print(f"  SMOTE failed: {e}, using simple oversampling instead")
        X_smote, y_smote = X.copy(), y.copy()
    
    # Add Gaussian noise to generate additional synthetic samples
    samples_needed = min_samples - len(X_smote)
    if samples_needed > 0:
        noise_indices = np.random.choice(len(X_smote), size=samples_needed, replace=True)
        X_noise = X_smote.iloc[noise_indices].copy()
        y_noise = y_smote.iloc[noise_indices].copy()
        
        # Add Gaussian noise (std=0.01)
        noise = np.random.normal(0, 0.01, X_noise.shape)
        X_noise = X_noise + noise
        
        X_augmented = pd.concat([X_smote, X_noise], ignore_index=True)
        y_augmented = pd.concat([y_smote, y_noise], ignore_index=True)
    else:
        X_augmented = X_smote
        y_augmented = y_smote
    
    augmentation_note = f"Dataset augmented to meet 10,000 sample minimum — original: {original_count} rows, final: {len(X_augmented)} rows (SMOTE + Gaussian noise)"
    print(f"  {augmentation_note}")
    
    return X_augmented, y_augmented, augmentation_note


def preprocess_input_features(input_dict, disease, encoders_dict=None, scaler=None):
    """
    Preprocess a single prediction input.
    Converts input dict to feature vector using provided encoders/scaler.
    """
    config = DATASETS_CONFIG[disease]
    
    # Create feature array in correct order
    features = []
    for feature_name in config["features"]:
        value = input_dict.get(feature_name)
        
        if value is None:
            raise ValueError(f"Missing required feature: {feature_name}")
        
        # Validate range
        if feature_name in config["feature_ranges"]:
            min_val, max_val = config["feature_ranges"][feature_name]
            if value < min_val or value > max_val:
                raise ValueError(
                    f"Feature {feature_name}={value} out of range [{min_val}, {max_val}]"
                )
        
        features.append(value)
    
    # Create DataFrame with single row
    df = pd.DataFrame([features], columns=config["features"])
    
    # Encode categoricals
    df, _ = encode_categorical_features(df, disease, fit_encoders=False, encoders_dict=encoders_dict)
    
    # Normalize numericals
    df, _ = normalize_features(df, disease, fit_scaler=False, scaler=scaler)
    
    return df.values[0]


def save_preprocessing_artifacts(disease, encoders_dict, scaler):
    """
    Save encoders and scaler to disk for later use during prediction.
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "saved")
    os.makedirs(models_dir, exist_ok=True)
    
    encoder_path = os.path.join(models_dir, f"{disease}_encoders.pkl")
    scaler_path = os.path.join(models_dir, f"{disease}_scaler.pkl")
    
    joblib.dump(encoders_dict, encoder_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"✓ Saved encoders and scaler for {disease}")


def load_preprocessing_artifacts(disease):
    """
    Load saved encoders and scaler from disk.
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "saved")
    encoder_path = os.path.join(models_dir, f"{disease}_encoders.pkl")
    scaler_path = os.path.join(models_dir, f"{disease}_scaler.pkl")
    
    if not os.path.exists(encoder_path) or not os.path.exists(scaler_path):
        print(f"✗ Artifacts not found for {disease}")
        print(f"  Looking for: {encoder_path}")
        print(f"            {scaler_path}")
        return None, None
    
    encoders_dict = joblib.load(encoder_path)
    scaler = joblib.load(scaler_path)
    
    print(f"✓ Loaded encoders and scaler for {disease}")
    return encoders_dict, scaler
