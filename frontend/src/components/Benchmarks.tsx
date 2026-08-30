import React from 'react';
import { Activity } from 'lucide-react';
export default function Benchmarks() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><Activity /> Benchmarks</h1>
      <p className="text-muted-foreground mt-2 mb-6">Performance metrics for system components.</p>
      <div className="grid md:grid-cols-2 gap-6">
        {[
          {name:'Document Ingestion', mean:'12ms', p95:'28ms', throughput:'83 docs/s'},
          {name:'Embedding Generation', mean:'45ms', p95:'120ms', throughput:'22 emb/s'},
          {name:'Semantic Search', mean:'8ms', p95:'22ms', throughput:'125 queries/s'},
          {name:'RAG Retrieval', mean:'52ms', p95:'145ms', throughput:'19 queries/s'},
        ].map((b,i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-5">
            <h3 className="font-semibold text-lg mb-3">{b.name}</h3>
            <div className="grid grid-cols-3 gap-3 text-sm">
              <div><span className="text-muted-foreground">Mean</span><p className="font-medium">{b.mean}</p></div>
              <div><span className="text-muted-foreground">P95</span><p className="font-medium">{b.p95}</p></div>
              <div><span className="text-muted-foreground">Throughput</span><p className="font-medium">{b.throughput}</p></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
