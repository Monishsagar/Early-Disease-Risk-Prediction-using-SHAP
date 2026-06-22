'use client';

interface RecommendationListProps {
  recommendations: string[];
}

export default function RecommendationList({ recommendations }: RecommendationListProps) {
  const icons = ['💊', '🏃', '📋'];

  return (
    <div className="w-full">
      <h3 className="text-lg font-bold text-gray-900 mb-4" style={{ fontFamily: 'Georgia, serif' }}>
        Clinical Recommendations
      </h3>
      
      <div className="space-y-3">
        {recommendations.map((recommendation, index) => (
          <div key={index} className="flex items-start space-x-3 bg-blue-50 p-4 rounded-lg">
            <span className="text-2xl flex-shrink-0">{icons[index % icons.length]}</span>
            <div>
              <div className="font-semibold text-gray-900">Recommendation {index + 1}</div>
              <p className="text-gray-700 mt-1">{recommendation}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
