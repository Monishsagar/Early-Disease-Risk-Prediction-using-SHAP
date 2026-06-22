"""
Dataset configuration for all 4 diseases.
Defines download URLs, feature specs, ranges, and preprocessing metadata.
"""

DATASETS_CONFIG = {
    "heart": {
        "name": "Cardiovascular Disease Dataset",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data",
        "target": "cardio",
        "features": [
            "age", "gender", "height", "weight", "ap_hi", "ap_lo",
            "cholesterol", "gluc", "smoke", "alco", "active"
        ],
        "categorical": ["gender", "cholesterol", "gluc", "smoke", "alco", "active"],
        "numerical": ["age", "height", "weight", "ap_hi", "ap_lo"],
        "feature_ranges": {
            "age": (1, 100),
            "gender": (1, 2),
            "height": (100, 220),
            "weight": (30, 200),
            "ap_hi": (80, 200),
            "ap_lo": (50, 130),
            "cholesterol": (1, 3),
            "gluc": (1, 3),
            "smoke": (0, 1),
            "alco": (0, 1),
            "active": (0, 1)
        },
        "min_samples": 10000
    },
    "diabetes": {
        "name": "CDC BRFSS Diabetes Health Indicators",
        "url": "https://raw.githubusercontent.com/dsrscientist/dataset1/master/diabetes_binary_health_indicators_BRFSS2015.csv",
        "target": "Diabetes_binary",
        "sample_size": 50000,  # Sample 50k rows randomly for performance
        "features": [
            "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
            "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
            "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
            "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
        ],
        "categorical": [
            "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
            "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
            "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "Sex", "Age",
            "Education", "Income"
        ],
        "numerical": ["BMI", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk"],
        "feature_ranges": {
            "HighBP": (0, 1),
            "HighChol": (0, 1),
            "CholCheck": (0, 1),
            "BMI": (10, 60),
            "Smoker": (0, 1),
            "Stroke": (0, 1),
            "HeartDiseaseorAttack": (0, 1),
            "PhysActivity": (0, 1),
            "Fruits": (0, 1),
            "Veggies": (0, 1),
            "HvyAlcoholConsump": (0, 1),
            "AnyHealthcare": (0, 1),
            "NoDocbcCost": (0, 1),
            "GenHlth": (1, 5),
            "MentHlth": (0, 30),
            "PhysHlth": (0, 30),
            "DiffWalk": (0, 1),
            "Sex": (0, 1),
            "Age": (1, 13),
            "Education": (1, 6),
            "Income": (1, 8)
        },
        "min_samples": 10000
    },
    "liver": {
        "name": "Hepatitis C Prediction Dataset",
        "url": "https://raw.githubusercontent.com/aryashah2k/Hepatitis-C-Prediction/main/HepatitisCdata.csv",
        "target": "Category",
        "target_binarize": True,
        "features": [
            "Age", "Sex", "ALB", "ALP", "ALT", "AST", "BIL", "CHE",
            "CHOL", "CREA", "GGT", "PROT"
        ],
        "categorical": ["Sex"],
        "numerical": ["Age", "ALB", "ALP", "ALT", "AST", "BIL", "CHE", "CHOL", "CREA", "GGT", "PROT"],
        "feature_ranges": {
            "Age": (1, 100),
            "Sex": (1, 2),
            "ALB": (10, 60),
            "ALP": (10, 400),
            "ALT": (5, 200),
            "AST": (5, 200),
            "BIL": (1, 250),
            "CHE": (1, 20),
            "CHOL": (1, 10),
            "CREA": (10, 1500),
            "GGT": (5, 400),
            "PROT": (30, 100)
        },
        "min_samples": 10000
    },
    "kidney": {
        "name": "Chronic Kidney Disease Dataset",
        "url": "https://raw.githubusercontent.com/dsrscientist/dataset1/master/kidney_disease.csv",
        "target": "classification",
        "features": [
            "age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba",
            "bgr", "bu", "sc", "sod", "pot", "hemo", "pcv", "wc", "rc",
            "htn", "dm", "cad", "appet", "pe", "ane"
        ],
        "categorical": [
            "rbc", "pc", "pcc", "ba", "htn", "dm", "cad", "appet", "pe", "ane"
        ],
        "numerical": [
            "age", "bp", "sg", "al", "su", "bgr", "bu", "sc", "sod",
            "pot", "hemo", "pcv", "wc", "rc"
        ],
        "feature_ranges": {
            "age": (1, 120),
            "bp": (1, 250),
            "sg": (1.005, 1.025),
            "al": (0, 5),
            "su": (0, 5),
            "bgr": (10, 500),
            "bu": (2, 200),
            "sc": (0.1, 10),
            "sod": (100, 160),
            "pot": (2, 10),
            "hemo": (3, 18),
            "pcv": (10, 60),
            "wc": (2000, 20000),
            "rc": (2, 8)
        },
        "min_samples": 10000
    }
}

RISK_THRESHOLDS = {
    "low": 30,      # < 30 = Low risk
    "moderate": 70  # 30-70 = Moderate, > 70 = High
}

CLINICAL_RECOMMENDATIONS = {
    "heart": {
        "low": [
            "Continue regular physical exercise (150 minutes/week)",
            "Maintain healthy diet low in saturated fats",
            "Regular blood pressure and cholesterol monitoring"
        ],
        "moderate": [
            "Schedule consultation with cardiologist",
            "Increase physical activity gradually (30 min/day)",
            "Monitor blood pressure daily and maintain medication compliance"
        ],
        "high": [
            "Urgent cardiology consultation required",
            "Consider advanced diagnostic imaging (ECG, stress test)",
            "Implement aggressive risk factor management and medication"
        ]
    },
    "diabetes": {
        "low": [
            "Maintain balanced diet with controlled carbohydrates",
            "Regular physical activity (minimum 150 minutes/week)",
            "Annual diabetes screening and monitoring"
        ],
        "moderate": [
            "Consult with endocrinologist for risk assessment",
            "Begin lifestyle modifications: diet, exercise, weight management",
            "Monitor blood glucose levels regularly"
        ],
        "high": [
            "Urgent endocrinology consultation required",
            "Comprehensive metabolic screening needed",
            "Implement intensive lifestyle intervention program"
        ]
    },
    "liver": {
        "low": [
            "Limit alcohol consumption to safe levels",
            "Maintain healthy weight and regular exercise",
            "Annual liver function tests"
        ],
        "moderate": [
            "Hepatology consultation recommended",
            "Reduce alcohol and monitor diet",
            "Regular liver function panel monitoring"
        ],
        "high": [
            "Urgent hepatology consultation required",
            "Advanced liver imaging and biopsy may be needed",
            "Comprehensive metabolic and hepatic assessment"
        ]
    },
    "kidney": {
        "low": [
            "Maintain healthy blood pressure and blood glucose",
            "Stay hydrated and limit sodium intake",
            "Annual kidney function screening (eGFR, creatinine)"
        ],
        "moderate": [
            "Nephrology consultation advised",
            "Monitor blood pressure and proteinuria regularly",
            "Reduce sodium intake and manage comorbidities"
        ],
        "high": [
            "Urgent nephrology evaluation required",
            "Comprehensive renal function assessment needed",
            "Consider renal protection therapy and close monitoring"
        ]
    }
}
