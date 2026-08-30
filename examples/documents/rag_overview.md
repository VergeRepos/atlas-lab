# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation is an AI framework that combines information
retrieval with text generation. Instead of relying solely on a language model's
parametric knowledge, RAG retrieves relevant documents from an external
knowledge base and uses them to generate more accurate, grounded answers.

## Architecture

A typical RAG system consists of:
1. **Document Processor**: Ingests and chunks documents
2. **Embedding Model**: Converts text chunks into dense vector representations
3. **Vector Store**: Stores embeddings for efficient similarity search
4. **Retriever**: Finds the most relevant chunks for a query
5. **Generator**: Uses the retrieved context to produce a response

## Benefits

- **Factual grounding**: Reduces hallucination by providing source material
- **Up-to-date information**: Can access knowledge beyond the training cutoff
- **Domain adaptation**: Easy to add domain-specific knowledge
- **Transparency**: Sources can be cited for every answer

## Retrieval Strategies

### Dense Retrieval
Uses vector similarity (cosine) over dense embeddings. Strong for semantic
matching but may miss exact keyword matches.

### Sparse Retrieval
Traditional methods like BM25 or TF-IDF. Excellent for keyword matching and
rare terms, but limited semantic understanding.

### Hybrid Retrieval
Combines dense and sparse scores. Often achieves the best of both worlds,
improving both precision and recall.
