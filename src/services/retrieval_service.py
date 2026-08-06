from typing import Any, Dict, List, Optional
from src.repositories.chroma_repository import ChromaRepository


class RetrievalService:

    def __init__(self, quran_repo: ChromaRepository, hadith_repo: Optional[ChromaRepository] = None):
        self.quran_repo = quran_repo
        self.hadith_repo = hadith_repo

    def retrieve(self, query: str, quran_k: int = 3, hadith_k: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        quran_results = self.quran_repo.search(query=query, top_k=quran_k)
        hadith_results = []
        if self.hadith_repo is not None:
            hadith_results = self.hadith_repo.search(query=query, top_k=hadith_k)

        return {"quran": quran_results, "hadith": hadith_results}