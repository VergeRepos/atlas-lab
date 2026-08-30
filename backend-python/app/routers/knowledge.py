"""Knowledge graph router."""
from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from ..services.knowledge_graph_service import KnowledgeGraphService

router = APIRouter()
kg_service = KnowledgeGraphService()

@router.get("/")
async def get_graph():
    return kg_service.get_graph_data()

@router.post("/nodes")
async def add_node(node_type: str, label: str, description: Optional[str] = None):
    return kg_service.add_node(node_type, label, description)

@router.post("/edges")
async def add_edge(source_id: str, target_id: str, relationship: str, weight: float = 1.0):
    edge = kg_service.add_edge(source_id, target_id, relationship, weight)
    if not edge:
        raise HTTPException(status_code=400, detail="Could not create edge (check node IDs)")
    return edge

@router.get("/nodes/{node_id}")
async def get_node(node_id: str):
    node = kg_service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@router.get("/nodes/{node_id}/neighbors")
async def get_neighbors(node_id: str, relationship: Optional[str] = None):
    return kg_service.get_neighbors(node_id, relationship)
