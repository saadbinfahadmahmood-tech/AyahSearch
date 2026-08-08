from typing import Any, Dict, List, Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.config.settings import settings
from src.models.vector_record import VectorRecord


class ChromaRepository:

    def __init__(self, db_path: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=db_path)
        
        self.embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, records: List[VectorRecord], batch_size: int = 5) -> None:
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            ids = [r.id for r in batch]
            documents = [r.document for r in batch]
            metadatas = [r.metadata for r in batch]

            # No manual embed_batch() needed! Chroma handles it automatically.
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    def search(
        self,
        query: str,
        top_k: int = 3,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        query_kwargs = {
            "query_texts": [query],  # Pass raw query text directly!
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }
        
        if where:
            query_kwargs["where"] = where

        results = self.collection.query(**query_kwargs)

        retrieved = []
        if results and results.get("documents"):
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            ids = results["ids"][0]
            dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)

            for doc_id, doc, meta, dist in zip(ids, docs, metas, dists):
                retrieved.append({
                    "id": doc_id,
                    "document": doc,
                    "metadata": meta,
                    "distance": dist
                })

        return retrieved