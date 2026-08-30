"""Timeline router."""
from fastapi import APIRouter
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

router = APIRouter()
_events: List[Dict[str, Any]] = []

@router.get("/")
async def get_timeline(project_id: str):
    return {"events": [e for e in _events if e.get("project_id") == project_id]}

@router.post("/")
async def add_event(
    project_id: str, event_type: str, title: str,
    description: str = "", date: Optional[str] = None,
    linked_entity_id: str = None, linked_entity_type: str = None
):
    event = {
        "id": str(uuid.uuid4()),
        "project_id": project_id,
        "type": event_type,
        "title": title,
        "description": description,
        "date": date or datetime.now(timezone.utc).isoformat(),
        "linked_entity_id": linked_entity_id,
        "linked_entity_type": linked_entity_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _events.append(event)
    return event
