"""Flashcard router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from ..services.flashcard_service import SpacedRepetitionService

router = APIRouter()
sr_service = SpacedRepetitionService()
logger = logging.getLogger(__name__)

@router.post("/decks")
async def create_deck(name: str, description: Optional[str] = None):
    return sr_service.create_deck(name, description)

@router.get("/decks/{deck_id}")
async def get_deck(deck_id: str):
    deck = sr_service.decks.get(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

@router.post("/decks/{deck_id}/cards")
async def add_card(deck_id: str, front: str, back: str, tags: Optional[List[str]] = None):
    return sr_service.add_card(deck_id, front, back, tags)

@router.get("/decks/{deck_id}/due")
async def get_due_cards(deck_id: str, limit: int = 20):
    return sr_service.get_due_cards(deck_id, limit)

@router.post("/reviews")
async def record_review(card_id: str, quality: int, response_time_ms: int = 1000):
    try:
        return sr_service.record_review(card_id, quality, response_time_ms)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/stats/{deck_id}")
async def get_stats(deck_id: str):
    return sr_service.get_review_stats(deck_id)
