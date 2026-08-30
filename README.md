# Atlas Lab - AI-Powered Research and Learning Workstation

<div align="center">

![Atlas Lab Banner](docs/images/banner.png)

**A production-quality desktop application for researchers, students, and developers**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://react.dev/)
[![Tauri 2.0](https://img.shields.io/badge/tauri-2.0-blue.svg)](https://tauri.app/)

[Features](#features) • [Installation](#installation) • [Screenshots](#screenshots) • [Documentation](#documentation)

</div>

---

## Overview

Atlas Lab is a comprehensive AI-powered research workstation that runs entirely on your desktop. Import documents, analyze data, run ML experiments, build knowledge graphs, and learn with spaced repetition — all with full privacy and offline-first design.

![Dashboard Overview](docs/images/dashboard-overview.png)
*Main dashboard showing research projects, recent activity, and quick actions*

## ✨ Key Features

### 🔬 Research Workspace
Create research projects with questions, hypotheses, experiments, and notes. Track your entire research lifecycle in one place.

![Research Workspace](docs/images/research-workspace.gif)
*Creating a new research project and adding experiments*

### 📚 Document Processing
Import PDFs, TXT, Markdown, CSV, and DOCX files. Automatic text extraction, chunking, and embedding generation.

![Document Import](docs/images/document-import.gif)
*Importing and processing multiple document types*

### 🤖 RAG Assistant
Ask questions about your documents and get AI-powered answers with source citations, relevance scores, and page numbers.

![RAG Assistant](docs/images/rag-assistant.png)
*AI assistant providing answers with source attribution*

### 🕸️ Knowledge Graph
Automatically build and visualize relationships between concepts, documents, and entities. Interactive force-directed graph with search and filtering.

![Knowledge Graph](docs/images/knowledge-graph.png)
*Interactive knowledge graph showing concept relationships*

### 🧪 ML Lab
Run machine learning experiments with classification, regression, and clustering. Full reproducibility with parameter tracking and metrics.

![ML Lab](docs/images/ml-lab.gif)
*Running a classification experiment on customer churn data*

### 📊 Data Analysis
Import CSV datasets and get automatic statistics, correlations, distributions, and visualizations.

![Data Analysis](docs/images/data-analysis.png)
*CSV analysis showing statistics and correlations*

### 🎓 Learning Mode
Structured learning paths for topics like Linear Algebra, Neural Networks, and Transformers. Track progress and mastery.

![Learning Mode](docs/images/learning-mode.png)
*Learning path with topic breakdown and progress tracking*

### 🗂️ Spaced Repetition
Adaptive flashcard system using the SM-2 algorithm. Auto-generate cards from your notes and optimize review scheduling.

![Flashcards](docs/images/flashcards.gif)
*Reviewing flashcards with quality rating*

### 📝 Paper Workspace
Write technical papers with automatic citation management, reference formatting (APA/MLA/IEEE), and document statistics.

![Paper Workspace](docs/images/paper-workspace.png)
*Writing a research paper with citation insertion*

### ⌨️ Command Palette
Quick access to all features with `Ctrl+K` / `Cmd+K`. Search commands, navigate, and execute actions without leaving the keyboard.

![Command Palette](docs/images/command-palette.png)
*Command palette for quick navigation*

### 📈 System Monitoring
Real-time CPU, RAM, and disk usage. Monitor your system while running intensive ML experiments.

![System Monitor](docs/images/system-monitor.png)
*System monitoring dashboard*

## 🚀 Installation

### Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/atlas-lab.git
cd atlas-lab

# Install Python dependencies
cd backend-python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Run development servers
# Terminal 1: Start Python backend
cd backend-python
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Terminal 3: Start Tauri desktop app
cd backend-tauri
cargo tauri dev
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

## 📸 Screenshots

<details>
<summary>Click to expand all screenshots</summary>

### Dashboard
![Dashboard](docs/images/dashboard-full.png)

### Documents View
![Documents](docs/images/documents-view.png)

### Experiments Tracking
![Experiments](docs/images/experiments-tracking.png)

### Datasets Management
![Datasets](docs/images/datasets-management.png)

### Timeline View
![Timeline](docs/images/timeline-view.png)

### Benchmarks
![Benchmarks](docs/images/benchmarks-view.png)

### Settings
![Settings](docs/images/settings-view.png)

</details>

## 🎬 Demo Videos

| Feature | Demo |
|---------|------|
| **Full Walkthrough** | ![Full Demo](docs/images/demo-full.gif) |
| **Document Ingestion** | ![Document Demo](docs/images/demo-documents.gif) |
| **RAG Query** | ![RAG Demo](docs/images/demo-rag.gif) |
| **ML Experiment** | ![ML Demo](docs/images/demo-ml.gif) |
| **Knowledge Graph** | ![Graph Demo](docs/images/demo-graph.gif) |

## 🏗️ Architecture

Atlas Lab uses a clean, modular architecture:

```
┌─────────────────────────────────────┐
│   React + TypeScript Frontend       │
│   (Tailwind CSS, Zustand)          │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Tauri 2.0 Desktop Shell          │
│   (Rust, System Integration)       │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   FastAPI Python Backend           │
│   (AI/ML Services, RAG)            │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   SQLite Database                  │
│   (Documents, Embeddings, Metrics) │
└────────────────────────────────────┘
```

**Tech Stack:**
- **Frontend**: React 18, TypeScript, Tailwind CSS, Lucide Icons
- **Desktop**: Tauri 2.0 (Rust), `rusqlite`, `sysinfo`
- **Backend**: FastAPI, Pydantic, sentence-transformers
- **ML**: scikit-learn, pandas, numpy
- **Database**: SQLite with vector extensions
- **AI**: Ollama (local), OpenAI/Anthropic (optional)

## 📖 Documentation

- [Installation Guide](INSTALL.md)
- [Development Guide](DEVELOPMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [API Documentation](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Security Policy](SECURITY.md)
- [Performance Benchmarks](BENCHMARKS.md)

## 🧪 Example Project

Atlas Lab includes a complete example: **"Does Retrieval Strategy Affect RAG Answer Quality?"**

This demonstrates:
- Document ingestion (ML, RAG, and embeddings papers)
- Multiple retrieval strategies (Dense, Sparse, Hybrid)
- Metrics collection (precision@5, recall@5, latency)
- Result analysis and visualization

Run it: `File → Open Example Project → RAG Comparison`

## 🛠️ Development

### Running Tests

```bash
# Python backend tests
cd backend-python
pytest -v

# Frontend tests
cd frontend
npm test

# Rust tests
cd backend-tauri
cargo test
```

### Building for Production

```bash
# Build desktop app
cd backend-tauri
cargo tauri build

# Outputs to: src-tauri/target/release/bundle/
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development workflow
- Pull request process
- Testing requirements

## 📊 Performance

| Operation | Time | Memory |
|-----------|------|--------|
| PDF import (1MB) | ~850ms | 30MB |
| Embedding generation (1K chars) | ~120ms | 15MB |
| RAG query (100 docs) | ~45ms | 25MB |
| ML experiment (10K rows) | ~3.2s | 80MB |

See [BENCHMARKS.md](BENCHMARKS.md) for detailed performance metrics.

## 🔒 Privacy & Security

- **Offline-first**: Works without internet
- **Local processing**: All AI runs on your machine by default
- **No telemetry**: Zero data collection unless explicitly enabled
- **Encrypted storage**: SQLite with optional encryption
- **Open source**: Fully auditable code

See [SECURITY.md](SECURITY.md) for security guidelines.

## 🗺️ Roadmap

- [ ] Multimodal document processing (images, audio)
- [ ] Real-time collaboration features
- [ ] Cloud sync (optional, encrypted)
- [ ] Mobile companion app
- [ ] Plugin system for extensibility
- [ ] Advanced visualization tools

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

Built with these amazing open-source projects:
- [Tauri](https://tauri.app/) - Desktop framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [React](https://react.dev/) - UI library
- [sentence-transformers](https://www.sbert.net/) - Embedding models
- [scikit-learn](https://scikit-learn.org/) - Machine learning

## 📮 Support

- 📖 [Documentation](docs/)
- 🐛 [Report Bug](https://github.com/yourusername/atlas-lab/issues)
- 💡 [Request Feature](https://github.com/yourusername/atlas-lab/issues)
- 💬 [Discussions](https://github.com/yourusername/atlas-lab/discussions)

---

<div align="center">

**Made with ❤️ for researchers and learners everywhere**

⭐ Star us on GitHub if Atlas Lab helps your research!

</div>
