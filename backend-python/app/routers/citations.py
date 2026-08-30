"""Citation router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from ..services.citation_service import CitationService

router = APIRouter()
citation_service = CitationService()
logger = logging.getLogger(__name__)

@router.post("/")
async def add_citation(
    source_id: str, authors: List[str], title: str,
    year: Optional[int] = None, doi: Optional[str] = None,
    url: Optional[str] = None, citation_type: str = "article"
):
    return citation_service.add_citation(source_id, authors, title, year, doi, url, citation_type)

@router.get("/")
async def list_citations():
    return citation_service.list_citations()

@router.get("/{citation_id}")
async def get_citation(citation_id: str):
    c = citation_service.get_citation(citation_id)
    if not c:
        raise HTTPException(status_code=404, detail="Citation not found")
    return c

@router.get("/{citation_id}/format/{fmt}")
async def format_citation(citation_id: str, fmt: str = "apa"):
    try:
        return {"formatted": citation_service.format_citation(citation_id, fmt)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
