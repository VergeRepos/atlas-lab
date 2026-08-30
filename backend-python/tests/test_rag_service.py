"""Tests for RAG service."""
import pytest
from app.services.rag_service import RAGService, VectorStore

class TestVectorStore:
    def test_add_and_search(self):
        vs = VectorStore()
        vs.add_chunk("c1", "test content", [0.1]*384, "doc1")
        vs.build_index()
        results = vs.search([0.1]*384, top_k=1)
        assert len(results) == 1
        assert results[0][0] == "c1"

    def test_empty_search(self):
        vs = VectorStore()
        vs.build_index()
        results = vs.search([0.0]*384)
        assert len(results) == 0

    def test_min_score_filter(self):
        vs = VectorStore()
        vs.add_chunk("c1", "content one", [1.0]*384, "doc1")
        vs.add_chunk("c2", "content two", [0.1]*384, "doc1")
        vs.build_index()
        results = vs.search([1.0]*384, top_k=2, min_score=0.5)
        assert len(results) == 1
        assert results[0][0] == "c1"

class TestRAGService:
    def test_init(self):
        rag = RAGService()
        assert rag.retrieval_top_k == 5
        assert rag.chunk_size == 1024

    def test_calculate_confidence(self):
        rag = RAGService()
        # Test with empty list
        assert rag._calculate_confidence([]) == 0.0
