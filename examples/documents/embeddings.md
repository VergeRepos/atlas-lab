# Embedding Models for Retrieval

Text embeddings are dense vector representations of text. They are learned
such that semantically similar texts are close in the vector space.

## Popular Models

### Sentence-BERT (SBERT)
A modification of BERT that produces semantically meaningful sentence
embeddings using siamese networks. Common checkpoints:
- all-MiniLM-L6-v2 (384 dim, fast)
- all-mpnet-base-v2 (768 dim, more accurate)

### OpenAI Embeddings
- text-embedding-ada-002 (1536 dim)
- text-embedding-3-small/large

### Local Models via Ollama
- nomic-embed-text
- mxbai-embed-large

## Choosing a Model

Trade-offs to consider:
- **Dimensionality**: Higher is more expressive but slower
- **Speed**: Critical for real-time applications
- **Domain**: General vs. specialized models
- **License**: Open weights vs. proprietary

## Best Practices

1. Chunk documents into reasonable sizes (256-1024 tokens)
2. Include overlap between chunks (10-20%)
3. Re-rank top candidates with a cross-encoder for best results
4. Cache embeddings to avoid recomputation
