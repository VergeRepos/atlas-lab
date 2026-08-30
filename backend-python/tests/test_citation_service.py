"""Tests for citation service."""
import pytest
from app.services.citation_service import CitationService

def test_add_citation():
    svc = CitationService()
    c = svc.add_citation(
        source_id="doc1",
        authors=["Smith, J."],
        title="A Test Paper",
        year=2024,
        citation_type="article"
    )
    assert c.title == "A Test Paper"
    assert c.year == 2024
    assert c.authors == ["Smith, J."]

def test_add_citation_validation():
    svc = CitationService()
    with pytest.raises(ValueError):
        svc.add_citation(source_id="doc1", authors=[], title="", citation_type="article")

def test_format_apa_single_author():
    svc = CitationService()
    c = svc.add_citation("doc1", ["Smith, J."], "Test Title", 2024)
    formatted = svc.format_citation(c.id, "apa")
    assert "Smith" in formatted
    assert "2024" in formatted
    assert "Test Title" in formatted

def test_format_apa_multiple_authors():
    svc = CitationService()
    c = svc.add_citation("doc1", ["Smith, J.", "Doe, A."], "Test Title", 2024)
    formatted = svc.format_citation(c.id, "apa")
    assert "Smith" in formatted
    assert "et al." in formatted

def test_format_mla():
    svc = CitationService()
    c = svc.add_citation("doc1", ["Smith, J."], "Test Title", 2024)
    formatted = svc.format_citation(c.id, "mla")
    assert "Smith" in formatted

def test_format_ieee():
    svc = CitationService()
    c = svc.add_citation("doc1", ["Smith, J."], "Test Title", 2024)
    formatted = svc.format_citation(c.id, "ieee")
    assert "Smith" in formatted
    assert "[1]" in formatted

def test_extract_from_text():
    svc = CitationService()
    text = "See https://example.com/paper and DOI: 10.1234/test.2024"
    extracted = svc.extract_from_text(text)
    assert any(e["type"] == "url" for e in extracted)
    assert any(e["type"] == "doi" for e in extracted)
