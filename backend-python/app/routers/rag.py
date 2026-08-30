"""
RAG (Retrieval-Augmented Generation) API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from ..services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize RAG service
rag_service = RAGService()


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    model_id: Optional[str] = None
    is_local: bool = True
    temperature: float = 0.7
    max_tokens: int = 1024


@router.post("/ask")
async def ask_question(request: QueryRequest):
    """Ask a question and get an AI response with source attribution."""
    try:
        result = await rag_service.generate_response(
            query=request.query,
            top_k=request.top_k,
            model_id=request.model_id,
            is_local=request.is_local,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return result
    except Exception as e:
        logger.error(f"Error in RAG: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get statistics about the RAG system."""
    return {
        "total_chunks": len(rag_service.vector_store.chunks),
        "index_built": rag_service.vector_store.index_built,
        "embedding_model": rag_service.embedding_service.model_name,
    }