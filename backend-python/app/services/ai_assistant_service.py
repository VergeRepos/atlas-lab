"""
AI Research Assistant Service
"""

import time
from typing import List, Optional, Dict, Any
import numpy as np

from ..models.database import RetrievedChunk, AISource
from ..services.rag_service import RAGService
from ..services.document_service import DocumentProcessor, EmbeddingService


class AIAssistantService:
    """Main AI assistant service for research questions."""

    def __init__(
        self,
        rag_service: RAGService,
        embedding_service: EmbeddingService,
    ):
        self.rag_service = rag_service
        self.embedding_service = embedding_service
        self.document_processor = DocumentProcessor()

    def answer_question(
        self,
        query: str,
        model_id: Optional[str] = None,
        is_local: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """Answer a research question using RAG."""
        start_time = time.time()

        # Retrieve relevant chunks
        retrieved_chunks = self.rag_service.retrieve(query, top_k=5, min_relevance=0.0)

        if not retrieved_chunks:
            return {
                'answer': 'I don\'t have enough evidence in the indexed sources to answer this reliably.',
                'sources': [],
                'confidence': 0.0,
                'latency_ms': int((time.time() - start_time) * 1000),
                'model': model_id or 'none',
                'is_local': is_local,
                'retrieved_chunks': [],
            }

        # Build context from retrieved chunks
        context_parts = []
        sources = []
        for chunk in retrieved_chunks:
            context_parts.append(f"[Source: {chunk.document_id}, Score: {chunk.score:.3f}]\n{chunk.content}")
            sources.append({
                'chunk_id': chunk.chunk_id,
                'document_id': chunk.document_id,
                'content': chunk.content,
                'relevance_score': chunk.score,
                'metadata': chunk.metadata,
            })

        context = '\n---\n'.join(context_parts)

        # Generate response
        prompt = f"""You are Atlas Lab, an AI research assistant.
Answer the question based ONLY on the provided sources.
Be concise, accurate, and cite your sources.
Avoid speculation. If information is not in the sources, state that clearly.

Context:
{context}

Question: {query}
"""

        if is_local and model_id:
            answer = self._generate_response(prompt, model_id, temperature, max_tokens)
        else:
            answer = "Remote AI integration pending. Local mode available with Ollama."

        # Calculate confidence based on sources
        confidence = self._calculate_confidence(retrieved_chunks)

        return {
            'answer': answer,
            'sources': sources,
            'confidence': confidence,
            'latency_ms': int((time.time() - start_time) * 1000),
            'model': model_id or 'none',
            'is_local': is_local,
            'retrieved_chunks': [
                {
                    'chunk_id': chunk.chunk_id,
                    'document_id': chunk.document_id,
                    'content': chunk.content,
                    'score': chunk.score,
                    'page_number': chunk.metadata.get('page_number'),
                }
                for chunk in retrieved_chunks
            ],
        }

    def _generate_response(
        self,
        prompt: str,
        model_id: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using a local model."""
        # In a real implementation, this would call Ollama or another local LLM
        # For now, we'll return a placeholder
        return "Response generation with local model pending. Ollama integration required."

    def _calculate_confidence(self, retrieved_chunks: List) -> float:
        """Calculate confidence score based on retrieved chunks."""
        if not retrieved_chunks:
            return 0.0

        # Weighted average of chunk scores
        total_score = sum(chunk.score for chunk in retrieved_chunks)
        avg_score = total_score / len(retrieved_chunks)

        # Boost confidence if we have sufficient evidence
        evidence_bonus = min(1.0, len(retrieved_chunks) / 5.0)
        confidence = avg_score * 0.7 + evidence_bonus * 0.3

        return float(min(1.0, confidence))