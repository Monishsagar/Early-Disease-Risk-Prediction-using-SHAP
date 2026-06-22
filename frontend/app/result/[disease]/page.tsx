'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Header from '@/components/Header';
import RiskGauge from '@/components/RiskGauge';
import RiskFactorChart from '@/components/RiskFactorChart';
import RecommendationList from '@/components/RecommendationList';
import { PredictionResponse } from '@/types/prediction';

interface ResultPageProps {
  params: { disease: string };
}

export default function ResultPage({ params }: ResultPageProps) {
  const disease = params.disease;
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(`prediction_${disease}`);
      if (stored) {
        const data = JSON.parse(stored);
        setResult(data.result);
      } else {
        setError('No prediction result found. Please run a prediction first.');
      }
    } catch (err) {
      setError('Failed to load prediction result.');
    } finally {
      setLoading(false);
    }
  }, [disease]);

  if (loading) {
    return (
      <main className="bg-gray-50 min-h-screen">
        <Header />
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <p className="text-gray-600">Loading results...</p>
        </div>
      </main>
    );
  }

  if (error || !result) {
    return (
      <main className="bg-gray-50 min-h-screen">
        <Header />
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-600 mb-6">{error || 'Unknown error occurred.'}</p>
          <Link href="/">
            <button className="bg-cyan-500 hover:bg-cyan-600 text-white font-semibold py-2 px-6 rounded-lg">
              Back to Home
            </button>
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="bg-gray-50 min-h-screen">
      <Header />

      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Patient Risk Summary */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2
            className="text-3xl font-bold text-gray-900 mb-8 text-center"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            Prediction Results for {disease.charAt(0).toUpperCase() + disease.slice(1)} Disease
          </h2>

          {/* Risk Gauge */}
          <div className="flex justify-center mb-12">
            <RiskGauge riskScore={result.risk_score} riskLevel={result.risk_level} />
          </div>

          {/* Confidence Score */}
          <div className="text-center mb-8">
            <p className="text-gray-600">
              <span className="font-semibold">Model Confidence:</span>{' '}
              {(result.confidence * 100).toFixed(2)}%
            </p>
          </div>
        </div>

        {/* SHAP Risk Factors */}
        {result.top_risk_factors && result.top_risk_factors.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-2" style={{ fontFamily: 'Georgia, serif' }}>
              SHAP Explainability — Top Risk Factors
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              These are the features that influenced the prediction the most, computed via SHAP (SHapley Additive exPlanations).
              A <span className="text-red-600 font-semibold">positive</span> contribution increases risk;
              a <span className="text-green-600 font-semibold">negative</span> contribution reduces risk.
            </p>
            <RiskFactorChart riskFactors={result.top_risk_factors} />
          </div>
        )}

        {/* Risk Factors and Recommendations Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Top Risk Factor Detail Table */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4" style={{ fontFamily: 'Georgia, serif' }}>
              Risk Factor Details
            </h3>
            <div className="space-y-3">
              {result.top_risk_factors.map((factor, index) => (
                <div key={index} className="flex items-center justify-between border-b border-gray-100 pb-3">
                  <div>
                    <span className="font-semibold text-gray-800">{factor.feature}</span>
                    <span className="ml-2 text-sm text-gray-500">
                      (value: {typeof factor.feature_value === 'number' ? factor.feature_value.toFixed(2) : factor.feature_value})
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`text-sm font-bold ${
                        factor.shap_value > 0 ? 'text-red-600' : 'text-green-600'
                      }`}
                    >
                      {factor.shap_value > 0 ? '▲ Risk +' : '▼ Risk '}
                      {Math.abs(factor.shap_value).toFixed(4)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Clinical Recommendations */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <RecommendationList recommendations={result.recommendations} />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4">
          <Link href="/">
            <button className="bg-cyan-500 hover:bg-cyan-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
              Check Another Disease
            </button>
          </Link>
          <Link href={`/predict/${disease}`}>
            <button className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
              New Prediction
            </button>
          </Link>
        </div>
      </div>
    </main>
  );
}
