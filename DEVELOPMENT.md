# Development Guide

## Prerequisites

- Node.js 18+
- Python 3.10+
- Rust (for Tauri development)
- npm or yarn

## Installation

```bash
# Clone repository
git clone https://github.com/atlaslab/atlas-lab.git
cd atlas-lab

# Install frontend dependencies
cd frontend
npm install

# Install Python dependencies
cd ../backend-python
pip install -r requirements.txt

# Install Rust (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Running Locally

### Frontend Only (Development)
```bash
cd frontend
npm start
```

### Tauri Desktop App
```bash
cd backend-tauri
cargo build
```

### Python Backend
```bash
cd backend-python
uvicorn app.main:app --reload --port 8000
```

## Project Structure

```
atlas-lab/
├── frontend/              # React TypeScript app
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── contexts/    # React contexts
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API calls
│   │   ├── stores/      # State management
│   │   ├── types/       # TypeScript types
│   │   └── utils/       # Utilities
│   └── public/          # Static assets
├── backend-tauri/        # Rust Tauri backend
│   └── src/
│       ├── main.rs       # Entry point
│       ├── database.rs   # SQLite operations
│       ├── commands.rs   # Tauri commands
│       └── error.rs      # Error types
├── backend-python/       # Python FastAPI backend
│   └── app/
│       ├── routers/      # API endpoints
│       ├── services/     # Business logic
│       └── models/       # Data models
└── docs/                 # Documentation
```

## Adding New Features

### 1. Add a New Frontend Component
1. Create component in `frontend/src/components/`
2. Use TypeScript types from `frontend/src/types/`
3. Add to routing in `App.tsx`

### 2. Add a New Python Service
1. Create service class in `backend-python/app/services/`
2. Add Pydantic models if needed
3. Create router endpoint in `backend-python/app/routers/`
4. Register router in `main.py`

### 3. Add Database Table
1. Add model in `backend-tauri/src/database.rs`
2. Add migration SQL
3. Create CRUD functions

## Testing

```bash
# Frontend tests
cd frontend
npm test

# Python tests
cd backend-python
pytest tests/
```

## Building for Production

```bash
# Build frontend
cd frontend
npm run build

# Build Tauri app
cd backend-tauri
cargo build --release
```

## Code Style

- Use ESLint for frontend linting
- Use Black for Python formatting
- Use rustfmt for Rust formatting
- Follow conventional commits for git messages
