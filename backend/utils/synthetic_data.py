"""
Synthetic dataset generator for medical datasets.
Creates realistic synthetic medical data if URLs fail.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(CACHE_DIR, exist_ok=True)


def generate_heart_disease_dataset(n_samples=68000):
    """Generate synthetic heart disease dataset with realistic distributions."""
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(1, 100, n_samples),
        'gender': np.random.choice([1, 2], n_samples),
        'height': np.random.normal(170, 10, n_samples).astype(int),
        'weight': np.random.normal(75, 15, n_samples).astype(int),
        'ap_hi': np.random.normal(130, 20, n_samples).astype(int),
        'ap_lo': np.random.normal(80, 15, n_samples).astype(int),
        'cholesterol': np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.35, 0.15]),
        'gluc': np.random.choice([1, 2, 3], n_samples, p=[0.6, 0.3, 0.1]),
        'smoke': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'alco': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'active': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
    }
    
    # Create target with realistic correlation
    target = (
        (data['age'] > 50) * 0.3 +
        (data['ap_hi'] > 140) * 0.3 +
        (data['cholesterol'] > 1) * 0.2 +
        (data['smoke'] == 1) * 0.15 +
        np.random.random(n_samples) * 0.05
    ) > 0.5
    
    data['cardio'] = target.astype(int)
    return pd.DataFrame(data)


def generate_diabetes_dataset(n_samples=50000):
    """Generate synthetic diabetes dataset."""
    np.random.seed(42)
    
    data = {
        'HighBP': np.random.choice([0, 1], n_samples, p=[0.65, 0.35]),
        'HighChol': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        'CholCheck': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'BMI': np.random.normal(26, 5, n_samples),
        'Smoker': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'Stroke': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'HeartDiseaseorAttack': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'PhysActivity': np.random.choice([0, 1], n_samples, p=[0.45, 0.55]),
        'Fruits': np.random.choice([0, 1], n_samples, p=[0.35, 0.65]),
        'Veggies': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
        'HvyAlcoholConsump': np.random.choice([0, 1], n_samples, p=[0.92, 0.08]),
        'AnyHealthcare': np.random.choice([0, 1], n_samples, p=[0.1, 0.9]),
        'NoDocbcCost': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'GenHlth': np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.25, 0.35, 0.25, 0.1, 0.05]),
        'MentHlth': np.random.choice(list(range(0, 31)), n_samples),
        'PhysHlth': np.random.choice(list(range(0, 31)), n_samples),
        'DiffWalk': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'Sex': np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
        'Age': np.random.choice(list(range(1, 14)), n_samples),
        'Education': np.random.choice(list(range(1, 7)), n_samples),
        'Income': np.random.choice(list(range(1, 9)), n_samples),
    }
    
    # Create target with realistic correlation
    target = (
        (data['HighBP'] == 1) * 0.25 +
        (data['BMI'] > 30) * 0.25 +
        (data['Age'] > 9) * 0.2 +
        (data['GenHlth'] > 2) * 0.15 +
        np.random.random(n_samples) * 0.15
    ) > 0.5
    
    data['Diabetes_binary'] = target.astype(int)
    return pd.DataFrame(data)


def generate_liver_disease_dataset(n_samples=30000):
    """Generate synthetic liver disease dataset."""
    np.random.seed(42)
    
    data = {
        'Age': np.random.randint(1, 100, n_samples),
        'Sex': np.random.choice([1, 2], n_samples, p=[0.6, 0.4]),
        'ALB': np.random.normal(38, 5, n_samples),
        'ALP': np.random.normal(85, 30, n_samples),
        'ALT': np.random.normal(35, 25, n_samples),
        'AST': np.random.normal(32, 20, n_samples),
        'BIL': np.random.normal(10, 8, n_samples),
        'CHE': np.random.normal(8, 2, n_samples),
        'CHOL': np.random.normal(4.5, 1.5, n_samples),
        'CREA': np.random.normal(80, 30, n_samples),
        'GGT': np.random.normal(50, 40, n_samples),
        'PROT': np.random.normal(70, 5, n_samples),
    }
    
    # Create target: 0=healthy, 1=liver disease
    # Use enzyme levels and age as indicators
    target = (
        (data['ALT'] > 40) * 0.3 +
        (data['AST'] > 40) * 0.3 +
        (data['BIL'] > 15) * 0.2 +
        (data['Age'] > 50) * 0.1 +
        np.random.random(n_samples) * 0.1
    ) > 0.5
    
    data['Category'] = ['1=Hepatitis C' if t else '0=Blood Donor' for t in target]
    return pd.DataFrame(data)


def generate_kidney_disease_dataset(n_samples=30000):
    """Generate synthetic kidney disease dataset."""
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(1, 120, n_samples),
        'bp': np.random.normal(120, 20, n_samples).astype(int),
        'sg': np.random.normal(1.015, 0.005, n_samples),
        'al': np.random.choice(list(range(0, 6)), n_samples),
        'su': np.random.choice(list(range(0, 6)), n_samples),
        'rbc': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'pc': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'pcc': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'ba': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'bgr': np.random.normal(120, 40, n_samples).astype(int),
        'bu': np.random.normal(60, 30, n_samples).astype(int),
        'sc': np.random.normal(1.0, 0.5, n_samples),
        'sod': np.random.normal(140, 5, n_samples).astype(int),
        'pot': np.random.normal(4.5, 1, n_samples),
        'hemo': np.random.normal(13, 2, n_samples),
        'pcv': np.random.normal(40, 8, n_samples).astype(int),
        'wc': np.random.randint(5000, 15000, n_samples),
        'rc': np.random.normal(5, 1, n_samples),
        'htn': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        'dm': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'cad': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'appet': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
        'pe': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'ane': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
    }
    
    # Create target: ckd=1, notckd=0
    target = (
        (data['sc'] > 1.2) * 0.3 +
        (data['bu'] > 80) * 0.25 +
        (data['htn'] == 1) * 0.25 +
        (data['dm'] == 1) * 0.15 +
        np.random.random(n_samples) * 0.05
    ) > 0.5
    
    data['classification'] = ['ckd' if t else 'notckd' for t in target]
    return pd.DataFrame(data)


def create_or_load_synthetic_data(disease):
    """
    Create or load synthetic dataset for disease.
    Returns DataFrame.
    """
    cache_path = os.path.join(CACHE_DIR, f"{disease}_raw.csv")
    
    if os.path.exists(cache_path):
        print(f"✓ Loading cached synthetic dataset for {disease}")
        return pd.read_csv(cache_path)
    
    print(f"📊 Generating synthetic dataset for {disease}...")
    
    if disease == "heart":
        df = generate_heart_disease_dataset(n_samples=68000)
    elif disease == "diabetes":
        df = generate_diabetes_dataset(n_samples=50000)
    elif disease == "liver":
        df = generate_liver_disease_dataset(n_samples=30000)
    elif disease == "kidney":
        df = generate_kidney_disease_dataset(n_samples=30000)
    else:
        raise ValueError(f"Unknown disease: {disease}")
    
    df.to_csv(cache_path, index=False)
    print(f"✓ Generated and cached synthetic dataset for {disease} ({len(df)} samples)")
    
    return df
