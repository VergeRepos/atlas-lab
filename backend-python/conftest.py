import pytest
import sys
import os

# Ensure the app package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))


@pytest.fixture
def sample_text():
    return "Machine learning is a subset of artificial intelligence."


@pytest.fixture
def sample_query():
    return "What is machine learning?"


@pytest.fixture
def mock_document():
    return {
        "id": "test-doc-1",
        "title": "Test Document",
        "content": "This is a test document about machine learning.",
        "file_path": "/test/doc.md",
        "file_type": "md",
        "created_at": "2024-01-01T00:00:00Z",
    }
