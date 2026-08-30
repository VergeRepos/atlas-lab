import React, { useState } from 'react';
import { Brain, CheckCircle, Clock, BookOpen } from 'lucide-react';
export default function Learning() {
  const [subject, setSubject] = useState('Linear Algebra');
  const topics = [
    { title: 'Vectors and Vector Spaces', completed: true },
    { title: 'Matrices and Operations', completed: true },
    { title: 'Eigenvalues and Eigenvectors', completed: false },
  ];
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold flex items-center gap-3"><Brain /> Learning Mode</h1>
      <p className="text-muted-foreground mt-2 mb-6">Structured paths with mastery tracking.</p>
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-card border border-border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">{subject}</h2>
          <div className="space-y-4">
            {topics.map((t,i) => (
              <div key={i} className="flex items-center gap-3 p-3 bg-secondary/50 rounded border border-border/50">
                {t.completed ? <CheckCircle className="text-emerald-500" size={20}/> : <Clock className="text-amber-500" size={20}/>}
                <div><h3 className="font-medium">{t.title}</h3><p className="text-xs text-muted-foreground">{t.completed ? 'Completed' : 'In progress'}</p></div>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Current Topic</h2>
          <div className="p-4 bg-secondary/30 rounded border border-border/30">
            <h3 className="font-semibold text-lg">Eigenvalues and Eigenvectors</h3>
            <p className="text-sm text-muted-foreground mt-1">Eigenvectors are non-zero vectors that don't change direction under linear transformations.</p>
            <div className="mt-4 text-xs space-y-1 text-muted-foreground">
              <p>Prerequisites: Matrices and Operations</p>
              <p>Difficulty: Intermediate</p>
              <p>Estimated time: 45 min</p>
            </div>
            <button className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">Continue Learning</button>
          </div>
        </div>
      </div>
    </div>
  );
}
