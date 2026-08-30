"""Tests for learning service."""
import pytest
from app.services.learning_service import LearningService

def test_generate_path_linear_algebra():
    svc = LearningService()
    path = svc.generate_path("linear_algebra")
    assert path is not None
    assert len(path.topics) > 0
    assert path.subject == "linear_algebra"
    assert path.title == "Linear Algebra"

def test_generate_path_neural_networks():
    svc = LearningService()
    path = svc.generate_path("neural_networks")
    assert path is not None
    assert path.subject == "neural_networks"

def test_generate_path_not_found():
    svc = LearningService()
    path = svc.generate_path("unknown_subject_xyz")
    assert path is None

def test_generate_path_case_insensitive():
    svc = LearningService()
    path = svc.generate_path("Linear Algebra")
    assert path is not None

def test_list_subjects():
    svc = LearningService()
    subjects = svc.list_subjects()
    assert len(subjects) >= 8
    subject_ids = [s["id"] for s in subjects]
    assert "linear_algebra" in subject_ids
    assert "neural_networks" in subject_ids

def test_topic_prerequisites():
    svc = LearningService()
    path = svc.generate_path("linear_algebra")
    topic = path.topics[1]
    assert len(topic.prerequisites) > 0
    assert "Vectors and Vector Spaces" in topic.prerequisites
