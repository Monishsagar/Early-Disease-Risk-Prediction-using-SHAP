import axios, { AxiosInstance } from 'axios';
import {
  PredictionResponse,
  DatasetStats,
  HealthResponse,
  PredictionRequest,
} from '@/types/prediction';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/api/health');
  return response.data;
};

// Get dataset statistics
export const getDatasetStats = async (disease: string): Promise<DatasetStats> => {
  const response = await apiClient.get<DatasetStats>(`/api/dataset/stats/${disease}`);
  return response.data;
};

// Get all dataset statistics (for dashboard)
export const getAllDatasetStats = async (diseases: string[]): Promise<DatasetStats[]> => {
  const promises = diseases.map((disease) => getDatasetStats(disease));
  return Promise.all(promises);
};

// Predict disease risk
export const predictDisease = async (
  disease: string,
  data: PredictionRequest
): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(`/api/predict/${disease}`, data);
  return response.data;
};

// Error handler
export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      return error.response.data?.detail || error.response.statusText || 'An error occurred';
    }
    if (error.request) {
      return 'No response from server. Please check if the API is running.';
    }
    return error.message;
  }
  return 'An unexpected error occurred';
};

export default apiClient;
