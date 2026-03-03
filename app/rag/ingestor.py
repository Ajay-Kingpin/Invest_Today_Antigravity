from app.rag.vector_db import VectorDB
from bs4 import BeautifulSoup
import requests
import uuid

class Ingestor:
    def __init__(self):
        self.db = VectorDB()

    def ingest_url(self, url: str, metadata: dict = None):
        """Extract text from a URL and add to VectorDB."""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            
            # Simple chunking by paragraph for now
            chunks = [c for c in text.split("\n\n") if len(c) > 100]
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = [metadata or {} for _ in chunks]
            
            self.db.add_documents(chunks, ids, metadatas)
            return True
        except Exception:
            return False

    def ingest_text(self, text: str, metadata: dict = None):
        """Ingest raw text directly."""
        chunks = [c for c in text.split("\n\n") if len(c) > 50]
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [metadata or {} for _ in chunks]
        self.db.add_documents(chunks, ids, metadatas)
        return True
