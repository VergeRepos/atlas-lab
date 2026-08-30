import React, { useState } from 'react';
import { FlaskConical, Play, BarChart3, Table, AlertCircle, CheckCircle2 } from 'lucide-react';

interface Experiment {
  id: string;
  name: string;
  task: 'classification' | 'regression' | 'clustering';
  algorithm: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  metrics: { accuracy?: number; f1?: number; rmse?: number; r2?: number };
  createdAt: Date;
}

const MLLab: React.FC = () => {
  const [experiments] = useState<Experiment[]>([
    { id: '1', name: 'Customer Churn Classification', task: 'classification', algorithm: 'Random Forest', status: 'completed', metrics: { accuracy: 0.94, f1: 0.91 }, createdAt: new Date('2026-08-25') },
    { id: '2', name: 'House Price Prediction', task: 'regression', algorithm: 'Linear Regression', status: 'completed', metrics: { rmse: 2450, r2: 0.87 }, createdAt: new Date('2026-08-26') },
  ]);

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <FlaskConical className="text-primary" /> ML Lab
          </h1>
          <p className="text-sm text-muted-foreground mt-1">Run machine learning experiments with scikit-learn</p>
        </div>
        <button className="px-4 py-2 bg-primary text-primary-foreground font-medium rounded-md flex items-center gap-2">
          <Play size={16} /> New Experiment
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-card border border-border rounded-lg">
          <span className="text-xs text-muted-foreground">Total Experiments</span>
          <p className="text-2xl font-bold mt-1">{experiments.length}</p>
        </div>
        <div className="p-4 bg-card border border-border rounded-lg">
          <span className="text-xs text-muted-foreground">Best Accuracy</span>
          <p className="text-2xl font-bold mt-1 text-emerald-500">94%</p>
        </div>
        <div className="p-4 bg-card border border-border rounded-lg">
          <span className="text-xs text-muted-foreground">Datasets Loaded</span>
          <p className="text-2xl font-bold mt-1">3</p>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg">
        <div className="p-4 border-b border-border">
          <h3 className="font-semibold">Recent Experiments</h3>
        </div>
        <div className="divide-y divide-border">
          {experiments.map((exp) => (
            <div key={exp.id} className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                {exp.status === 'completed' ? (
                  <CheckCircle2 className="text-emerald-500" size={20} />
                ) : (
                  <AlertCircle className="text-amber-500" size={20} />
                )}
                <div>
                  <p className="font-medium text-sm">{exp.name}</p>
                  <p className="text-xs text-muted-foreground">{exp.algorithm} • {exp.task}</p>
                </div>
              </div>
              <div className="text-right">
                {exp.metrics.accuracy && <p className="text-sm font-medium">Accuracy: {(exp.metrics.accuracy * 100).toFixed(1)}%</p>}
                {exp.metrics.r2 && <p className="text-sm font-medium">R²: {exp.metrics.r2.toFixed(2)}</p>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MLLab;