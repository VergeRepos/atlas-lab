"""Embedding service using sentence-transformers."""
from typing import List, Optional
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.has_model = True
        except Exception:
            self.model = None
            self.has_model = False

    def generate_embedding(self, text: str) -> Optional[List[float]]:
        if not self.has_model or self.model is None:
            return None
        embedding = self.model.encode(text, show_progress_bar=False)
        return embedding.tolist()
