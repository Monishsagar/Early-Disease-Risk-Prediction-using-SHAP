'use client';

import Link from 'next/link';
import { DatasetStats } from '@/types/prediction';

interface DiseaseCardProps {
  disease: string;
  displayName: string;
  icon: string;
  stats: DatasetStats | null;
  loading: boolean;
}

const DISEASE_ICONS: { [key: string]: string } = {
  heart: '❤️',
  diabetes: '🩺',
  liver: '🧬',
  kidney: '💧',
};

export default function DiseaseCard({
  disease,
  displayName,
  stats,
  loading,
}: DiseaseCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">
      <div className="text-4xl mb-4">{DISEASE_ICONS[disease] || '🏥'}</div>
      
      <h3 className="text-xl font-bold text-gray-900 mb-4" style={{ fontFamily: 'Georgia, serif' }}>
        {displayName}
      </h3>

      {loading ? (
        <div className="space-y-2 mb-4">
          <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
        </div>
      ) : stats ? (
        <div className="space-y-2 mb-4 text-sm text-gray-600">
          <p>
            <span className="font-semibold">Samples:</span> {stats.total_samples.toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Accuracy:</span> {(stats.accuracy * 100).toFixed(2)}%
          </p>
          <p>
            <span className="font-semibold">AUC Score:</span> {stats.auc_score.toFixed(4)}
          </p>
          {stats.augmentation_note && (
            <p className="text-xs text-yellow-600 mt-2">
              📊 {stats.augmentation_note}
            </p>
          )}
        </div>
      ) : (
        <div className="text-gray-500 text-sm mb-4">No data available</div>
      )}

      <Link href={`/predict/${disease}`}>
        <button className="w-full bg-cyan-500 hover:bg-cyan-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
          Predict Risk
        </button>
      </Link>
    </div>
  );
}
