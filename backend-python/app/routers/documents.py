"""
Document API endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional, List
import os
import shutil
from pathlib import Path
import logging

from ..services.document_service import DocumentProcessor, EmbeddingService
from ..services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
document_processor = DocumentProcessor()
embedding_service = EmbeddingService()

# Shared RAG service instance
rag_service = RAGService()

# Configure upload directory
UPLOAD_DIR = Path(os.environ.get("ATLAS_UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    project_id: Optional[str] = Form(None)
):
    """Upload and process a document."""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Check file extension
        allowed_extensions = {'.pdf', '.txt', '.md', '.csv', '.docx'}
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. Allowed: {allowed_extensions}"
            )

        # Save file
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process document
        result = rag_service.ingest_document(str(file_path), project_id)

        return {
            "status": "success",
            "document": {
                "id": result['document'].id,
                "filename": result['document'].filename,
                "file_type": result['document'].file_type,
                "file_size": result['document'].file_size,
                "word_count": result['document'].word_count,
            },
            "chunks_processed": result['chunks_processed'],
            "chunks_total": result['chunks_total'],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def semantic_search(query: str, top_k: int = 5):
    """Perform semantic search over ingested documents."""
    try:
        chunks = rag_service.retrieve(query, top_k=top_k)
        return {
            "query": query,
            "results": [
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "score": chunk.score,
                    "metadata": chunk.metadata,
                }
                for chunk in chunks
            ],
            "count": len(chunks),
        }
    except Exception as e:
        logger.error(f"Error in semantic search: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_documents():
    """List all ingested documents."""
    try:
        chunks_data = []
        for chunk_id, chunk in rag_service.vector_store.chunks.items():
            chunks_data.append({
                "chunk_id": chunk_id,
                "document_id": chunk.get("document_id"),
                "content_preview": chunk.get("content", "")[:200],
                "metadata": chunk.get("metadata", {}),
            })
        return {
            "documents": chunks_data,
            "total_chunks": len(chunks_data),
        }
    except Exception as e:
        logger.error(f"Error listing documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its chunks."""
    try:
        # Remove from vector store
        chunks_to_remove = [
            chunk_id for chunk_id, chunk in rag_service.vector_store.chunks.items()
            if chunk.get("document_id") == document_id
        ]

        for chunk_id in chunks_to_remove:
            rag_service.vector_store.chunks.pop(chunk_id, None)
            rag_service.vector_store.vectors.pop(chunk_id, None)

        # Rebuild index
        rag_service.vector_store.build_index()

        return {
            "status": "deleted",
            "chunks_removed": len(chunks_to_remove),
        }
    except Exception as e:
        logger.error(f"Error deleting document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))