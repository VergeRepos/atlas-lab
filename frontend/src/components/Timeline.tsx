import React from 'react';
import { Clock } from 'lucide-react';
export default function Timeline() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><Clock /> Research Timeline</h1>
      <p className="text-muted-foreground mt-2 mb-6">Track your research evolution over time.</p>
      <div className="relative border-l-2 border-border ml-4 space-y-8 pb-8">
        {[
          {date:'Aug 28, 2026', type:'experiment', title:'RAG Dense Retrieval Test', desc:'Completed baseline retrieval experiment'},
          {date:'Aug 26, 2026', type:'note', title:'Literature Review Started', desc:'Reviewed 5 papers on retrieval strategies'},
          {date:'Aug 24, 2026', type:'discovery', title:'Interesting Pattern Found', desc:'Hybrid retrieval outperforms dense alone'},
          {date:'Aug 20, 2026', type:'milestone', title:'Project Created', desc:'Initial project setup and document import'},
        ].map((e,i) => (
          <div key={i} className="ml-6 bg-card border border-border rounded-lg p-4">
            <p className="text-xs text-primary font-semibold">{e.date}</p>
            <h3 className="font-semibold mt-1">{e.title}</h3>
            <p className="text-sm text-muted-foreground">{e.desc}</p>
            <span className="inline-block mt-2 text-xs px-2 py-0.5 bg-secondary rounded">{e.type}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
