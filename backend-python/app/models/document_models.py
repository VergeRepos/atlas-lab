"""
Data models for document processing
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from uuid import uuid4
import hashlib
from pathlib import Path


class DocumentChunk(BaseModel):
    """Represents a chunk of text from a document."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    document_id: str
    content: str
    chunk_index: int
    start_char: int = 0
    end_char: int = 0
    page_number: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @validator('metadata')
    def validate_metadata(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Metadata must be a dictionary")
        return v


class Embedding(BaseModel):
    """Represents an embedding vector for a text chunk."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    chunk_id: str
    model: str
    vector: List[float]
    dimensions: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator('dimensions')
    def validate_dimensions(cls, v, values):
        if v != len(values.get('vector', [])):
            raise ValueError("Dimensions must match vector length")
        return v

    @validator('vector')
    def validate_vector(cls, v):
        if not v or not all(isinstance(x, float) for x in v):
            raise ValueError("Vector must be a non-empty list of floats")
        return v


class Document(BaseModel):
    """Represents a processed document."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    project_id: Optional[str] = None
    filename: str
    file_path: str
    file_type: str  # pdf, txt, md, csv, docx
    file_size: int
    title: Optional[str] = None
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None
    status: str = "pending"  # pending, processing, completed, failed
    error: Optional[str] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    checksum: str

    @validator('file_type')
    def validate_file_type(cls, v):
        allowed_types = {'pdf', 'txt', 'md', 'csv', 'docx'}
        if v.lower() not in allowed_types:
            raise ValueError(f"File type must be one of: {allowed_types}")
        return v.lower()

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = {'pending', 'processing', 'completed', 'failed'}
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v.lower()

    @validator('checksum')
    def calculate_checksum(cls, v, values):
        if v == '' and 'file_path' in values:
            return cls._calculate_file_checksum(values['file_path'])
        return v

    @staticmethod
    def _calculate_file_checksum(file_path: str) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()