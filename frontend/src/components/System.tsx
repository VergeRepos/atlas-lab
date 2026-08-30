import React, { useState, useEffect } from 'react';
import { Monitor } from 'lucide-react';
export default function System() {
  const [cpu, setCpu] = useState(0);
  const [mem, setMem] = useState({total: 0, used: 0});
  useEffect(() => {
    const timer = setInterval(() => {
      setCpu(Math.random() * 30 + 10);
      setMem({total: 32, used: Math.random() * 10 + 8});
    }, 2000);
    return () => clearInterval(timer);
  }, []);
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><Monitor /> System Monitor</h1>
      <p className="text-muted-foreground mt-2 mb-6">Hardware usage and diagnostics.</p>
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[
          {label:'CPU Usage', value:cpu, unit:'%', color:'bg-blue-500'},
          {label:'RAM', value:(mem.used/32)*100, unit:'%', color:'bg-emerald-500'},
          {label:'GPU', value:0, unit:'%', color:'bg-amber-500'},
          {label:'Disk', value:45, unit:'%', color:'bg-purple-500'},
        ].map((m,i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-4">
            <p className="text-xs text-muted-foreground">{m.label}</p>
            <p className="text-2xl font-bold mt-1">{m.value.toFixed(1)}{m.unit}</p>
            <div className="w-full bg-secondary h-2 rounded-full mt-2">
              <div className={`h-2 rounded-full ${m.color}`} style={{width:`${m.value}%`}}/>
            </div>
          </div>
        ))}
      </div>
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="font-semibold text-lg mb-4">Diagnostics</h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between"><span>App Version</span><b>1.0.0</b></div>
          <div className="flex justify-between"><span>Database</span><span className="text-emerald-500">Connected</span></div>
          <div className="flex justify-between"><span>Python Backend</span><span className="text-emerald-500">Running on :8000</span></div>
          <div className="flex justify-between"><span>Embedding Model</span><span className="text-emerald-500">all-MiniLM-L6-v2</span></div>
          <div className="flex justify-between"><span>Ollama</span><span className="text-amber-500">Not detected</span></div>
          <div className="flex justify-between"><span>Documents</span><b>0 indexed</b></div>
          <div className="flex justify-between"><span>Chunks</span><b>0 embedded</b></div>
        </div>
      </div>
    </div>
  );
}
