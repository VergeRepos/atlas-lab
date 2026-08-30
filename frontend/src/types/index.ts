// Core domain types for Atlas Lab

// ============================================================================
// Project & Research Types
// ============================================================================

export interface Project {
  id: string;
  name: string;
  description: string;
  research_question?: string;
  created_at: string;
  updated_at: string;
  status: 'active' | 'completed' | 'archived';
  tags: string[];
}

export interface ResearchQuestion {
  id: string;
  project_id: string;
  question: string;
  hypothesis?: string;
  status: 'open' | 'answered' | 'partial';
  created_at: string;
  updated_at: string;
}

export interface Hypothesis {
  id: string;
  project_id: string;
  question_id: string;
  statement: string;
  variables: string[];
  created_at: string;
  tested: boolean;
  results?: string;
}

export interface Note {
  id: string;
  project_id: string;
  title: string;
  content: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  linked_concepts: string[];
}

export interface Source {
  id: string;
  project_id: string;
  document_id?: string;
  citation_key: string;
  authors: string[];
  title: string;
  year?: number;
  doi?: string;
  url?: string;
  type: 'article' | 'book' | 'paper' | 'website' | 'other';
  metadata: Record<string, unknown>;
}

// ============================================================================
// Document Types
// ============================================================================

export interface Document {
  id: string;
  project_id?: string;
  filename: string;
  file_path: string;
  file_type: 'pdf' | 'txt' | 'md' | 'csv' | 'docx';
  file_size: number;
  title?: string;
  author?: string;
  created_at: string;
  processed_at?: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  error?: string;
  page_count?: number;
  word_count?: number;
  checksum: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  content: string;
  chunk_index: number;
  start_char: number;
  end_char: number;
  page_number?: number;
  metadata: Record<string, unknown>;
}

export interface Embedding {
  id: string;
  chunk_id: string;
  model: string;
  vector: number[];
  dimensions: number;
  created_at: string;
}

// ============================================================================
// Experiment Types
// ============================================================================

export interface Experiment {
  id: string;
  project_id: string;
  name: string;
  description: string;
  hypothesis?: string;
  status: 'planned' | 'running' | 'completed' | 'failed' | 'cancelled';
  created_at: string;
  started_at?: string;
  completed_at?: string;
  parameters: Record<string, unknown>;
  random_seed?: number;
  environment: EnvironmentInfo;
}

export interface EnvironmentInfo {
  python_version: string;
  packages: Record<string, string>;
  hardware: HardwareInfo;
  os: string;
}

export interface HardwareInfo {
  cpu_model: string;
  cpu_count: number;
  memory_total: number;
  gpu_available: boolean;
  gpu_model?: string;
  gpu_memory?: number;
}

export interface ExperimentResult {
  id: string;
  experiment_id: string;
  metrics: Record<string, number>;
  output_files: string[];
  dataset_hash: string;
  created_at: string;
}

export interface Dataset {
  id: string;
  project_id: string;
  name: string;
  description?: string;
  file_path: string;
  file_type: 'csv' | 'json' | 'parquet';
  row_count: number;
  column_count: number;
  columns: ColumnInfo[];
  created_at: string;
  checksum: string;
}

export interface ColumnInfo {
  name: string;
  type: 'numeric' | 'categorical' | 'datetime' | 'boolean' | 'text';
  nullable: boolean;
  unique_count?: number;
  null_count?: number;
  sample_values?: unknown[];
}

// ============================================================================
// Learning Types
// ============================================================================

export interface LearningPath {
  id: string;
  subject: string;
  title: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  topics: LearningTopic[];
  created_at: string;
  updated_at: string;
  mastery_score: number;
}

export interface LearningTopic {
  id: string;
  path_id: string;
  title: string;
  explanation: string;
  prerequisites: string[];
  examples: Example[];
  exercises: Exercise[];
  mini_projects: MiniProject[];
  review_questions: ReviewQuestion[];
  order: number;
  mastery_level: 'not_started' | 'learning' | 'reviewing' | 'mastered';
  time_spent_minutes: number;
}

export interface Example {
  id: string;
  title: string;
  description: string;
  code?: string;
  output?: string;
  explanation: string;
}

export interface Exercise {
  id: string;
  title: string;
  description: string;
  hints: string[];
  solution?: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface MiniProject {
  id: string;
  title: string;
  description: string;
  requirements: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface ReviewQuestion {
  id: string;
  question: string;
  answer: string;
  type: 'definition' | 'explanation' | 'application' | 'analysis';
}

// ============================================================================
// Flashcard Types
// ============================================================================

export interface Flashcard {
  id: string;
  deck_id: string;
  front: string;
  back: string;
  source_note_id?: string;
  tags: string[];
  difficulty: number;
  created_at: string;
  updated_at: string;
}

export interface FlashcardDeck {
  id: string;
  name: string;
  description?: string;
  card_count: number;
  due_count: number;
  new_count: number;
  created_at: string;
  updated_at: string;
}

export interface ReviewSession {
  id: string;
  deck_id: string;
  started_at: string;
  completed_at?: string;
  cards_reviewed: number;
  correct_count: number;
  again_count: number;
  hard_count: number;
  good_count: number;
  easy_count: number;
}

export interface CardReview {
  id: string;
  card_id: string;
  session_id: string;
  quality: 0 | 1 | 2 | 3 | 4 | 5;
  interval: number;
  ease_factor: number;
  reviewed_at: string;
  response_time_ms: number;
}

// ============================================================================
// Paper Types
// ============================================================================

export interface Paper {
  id: string;
  project_id: string;
  title: string;
  abstract?: string;
  sections: PaperSection[];
  citations: Citation[];
  created_at: string;
  updated_at: string;
  word_count: number;
  status: 'draft' | 'in_review' | 'published';
}

export interface PaperSection {
  id: string;
  title: string;
  content: string;
  order: number;
  type: 'abstract' | 'introduction' | 'related_work' | 'methodology' | 'results' | 'discussion' | 'conclusion' | 'references' | 'custom';
}

export interface Citation {
  id: string;
  paper_id: string;
  source_id: string;
  location: string;
  format: 'apa' | 'mla' | 'ieee';
}

// ============================================================================
// Knowledge Graph Types
// ============================================================================

export interface KnowledgeNode {
  id: string;
  type: 'concept' | 'paper' | 'person' | 'technology' | 'experiment' | 'question';
  label: string;
  description?: string;
  properties: Record<string, unknown>;
  x?: number;
  y?: number;
}

export interface KnowledgeEdge {
  id: string;
  source_id: string;
  target_id: string;
  relationship: string;
  weight: number;
  properties: Record<string, unknown>;
}

export interface KnowledgeGraph {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
}

// ============================================================================
// AI & RAG Types
// ============================================================================

export interface AIResponse {
  id: string;
  query: string;
  answer: string;
  model: string;
  sources: AISource[];
  confidence: number;
  generated_at: string;
  latency_ms: number;
  is_local: boolean;
  retrieved_chunks: RetrievedChunk[];
}

export interface AISource {
  document_id: string;
  document_title: string;
  chunk_id: string;
  content: string;
  page_number?: number;
  relevance_score: number;
  citation: string;
}

export interface RetrievedChunk {
  chunk_id: string;
  document_id: string;
  content: string;
  score: number;
  page_number?: number;
}

export interface RAGConfig {
  embedding_model: string;
  llm_model: string;
  chunk_size: number;
  chunk_overlap: number;
  retrieval_top_k: number;
  reranking_enabled: boolean;
  temperature: number;
  max_tokens: number;
}

// ============================================================================
// Benchmark Types
// ============================================================================

export interface BenchmarkResult {
  id: string;
  name: string;
  description: string;
  category: 'ingestion' | 'embedding' | 'search' | 'rag' | 'database' | 'ml';
  metrics: BenchmarkMetrics;
  environment: EnvironmentInfo;
  created_at: string;
  duration_ms: number;
}

export interface BenchmarkMetrics {
  mean: number;
  median: number;
  p95: number;
  p99: number;
  min: number;
  max: number;
  std_dev: number;
  throughput?: number;
  sample_count: number;
}

// ============================================================================
// System Types
// ============================================================================

export interface SystemStatus {
  version: string;
  python_backend: ServiceStatus;
  tauri_backend: ServiceStatus;
  database: ServiceStatus;
  ollama?: OllamaStatus;
  gpu_available: boolean;
  storage_usage: StorageInfo;
  recent_errors: LogEntry[];
  task_queue: TaskInfo[];
}

export interface ServiceStatus {
  connected: boolean;
  version?: string;
  latency_ms?: number;
  error?: string;
}

export interface OllamaStatus {
  available: boolean;
  version?: string;
  models: OllamaModel[];
}

export interface OllamaModel {
  name: string;
  size: number;
  context_length: number;
  modified_at: string;
}

export interface StorageInfo {
  total: number;
  used: number;
  available: number;
  data_directory: string;
}

export interface LogEntry {
  timestamp: string;
  level: 'debug' | 'info' | 'warning' | 'error';
  message: string;
  source?: string;
}

export interface TaskInfo {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: number;
  started_at?: string;
  error?: string;
}

// ============================================================================
// UI Types
// ============================================================================

export type Theme = 'light' | 'dark' | 'system';
export type ViewMode = 'list' | 'grid' | 'detail';

export interface CommandPaletteAction {
  id: string;
  label: string;
  description?: string;
  shortcut?: string;
  icon?: string;
  action: () => void;
  category: string;
}

export interface PanelState {
  width?: number;
  height?: number;
  collapsed: boolean;
  position: 'left' | 'right' | 'top' | 'bottom';
}

// ============================================================================
// Search Types
// ============================================================================

export interface SearchResult {
  type: 'document' | 'note' | 'source' | 'experiment' | 'flashcard';
  id: string;
  title: string;
  snippet: string;
  relevance: number;
  metadata: Record<string, unknown>;
}

export interface SearchFilters {
  types?: SearchResult['type'][];
  project_ids?: string[];
  date_from?: string;
  date_to?: string;
  tags?: string[];
}

// ============================================================================
// Analytics Types
// ============================================================================

export interface DatasetAnalysis {
  id: string;
  dataset_id: string;
  summary: DatasetSummary;
  statistics: ColumnStatistics[];
  correlations: CorrelationPair[];
  missing_values: MissingValueAnalysis;
  outliers: OutlierAnalysis;
  distributions: DistributionInfo[];
  charts: ChartConfig[];
  created_at: string;
}

export interface DatasetSummary {
  row_count: number;
  column_count: number;
  numeric_columns: string[];
  categorical_columns: string[];
  total_missing: number;
  memory_usage_bytes: number;
}

export interface ColumnStatistics {
  column: string;
  type: string;
  count: number;
  null_count: number;
  unique_count?: number;
  mean?: number;
  std?: number;
  min?: number;
  max?: number;
  median?: number;
  mode?: unknown;
  distribution?: string;
}

export interface CorrelationPair {
  column1: string;
  column2: string;
  correlation: number;
  p_value: number;
  significant: boolean;
}

export interface MissingValueAnalysis {
  total_missing: number;
  columns: { column: string; missing_count: number; missing_percent: number }[];
}

export interface OutlierAnalysis {
  method: 'iqr' | 'zscore';
  total_outliers: number;
  by_column: { column: string; outlier_count: number; outlier_percent: number }[];
}

export interface DistributionInfo {
  column: string;
  bins: { bin_start: number; bin_end: number; count: number }[];
  skewness: number;
  kurtosis: number;
}

export interface ChartConfig {
  type: 'histogram' | 'scatter' | 'box' | 'heatmap' | 'bar' | 'line';
  title: string;
  x_column: string;
  y_column?: string;
  config: Record<string, unknown>;
}

// ============================================================================
// ML Types
// ============================================================================

export interface MLExperiment {
  id: string;
  project_id: string;
  name: string;
  task_type: 'classification' | 'regression' | 'clustering';
  algorithm: string;
  parameters: Record<string, unknown>;
  dataset_id: string;
  target_column: string;
  feature_columns: string[];
  created_at: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  started_at?: string;
  completed_at?: string;
  training_time_ms?: number;
}

export interface MLResult {
  experiment_id: string;
  metrics: MLMetrics;
  model_params: Record<string, unknown>;
  feature_importance?: Record<string, number>;
  confusion_matrix?: number[][];
  created_at: string;
}

export interface MLMetrics {
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1?: number;
  roc_auc?: number;
  rmse?: number;
  mae?: number;
  r2?: number;
  silhouette_score?: number;
  inertia?: number;
}

// ============================================================================
// Timeline Types
// ============================================================================

export interface TimelineEvent {
  id: string;
  project_id: string;
  type: 'experiment' | 'note' | 'paper' | 'discovery' | 'result' | 'milestone';
  title: string;
  description: string;
  date: string;
  linked_entity_id?: string;
  linked_entity_type?: string;
  created_at: string;
}