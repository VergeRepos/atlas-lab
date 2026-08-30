import React from 'react';
import { Quote } from 'lucide-react';
export default function Citations() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><Quote /> Citations</h1>
      <p className="text-muted-foreground mt-2 mb-6">Manage references in APA, MLA, IEEE formats.</p>
      <div className="space-y-4">
        {[
          {authors:['Smith, J., Doe, A.'], title:'Retrieval-Augmented Generation: A Survey', year:2024, type:'article'},
          {authors:['Johnson, M.'], title:'Neural Network Architectures', year:2023, type:'book'},
        ].map((c,i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-4">
            <p className="text-sm">{c.authors.join(', ')} ({c.year}). <b>{c.title}</b>.</p>
            <p className="text-xs text-muted-foreground mt-1">Type: {c.type} | Format: APA</p>
          </div>
        ))}
      </div>
    </div>
  );
}
