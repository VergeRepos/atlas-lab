"""
Experiment tracking API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class ExperimentCreate(BaseModel):
    project_id: str
    name: str
    description: Optional[str] = None
    hypothesis: Optional[str] = None
    parameters: Dict[str, Any] = {}
    random_seed: Optional[int] = 42


class ExperimentResponse(BaseModel):
    id: str
    project_id: str
    name: str
    description: Optional[str]
    hypothesis: Optional[str]
    status: str
    created_at: str


# In-memory store for demo (replace with SQLite via Rust backend)
_experiments: Dict[str, Dict[str, Any]] = {}


@router.get("/")
async def list_experiments(project_id: Optional[str] = None):
    """List all experiments, optionally filtered by project."""
    if project_id:
        return {"experiments": [e for e in _experiments.values() if e.get("project_id") == project_id]}
    return {"experiments": list(_experiments.values())}


@router.post("/")
async def create_experiment(exp: ExperimentCreate):
    """Create a new experiment."""
    import uuid
    experiment = {
        "id": str(uuid.uuid4()),
        "project_id": exp.project_id,
        "name": exp.name,
        "description": exp.description,
        "hypothesis": exp.hypothesis,
        "status": "planned",
        "created_at": str(uuid.uuid4()),
        "parameters": exp.parameters,
        "random_seed": exp.random_seed,
    }
    _experiments[experiment["id"]] = experiment
    return experiment


@router.get("/{experiment_id}")
async def get_experiment(experiment_id: str):
    """Get a specific experiment."""
    exp = _experiments.get(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp


@router.delete("/{experiment_id}")
async def delete_experiment(experiment_id: str):
    """Delete an experiment."""
    if experiment_id in _experiments:
        del _experiments[experiment_id]
    return {"status": "deleted"}


@router.post("/{experiment_id}/start")
async def start_experiment(experiment_id: str):
    """Mark experiment as running."""
    exp = _experiments.get(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    exp["status"] = "running"
    return exp


@router.post("/{experiment_id}/complete")
async def complete_experiment(experiment_id: str, results: Dict[str, Any]):
    """Mark experiment as completed with results."""
    exp = _experiments.get(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    exp["status"] = "completed"
    exp["results"] = results
    return exp
