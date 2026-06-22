'use client';

interface RiskGaugeProps {
  riskScore: number;
  riskLevel: 'Low' | 'Moderate' | 'High';
}

export default function RiskGauge({ riskScore, riskLevel }: RiskGaugeProps) {
  const getColor = () => {
    if (riskScore < 30) return '#22c55e'; // Green
    if (riskScore < 70) return '#eab308'; // Yellow
    return '#ef4444'; // Red
  };

  const color = getColor();
  const angle = (riskScore / 100) * 180; // 0-180 degrees for semicircle

  const getBadgeColor = () => {
    switch (riskLevel) {
      case 'Low':
        return 'bg-green-100 text-green-800';
      case 'Moderate':
        return 'bg-yellow-100 text-yellow-800';
      case 'High':
        return 'bg-red-100 text-red-800';
    }
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      {/* Semicircular Gauge */}
      <div className="relative w-64 h-32">
        {/* SVG Semicircle */}
        <svg
          className="w-full h-full"
          viewBox="0 0 200 110"
          preserveAspectRatio="xMidYMid meet"
        >
          {/* Background semicircle */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="12"
          />

          {/* Color gradient semicircle */}
          <defs>
            <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#22c55e" />
              <stop offset="50%" stopColor="#eab308" />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>
          </defs>

          {/* Active gauge arc */}
          <path
            d={`M ${20 + 80 * Math.sin((angle * Math.PI) / 180)} ${
              100 - 80 * Math.cos((angle * Math.PI) / 180)
            } A 80 80 0 0 0 20 100`}
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
          />

          {/* Needle */}
          <line
            x1="100"
            y1="100"
            x2={100 + 70 * Math.sin((angle * Math.PI) / 180)}
            y2={100 - 70 * Math.cos((angle * Math.PI) / 180)}
            stroke="#374151"
            strokeWidth="3"
          />
          <circle cx="100" cy="100" r="6" fill="#374151" />
        </svg>

        {/* Center Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-8">
          <span className="text-4xl font-bold text-gray-900">{riskScore}%</span>
        </div>
      </div>

      {/* Risk Level Badge */}
      <div className={`px-4 py-2 rounded-full font-semibold text-lg ${getBadgeColor()}`}>
        {riskLevel} Risk
      </div>

      {/* Risk Scale Legend */}
      <div className="flex justify-between w-full max-w-sm text-xs text-gray-600">
        <span>Low (&lt;30)</span>
        <span>Moderate (30-70)</span>
        <span>High (&gt;70)</span>
      </div>
    </div>
  );
}
