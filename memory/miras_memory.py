import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from memory.embedding_utils import EmbeddingUtils
import config

class MIRASMemory:
    def __init__(self, surprise_threshold=None, max_size=None):
        self.surprise_threshold = surprise_threshold or config.SURPRISE_THRESHOLD
        self.max_size = max_size or config.MEMORY_MAX_SIZE
        self.embedding_utils = EmbeddingUtils()
        self.memories = []
        
    def add_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        embedding = self.embedding_utils.generate_embedding(content)
        
        existing_embeddings = [m['embedding'] for m in self.memories]
        novelty_score = self.embedding_utils.compute_novelty_score(embedding, existing_embeddings)
        
        if novelty_score >= self.surprise_threshold:
            memory_entry = {
                'content': content,
                'embedding': embedding,
                'novelty_score': novelty_score,
                'timestamp': time.time(),
                'access_count': 0,
                'metadata': metadata or {}
            }
            
            self.memories.append(memory_entry)
            
            if len(self.memories) > self.max_size:
                self._consolidate_memories()
            
            return True
        return False
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.memories:
            return []
        
        query_embedding = self.embedding_utils.generate_embedding(query)
        
        scored_memories = []
        current_time = time.time()
        
        for memory in self.memories:
            similarity = self.embedding_utils.cosine_similarity(query_embedding, memory['embedding'])
            
            time_decay = np.exp(-(current_time - memory['timestamp']) / (86400 * 7))
            access_boost = 1 + (memory['access_count'] * 0.1)
            
            score = similarity * time_decay * access_boost
            
            scored_memories.append({
                'memory': memory,
                'score': score,
                'similarity': similarity
            })
        
        scored_memories.sort(key=lambda x: x['score'], reverse=True)
        
        top_memories = scored_memories[:top_k]
        for item in top_memories:
            item['memory']['access_count'] += 1
        
        return [item['memory'] for item in top_memories]
    
    def _consolidate_memories(self):
        current_time = time.time()
        
        for memory in self.memories:
            time_factor = np.exp(-(current_time - memory['timestamp']) / (86400 * 30))
            access_factor = memory['access_count'] / (1 + memory['access_count'])
            novelty_factor = memory['novelty_score']
            
            memory['retention_score'] = (time_factor * 0.3 + 
                                        access_factor * 0.4 + 
                                        novelty_factor * 0.3)
        
        self.memories.sort(key=lambda x: x['retention_score'], reverse=True)
        self.memories = self.memories[:self.max_size]
    
    def save_to_file(self, filename: str):

        serializable_memories = []
        for memory in self.memories:
            mem_dict = {
                'content': memory['content'],
                'embedding': memory['embedding'].tolist() if hasattr(memory['embedding'], 'tolist') else memory['embedding'],
                'timestamp': memory['timestamp'],
                'novelty_score': float(memory['novelty_score']),  # Convert to Python float
                'access_count': int(memory['access_count']),  # Convert to Python int
                'importance': float(memory['importance']) if 'importance' in memory else 0.0
            }
            serializable_memories.append(mem_dict)
        
        with open(filename, 'w') as f:
            json.dump(serializable_memories, f, indent=2)
    
    def load_from_file(self, filepath: str):
        with open(filepath, 'r') as f:
            loaded_memories = json.load(f)
        
        self.memories = []
        for memory in loaded_memories:
            memory['embedding'] = np.array(memory['embedding'])
            self.memories.append(memory)
    
    def get_stats(self) -> Dict[str, Any]:
        if not self.memories:
            return {
                'total_memories': 0,
                'avg_novelty': 0,
                'avg_access_count': 0
            }
        
        return {
            'total_memories': len(self.memories),
            'avg_novelty': np.mean([m['novelty_score'] for m in self.memories]),
            'avg_access_count': np.mean([m['access_count'] for m in self.memories]),
            'oldest_memory': datetime.fromtimestamp(min(m['timestamp'] for m in self.memories)).isoformat(),
            'newest_memory': datetime.fromtimestamp(max(m['timestamp'] for m in self.memories)).isoformat()
        }
