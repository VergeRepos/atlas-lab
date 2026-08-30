"""Data analysis router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from ..services.data_analysis_service import DataAnalysisService

router = APIRouter()
service = DataAnalysisService()
logger = logging.getLogger(__name__)

class AnalyzeRequest(BaseModel):
    file_path: str
    dataset_name: str
    project_id: str

@router.post("/analyze")
async def analyze_dataset(req: AnalyzeRequest):
    try:
        result = service.analyze_dataset(req.file_path, req.dataset_name, req.project_id)
        return result
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preview")
async def preview_dataset(file_path: str, n_rows: int = 10):
    try:
        return service.get_preview(file_path, n_rows)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
