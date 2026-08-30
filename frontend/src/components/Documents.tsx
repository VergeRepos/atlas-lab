import React, { useState, useRef } from 'react';
import { Upload, FileText, File, FileCheck, X, Loader2, CheckCircle2, AlertCircle, Trash2, Eye } from 'lucide-react';

interface Document {
  id: string;
  filename: string;
  fileType: 'pdf' | 'txt' | 'md' | 'csv' | 'docx';
  fileSize: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  wordCount?: number;
  chunkCount?: number;
  uploadedAt: Date;
  error?: string;
}

const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([
    { id: '1', filename: 'Retrieval_Augmented_Generation_Survey.pdf', fileType: 'pdf', fileSize: 2400000, status: 'completed', wordCount: 12400, chunkCount: 142, uploadedAt: new Date('2026-08-28') },
    { id: '2', filename: 'Dense_vs_Sparse_Empirical_Study.pdf', fileType: 'pdf', fileSize: 1850000, status: 'completed', wordCount: 9800, chunkCount: 118, uploadedAt: new Date('2026-08-28') },
    { id: '3', filename: 'BM25_Explained.md', fileType: 'md', fileSize: 45000, status: 'completed', wordCount: 2100, chunkCount: 24, uploadedAt: new Date('2026-08-29') },
    { id: '4', filename: 'Hybrid_Retrieval_Notes.txt', fileType: 'txt', fileSize: 12000, status: 'completed', wordCount: 580, chunkCount: 8, uploadedAt: new Date('2026-08-29') },
  ]);

  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => setDragging(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    // Handle dropped files
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      // Process files
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText className="text-red-500" size={20} />;
      case 'csv': return <File className="text-emerald-500" size={20} />;
      default: return <File className="text-blue-500" size={20} />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <span className="flex items-center gap-1 text-xs font-medium text-emerald-500"><CheckCircle2 size={12} /> Indexed</span>;
      case 'processing':
        return <span className="flex items-center gap-1 text-xs font-medium text-amber-500"><Loader2 size={12} className="animate-spin" /> Processing</span>;
      case 'failed':
        return <span className="flex items-center gap-1 text-xs font-medium text-red-500"><AlertCircle size={12} /> Failed</span>;
      default:
        return <span className="text-xs text-muted-foreground">Pending</span>;
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Document Library</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Import and index documents for semantic search and AI-powered analysis.
        </p>
      </div>

      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors mb-8 ${
          dragging ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
        }`}
      >
        <Upload className="mx-auto mb-3 text-muted-foreground" size={32} />
        <p className="text-sm font-medium">Drop files here or click to upload</p>
        <p className="text-xs text-muted-foreground mt-1">Supports PDF, TXT, Markdown, CSV, DOCX</p>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.txt,.md,.csv,.docx"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* Document List */}
      <div className="space-y-3">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="bg-card border border-border rounded-lg p-4 flex items-center justify-between hover:border-primary/30 transition-colors"
          >
            <div className="flex items-center gap-3">
              {getFileIcon(doc.fileType)}
              <div>
                <p className="text-sm font-medium">{doc.filename}</p>
                <div className="flex items-center gap-3 text-xs text-muted-foreground mt-0.5">
                  <span>{formatFileSize(doc.fileSize)}</span>
                  <span>•</span>
                  <span>{doc.wordCount?.toLocaleString()} words</span>
                  <span>•</span>
                  <span>{doc.chunkCount} chunks</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {getStatusBadge(doc.status)}
              <div className="flex gap-1">
                <button className="p-1.5 hover:bg-secondary rounded transition-colors" title="Preview">
                  <Eye size={14} />
                </button>
                <button className="p-1.5 hover:bg-secondary rounded transition-colors text-red-500" title="Delete">
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Stats Footer */}
      <div className="mt-8 p-4 bg-secondary/30 rounded-lg border border-border/50 text-xs text-muted-foreground flex justify-between">
        <span>{documents.length} documents indexed</span>
        <span>{(documents.reduce((a, b) => a + (b.chunkCount || 0), 0)).toLocaleString()} total chunks</span>
        <span>{formatFileSize(documents.reduce((a, b) => a + b.fileSize, 0))} total size</span>
      </div>
    </div>
  );
};

export default Documents;