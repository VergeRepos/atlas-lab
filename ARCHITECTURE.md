# Atlas Lab Architecture

## Overview

Atlas Lab uses a clean architecture separating concerns across 4 layers:

- **Presentation Layer**: React + TypeScript + Tailwind CSS
- **Desktop Layer**: Tauri (Rust backend for system integration)
- **Services Layer**: Python FastAPI for AI/ML processing
- **Persistence Layer**: SQLite with proper migrations

## Technology Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- Lucide React for icons
- Zustand for lightweight state management
- Custom hooks for data fetching
- Dark/light mode via ThemeContext
- Command palette (Ctrl+K) for quick navigation

### Desktop (Tauri/Rust)
- Tauri 2.0 for native desktop experience
- SQLite database via rusqlite
- Direct file system access
- System monitoring via sysinfo
- Secure command handling
- Path traversal protection in file operations

### Python Backend
- FastAPI for REST API endpoints
- SQLite with SQLAlchemy ORM
- PDF processing via pdfminer.six
- DOCX extraction via python-docx
- Embedding generation via sentence-transformers
- ML experiments via scikit-learn
- Data analysis via pandas and scipy
- Vector search in memory with NumPy

### Database Schema
- Users & Projects
- Documents & Chunks
- Embeddings (vector storage)
- Experiments & Results
- Flashcards, Reviews
- Citations & Knowledge Graph
- Benchmarks

## Key Design Decisions

1. **Offline-First**: All data stored locally; internet only for optional cloud AI
2. **Local AI**: Supports Ollama; no paid API required
3. **Reproducible Experiments**: Every experiment stores config, dataset hash, seed, results
4. **Source Transparency**: Every AI answer shows sources, scores, and timestamp
5. **No Hallucination**: RAG only uses indexed documents; clearly states when evidence is insufficient
6. **Building on Proven Patterns**: Uses standard libraries (FastAPI, scikit-learn, React, Tauri)

## Security

- Path traversal protection for all file operations
- Input validation on all endpoints
- No arbitrary shell execution from user input
- Local-only processing by default (no silent uploads)
- SQLite database in user data directory (not globally writable)
