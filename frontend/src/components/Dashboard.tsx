import React from 'react';
import { Plus, BookOpen, Brain, FlaskConical, Search, Clock, Award } from 'lucide-react';

interface DashboardProps {
  onNavigate: (view: any) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Welcome Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Welcome to Atlas Lab</h1>
        <p className="text-muted-foreground mt-2">
          Your AI-powered research and learning workstation. Conduct experiments, analyze data, and build knowledge.
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <button
          onClick={() => onNavigate('research')}
          className="p-6 bg-card border border-border rounded-lg text-left hover:border-primary transition-colors group"
        >
          <Plus className="text-primary mb-3 group-hover:scale-110 transition-transform" size={24} />
          <h3 className="font-semibold text-lg">New Project</h3>
          <p className="text-sm text-muted-foreground mt-1">Start a new research workspace</p>
        </button>

        <button
          onClick={() => onNavigate('documents')}
          className="p-6 bg-card border border-border rounded-lg text-left hover:border-primary transition-colors group"
        >
          <BookOpen className="text-primary mb-3 group-hover:scale-110 transition-transform" size={24} />
          <h3 className="font-semibold text-lg">Import Documents</h3>
          <p className="text-sm text-muted-foreground mt-1">Add PDFs, Markdown, TXT</p>
        </button>

        <button
          onClick={() => onNavigate('learning')}
          className="p-6 bg-card border border-border rounded-lg text-left hover:border-primary transition-colors group"
        >
          <Brain className="text-primary mb-3 group-hover:scale-110 transition-transform" size={24} />
          <h3 className="font-semibold text-lg">Start Learning</h3>
          <p className="text-sm text-muted-foreground mt-1">Explore structured courses</p>
        </button>

        <button
          onClick={() => onNavigate('experiments')}
          className="p-6 bg-card border border-border rounded-lg text-left hover:border-primary transition-colors group"
        >
          <FlaskConical className="text-primary mb-3 group-hover:scale-110 transition-transform" size={24} />
          <h3 className="font-semibold text-lg">Run Experiment</h3>
          <p className="text-sm text-muted-foreground mt-1">Launch an ML pipeline</p>
        </button>
      </div>

      {/* Featured Example Project Banner */}
      <div className="bg-primary/10 border border-primary/30 rounded-lg p-6 mb-8 flex items-center justify-between">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider bg-primary/20 text-primary px-2 py-1 rounded">Sample Project Available</span>
          <h2 className="text-xl font-bold mt-2">Does retrieval strategy affect RAG answer quality?</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Explore a complete pre-configured research project comparing Dense, Sparse, and Hybrid retrieval methods.
          </p>
        </div>
        <button
          onClick={() => onNavigate('research')}
          className="px-4 py-2 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 transition-colors shrink-0 ml-4"
        >
          Open Project
        </button>
      </div>

      {/* Stats and Recent Activity */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
            <Clock size={18} className="text-primary" />
            Recent Research
          </h3>
          <div className="space-y-3">
            <div className="p-3 bg-secondary/50 rounded border border-border/50">
              <p className="font-medium text-sm">RAG Retrieval Comparison</p>
              <p className="text-xs text-muted-foreground">3 experiments • 12 documents</p>
            </div>
            <div className="p-3 bg-secondary/50 rounded border border-border/50">
              <p className="font-medium text-sm">Neural Network Architectures</p>
              <p className="text-xs text-muted-foreground">5 notes • 2 datasets</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
            <Award size={18} className="text-primary" />
            Learning Progress
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Linear Algebra</span>
                <span className="text-muted-foreground">75%</span>
              </div>
              <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
                <div className="bg-primary h-full w-3/4"></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Neural Networks</span>
                <span className="text-muted-foreground">40%</span>
              </div>
              <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
                <div className="bg-primary h-full w-2/5"></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
            <Search size={18} className="text-primary" />
            System Health
          </h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Database:</span>
              <span className="text-emerald-500 font-medium">SQLite Connected</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">AI Engine:</span>
              <span className="text-emerald-500 font-medium">Local Embeddings Active</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Ollama:</span>
              <span className="text-amber-500 font-medium">Ready (Offline mode)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;