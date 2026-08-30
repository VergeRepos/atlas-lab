import React from 'react';
import { FlaskConical, Plus, Clock } from 'lucide-react';
export default function Experiments() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><FlaskConical /> Experiments</h1>
      <p className="text-muted-foreground mt-2 mb-6">Track experiments with full reproducibility.</p>
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Active Experiments</h2>
        <div className="space-y-3">
          {[
            {name:"RAG Dense Retrieval", status:"running", params:"top_k=5, chunk=1024", time:"2m 14s"},
            {name:"Linear Regression Model", status:"completed", params:"features: 4, alpha=0.1", time:"45s"},
          ].map((e,i) => (
            <div key={i} className="p-4 bg-secondary/50 rounded border border-border/50 flex items-center justify-between">
              <div><h3 className="font-medium">{e.name}</h3><p className="text-xs text-muted-foreground">{e.params}</p></div>
              <div className="text-right"><span className={`text-xs px-2 py-0.5 rounded ${e.status==='running'?'bg-amber-100 text-amber-700':'bg-emerald-100 text-emerald-700'}`}>{e.status}</span><p className="text-xs mt-1">{e.time}</p></div>
            </div>
          ))}
        </div>
        <button className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 flex items-center gap-2"><Plus size={16}/> New Experiment</button>
      </div>
      <div className="mt-6 bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-3">Experiment Log</h2>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div><span className="text-muted-foreground">Total:</span> <b>12</b></div>
          <div><span className="text-muted-foreground">Running:</span> <b>2</b></div>
          <div><span className="text-muted-foreground">Completed:</span> <b>8</b></div>
        </div>
      </div>
    </div>
  );
}
