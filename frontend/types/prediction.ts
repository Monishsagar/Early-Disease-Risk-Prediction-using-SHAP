"""
TypeScript interfaces and types for API communication.
"""

export interface RiskFactor {
  feature: string;
  contribution: string;
  shap_value: number;
  feature_value: number;
}

export interface PredictionResponse {
  risk_score: number;
  risk_level: "Low" | "Moderate" | "High";
  confidence: number;
  top_risk_factors: RiskFactor[];
  recommendations: string[];
}

export interface DatasetStats {
  disease: string;
  total_samples: number;
  feature_count: number;
  positive_cases: number;
  accuracy: number;
  auc_score: number;
  augmentation_note: string | null;
}

export interface HealthResponse {
  status: string;
}

// Disease-specific prediction request types
export interface HeartPredictionRequest {
  age: number;
  gender: number;
  height: number;
  weight: number;
  ap_hi: number;
  ap_lo: number;
  cholesterol: number;
  gluc: number;
  smoke: number;
  alco: number;
  active: number;
}

export interface DiabetesPredictionRequest {
  HighBP: number;
  HighChol: number;
  CholCheck: number;
  BMI: number;
  Smoker: number;
  Stroke: number;
  HeartDiseaseorAttack: number;
  PhysActivity: number;
  Fruits: number;
  Veggies: number;
  HvyAlcoholConsump: number;
  AnyHealthcare: number;
  NoDocbcCost: number;
  GenHlth: number;
  MentHlth: number;
  PhysHlth: number;
  DiffWalk: number;
  Sex: number;
  Age: number;
  Education: number;
  Income: number;
}

export interface LiverPredictionRequest {
  Age: number;
  Sex: number;
  ALB: number;
  ALP: number;
  ALT: number;
  AST: number;
  BIL: number;
  CHE: number;
  CHOL: number;
  CREA: number;
  GGT: number;
  PROT: number;
}

export interface KidneyPredictionRequest {
  age: number;
  bp: number;
  sg: number;
  al: number;
  su: number;
  rbc: number;
  pc: number;
  pcc: number;
  ba: number;
  bgr: number;
  bu: number;
  sc: number;
  sod: number;
  pot: number;
  hemo: number;
  pcv: number;
  wc: number;
  rc: number;
  htn: number;
  dm: number;
  cad: number;
  appet: number;
  pe: number;
  ane: number;
}

export type PredictionRequest = 
  | HeartPredictionRequest 
  | DiabetesPredictionRequest 
  | LiverPredictionRequest 
  | KidneyPredictionRequest;

export interface StoredPredictionResult {
  disease: string;
  input: PredictionRequest;
  result: PredictionResponse;
  timestamp: string;
}
