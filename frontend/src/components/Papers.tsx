import React from 'react';
import { FileCode } from 'lucide-react';
export default function Papers() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><FileCode /> Research Papers</h1>
      <p className="text-muted-foreground mt-2 mb-6">Write, cite, and format technical papers.</p>
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Paper Sections</h2>
        {['Abstract','Introduction','Related Work','Methodology','Results','Discussion','Conclusion','References'].map(s => (
          <div key={s} className="p-3 bg-secondary/20 rounded border border-border/30 mb-2 hover:bg-secondary/50 transition-colors cursor-pointer">
            <h3 className="font-medium">{s}</h3>
          </div>
        ))}
      </div>
      <div className="mt-6 grid md:grid-cols-2 gap-6">
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-3">Citations</h3>
          <div className="text-sm text-muted-foreground space-y-1">
            <p>Smith, J. (2024). <i>Retrieval Strategies in RAG.</i></p>
            <p>Doe, A. (2023). Deep Learning Fundamentals.</p>
          </div>
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-3">Paper Stats</h3>
          <div className="text-sm space-y-1 text-muted-foreground">
            <p>Words: 3,420</p>
            <p>References: 12</p>
            <p>Sections: 8</p>
          </div>
        </div>
      </div>
    </div>
  );
}
