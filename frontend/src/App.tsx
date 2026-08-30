import React, { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Research from './components/Research';
import Knowledge from './components/Knowledge';
import Documents from './components/Documents';
import Experiments from './components/Experiments';
import Datasets from './components/Datasets';
import MLLab from './components/MLLab';
import Learning from './components/Learning';
import Flashcards from './components/Flashcards';
import Papers from './components/Papers';
import Citations from './components/Citations';
import Timeline from './components/Timeline';
import Benchmarks from './components/Benchmarks';
import System from './components/System';
import Settings from './components/Settings';
import CommandPalette from './components/CommandPalette';
import { AppProvider, useApp } from './contexts/AppContext';
import { ThemeProvider } from './contexts/ThemeContext';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css';

type View = 'dashboard' | 'research' | 'knowledge' | 'documents' | 'experiments' | 'datasets' | 'ml' | 'learning' | 'flashcards' | 'papers' | 'citations' | 'timeline' | 'benchmarks' | 'system' | 'settings';

const AppContent: React.FC = () => {
  const [currentView, setCurrentView] = useState<View>('dashboard');
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

  useEffect(() => {
    // Keyboard shortcut for command palette
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard onNavigate={setCurrentView} />;
      case 'research':
        return <Research />;
      case 'knowledge':
        return <Knowledge />;
      case 'documents':
        return <Documents />;
      case 'experiments':
        return <Experiments />;
      case 'datasets':
        return <Datasets />;
      case 'ml':
        return <MLLab />;
      case 'learning':
        return <Learning />;
      case 'flashcards':
        return <Flashcards />;
      case 'papers':
        return <Papers />;
      case 'citations':
        return <Citations />;
      case 'timeline':
        return <Timeline />;
      case 'benchmarks':
        return <Benchmarks />;
      case 'system':
        return <System />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard onNavigate={setCurrentView} />;
    }
  };

  return (
    <div className="flex h-screen bg-background text-foreground">
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />
      <main className="flex-1 overflow-y-auto">
        {renderView()}
      </main>
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
        onNavigate={setCurrentView}
      />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AppProvider>
          <AppContent />
        </AppProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
};

export default App;