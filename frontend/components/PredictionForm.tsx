'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { predictDisease, handleApiError } from '@/lib/api';

interface PredictionFormProps {
  disease: string;
}

interface SelectOption {
  value: number;
  label: string;
}

interface FormField {
  name: string;
  label: string;
  type: 'number' | 'select' | 'boolean';
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  helper?: string;
  options?: SelectOption[];
}

const FORM_CONFIGS: { [key: string]: FormField[] } = {
  heart: [
    {
      name: 'age',
      label: 'Age',
      type: 'number',
      min: 1,
      max: 100,
      unit: 'years',
      helper: 'Patient age in years',
    },
    {
      name: 'gender',
      label: 'Gender',
      type: 'select',
      options: [
        { value: 1, label: 'Male' },
        { value: 2, label: 'Female' },
      ],
    },
    {
      name: 'height',
      label: 'Height',
      type: 'number',
      min: 100,
      max: 220,
      unit: 'cm',
    },
    {
      name: 'weight',
      label: 'Weight',
      type: 'number',
      min: 30,
      max: 200,
      unit: 'kg',
    },
    {
      name: 'ap_hi',
      label: 'Systolic Blood Pressure',
      type: 'number',
      min: 80,
      max: 200,
      unit: 'mmHg',
      helper: 'Normal: 90–120 mmHg',
    },
    {
      name: 'ap_lo',
      label: 'Diastolic Blood Pressure',
      type: 'number',
      min: 50,
      max: 130,
      unit: 'mmHg',
      helper: 'Normal: 60–80 mmHg',
    },
    {
      name: 'cholesterol',
      label: 'Cholesterol Level',
      type: 'select',
      options: [
        { value: 1, label: 'Normal (< 200 mg/dL)' },
        { value: 2, label: 'Above Normal (200–239 mg/dL)' },
        { value: 3, label: 'Well Above Normal (≥ 240 mg/dL)' },
      ],
    },
    {
      name: 'gluc',
      label: 'Glucose Level',
      type: 'select',
      options: [
        { value: 1, label: 'Normal (< 100 mg/dL)' },
        { value: 2, label: 'Above Normal (100–125 mg/dL)' },
        { value: 3, label: 'Well Above Normal (≥ 126 mg/dL)' },
      ],
    },
    { name: 'smoke', label: 'Smoker', type: 'boolean' },
    { name: 'alco', label: 'Alcohol Consumption', type: 'boolean' },
    { name: 'active', label: 'Physically Active', type: 'boolean' },
  ],

  diabetes: [
    { name: 'HighBP', label: 'High Blood Pressure (diagnosed)', type: 'boolean' },
    { name: 'HighChol', label: 'High Cholesterol (diagnosed)', type: 'boolean' },
    { name: 'CholCheck', label: 'Cholesterol Check in Last 5 Years', type: 'boolean' },
    {
      name: 'BMI',
      label: 'Body Mass Index (BMI)',
      type: 'number',
      min: 10,
      max: 60,
      step: 0.1,
      helper: 'Normal: 18.5–24.9',
    },
    { name: 'Smoker', label: 'Smoked ≥ 100 Cigarettes Lifetime', type: 'boolean' },
    { name: 'Stroke', label: 'History of Stroke', type: 'boolean' },
    { name: 'HeartDiseaseorAttack', label: 'History of Heart Disease / Attack', type: 'boolean' },
    { name: 'PhysActivity', label: 'Physical Activity in Past 30 Days', type: 'boolean' },
    { name: 'Fruits', label: 'Consume Fruit ≥ 1×/day', type: 'boolean' },
    { name: 'Veggies', label: 'Consume Vegetables ≥ 1×/day', type: 'boolean' },
    { name: 'HvyAlcoholConsump', label: 'Heavy Alcohol Consumption', type: 'boolean' },
    { name: 'AnyHealthcare', label: 'Has Any Healthcare Coverage', type: 'boolean' },
    { name: 'NoDocbcCost', label: 'Avoided Doctor Due to Cost (past year)', type: 'boolean' },
    {
      name: 'GenHlth',
      label: 'General Health',
      type: 'select',
      options: [
        { value: 1, label: '1 — Excellent' },
        { value: 2, label: '2 — Very Good' },
        { value: 3, label: '3 — Good' },
        { value: 4, label: '4 — Fair' },
        { value: 5, label: '5 — Poor' },
      ],
    },
    {
      name: 'MentHlth',
      label: 'Poor Mental Health Days',
      type: 'number',
      min: 0,
      max: 30,
      unit: 'days/month',
      helper: 'Days of poor mental health in the past 30 days',
    },
    {
      name: 'PhysHlth',
      label: 'Poor Physical Health Days',
      type: 'number',
      min: 0,
      max: 30,
      unit: 'days/month',
      helper: 'Days of poor physical health in the past 30 days',
    },
    { name: 'DiffWalk', label: 'Difficulty Walking / Climbing Stairs', type: 'boolean' },
    {
      name: 'Sex',
      label: 'Sex',
      type: 'select',
      options: [
        { value: 0, label: 'Female' },
        { value: 1, label: 'Male' },
      ],
    },
    {
      name: 'Age',
      label: 'Age Category',
      type: 'select',
      options: [
        { value: 1, label: '1 — Age 18–24' },
        { value: 2, label: '2 — Age 25–29' },
        { value: 3, label: '3 — Age 30–34' },
        { value: 4, label: '4 — Age 35–39' },
        { value: 5, label: '5 — Age 40–44' },
        { value: 6, label: '6 — Age 45–49' },
        { value: 7, label: '7 — Age 50–54' },
        { value: 8, label: '8 — Age 55–59' },
        { value: 9, label: '9 — Age 60–64' },
        { value: 10, label: '10 — Age 65–69' },
        { value: 11, label: '11 — Age 70–74' },
        { value: 12, label: '12 — Age 75–79' },
        { value: 13, label: '13 — Age 80+' },
      ],
    },
    {
      name: 'Education',
      label: 'Education Level',
      type: 'select',
      options: [
        { value: 1, label: '1 — Never attended school' },
        { value: 2, label: '2 — Grades 1–8 (Elementary)' },
        { value: 3, label: '3 — Grades 9–11 (Some high school)' },
        { value: 4, label: '4 — Grade 12 / GED (High school graduate)' },
        { value: 5, label: '5 — College 1–3 years (Some college)' },
        { value: 6, label: '6 — College 4+ years (College graduate)' },
      ],
    },
    {
      name: 'Income',
      label: 'Annual Household Income',
      type: 'select',
      options: [
        { value: 1, label: '1 — Less than $10,000' },
        { value: 2, label: '2 — $10,000–$14,999' },
        { value: 3, label: '3 — $15,000–$19,999' },
        { value: 4, label: '4 — $20,000–$24,999' },
        { value: 5, label: '5 — $25,000–$34,999' },
        { value: 6, label: '6 — $35,000–$49,999' },
        { value: 7, label: '7 — $50,000–$74,999' },
        { value: 8, label: '8 — $75,000 or more' },
      ],
    },
  ],

  liver: [
    {
      name: 'Age',
      label: 'Age',
      type: 'number',
      min: 1,
      max: 100,
      unit: 'years',
    },
    {
      name: 'Sex',
      label: 'Sex',
      type: 'select',
      options: [
        { value: 1, label: 'Male' },
        { value: 2, label: 'Female' },
      ],
    },
    {
      name: 'ALB',
      label: 'Albumin (ALB)',
      type: 'number',
      min: 10,
      max: 60,
      step: 0.1,
      unit: 'g/L',
      helper: 'Normal: 35–50 g/L',
    },
    {
      name: 'ALP',
      label: 'Alkaline Phosphatase (ALP)',
      type: 'number',
      min: 10,
      max: 400,
      step: 0.1,
      unit: 'U/L',
      helper: 'Normal: 30–120 U/L',
    },
    {
      name: 'ALT',
      label: 'Alanine Aminotransferase (ALT)',
      type: 'number',
      min: 5,
      max: 200,
      step: 0.1,
      unit: 'U/L',
      helper: 'Normal: 7–56 U/L',
    },
    {
      name: 'AST',
      label: 'Aspartate Aminotransferase (AST)',
      type: 'number',
      min: 5,
      max: 200,
      step: 0.1,
      unit: 'U/L',
      helper: 'Normal: 10–40 U/L',
    },
    {
      name: 'BIL',
      label: 'Bilirubin (BIL)',
      type: 'number',
      min: 1,
      max: 250,
      step: 0.1,
      unit: 'µmol/L',
      helper: 'Normal: 3–17 µmol/L',
    },
    {
      name: 'CHE',
      label: 'Cholinesterase (CHE)',
      type: 'number',
      min: 1,
      max: 20,
      step: 0.1,
      unit: 'kU/L',
      helper: 'Normal: 5–12 kU/L',
    },
    {
      name: 'CHOL',
      label: 'Cholesterol (CHOL)',
      type: 'number',
      min: 1,
      max: 10,
      step: 0.01,
      unit: 'mmol/L',
      helper: 'Normal: < 5.2 mmol/L',
    },
    {
      name: 'CREA',
      label: 'Creatinine (CREA)',
      type: 'number',
      min: 10,
      max: 1500,
      step: 0.1,
      unit: 'µmol/L',
      helper: 'Normal: 60–110 µmol/L',
    },
    {
      name: 'GGT',
      label: 'Gamma-Glutamyl Transferase (GGT)',
      type: 'number',
      min: 5,
      max: 400,
      step: 0.1,
      unit: 'U/L',
      helper: 'Normal: 0–65 U/L',
    },
    {
      name: 'PROT',
      label: 'Total Protein (PROT)',
      type: 'number',
      min: 30,
      max: 100,
      step: 0.1,
      unit: 'g/L',
      helper: 'Normal: 60–83 g/L',
    },
  ],

  kidney: [
    {
      name: 'age',
      label: 'Age',
      type: 'number',
      min: 1,
      max: 120,
      unit: 'years',
    },
    {
      name: 'bp',
      label: 'Blood Pressure',
      type: 'number',
      min: 50,
      max: 180,
      unit: 'mmHg',
      helper: 'Diastolic BP. Normal: 60–80 mmHg',
    },
    {
      name: 'sg',
      label: 'Urine Specific Gravity',
      type: 'select',
      options: [
        { value: 1.005, label: '1.005' },
        { value: 1.01, label: '1.010' },
        { value: 1.015, label: '1.015' },
        { value: 1.02, label: '1.020' },
        { value: 1.025, label: '1.025' },
      ],
    },
    {
      name: 'al',
      label: 'Albumin in Urine',
      type: 'select',
      options: [
        { value: 0, label: '0 — Absent' },
        { value: 1, label: '1 — Trace' },
        { value: 2, label: '2 — 1+' },
        { value: 3, label: '3 — 2+' },
        { value: 4, label: '4 — 3+' },
        { value: 5, label: '5 — 4+' },
      ],
    },
    {
      name: 'su',
      label: 'Sugar in Urine',
      type: 'select',
      options: [
        { value: 0, label: '0 — Absent' },
        { value: 1, label: '1 — Trace' },
        { value: 2, label: '2 — 1+' },
        { value: 3, label: '3 — 2+' },
        { value: 4, label: '4 — 3+' },
        { value: 5, label: '5 — 4+' },
      ],
    },
    {
      name: 'rbc',
      label: 'Red Blood Cells (Urine)',
      type: 'select',
      options: [
        { value: 1, label: 'Normal' },
        { value: 0, label: 'Abnormal' },
      ],
    },
    {
      name: 'pc',
      label: 'Pus Cell (Urine)',
      type: 'select',
      options: [
        { value: 1, label: 'Normal' },
        { value: 0, label: 'Abnormal' },
      ],
    },
    {
      name: 'pcc',
      label: 'Pus Cell Clumps (Urine)',
      type: 'select',
      options: [
        { value: 1, label: 'Present' },
        { value: 0, label: 'Not Present' },
      ],
    },
    {
      name: 'ba',
      label: 'Bacteria (Urine)',
      type: 'select',
      options: [
        { value: 1, label: 'Present' },
        { value: 0, label: 'Not Present' },
      ],
    },
    {
      name: 'bgr',
      label: 'Blood Glucose Random',
      type: 'number',
      min: 10,
      max: 500,
      unit: 'mg/dL',
      helper: 'Normal fasting: 70–100 mg/dL',
    },
    {
      name: 'bu',
      label: 'Blood Urea',
      type: 'number',
      min: 2,
      max: 200,
      unit: 'mg/dL',
      helper: 'Normal: 7–20 mg/dL',
    },
    {
      name: 'sc',
      label: 'Serum Creatinine',
      type: 'number',
      min: 0.1,
      max: 10,
      step: 0.1,
      unit: 'mg/dL',
      helper: 'Normal: 0.7–1.3 mg/dL',
    },
    {
      name: 'sod',
      label: 'Sodium',
      type: 'number',
      min: 100,
      max: 160,
      unit: 'mEq/L',
      helper: 'Normal: 136–145 mEq/L',
    },
    {
      name: 'pot',
      label: 'Potassium',
      type: 'number',
      min: 2,
      max: 10,
      step: 0.1,
      unit: 'mEq/L',
      helper: 'Normal: 3.5–5.0 mEq/L',
    },
    {
      name: 'hemo',
      label: 'Hemoglobin',
      type: 'number',
      min: 3,
      max: 18,
      step: 0.1,
      unit: 'g/dL',
      helper: 'Normal: 12–17 g/dL',
    },
    {
      name: 'pcv',
      label: 'Packed Cell Volume (Hematocrit)',
      type: 'number',
      min: 10,
      max: 60,
      unit: '%',
      helper: 'Normal: 36–50%',
    },
    {
      name: 'wc',
      label: 'White Blood Cell Count',
      type: 'number',
      min: 2000,
      max: 20000,
      unit: 'cells/µL',
      helper: 'Normal: 4,500–11,000 cells/µL',
    },
    {
      name: 'rc',
      label: 'Red Blood Cell Count',
      type: 'number',
      min: 2,
      max: 8,
      step: 0.1,
      unit: 'millions/µL',
      helper: 'Normal: 4.5–5.5 millions/µL',
    },
    { name: 'htn', label: 'Hypertension (diagnosed)', type: 'boolean' },
    { name: 'dm', label: 'Diabetes Mellitus (diagnosed)', type: 'boolean' },
    { name: 'cad', label: 'Coronary Artery Disease (diagnosed)', type: 'boolean' },
    {
      name: 'appet',
      label: 'Appetite',
      type: 'select',
      options: [
        { value: 1, label: 'Good' },
        { value: 0, label: 'Poor' },
      ],
    },
    { name: 'pe', label: 'Pedal Edema (foot swelling)', type: 'boolean' },
    { name: 'ane', label: 'Anemia (diagnosed)', type: 'boolean' },
  ],
};

const DISEASE_LABELS: { [key: string]: string } = {
  heart: 'Heart Disease',
  diabetes: 'Diabetes',
  liver: 'Liver Disease',
  kidney: 'Kidney Disease',
};

export default function PredictionForm({ disease }: PredictionFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState<{ [key: string]: number }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fields = FORM_CONFIGS[disease] || [];

  const handleChange = (fieldName: string, value: number) => {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const missingFields = fields.filter((f) => !(f.name in formData));
      if (missingFields.length > 0) {
        throw new Error(
          `Please fill all required fields: ${missingFields.map((f) => f.label).join(', ')}`
        );
      }

      const result = await predictDisease(disease, formData);

      localStorage.setItem(
        `prediction_${disease}`,
        JSON.stringify({
          disease,
          input: formData,
          result,
          timestamp: new Date().toISOString(),
        })
      );

      router.push(`/result/${disease}`);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const inputClass =
    'border border-gray-300 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-cyan-500 transition text-gray-800 bg-white';

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-8 rounded-xl shadow-md max-w-3xl mx-auto"
    >
      <h2
        className="text-2xl font-bold text-gray-900 mb-2"
        style={{ fontFamily: 'Georgia, serif' }}
      >
        Patient Information
      </h2>
      <p className="text-sm text-gray-500 mb-6">
        Enter clinical values for <strong>{DISEASE_LABELS[disease] || disease}</strong> risk assessment.
        All fields are required.
      </p>

      {error && (
        <div className="mb-5 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-8">
        {fields.map((field) => (
          <div key={field.name} className="flex flex-col">
            <label htmlFor={field.name} className="text-sm font-semibold text-gray-700 mb-1">
              {field.label}
              {field.unit && (
                <span className="ml-1 text-gray-400 font-normal">({field.unit})</span>
              )}
            </label>

            {field.type === 'number' && (
              <div>
                <input
                  id={field.name}
                  type="number"
                  min={field.min}
                  max={field.max}
                  step={field.step ?? 1}
                  value={formData[field.name] ?? ''}
                  onChange={(e) => handleChange(field.name, parseFloat(e.target.value))}
                  className={inputClass}
                  required
                  placeholder={`${field.min} – ${field.max}`}
                />
                {field.helper && (
                  <p className="text-xs text-gray-400 mt-1">{field.helper}</p>
                )}
              </div>
            )}

            {field.type === 'select' && (
              <select
                id={field.name}
                value={formData[field.name] ?? ''}
                onChange={(e) => handleChange(field.name, parseFloat(e.target.value))}
                className={inputClass}
                required
              >
                <option value="">— Select —</option>
                {field.options?.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            )}

            {field.type === 'boolean' && (
              <div className="flex space-x-3 mt-1">
                <button
                  type="button"
                  id={`${field.name}-yes`}
                  onClick={() => handleChange(field.name, 1)}
                  className={`flex-1 py-2 rounded-lg text-sm font-semibold border transition-colors ${
                    formData[field.name] === 1
                      ? 'bg-cyan-500 text-white border-cyan-500 shadow'
                      : 'bg-gray-50 text-gray-700 border-gray-300 hover:bg-gray-100'
                  }`}
                >
                  Yes
                </button>
                <button
                  type="button"
                  id={`${field.name}-no`}
                  onClick={() => handleChange(field.name, 0)}
                  className={`flex-1 py-2 rounded-lg text-sm font-semibold border transition-colors ${
                    formData[field.name] === 0
                      ? 'bg-cyan-500 text-white border-cyan-500 shadow'
                      : 'bg-gray-50 text-gray-700 border-gray-300 hover:bg-gray-100'
                  }`}
                >
                  No
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      <button
        type="submit"
        id="submit-prediction"
        disabled={loading}
        className="w-full bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors text-base shadow"
      >
        {loading ? (
          <span className="flex items-center justify-center space-x-2">
            <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            <span>Analyzing patient data...</span>
          </span>
        ) : (
          'Analyze Risk'
        )}
      </button>
    </form>
  );
}
