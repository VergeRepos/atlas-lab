import React, { useState } from 'react';
import { FlaskConical, Database, Brain, Sparkles, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface Experiment {
  id: string;
  name: string;
  status: 'planned' | 'running' | 'completed' | 'failed';
  task_type: string;
  algorithm: string;
  dataset_path: string;
  created_at: string;
  metrics?: Record<string, number>;
}

const experiments: Experiment[] = [
  { id: '1', name: 'Churn Prediction', status: 'completed', task_type: 'classification', algorithm: 'logistic_regression', dataset_path: '/data/churn.csv', created_at: '2024-01-20', metrics: { accuracy: 0.87, precision: 0.82, recall: 0.79 } },
  { id: '2', name: 'Customer Lifetime Value', status: 'running', task_type: 'regression', algorithm: 'random_forest', dataset_path: '/data/sales.csv', created_at: '2024-01-21' },
  { id: '3', name: 'Market Segmentation', status: 'planned', task_type: 'clustering', algorithm: 'k_means', dataset_path: '/data/feedback.csv', created_at: '2024-01-22' },
];

export default function Research() {
  const [hoverId, setHoverId] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3"><FlaskConical className="w-6 h-6" /> Research Workspace</h1>
          <p className="text-stone-400 text-sm">Design, run, and analyze experiments</p>
        </div>
        <button className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition">New Experiment</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard label="Active Experiments" value="3" icon={<FlaskConical className="w-5 h-5" />} />
        <StatCard label="Completed" value="14" icon={<CheckCircle className="w-5 h-5" />} />
        <StatCard label="Avg Accuracy" value="84.2%" icon={<Sparkles className="w-5 h-5" />} />
      </div>

      <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-stone-700/50 flex items-center justify-between">
          <h2 className="text-sm font-medium text-stone-200">Recent Experiments</h2>
          <div className="flex gap-2 text-xs">
            <button className="px-2 py-0.5 bg-stone-700 rounded text-stone-300">All</button>
            <button className="px-2 py-0.5 bg-stone-900 rounded text-stone-500">Completed</button>
            <button className="px-2 py-0.5 bg-stone-900 rounded text-stone-500">Running</button>
          </div>
        </div>
        <div className="divide-y divide-stone-700/30">
          {experiments.map(exp => (
            <div key={exp.id} onMouseEnter={() => setHoverId(exp.id)} onMouseLeave={() => setHoverId(null)} className={`px-4 py-3 flex items-center justify-between hover:bg-stone-700/30 transition ${hoverId === exp.id ? 'bg-stone-700/20' : ''}`}>
              <div className="flex items-center gap-3">
                <div className={`p-1.5 rounded-lg ${exp.status === 'completed' ? 'bg-emerald-900/30 text-emerald-400' : exp.status === 'running' ? 'bg-amber-900/30 text-amber-400' : 'bg-stone-800 text-stone-500'}`}>
                  <Brain className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-medium text-stone-100">{exp.name}</div>
                  <div className="text-xs text-stone-500">{exp.task_type} · {exp.algorithm} · {exp.dataset_path}</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {exp.status === 'running' && <span className="flex items-center gap-1 text-xs text-amber-400"><Clock className="w-3 h-3" /> Running</span>}
                {exp.status === 'completed' && exp.metrics && <span className="text-xs text-emerald-400 font-mono">Acc {exp.metrics.accuracy}</span>}
                {exp.status === 'planned' && <span className="text-xs text-stone-500">Planned</span>}
                <button className="text-xs text-stone-400 hover:text-white transition">View →</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon }: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-stone-500">{label}</span>
        <span className="text-emerald-400">{icon}</span>
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
    </div>
  );
}
