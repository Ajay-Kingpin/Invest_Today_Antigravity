import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings
import os

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents: list, ids: list, metadatas: list = None):
        """Add documents to the vector store."""
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def query(self, query_text: str, n_results: int = 3):
        """Query the vector store for relevant documents."""
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
