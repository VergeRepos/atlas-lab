import React, { useState } from 'react';
import { Settings as SettingsIcon, Server, Cpu, Database, Key, Globe, Shield, Monitor, Sun, Moon } from 'lucide-react';

interface SettingsState {
  theme: 'light' | 'dark' | 'system';
  ai_provider: 'local' | 'ollama' | 'openai' | 'anthropic';
  ollama_url: string;
  openai_key: string;
  anthropic_key: string;
  default_chunk_size: number;
  default_chunk_overlap: number;
  enable_telemetry: boolean;
  enable_remote_ai: boolean;
  embedding_model: string;
  vector_dim: number;
}

const defaultSettings: SettingsState = {
  theme: 'dark',
  ai_provider: 'local',
  ollama_url: 'http://localhost:11434',
  openai_key: '',
  anthropic_key: '',
  default_chunk_size: 512,
  default_chunk_overlap: 50,
  enable_telemetry: false,
  enable_remote_ai: false,
  embedding_model: 'all-MiniLM-L6-v2',
  vector_dim: 384,
};

export default function Settings() {
  const [settings, setSettings] = useState<SettingsState>(defaultSettings);
  const [saved, setSaved] = useState(false);

  const update = <K extends keyof SettingsState>(key: K, value: SettingsState[K]) => {
    setSettings(s => ({ ...s, [key]: value }));
    setSaved(false);
  };

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3"><SettingsIcon className="w-6 h-6" /> Settings</h1>
          <p className="text-stone-400 text-sm">Configure Atlas Lab to your preferences</p>
        </div>
        {saved && <div className="text-xs text-emerald-400">Settings saved</div>}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Section title="Appearance" icon={<Sun className="w-4 h-4" />}>
          <Row label="Theme">
            <select value={settings.theme} onChange={e => update('theme', e.target.value as any)} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm">
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="system">System</option>
            </select>
          </Row>
        </Section>

        <Section title="AI Provider" icon={<Server className="w-4 h-4" />}>
          <Row label="Provider">
            <select value={settings.ai_provider} onChange={e => update('ai_provider', e.target.value as any)} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm">
              <option value="local">Local (no AI)</option>
              <option value="ollama">Ollama</option>
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
            </select>
          </Row>
          {settings.ai_provider === 'ollama' && (
            <Row label="Ollama URL">
              <input value={settings.ollama_url} onChange={e => update('ollama_url', e.target.value)} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-full" />
            </Row>
          )}
          {settings.ai_provider === 'openai' && (
            <Row label="OpenAI API Key">
              <input type="password" value={settings.openai_key} onChange={e => update('openai_key', e.target.value)} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-full" />
            </Row>
          )}
          {settings.ai_provider === 'anthropic' && (
            <Row label="Anthropic API Key">
              <input type="password" value={settings.anthropic_key} onChange={e => update('anthropic_key', e.target.value)} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-full" />
            </Row>
          )}
        </Section>

        <Section title="Embeddings" icon={<Database className="w-4 h-4" />}>
          <Row label="Model">
            <input value={settings.embedding_model} onChange={e => update('embedding_model', e.target.value)} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-full" />
          </Row>
          <Row label="Vector Dim">
            <input type="number" value={settings.vector_dim} onChange={e => update('vector_dim', parseInt(e.target.value))} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-24" />
          </Row>
        </Section>

        <Section title="Document Chunking" icon={<Cpu className="w-4 h-4" />}>
          <Row label="Chunk Size">
            <input type="number" value={settings.default_chunk_size} onChange={e => update('default_chunk_size', parseInt(e.target.value))} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-24" />
          </Row>
          <Row label="Chunk Overlap">
            <input type="number" value={settings.default_chunk_overlap} onChange={e => update('default_chunk_overlap', parseInt(e.target.value))} className="bg-stone-800 border border-stone-700 text-stone-200 rounded px-2 py-1 text-sm w-24" />
          </Row>
        </Section>

        <Section title="Privacy" icon={<Shield className="w-4 h-4" />}>
          <Row label="Enable Telemetry">
            <input type="checkbox" checked={settings.enable_telemetry} onChange={e => update('enable_telemetry', e.target.checked)} />
          </Row>
          <Row label="Allow Remote AI">
            <input type="checkbox" checked={settings.enable_remote_ai} onChange={e => update('enable_remote_ai', e.target.checked)} />
          </Row>
        </Section>
      </div>

      <div className="flex justify-end">
        <button onClick={handleSave} className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition">Save Settings</button>
      </div>
    </div>
  );
}

function Section({ title, icon, children }: { title: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <div className="bg-stone-800/50 border border-stone-700/50 rounded-xl p-4">
      <h3 className="text-sm font-medium text-stone-200 mb-4 flex items-center gap-2">{icon} {title}</h3>
      <div className="space-y-3">{children}</div>
    </div>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <span className="text-xs text-stone-400">{label}</span>
      {children}
    </div>
  );
}
