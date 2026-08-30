"""ML Lab router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from ..services.ml_service import MLService

router = APIRouter()
ml_service = MLService()
logger = logging.getLogger(__name__)

@router.get("/algorithms")
async def list_algorithms():
    return ml_service.list_algorithms()

@router.post("/run")
async def run_experiment(
    task_type: str,
    algorithm: str,
    dataset_path: str,
    feature_columns: List[str],
    target_column: Optional[str] = None,
    parameters: Dict[str, Any] = None,
    project_id: str = "default",
):
    from datetime import datetime, timezone
    import uuid
    from ..models.database import MLExperiment
    parameters = parameters or {}
    try:
        exp = MLExperiment(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=f"{algorithm} - {task_type}",
            task_type=task_type,
            algorithm=algorithm,
            feature_columns=feature_columns,
            target_column=target_column,
            parameters=parameters,
            dataset_path=dataset_path,
            created_at=datetime.now(timezone.utc),
            status="planned",
        )
        result = ml_service.run_experiment(exp, dataset_path)
        return {"experiment_id": exp.id, "metrics": result.metrics, "model_params": result.model_params}
    except Exception as e:
        logger.error(f"ML error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
