'use client';

import { useEffect, useState } from 'react';
import Header from '@/components/Header';
import DiseaseCard from '@/components/DiseaseCard';
import { getAllDatasetStats } from '@/lib/api';
import { DatasetStats } from '@/types/prediction';

const DISEASES = [
  { id: 'heart', name: 'Heart Disease' },
  { id: 'diabetes', name: 'Diabetes' },
  { id: 'liver', name: 'Liver Disease' },
  { id: 'kidney', name: 'Kidney Disease' },
];

export default function Home() {
  const [stats, setStats] = useState<{ [key: string]: DatasetStats | null }>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const diseaseIds = DISEASES.map((d) => d.id);
        const results = await getAllDatasetStats(diseaseIds);

        const statsMap: { [key: string]: DatasetStats } = {};
        results.forEach((stat) => {
          statsMap[stat.disease] = stat;
        });

        setStats(statsMap);
      } catch (error) {
        console.error('Failed to fetch dataset statistics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <main className="bg-gray-50 min-h-screen">
      <Header />

      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {DISEASES.map((disease) => (
            <DiseaseCard
              key={disease.id}
              disease={disease.id}
              displayName={disease.name}
              stats={stats[disease.id] || null}
              loading={loading}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
