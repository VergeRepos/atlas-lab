"""
Database models for SQLite storage
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import uuid

from pydantic import BaseModel


# ============================================================================
# Project and Research Models
# ============================================================================

class Project(BaseModel):
    """Research project containing questions, hypotheses, notes, and more."""
    id: str = None
    name: str
    description: Optional[str] = None
    research_question: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    status: str = "active"  # active, completed, archived
    tags: List[str] = []


class ResearchQuestion(BaseModel):
    """A research question within a project."""
    id: str = None
    project_id: str
    question: str
    hypothesis: Optional[str] = None
    status: str = "open"  # open, answered, partial
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class Hypothesis(BaseModel):
    """A hypothesis to test within a project."""
    id: str = None
    project_id: str
    question_id: str
    statement: str
    variables: List[str] = []
    created_at: datetime = datetime.now(timezone.utc)
    tested: bool = False
    results: Optional[str] = None


class Note(BaseModel):
    """A note within a project."""
    id: str = None
    project_id: str
    title: str
    content: str
    tags: List[str] = []
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    linked_concepts: List[str] = []


# ============================================================================
# Experiment Models
# ============================================================================

class Experiment(BaseModel):
    """ML experiment tracking."""
    id: str = None
    project_id: str
    name: str
    description: Optional[str] = None
    hypothesis: Optional[str] = None
    status: str = "planned"  # planned, running, completed, failed, cancelled
    created_at: datetime = datetime.now(timezone.utc)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    parameters: Dict[str, Any] = {}
    random_seed: Optional[int] = None
    environment: Optional[Dict[str, Any]] = None


class ExperimentResult(BaseModel):
    """Results from an experiment."""
    id: str = None
    experiment_id: str
    metrics: Dict[str, float] = {}
    output_files: List[str] = []
    dataset_hash: str
    created_at: datetime = datetime.now(timezone.utc)


# ============================================================================
# Dataset Models
# ============================================================================

class ColumnInfo(BaseModel):
    """Information about a dataset column."""
    name: str
    type: str  # numeric, categorical, datetime, boolean, text
    nullable: bool = True
    unique_count: Optional[int] = None
    null_count: Optional[int] = None
    sample_values: List[Any] = []


class Dataset(BaseModel):
    """Dataset for experiments and analysis."""
    id: str = None
    project_id: str
    name: str
    description: Optional[str] = None
    file_path: str
    file_type: str  # csv, json, parquet
    row_count: int = 0
    column_count: int = 0
    columns: List[ColumnInfo] = []
    created_at: datetime = datetime.now(timezone.utc)
    checksum: str = ""


# ============================================================================
# Learning Models
# ============================================================================

class Example(BaseModel):
    """An example within a learning topic."""
    id: str = None
    title: str
    description: str
    code: Optional[str] = None
    output: Optional[str] = None
    explanation: str = ""


class Exercise(BaseModel):
    """An exercise within a learning topic."""
    id: str = None
    title: str
    description: str
    hints: List[str] = []
    solution: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard


class MiniProject(BaseModel):
    """A mini-project within a learning topic."""
    id: str = None
    title: str
    description: str
    requirements: List[str] = []
    difficulty: str = "intermediate"  # beginner, intermediate, advanced


class ReviewQuestion(BaseModel):
    """A review question for spaced repetition."""
    id: str = None
    question: str
    answer: str
    type: str = "definition"  # definition, explanation, application, analysis


class LearningTopic(BaseModel):
    """A topic within a learning path."""
    id: str = None
    path_id: str
    title: str
    explanation: str
    prerequisites: List[str] = []
    examples: List[Example] = []
    exercises: List[Exercise] = []
    mini_projects: List[MiniProject] = []
    review_questions: List[ReviewQuestion] = []
    order: int = 0
    mastery_level: str = "not_started"  # not_started, learning, reviewing, mastered
    time_spent_minutes: float = 0.0


class LearningPath(BaseModel):
    """Complete learning path for a subject."""
    id: str = None
    subject: str
    title: str
    description: str = ""
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    topics: List[LearningTopic] = []
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    mastery_score: float = 0.0


# ============================================================================
# Flashcard Models
# ============================================================================

class FlashcardDeck(BaseModel):
    """A deck of flashcards for spaced repetition."""
    id: str = None
    name: str
    description: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class Flashcard(BaseModel):
    """A single flashcard."""
    id: str = None
    deck_id: str
    front: str
    back: str
    source_note_id: Optional[str] = None
    tags: List[str] = []
    difficulty: float = 2.5  # 0-5 scale
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class CardReview(BaseModel):
    """A review instance of a flashcard."""
    id: str = None
    card_id: str
    session_id: str
    quality: int = 0  # 0-5 scale (again, hard, good, easy)
    interval: int = 0
    ease_factor: float = 2.5
    reviewed_at: datetime = datetime.now(timezone.utc)
    response_time_ms: int = 0


# ============================================================================
# Citation Models
# ============================================================================

class Citation(BaseModel):
    """Citation metadata."""
    id: str = None
    source_id: str
    authors: List[str] = []
    title: str
    year: Optional[int] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    citation_type: str = "article"  # article, book, paper, website, other
    metadata: Dict[str, Any] = {}


# ============================================================================
# Knowledge Graph Models
# ============================================================================

class KnowledgeNode(BaseModel):
    """Node in the knowledge graph."""
    id: str = None
    type: str  # concept, paper, person, technology, experiment, question
    label: str
    description: Optional[str] = None
    properties: Dict[str, Any] = {}
    x: Optional[float] = None
    y: Optional[float] = None


class KnowledgeEdge(BaseModel):
    """Edge in the knowledge graph."""
    id: str = None
    source_id: str
    target_id: str
    relationship: str
    weight: float = 1.0
    properties: Dict[str, Any] = {}


# ============================================================================
# RAG Models
# ============================================================================

class RetrievedChunk(BaseModel):
    """A chunk retrieved during RAG."""
    id: str = None
    chunk_id: str
    document_id: str
    content: str
    score: float = 0.0
    metadata: Dict[str, Any] = {}


class AIResponse(BaseModel):
    """Response from AI assistant with source attribution."""
    id: str = None
    query: str
    answer: str
    model: str
    sources: List[Dict[str, Any]] = []
    confidence: float = 0.0
    generated_at: datetime = datetime.now(timezone.utc)
    latency_ms: int = 0
    is_local: bool = True
    retrieved_chunks: List[Dict[str, Any]] = []


# ============================================================================
# Analysis Models
# ============================================================================

class ColumnStatistics(BaseModel):
    """Statistics for a dataset column."""
    column: str
    type: str
    count: int
    null_count: int = 0
    unique_count: Optional[int] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    median: Optional[float] = None
    mode: Optional[Any] = None
    distribution: Optional[str] = None


class CorrelationPair(BaseModel):
    """Correlation between two columns."""
    column1: str
    column2: str
    correlation: float
    p_value: float
    significant: bool = False


class MissingValueAnalysis(BaseModel):
    """Analysis of missing values."""
    total_missing: int = 0
    columns: List[Dict[str, Any]] = []


class OutlierAnalysis(BaseModel):
    """Outlier detection results."""
    method: str = "iqr"  # iqr, zscore
    total_outliers: int = 0
    by_column: List[Dict[str, Any]] = []


class ChartConfig(BaseModel):
    """Configuration for a chart."""
    type: str  # histogram, scatter, box, heatmap, bar, line
    title: str
    x_column: str
    y_column: Optional[str] = None
    config: Dict[str, Any] = {}


class DatasetAnalysis(BaseModel):
    """Complete dataset analysis."""
    id: str = None
    dataset_id: str
    summary: Dict[str, Any] = {}
    statistics: List[ColumnStatistics] = []
    correlations: List[CorrelationPair] = []
    missing_values: MissingValueAnalysis = MissingValueAnalysis()
    outliers: OutlierAnalysis = OutlierAnalysis()
    charts: List[ChartConfig] = []
    created_at: datetime = datetime.now(timezone.utc)


# ============================================================================
# ML Models
# ============================================================================

class MLMetrics(BaseModel):
    """Metrics for ML experiments."""
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    roc_auc: Optional[float] = None
    rmse: Optional[float] = None
    mae: Optional[float] = None
    r2: Optional[float] = None
    silhouette_score: Optional[float] = None
    inertia: Optional[float] = None


class MLResult(BaseModel):
    """Results from an ML experiment."""
    experiment_id: str
    metrics: MLMetrics
    model_params: Dict[str, Any] = {}
    feature_importance: Dict[str, float] = {}
    confusion_matrix: List[List[int]] = []
    created_at: datetime = datetime.now(timezone.utc)


# ============================================================================
# Benchmark Models
# ============================================================================

class BenchmarkMetrics(BaseModel):
    """Benchmark execution metrics."""
    mean: float = 0.0
    median: float = 0.0
    p95: float = 0.0
    p99: float = 0.0
    min: float = 0.0
    max: float = 0.0
    std_dev: float = 0.0
    throughput: Optional[float] = None
    sample_count: int = 0


class BenchmarkResult(BaseModel):
    """Benchmark result."""
    id: str = None
    name: str
    description: str = ""
    category: str = "general"  # ingestion, embedding, search, rag, database, ml
    metrics: BenchmarkMetrics
    environment: Dict[str, Any] = {}
    created_at: datetime = datetime.now(timezone.utc)
    duration_ms: int = 0


# ============================================================================
# Timeline Event Models
# ============================================================================

class TimelineEvent(BaseModel):
    """Event in the research timeline."""
    id: str = None
    project_id: str
    type: str  # experiment, note, paper, discovery, result, milestone
    title: str
    description: str = ""
    date: datetime = datetime.now(timezone.utc)
    linked_entity_id: Optional[str] = None
    linked_entity_type: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)
class MLExperiment(BaseModel):
    id: str = None
    project_id: str
    name: str
    task_type: str = "classification"
    algorithm: str = "logistic_regression"
    feature_columns: List[str] = []
    target_column: Optional[str] = None
    parameters: Dict[str, Any] = {}
    dataset_path: str = ""
    created_at: datetime = datetime.now(timezone.utc)
    status: str = "planned"
