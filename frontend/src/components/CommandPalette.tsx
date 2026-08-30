import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Command, Search, FileText, Brain, Database, FlaskConical, Clock, BookOpen, Terminal } from 'lucide-react';

interface CommandItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  action: () => void;
  category: string;
}

export default function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const commands: CommandItem[] = [
    { id: 'docs', label: 'Open Documents', icon: <FileText className="w-4 h-4" />, action: () => alert('Documents'), category: 'Navigation' },
    { id: 'rag', label: 'Ask RAG Assistant', icon: <Brain className="w-4 h-4" />, action: () => alert('RAG'), category: 'AI' },
    { id: 'db', label: 'Data Analysis', icon: <Database className="w-4 h-4" />, action: () => alert('Analysis'), category: 'Data' },
    { id: 'ml', label: 'ML Experiments', icon: <FlaskConical className="w-4 h-4" />, action: () => alert('ML'), category: 'Science' },
    { id: 'learning', label: 'Learning Path', icon: <BookOpen className="w-4 h-4" />, action: () => alert('Learning'), category: 'Study' },
    { id: 'timeline', label: 'Timeline', icon: <Clock className="w-4 h-4" />, action: () => alert('Timeline'), category: 'History' },
  ];

  const filtered = commands.filter(c => c.label.toLowerCase().includes(query.toLowerCase()) || c.category.toLowerCase().includes(query.toLowerCase()));

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === 'k') { e.preventDefault(); setOpen(o => !o); }
      if (e.key === 'Escape') setOpen(false);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  useEffect(() => {
    if (open && inputRef.current) setTimeout(() => inputRef.current?.focus(), 50);
  }, [open]);

  return (
    <>
      <button onClick={() => setOpen(true)} className="flex items-center gap-2 px-3 py-2 text-sm text-stone-400 bg-stone-800/60 rounded-lg border border-stone-700/50 hover:border-stone-600 transition" aria-label="Open command palette">
        <Command className="w-3.5 h-3.5" /> <span>Command</span> <kbd className="ml-1 text-xs font-mono bg-stone-700 px-1 rounded">⌘K</kbd>
      </button>
      {open && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] bg-black/60 backdrop-blur-sm" onClick={() => setOpen(false)}>
          <div className="w-full max-w-lg bg-stone-900 border border-stone-700 rounded-xl shadow-2xl overflow-hidden" onClick={e => e.stopPropagation()}>
            <div className="flex items-center gap-3 px-4 py-3 border-b border-stone-800">
              <Search className="w-4 h-4 text-stone-400" />
              <input ref={inputRef} className="bg-transparent outline-none text-sm text-white w-full placeholder:text-stone-500" placeholder="Search commands..." value={query} onChange={e => setQuery(e.target.value)} />
              <kbd className="text-xs font-mono text-stone-500">ESC</kbd>
            </div>
            <div className="max-h-[60vh] overflow-y-auto py-2">
              {filtered.length === 0 && <div className="px-4 py-4 text-sm text-stone-500">No results</div>}
              {filtered.map(c => (
                <button key={c.id} onClick={() => { c.action(); setOpen(false); }} className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-stone-800 text-left transition">
                  <span className="text-stone-300">{c.icon}</span>
                  <div>
                    <div className="text-sm text-stone-100">{c.label}</div>
                    <div className="text-xs text-stone-500">{c.category}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
