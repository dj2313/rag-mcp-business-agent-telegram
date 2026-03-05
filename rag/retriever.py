try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import os
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")
COLLECTION_NAME = "business_docs"

def get_embeddings():
    """Returns the local embedding model."""
    print("Loading embedding model (this may take a minute the first time)...")
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    """Returns the Chroma vector store instance."""
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

def query_rag(query_text: str, k: int = 3):
    """
    Queries the vector store for the most relevant chunks.
    Returns a list of document strings.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query_text, k=k)
    return [doc.page_content for doc in results]

if __name__ == "__main__":
    # Test if we can initialize
    print(f"Chroma DB Path: {CHROMA_PATH}")
    store = get_vector_store()
    print("Vector store initialized successfully.")
