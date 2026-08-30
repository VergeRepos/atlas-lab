import React from 'react';
import {
  Home, Beaker, Brain, FileText, FlaskConical, Database, Cpu,
  GraduationCap, CreditCard, FileCode, Quote, Clock, Activity,
  Monitor, Settings as SettingsIcon
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentView, onViewChange }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'research', label: 'Research', icon: Beaker },
    { id: 'knowledge', label: 'Knowledge', icon: Brain },
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'experiments', label: 'Experiments', icon: FlaskConical },
    { id: 'datasets', label: 'Datasets', icon: Database },
    { id: 'ml', label: 'ML Lab', icon: Cpu },
    { id: 'learning', label: 'Learning', icon: GraduationCap },
    { id: 'flashcards', label: 'Flashcards', icon: CreditCard },
    { id: 'papers', label: 'Papers', icon: FileCode },
    { id: 'citations', label: 'Citations', icon: Quote },
    { id: 'timeline', label: 'Timeline', icon: Clock },
    { id: 'benchmarks', label: 'Benchmarks', icon: Activity },
    { id: 'system', label: 'System', icon: Monitor },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  return (
    <aside className="w-64 bg-card border-r border-border flex flex-col">
      <div className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold text-primary">Atlas Lab</h1>
        <p className="text-sm text-muted-foreground mt-1">Research Workstation</p>
      </div>

      <nav className="flex-1 p-4 overflow-y-auto">
        <ul className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;

            return (
              <li key={item.id}>
                <button
                  onClick={() => onViewChange(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'hover:bg-secondary text-foreground'
                  }`}
                >
                  <Icon size={20} />
                  <span className="text-sm font-medium">{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="p-4 border-t border-border text-xs text-muted-foreground">
        <p>v1.0.0</p>
        <p className="mt-1">Press Ctrl+K for commands</p>
      </div>
    </aside>
  );
};

export default Sidebar;