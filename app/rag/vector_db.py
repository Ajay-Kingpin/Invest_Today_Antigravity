import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class VectorDB:
    def __init__(self):
        self.index_path = settings.FAISS_INDEX_PATH
        self.metadata_path = f"{self.index_path}.pkl"
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def add_documents(self, documents: list, ids: list, metadatas: list = None):
        """Add documents to the FAISS index."""
        if not documents:
            return

        embeddings = self.embedding_model.encode(documents)
        embeddings = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings)
        
        for i, doc in enumerate(documents):
            self.metadata.append({
                "id": ids[i],
                "content": doc,
                "metadata": metadatas[i] if metadatas else {}
            })
            
        self._save()

    def query(self, query_text: str, n_results: int = 3):
        """Query the FAISS index for relevant documents."""
        query_embedding = self.embedding_model.encode([query_text])
        query_embedding = np.array(query_embedding).astype('float32')
        
        distances, indices = self.index.search(query_embedding, n_results)
        
        results = {
            "documents": [[]],
            "metadatas": [[]],
            "ids": [[]],
            "distances": [[]]
        }
        
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                res = self.metadata[idx]
                results["documents"][0].append(res["content"])
                results["metadatas"][0].append(res["metadata"])
                results["ids"][0].append(res["id"])
        
        return results

    def _save(self):
        """Save the FAISS index and metadata to disk."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
