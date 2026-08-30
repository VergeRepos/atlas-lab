"""Tests for knowledge graph service."""
import pytest
from app.services.knowledge_graph_service import KnowledgeGraphService

def test_add_node():
    kg = KnowledgeGraphService()
    node = kg.add_node("concept", "Machine Learning", "Study of ML")
    assert node.label == "Machine Learning"
    assert node.type == "concept"
    assert node.id in kg.nodes

def test_add_edge():
    kg = KnowledgeGraphService()
    n1 = kg.add_node("concept", "Neural Networks")
    n2 = kg.add_node("concept", "Deep Learning")
    edge = kg.add_edge(n1.id, n2.id, "related_to")
    assert edge is not None
    assert edge.relationship == "related_to"

def test_add_edge_invalid_nodes():
    kg = KnowledgeGraphService()
    edge = kg.add_edge("fake1", "fake2", "related")
    assert edge is None

def test_get_neighbors():
    kg = KnowledgeGraphService()
    n1 = kg.add_node("concept", "A")
    n2 = kg.add_node("concept", "B")
    kg.add_edge(n1.id, n2.id, "related_to")
    neighbors = kg.get_neighbors(n1.id)
    assert len(neighbors) == 1
    assert neighbors[0][0].label == "B"

def test_search_nodes():
    kg = KnowledgeGraphService()
    kg.add_node("concept", "Neural Networks")
    kg.add_node("paper", "Neural Networks Paper")
    kg.add_node("concept", "Deep Learning")
    results = kg.search_nodes("neural")
    assert len(results) >= 2

def test_get_graph_data():
    kg = KnowledgeGraphService()
    n1 = kg.add_node("concept", "A")
    n2 = kg.add_node("concept", "B")
    kg.add_edge(n1.id, n2.id, "related")
    data = kg.get_graph_data()
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1

def test_compute_importance():
    kg = KnowledgeGraphService()
    n1 = kg.add_node("concept", "A")
    n2 = kg.add_node("concept", "B")
    n3 = kg.add_node("concept", "C")
    kg.add_edge(n1.id, n2.id, "related")
    kg.add_edge(n1.id, n3.id, "related")
    importance = kg.compute_node_importance()
    assert importance[n1.id] >= importance[n2.id]
