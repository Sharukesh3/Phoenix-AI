import pytest
from memory.miras_memory import MIRASMemory
from memory.embedding_utils import EmbeddingUtils

def test_memory_initialization():
    memory = MIRASMemory(surprise_threshold=0.7, max_size=100)
    assert memory.surprise_threshold == 0.7
    assert memory.max_size == 100
    assert len(memory.memories) == 0

def test_add_novel_memory():
    memory = MIRASMemory(surprise_threshold=0.7)
    
    result = memory.add_memory("Python is a programming language")
    assert result == True
    assert len(memory.memories) == 1

def test_add_similar_memory():
    memory = MIRASMemory(surprise_threshold=0.9)
    
    memory.add_memory("Python is a programming language")
    result = memory.add_memory("Python is a programming language")
    
    assert result == False

def test_retrieve_memories():
    memory = MIRASMemory(surprise_threshold=0.5)
    
    memory.add_memory("Python programming")
    memory.add_memory("Machine learning with TensorFlow")
    memory.add_memory("Web development with React")
    
    results = memory.retrieve("Python", top_k=2)
    assert len(results) <= 2
    assert results[0]['content'] == "Python programming"

def test_memory_consolidation():
    memory = MIRASMemory(surprise_threshold=0.5, max_size=5)
    
    for i in range(10):
        memory.add_memory(f"Memory content {i}")
    
    assert len(memory.memories) <= 5

def test_embedding_similarity():
    utils = EmbeddingUtils()
    
    emb1 = utils.generate_embedding("Python programming")
    emb2 = utils.generate_embedding("Python coding")
    
    similarity = utils.cosine_similarity(emb1, emb2)
    assert 0 <= similarity <= 1
    assert similarity > 0.5

def test_novelty_score():
    utils = EmbeddingUtils()
    
    existing = [
        utils.generate_embedding("Python"),
        utils.generate_embedding("Java")
    ]
    
    new_emb = utils.generate_embedding("Rust programming")
    novelty = utils.compute_novelty_score(new_emb, existing)
    
    assert 0 <= novelty <= 1

def test_memory_stats():
    memory = MIRASMemory()
    
    memory.add_memory("Test memory 1")
    memory.add_memory("Test memory 2")
    
    stats = memory.get_stats()
    assert stats['total_memories'] == 2
    assert 'avg_novelty' in stats
    assert 'avg_access_count' in stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
