import React, { useState } from 'react';
import { Network, Plus, ZoomIn, ZoomOut, RefreshCw, Search, Trash2 } from 'lucide-react';

interface Node {
  id: string;
  label: string;
  type: 'concept' | 'document' | 'entity' | 'topic';
  x: number;
  y: number;
}

interface Edge {
  source: string;
  target: string;
  label?: string;
}

const initialNodes: Node[] = [
  { id: '1', label: 'RAG', type: 'concept', x: 200, y: 150 },
  { id: '2', label: 'Embeddings', type: 'concept', x: 400, y: 100 },
  { id: '3', label: 'Vector DB', type: 'concept', x: 600, y: 200 },
  { id: '4', label: 'Transformer', type: 'concept', x: 350, y: 280 },
  { id: '5', label: 'Paper: RAG', type: 'document', x: 100, y: 280 },
  { id: '6', label: 'Paper: BERT', type: 'document', x: 550, y: 350 },
  { id: '7', label: 'Ollama', type: 'entity', x: 700, y: 100 },
];

const initialEdges: Edge[] = [
  { source: '1', target: '2', label: 'uses' },
  { source: '1', target: '3', label: 'queries' },
  { source: '2', target: '4', label: 'based on' },
  { source: '5', target: '1', label: 'cites' },
  { source: '6', target: '4', label: 'introduces' },
  { source: '7', target: '4', label: 'serves' },
];

const colorFor = (type: string) => type === 'concept' ? '#10b981' : type === 'document' ? '#f59e0b' : type === 'entity' ? '#3b82f6' : '#a78bfa';

export default function Knowledge() {
  const [search, setSearch] = useState('');
  const [zoom, setZoom] = useState(1);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3"><Network className="w-6 h-6" /> Knowledge Graph</h1>
          <p className="text-stone-400 text-sm">Explore relationships between concepts and documents</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-stone-800 hover:bg-stone-700 text-stone-300 text-xs font-medium rounded-lg transition"><Plus className="w-3.5 h-3.5" /> Add Node</button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl p-4">
          <h3 className="text-sm font-medium text-stone-200 mb-3">Search</h3>
          <div className="flex items-center gap-2 px-2 py-1.5 bg-stone-900/50 border border-stone-700/50 rounded">
            <Search className="w-3.5 h-3.5 text-stone-500" />
            <input value={search} onChange={e => setSearch(e.target.value)} className="bg-transparent outline-none text-xs text-stone-200 w-full" placeholder="Find nodes..." />
          </div>
          <div className="mt-4 space-y-1.5 text-xs">
            <div className="text-stone-500 mb-2">Legend</div>
            <Legend color="#10b981" label="Concept" />
            <Legend color="#f59e0b" label="Document" />
            <Legend color="#3b82f6" label="Entity" />
            <Legend color="#a78bfa" label="Topic" />
          </div>
          <div className="mt-4 pt-3 border-t border-stone-700/50">
            <div className="text-stone-500 text-xs mb-2">Stats</div>
            <div className="space-y-1 text-xs text-stone-300">
              <div className="flex justify-between"><span>Nodes</span><span className="font-mono">{initialNodes.length}</span></div>
              <div className="flex justify-between"><span>Edges</span><span className="font-mono">{initialEdges.length}</span></div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-3 bg-stone-800/50 border border-stone-700/50 rounded-xl overflow-hidden">
          <div className="flex items-center justify-between px-4 py-2 border-b border-stone-700/50">
            <span className="text-xs text-stone-400">Force-directed graph · 2D view</span>
            <div className="flex items-center gap-1">
              <button onClick={() => setZoom(z => Math.min(2, z + 0.1))} className="p-1 hover:bg-stone-700 rounded"><ZoomIn className="w-3.5 h-3.5 text-stone-400" /></button>
              <button onClick={() => setZoom(z => Math.max(0.5, z - 0.1))} className="p-1 hover:bg-stone-700 rounded"><ZoomOut className="w-3.5 h-3.5 text-stone-400" /></button>
              <button className="p-1 hover:bg-stone-700 rounded"><RefreshCw className="w-3.5 h-3.5 text-stone-400" /></button>
            </div>
          </div>
          <div className="relative" style={{ height: '480px' }}>
            <svg viewBox="0 0 800 480" className="w-full h-full" style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }}>
              <g>
                {initialEdges.map((e, i) => {
                  const s = initialNodes.find(n => n.id === e.source);
                  const t = initialNodes.find(n => n.id === e.target);
                  if (!s || !t) return null;
                  return <line key={i} x1={s.x} y1={s.y} x2={t.x} y2={t.y} stroke="#57534e" strokeWidth="1.5" />;
                })}
              </g>
              <g>
                {initialNodes.map(n => (
                  <g key={n.id} className="cursor-pointer">
                    <circle cx={n.x} cy={n.y} r="18" fill={colorFor(n.type)} opacity="0.85" />
                    <text x={n.x} y={n.y + 4} textAnchor="middle" fontSize="10" fill="white" fontWeight="600">{n.label.charAt(0)}</text>
                    <text x={n.x} y={n.y + 35} textAnchor="middle" fontSize="10" fill="#d6d3d1">{n.label}</text>
                  </g>
                ))}
              </g>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
      <span className="text-stone-400">{label}</span>
    </div>
  );
}
