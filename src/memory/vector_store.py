import os
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

# Global config
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "career_guide_memory"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_embeddings(provider="ollama", model="llama3"):
    """
    Factory to get the embedding model.
    Defaults to Ollama, falls back to SentenceTransformers (HuggingFace).
    """
    if provider == "ollama":
        try:
            embeddings = OllamaEmbeddings(
                base_url=OLLAMA_BASE_URL,
                model=model
            )
            # Try a dummy embedding to check connection
            embeddings.embed_query("test")
            return embeddings
        except Exception as e:
            print(f"Warning: Failed to connect to Ollama: {e}. Falling back to local HuggingFace.")
            return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    else:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    """
    Returns the Qdrant vector store instance.
    """
    embeddings = get_embeddings()
    
    client = QdrantClient(url=QDRANT_URL)
    
    # Check if collection exists
    from qdrant_client.http import models
    if not client.collection_exists(COLLECTION_NAME):
        # Determine vector size dynamically
        sample_embedding = embeddings.embed_query("test")
        vector_size = len(sample_embedding)
        
        print(f"Creating collection '{COLLECTION_NAME}' with vector size {vector_size}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )

    # Return LangChain Qdrant wrapper
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
