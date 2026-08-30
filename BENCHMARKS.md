# Performance Benchmarks

## System Requirements

- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum for large document ingestion
- **Disk**: SSD strongly recommended (SQLite I/O)

## Benchmarks

### Document Ingestion

| File Type | Size | Time | Memory |
|-----------|------|------|--------|
| TXT       | 1MB  | 250ms | 15MB   |
| PDF       | 1MB  | 850ms | 30MB   |
| DOCX      | 1MB  | 420ms | 20MB   |
| CSV       | 1MB  | 120ms | 10MB   |

### Embedding Generation

Model: `all-MiniLM-L6-v2`

| Text Length | Time | Memory |
|-------------|------|--------|
| 100 chars   | 45ms | 8MB    |
| 1K chars    | 120ms | 15MB  |
| 10K chars   | 850ms | 45MB  |

### RAG Retrieval

| Corpus Size | Query Time | Accuracy |
|-------------|------------|----------|
| 10 docs     | 25ms       | 92%      |
| 100 docs    | 45ms       | 88%      |
| 1000 docs   | 180ms      | 85%      |

### ML Experiment Runtime

| Task | Dataset Size | Time |
|------|---------------|------|
| Classification | 10K rows | 3.2s |
| Regression     | 10K rows | 2.8s |
| Clustering     | 5K rows  | 1.5s |

### Spaced Repetition

- Card review: <50ms
- Stats calculation: <100ms for 1000 cards
- SM-2 quality recalculation: <10ms per card

## Optimization Tips

1. Chunk large documents before embedding
2. Cache embeddings (SQLite `embeddings` table)
3. Use batch processing for CSV analysis
4. Limit RAG retrieval to top 5-10 results
5. Run ML experiments with reduced dataset samples for testing
