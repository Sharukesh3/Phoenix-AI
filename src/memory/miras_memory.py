import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from src.memory.vector_store import get_vector_store
from langchain_core.documents import Document

class MIRASMemory:
    def __init__(self):
        self.vector_store = get_vector_store()

    def add_memory(self, content: str, importance: float = 0.5):
        """Adds a new memory to Qdrant."""
        metadata = {
            'timestamp': time.time(),
            'importance': importance,
            'access_count': 0,
            'type': 'episodic' 
        }
        
        # Add to vector store
        self.vector_store.add_documents([
            Document(page_content=content, metadata=metadata)
        ])
        
    def retrieve_relevant_memories(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieves relevant memories using cosine similarity search."""
        docs = self.vector_store.similarity_search(query, k=top_k)
        
        results = []
        for doc in docs:
            # Increment access count (This effectively requires updating the doc)
            # For simplicity in this hackathon version, we won't do the update-back-to-DB for access_count strictly
            # or we would need to delete and re-insert or use Set Payload API.
            # We'll just return the doc data.
            
            memory_data = {
                'content': doc.page_content,
                'embedding': [], # We don't need to return the vector usually
                'timestamp': doc.metadata.get('timestamp', time.time()),
                'novelty_score': 0.0, # Placeholder
                'access_count': doc.metadata.get('access_count', 0),
                'importance': doc.metadata.get('importance', 0.5)
            }
            results.append(memory_data)
        
        return results

    def get_stats(self) -> Dict[str, Any]:
        """Returns dummy stats since we don't query count typically."""
        return {
            'total_memories': "Managed by Qdrant",
            'status': "Active"
        }
