# Installation Guide

## System Requirements

- **Operating System**: Windows 10+, macOS 11+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB minimum, 8GB recommended for ML workloads
- **Storage**: 2GB free space
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **Rust**: 1.70 or higher (for Tauri desktop)

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/atlas-lab.git
cd atlas-lab
```

## Step 2: Backend (Python)

```bash
cd backend-python

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, for advanced NLP)
python -m spacy download en_core_web_sm
```

### Troubleshooting Python Install

If you encounter issues with `sentence-transformers`:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers
```

If you have an NVIDIA GPU:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

## Step 3: Frontend (Node.js)

```bash
cd frontend

# Install dependencies
npm install

# Verify installation
npm run build
```

## Step 4: Desktop Shell (Tauri - Optional)

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Tauri CLI
cargo install tauri-cli

# Build desktop app
cd backend-tauri
cargo tauri build
```

## Step 5: Verify Installation

```bash
# Start backend
cd backend-python
uvicorn app.main:app --reload --port 8000

# In another terminal, test the API
curl http://localhost:8000/
```

Expected output: API health check JSON.

## Optional: Ollama Setup (for Local LLM)

```bash
# Install Ollama from https://ollama.com
# Then pull a model
ollama pull llama2
```

Configure Atlas Lab to use Ollama in Settings → AI Models.

## Common Issues

### Port Already in Use
Change the port: `uvicorn app.main:app --port 8001`

### Missing SQLite
- Linux: `sudo apt install sqlite3`
- macOS: `brew install sqlite3`
- Windows: Included with Python

### Permission Errors on Linux
```bash
chmod +x start.sh
```

## Next Steps

- Read [DEVELOPMENT.md](DEVELOPMENT.md) for development workflow
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Check [BENCHMARKS.md](BENCHMARKS.md) for performance information
