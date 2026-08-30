"""Learning router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from ..services.learning_service import LearningService

router = APIRouter()
learning_service = LearningService()
logger = logging.getLogger(__name__)

@router.get("/subjects")
async def list_subjects():
    return learning_service.list_subjects()

@router.get("/path/{subject}")
async def get_learning_path(subject: str, difficulty: str = "beginner"):
    path = learning_service.generate_path(subject, difficulty)
    if not path:
        raise HTTPException(status_code=404, detail="Subject not found")
    return path
