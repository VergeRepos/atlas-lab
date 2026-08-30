import React, { useState } from 'react';
import { Database, Upload, Trash2, Download, Table, BarChart3, AlertCircle, CheckCircle } from 'lucide-react';

interface Dataset {
  id: string;
  name: string;
  file_path: string;
  rows: number;
  columns: number;
  created_at: string;
  preview?: string[];
}

const mockDatasets: Dataset[] = [
  { id: '1', name: 'Customer Churn', file_path: '/data/churn.csv', rows: 1000, columns: 12, created_at: '2024-01-15', preview: ['id', 'age', 'income', 'purchases', 'recency', 'target'] },
  { id: '2', name: 'Sales 2024', file_path: '/data/sales.csv', rows: 5000, columns: 8, created_at: '2024-01-20', preview: ['date', 'product', 'quantity', 'price', 'region'] },
  { id: '3', name: 'Customer Feedback', file_path: '/data/feedback.csv', rows: 2500, columns: 15, created_at: '2024-01-22', preview: ['id', 'rating', 'comment', 'category', 'sentiment'] },
];

export default function Datasets() {
  const [datasets] = useState<Dataset[]>(mockDatasets);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Datasets</h1>
          <p className="text-stone-400 text-sm">Manage and analyze your tabular data</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition">
            <Upload className="w-4 h-4" /> Import CSV
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl">
            <div className="px-4 py-3 border-b border-stone-700/50">
              <h2 className="text-sm font-medium text-stone-200">Your Datasets</h2>
            </div>
            <div className="divide-y divide-stone-700/30">
              {datasets.map(ds => (
                <div key={ds.id} onClick={() => setSelectedDataset(ds)} className={`px-4 py-3 cursor-pointer hover:bg-stone-700/30 transition ${selectedDataset?.id === ds.id ? 'bg-stone-700/40 border-l-2 border-emerald-500' : ''}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-stone-700/50 rounded-lg"><Database className="w-4 h-4 text-stone-300" /></div>
                      <div>
                        <div className="text-sm font-medium text-stone-100">{ds.name}</div>
                        <div className="text-xs text-stone-500">{ds.file_path}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 text-xs text-stone-400">
                      <span>{ds.rows.toLocaleString()} rows</span>
                      <span>{ds.columns} cols</span>
                      <button className="p-1 hover:bg-stone-600/50 rounded transition"><Trash2 className="w-3.5 h-3.5" /></button>
                    </div>
                  </div>
                </div>
              ))}
              {datasets.length === 0 && (
                <div className="px-4 py-8 text-center">
                  <Database className="w-8 h-8 text-stone-600 mx-auto mb-2" />
                  <p className="text-sm text-stone-500">No datasets yet</p>
                  <p className="text-xs text-stone-600">Import a CSV to get started</p>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {selectedDataset ? (
            <>
              <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl p-4">
                <h3 className="text-sm font-medium text-stone-200 mb-3">{selectedDataset.name}</h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between"><span className="text-stone-500">Rows</span><span className="text-stone-300">{selectedDataset.rows.toLocaleString()}</span></div>
                  <div className="flex justify-between"><span className="text-stone-500">Columns</span><span className="text-stone-300">{selectedDataset.columns}</span></div>
                  <div className="flex justify-between"><span className="text-stone-500">Created</span><span className="text-stone-300">{selectedDataset.created_at}</span></div>
                </div>
                <div className="mt-4 flex gap-2">
                  <button className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 text-xs font-medium rounded-lg transition"><Table className="w-3.5 h-3.5" /> Preview</button>
                  <button className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 text-xs font-medium rounded-lg transition"><BarChart3 className="w-3.5 h-3.5" /> Analyze</button>
                </div>
              </div>
              <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl p-4">
                <h3 className="text-sm font-medium text-stone-200 mb-3">Columns</h3>
                <div className="flex flex-wrap gap-1.5">
                  {selectedDataset.preview?.map(col => (
                    <span key={col} className="px-2 py-1 bg-stone-700/50 text-stone-300 text-xs rounded">{col}</span>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl p-6 text-center">
              <AlertCircle className="w-8 h-8 text-stone-600 mx-auto mb-2" />
              <p className="text-sm text-stone-500">Select a dataset</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
