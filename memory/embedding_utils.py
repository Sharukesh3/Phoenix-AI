import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingUtils:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embedding(self, text):
        if isinstance(text, list):
            return self.model.encode(text)
        return self.model.encode([text])[0]
    
    def cosine_similarity(self, emb1, emb2):
        if len(emb1.shape) == 1:
            emb1 = emb1.reshape(1, -1)
        if len(emb2.shape) == 1:
            emb2 = emb2.reshape(1, -1)
        return cosine_similarity(emb1, emb2)[0][0]
    
    def compute_novelty_score(self, new_embedding, existing_embeddings):
        if len(existing_embeddings) == 0:
            return 1.0
        
        similarities = []
        for existing_emb in existing_embeddings:
            sim = self.cosine_similarity(new_embedding, existing_emb)
            similarities.append(sim)
        
        max_similarity = max(similarities)
        novelty = 1.0 - max_similarity
        return novelty
