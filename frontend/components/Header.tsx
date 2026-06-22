'use client';

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900" style={{ fontFamily: 'Georgia, serif' }}>
          Early Disease Risk Prediction
        </h1>
        <p className="text-gray-600 mt-2 text-lg">
          AI-powered Clinical Decision Support
        </p>
      </div>
    </header>
  );
}
