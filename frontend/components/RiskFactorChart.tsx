'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { RiskFactor } from '@/types/prediction';

interface RiskFactorChartProps {
  riskFactors: RiskFactor[];
}

export default function RiskFactorChart({ riskFactors }: RiskFactorChartProps) {
  const data = riskFactors.map((factor) => ({
    name: factor.feature,
    absValue: parseFloat(Math.abs(factor.shap_value).toFixed(4)),
    shap_value: factor.shap_value,
    feature_value: factor.feature_value,
    contribution: factor.contribution,
  }));

  return (
    <div className="w-full">
      <ResponsiveContainer width="100%" height={220}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 40, left: 160, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis
            type="number"
            tickFormatter={(v) => v.toFixed(3)}
            tick={{ fontSize: 11, fill: '#6b7280' }}
          />
          <YAxis
            dataKey="name"
            type="category"
            width={150}
            tick={{ fontSize: 12, fill: '#374151', fontWeight: 600 }}
          />
          <Tooltip
            formatter={(value: number, _name: string, props: any) => [
              `SHAP: ${props.payload.contribution}`,
              `Feature: ${props.payload.name}`,
            ]}
            contentStyle={{
              backgroundColor: '#f9fafb',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px',
            }}
          />
          <Bar dataKey="absValue" radius={[0, 8, 8, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.shap_value > 0 ? '#ef4444' : '#22c55e'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Color legend */}
      <div className="flex items-center space-x-6 mt-3 text-xs text-gray-500 pl-2">
        <span className="flex items-center space-x-1">
          <span className="inline-block w-3 h-3 rounded-sm bg-red-500" />
          <span>Increases risk</span>
        </span>
        <span className="flex items-center space-x-1">
          <span className="inline-block w-3 h-3 rounded-sm bg-green-500" />
          <span>Decreases risk</span>
        </span>
      </div>
    </div>
  );
}
