# Sample Research Project: Does Retrieval Strategy Affect RAG Answer Quality?

## Overview

This is the Atlas Lab sample research project. It demonstrates the full workflow:
document ingestion, multiple retrieval strategies, comparison, and visualization.

## Research Question

Does the retrieval strategy (Dense, Sparse, Hybrid) affect RAG answer quality,
as measured by precision, recall, and latency?

## Hypotheses

H1: Dense retrieval produces higher precision for factoid questions.
H2: Hybrid retrieval improves recall for multi-hop questions.
H3: Sparse retrieval is faster but lower recall for long passages.

## Documents

The documents/ folder contains synthetic passages covering:
- Machine learning fundamentals
- Retrieval-augmented generation
- Information retrieval theory
- Embedding models
- Vector databases

## Experiments

Three experiments will be run:
1. Dense retrieval only (cosine similarity over MiniLM embeddings)
2. Sparse retrieval (BM25-style TF-IDF)
3. Hybrid (combine dense + sparse scores)

Metrics:
- Precision@5
- Recall@5
- Average latency (ms)
- Answer quality (human-rated)

## Results

Run the experiments via the API. See example Python script in scripts/.

## Conclusions

After analysis, the recommended strategy is recorded in the paper workspace.
