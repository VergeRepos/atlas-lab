"""
RAG Service
Retrieval-Augmented Generation with vector search and source attribution
"""

import time
from typing import List, Optional, Dict, Any, Tuple

import numpy as np

from ..models.database import RetrievedChunk, AISource
from ..services.document_service import DocumentProcessor, EmbeddingService


class VectorStore:
    """Simple vector store using cosine similarity."""

    def __init__(self):
        self.chunks: Dict[str, Dict[str, Any]] = {}
        self.vectors: Dict[str, np.ndarray] = {}
        self.index_built = False

    def add_chunk(
        self,
        chunk_id: str,
        content: str,
        embedding: List[float],
        document_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a chunk with its embedding."""
        vec = np.array(embedding, dtype=np.float32)
        self.chunks[chunk_id] = {
            'chunk_id': chunk_id,
            'content': content,
            'document_id': document_id,
            'metadata': metadata or {},
            'created_at': time.time(),
        }
        self.vectors[chunk_id] = vec
        self.index_built = False

    def build_index(self):
        """Build the search index."""
        if self.vectors:
            self.all_vectors = np.vstack(list(self.vectors.values()))
            self.all_ids = list(self.vectors.keys())
            # Normalize for cosine similarity
            norms = np.linalg.norm(self.all_vectors, axis=1, keepdims=True)
            norms = np.where(norms == 0, 1, norms)
            self.normalized_vectors = self.all_vectors / norms
            self.index_built = True

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        min_score: float = 0.0
    ) -> List[Tuple[str, float]]:
        """Search for most similar chunks."""
        if not self.index_built:
            self.build_index()

        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []
        query_vec = query_vec / query_norm

        # Compute cosine similarity
        similarities = np.dot(self.normalized_vectors, query_vec)
        scores = similarities

        # Get top-k indices
        if top_k >= len(scores):
            top_indices = np.argsort(scores)[::-1]
        else:
            top_indices = np.argpartition(scores, -top_k)[-top_k:]
            top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score >= min_score:
                chunk_id = self.all_ids[idx]
                results.append((chunk_id, score))

        return results


class RAGService:
    """RAG orchestration service."""

    def __init__(
        self,
        embedding_model: str = 'all-MiniLM-L6-v2',
        retrieval_top_k: int = 5,
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
    ):
        self.embedding_service = EmbeddingService(model_name=embedding_model)
        self.vector_store = VectorStore()
        self.retrieval_top_k = retrieval_top_k
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.document_processor = DocumentProcessor(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def ingest_document(
        self,
        file_path: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ingest a document: extract, chunk, and embed."""
        # Process document
        doc, chunks = self.document_processor.process_document(
            file_path,
            project_id=project_id
        )

        # Generate embeddings for each chunk
        embedded_chunks = []
        for chunk in chunks:
            embedding = self.embedding_service.generate_embedding(chunk.content)
            if embedding is not None:
                self.vector_store.add_chunk(
                    chunk_id=chunk.id,
                    content=chunk.content,
                    embedding=embedding,
                    document_id=doc.id,
                    metadata={
                        'chunk_index': chunk.chunk_index,
                        'page_number': chunk.metadata.get('page_number'),
                    }
                )
                embedded_chunks.append(chunk)

        self.vector_store.build_index()

        return {
            'document': doc,
            'chunks_processed': len(embedded_chunks),
            'chunks_total': len(chunks),
        }

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        min_relevance: float = 0.0
    ) -> List[RetrievedChunk]:
        """Retrieve relevant chunks for a query."""
        if top_k is None:
            top_k = self.retrieval_top_k

        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        if query_embedding is None:
            return []

        # Search vector store
        results = self.vector_store.search(
            query_embedding, top_k=top_k, min_score=min_relevance
        )

        # Convert to RetrievedChunk objects
        retrieved = []
        for chunk_id, score in results:
            chunk_data = self.vector_store.chunks.get(chunk_id, {})
            retrieved.append(RetrievedChunk(
                chunk_id=chunk_id,
                document_id=chunk_data.get('document_id', ''),
                content=chunk_data.get('content', ''),
                score=float(score),
                metadata=chunk_data.get('metadata', {}),
            ))

        return retrieved

    async def generate_response(
        self,
        query: str,
        top_k: int = 5,
        model_id: Optional[str] = None,
        is_local: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """Generate a response using RAG with source attribution."""
        start_time = time.time()

        # Step 1: Retrieve relevant chunks
        retrieved = self.retrieve(query, top_k=top_k, min_relevance=0.0)

        if not retrieved:
            return {
                'answer': 'I don\'t have enough evidence in the indexed sources to answer this reliably.',
                'sources': [],
                'confidence': 0.0,
                'latency_ms': int((time.time() - start_time) * 1000),
                'model': model_id or 'none',
                'is_local': is_local,
                'retrieved_chunks': [],
            }

        # Step 2: Build context from retrieved chunks
        context_parts = []
        sources = []
        for chunk in retrieved:
            doc_id = chunk.document_id
            content = chunk.content
            score = chunk.score

            context_parts.append(f"[Source: {doc_id}, Score: {score:.3f}]\n{content}")
            sources.append({
                'chunk_id': chunk.chunk_id,
                'document_id': doc_id,
                'content': content,
                'relevance_score': float(score),
                'metadata': chunk.metadata,
            })

        context = '\n---\n'.join(context_parts)

        # Step 3: Generate response
        prompt = self._build_prompt(query, context)

        if is_local and model_id:
            answer = await self._generate_local(prompt, model_id, temperature, max_tokens)
        else:
            answer = 'Response generation requires an AI model (local or remote).'

        confidence = self._calculate_confidence(retrieved)

        return {
            'answer': answer,
            'sources': sources,
            'confidence': confidence,
            'latency_ms': int((time.time() - start_time) * 1000),
            'model': model_id or 'none',
            'is_local': is_local,
            'retrieved_chunks': [
                {
                    'chunk_id': r.chunk_id,
                    'document_id': r.document_id,
                    'content': r.content,
                    'score': r.score,
                    'page_number': r.metadata.get('page_number'),
                }
                for r in retrieved
            ],
        }

    def _build_prompt(self, query: str, context: str) -> str:
        """Build the prompt for the LLM."""
        return f"""You are Atlas Lab, a helpful AI research assistant.
Answer the question based on the provided sources.
Be concise and accurate.

IMPORTANT: Only use information from the provided sources. If the sources don't contain enough information, clearly state that.

Context:
{context}

Question: {query}

Answer:"""

    async def _generate_local(
        self,
        prompt: str,
        model_id: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using a local model."""
        # This would integrate with Ollama or another local LLM
        # For now, return a placeholder
        return "Local model integration pending. Please ensure Ollama is running for local generation."

    def _calculate_confidence(self, retrieved: List) -> float:
        """Calculate confidence based on retrieved chunks."""
        if not retrieved:
            return 0.0
        # Average score, weighted by number of results
        avg_score = sum(r.score for r in retrieved) / len(retrieved)
        # Boost confidence if we have enough chunks
        count_bonus = min(1.0, len(retrieved) / 5.0)
        return float(min(1.0, (avg_score * 0.7) + (count_bonus * 0.3)))