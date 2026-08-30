# Contributing to Atlas Lab

## Development Setup

### Prerequisites
- Node.js 18+ (frontend)
- Python 3.10+ (backend)
- Rust 1.70+ (desktop shell)
- SQLite 3.x

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/atlas-lab.git
cd atlas-lab

# Install frontend dependencies
cd frontend && npm install

# Install Python dependencies
cd ../backend-python && pip install -r requirements.txt

# Run development servers
cd ../frontend && npm run dev        # Frontend on :5173
cd ../backend-python && uvicorn app.main:app --reload  # API on :8000
cd ../backend-tauri && cargo tauri dev  # Desktop (requires Tauri CLI)
```

## Architecture

```
atlas-lab/
├── frontend/          # React + TypeScript + Tailwind
├── backend-python/    # FastAPI + SQLite
├── backend-tauri/     # Rust desktop shell
└── examples/         # Sample documents and datasets
```

## Code Style

### Python
- Use async/await for all FastAPI routes
- Type hints required on all function signatures
- Pydantic models for all API schemas
- Max line length: 100

### TypeScript
- Strict mode enabled
- No `any` types
- Use functional components with hooks
- Tailwind for all styling

### Rust
- Clippy lints enabled
- No unsafe code unless documented
- Error handling with Result types

## Testing

```bash
# Python tests
cd backend-python && python -m pytest -v

# Frontend tests
cd frontend && npm test

# Tauri build
cd backend-tauri && cargo tauri build
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request with clear description

## Project Structure

### Frontend Components
- `Dashboard.tsx` - Main landing page
- `Documents.tsx` - Document management
- `MLLab.tsx` - Machine learning experiments
- `Research.tsx` - Research workspace

### Python Services
- `embedding_service.py` - Text embedding generation
- `rag_service.py` - RAG pipeline
- `ml_service.py` - ML experiment execution
- `flashcard_service.py` - Spaced repetition system

### Rust Commands
- Database operations via SQLite
- File system access with path validation
- System monitoring utilities
