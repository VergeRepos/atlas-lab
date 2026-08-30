"""
Citation Management Service
Handles citation metadata extraction and formatting
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import re
import hashlib

from ..models.database import Citation


class CitationService:
    """Service for managing citations."""

    # Supported citation formats
    FORMATS = ['apa', 'mla', 'ieee']

    def __init__(self):
        self.citations: Dict[str, Citation] = {}
        self.source_index: Dict[str, str] = {}  # hash -> citation_id

    def add_citation(
        self,
        source_id: str,
        authors: List[str],
        title: str,
        year: Optional[int] = None,
        doi: Optional[str] = None,
        url: Optional[str] = None,
        citation_type: str = "article",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Citation:
        """Add a new citation."""
        # Validate inputs
        if not title:
            raise ValueError("Title is required for citations")

        if citation_type not in ['article', 'book', 'paper', 'website', 'other']:
            raise ValueError(f"Invalid citation type: {citation_type}")

        citation_id = str(uuid.uuid4())
        citation = Citation(
            id=citation_id,
            source_id=source_id,
            authors=authors,
            title=title,
            year=year,
            doi=doi,
            url=url,
            citation_type=citation_type,
            metadata=metadata or {},
        )
        self.citations[citation_id] = citation

        # Index by hash for deduplication
        content_hash = self._compute_hash(citation)
        self.source_index[content_hash] = citation_id

        return citation

    def format_citation(
        self,
        citation_id: str,
        format: str = 'apa'
    ) -> str:
        """Format a citation in the specified style."""
        citation = self.citations.get(citation_id)
        if not citation:
            raise ValueError(f"Citation not found: {citation_id}")

        if format not in self.FORMATS:
            raise ValueError(f"Unsupported format: {format}")

        if format == 'apa':
            return self._format_apa(citation)
        elif format == 'mla':
            return self._format_mla(citation)
        elif format == 'ieee':
            return self._format_ieee(citation)

        return str(citation)

    def _format_apa(self, citation: Citation) -> str:
        """Format in APA style."""
        parts = []

        # Authors
        if citation.authors:
            if len(citation.authors) == 1:
                parts.append(citation.authors[0])
            elif len(citation.authors) == 2:
                parts.append(f"{citation.authors[0]} & {citation.authors[1]}")
            else:
                parts.append(
                    f"{citation.authors[0]} et al."
                )
            parts[-1] += "."

        # Year
        if citation.year:
            parts.append(f"({citation.year}).")

        # Title
        parts.append(citation.title)

        # DOI or URL
        if citation.doi:
            parts.append(f"https://doi.org/{citation.doi}")
        elif citation.url:
            parts.append(citation.url)

        return " ".join(parts)

    def _format_mla(self, citation: Citation) -> str:
        """Format in MLA style."""
        parts = []

        # Authors
        if citation.authors:
            if len(citation.authors) == 1:
                parts.append(citation.authors[0])
            else:
                parts.append(", ".join(citation.authors))
            parts.append(".")

        # Title
        parts.append(f"\"{citation.title}.\"")

        # Container/source info
        parts.append(f"Web. {datetime.now().year}.")

        return " ".join(parts)

    def _format_ieee(self, citation: Citation) -> str:
        """Format in IEEE style."""
        parts = []

        # Number placeholder
        parts.append("[1] ")

        # Authors (abbreviated first names)
        if citation.authors:
            parts.append(", ".join(citation.authors))
            parts.append(", ")

        # Title
        parts.append(f"\"{citation.title},\"")

        # Year
        if citation.year:
            parts.append(f" {citation.year}.")

        return "".join(parts)

    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract citation information from text."""
        extracted = []

        # DOI pattern
        doi_pattern = r'10\.\d{4,}/[^\s]+'
        dois = re.findall(doi_pattern, text)
        for doi in dois:
            extracted.append({
                'type': 'doi',
                'value': doi,
                'extracted': True,
            })

        # URL pattern
        url_pattern = r'https?://[^\s<>"]+'
        urls = re.findall(url_pattern, text)
        for url in urls:
            extracted.append({
                'type': 'url',
                'value': url,
                'extracted': True,
            })

        # Year pattern (4-digit years in parentheses)
        year_pattern = r'\((\d{4})\)'
        years = re.findall(year_pattern, text)

        return extracted

    def get_citation(self, citation_id: str) -> Optional[Citation]:
        """Get a citation by ID."""
        return self.citations.get(citation_id)

    def list_citations(self) -> List[Citation]:
        """List all citations."""
        return list(self.citations.values())

    def _compute_hash(self, citation: Citation) -> str:
        """Compute a hash for deduplication."""
        content = f"{citation.title}|{','.join(citation.authors)}|{citation.year or ''}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self, citation_id: str) -> Dict[str, Any]:
        """Convert citation to dictionary."""
        citation = self.citations.get(citation_id)
        if not citation:
            return {}
        return {
            'id': citation.id,
            'source_id': citation.source_id,
            'authors': citation.authors,
            'title': citation.title,
            'year': citation.year,
            'doi': citation.doi,
            'url': citation.url,
            'citation_type': citation.citation_type,
            'metadata': citation.metadata,
        }