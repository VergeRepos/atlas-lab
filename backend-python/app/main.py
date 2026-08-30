"""
Atlas Lab Python Backend
FastAPI service for AI, data processing, and ML experiments
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Atlas Lab Python Backend...")
    yield
    logger.info("Shutting down Atlas Lab Python Backend...")

app = FastAPI(
    title="Atlas Lab API",
    description="Python backend for AI research workstation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "atlas-lab-python-backend", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Atlas Lab Python Backend", "version": "1.0.0", "docs": "/docs"}

from .routers import documents, rag, experiments, analysis, ml, learning, flashcards, citations, timeline, benchmarks, knowledge

app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
app.include_router(experiments.router, prefix="/api/experiments", tags=["experiments"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(ml.router, prefix="/api/ml", tags=["ml"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(flashcards.router, prefix="/api/flashcards", tags=["flashcards"])
app.include_router(citations.router, prefix="/api/citations", tags=["citations"])
app.include_router(timeline.router, prefix="/api/timeline", tags=["timeline"])
app.include_router(benchmarks.router, prefix="/api/benchmarks", tags=["benchmarks"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
