'use client';

import Header from '@/components/Header';
import PredictionForm from '@/components/PredictionForm';
import Link from 'next/link';

interface PredictPageProps {
  params: { disease: string };
}

export default function PredictPage({ params }: PredictPageProps) {
  const disease = params.disease;

  const validDiseases = ['heart', 'diabetes', 'liver', 'kidney'];
  if (!validDiseases.includes(disease)) {
    return (
      <main className="bg-gray-50 min-h-screen">
        <Header />
        <div className="max-w-2xl mx-auto px-4 py-12 text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Invalid Disease</h2>
          <p className="text-gray-600 mb-6">
            The disease "{disease}" is not recognized. Please select a valid disease.
          </p>
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
      <div className="max-w-4xl mx-auto px-4 py-12">
        <Link href="/">
          <button className="mb-6 text-cyan-500 hover:text-cyan-600 font-semibold">
            ← Back to Home
          </button>
        </Link>
        <PredictionForm disease={disease} />
      </div>
    </main>
  );
}
