"""
Knowledge Graph Service
Manages relationships between concepts, papers, experiments, etc.
"""

import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone

from ..models.database import KnowledgeNode, KnowledgeEdge


class KnowledgeGraphService:
    """Service for building and querying knowledge graphs."""

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: Dict[str, KnowledgeEdge] = {}
        self._adjacency: Dict[str, List[str]] = {}

    def add_node(
        self,
        node_type: str,
        label: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> KnowledgeNode:
        """Add a node to the knowledge graph."""
        node_id = str(uuid.uuid4())
        node = KnowledgeNode(
            id=node_id,
            type=node_type,
            label=label,
            description=description,
            properties=properties or {},
        )
        self.nodes[node_id] = node
        self._adjacency[node_id] = []
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        weight: float = 1.0,
        properties: Optional[Dict[str, Any]] = None
    ) -> Optional[KnowledgeEdge]:
        """Add an edge between two nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None

        edge_id = str(uuid.uuid4())
        edge = KnowledgeEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
            weight=weight,
            properties=properties or {},
        )
        self.edges[edge_id] = edge

        # Update adjacency list
        if source_id not in self._adjacency:
            self._adjacency[source_id] = []
        self._adjacency[source_id].append(edge_id)

        return edge

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_neighbors(
        self, node_id: str, relationship: Optional[str] = None
    ) -> List[Tuple[KnowledgeNode, KnowledgeEdge]]:
        """Get neighboring nodes, optionally filtered by relationship type."""
        neighbors = []

        for edge in self.edges.values():
            if edge.source_id == node_id:
                target = self.nodes.get(edge.target_id)
                if target:
                    if relationship is None or edge.relationship == relationship:
                        neighbors.append((target, edge))

        return neighbors

    def search_nodes(
        self,
        query: str,
        node_type: Optional[str] = None,
        limit: int = 10
    ) -> List[KnowledgeNode]:
        """Search for nodes by label."""
        query_lower = query.lower()
        results = []

        for node in self.nodes.values():
            if node_type and node.type != node_type:
                continue

            # Simple substring match
            if query_lower in node.label.lower():
                results.append(node)

            if len(results) >= limit:
                break

        return results

    def extract_relationships(
        self,
        documents: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Extract potential relationships from document text.
        This is a simplified version - a real implementation would use NLP.
        """
        relationships = []

        # Common relationship patterns
        patterns = {
            'related_to': ['related to', 'connected to', 'associated with'],
            'uses': ['uses', 'utilizes', 'employs'],
            'depends_on': ['depends on', 'requires', 'needs'],
            'implements': ['implements', 'realizes', 'instantiates'],
            'improves': ['improves', 'enhances', 'extends'],
            'contradicts': ['contradicts', 'disputes', 'challenges'],
        }

        for doc_text in documents:
            for rel_type, keywords in patterns.items():
                for keyword in keywords:
                    if keyword in doc_text.lower():
                        relationships.append({
                            'type': rel_type,
                            'source_text': keyword,
                            'confidence': 0.5,  # Low confidence without NLP
                        })

        return relationships

    def get_graph_data(self) -> Dict[str, Any]:
        """Get the entire graph as a dictionary."""
        nodes = []
        for node in self.nodes.values():
            nodes.append({
                'id': node.id,
                'type': node.type,
                'label': node.label,
                'description': node.description,
                'properties': node.properties,
                'x': node.x,
                'y': node.y,
            })

        edges = []
        for edge in self.edges.values():
            edges.append({
                'id': edge.id,
                'source': edge.source_id,
                'target': edge.target_id,
                'relationship': edge.relationship,
                'weight': edge.weight,
                'properties': edge.properties,
            })

        return {'nodes': nodes, 'edges': edges}

    def compute_node_importance(self) -> Dict[str, float]:
        """Compute importance scores for nodes based on connections."""
        importance = {}

        for node_id in self.nodes:
            # Simple degree centrality
            in_degree = sum(1 for e in self.edges.values() if e.target_id == node_id)
            out_degree = sum(1 for e in self.edges.values() if e.source_id == node_id)

            # Normalized importance
            total_nodes = len(self.nodes)
            if total_nodes > 0:
                importance[node_id] = (in_degree + out_degree) / (2 * (total_nodes - 1))
            else:
                importance[node_id] = 0.0

        return importance

    def find_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 3
    ) -> List[List[str]]:
        """Find all paths between two nodes up to max_depth."""
        paths = []

        def dfs(current: str, target: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            if current == target and path:
                paths.append(path.copy())
                return

            for edge in self.edges.values():
                if edge.source_id == current and edge.target_id not in path:
                    path.append(edge.target_id)
                    dfs(edge.target_id, target, path, depth + 1)
                    path.pop()

        dfs(source_id, target_id, [source_id], 0)
        return paths

    def export_graph(self, format: str = 'json') -> Dict[str, Any]:
        """Export the knowledge graph."""
        return self.get_graph_data()