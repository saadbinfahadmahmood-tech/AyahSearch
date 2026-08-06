from typing import Any, Dict, List
from src.services.retrieval_service import RetrievalService
from src.services.llm_service import LLMService


class QAService:


    def __init__(self, retrieval_service: RetrievalService, llm_service: LLMService):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def _build_context(self, retrieved_docs: Dict[str, List[Dict[str, Any]]]) -> str:
        context_parts = []

        quran_docs = retrieved_docs.get("quran", [])
        if quran_docs:
            context_parts.append("=== QURAN VERSES ===")
            for idx, item in enumerate(quran_docs, 1):
                meta = item["metadata"]
                context_parts.append(
                    f"[{idx}] Surah {meta.get('surah_name_en')} ({meta.get('surah_no')}): Ayah {meta.get('ayah_no')}\n"
                    f"{item['document']}\n"
                )

        hadith_docs = retrieved_docs.get("hadith", [])
        if hadith_docs:
            context_parts.append("=== HADITH SELECTIONS ===")
            for idx, item in enumerate(hadith_docs, 1):
                meta = item["metadata"]
                context_parts.append(
                    f"[{idx}] Collection: {meta.get('collection_name')} - Book: {meta.get('book_name')} - Hadith No: {meta.get('hadith_no')}\n"
                    f"{item['document']}\n"
                )

        return "\n".join(context_parts)

    def _format_citations(self, retrieved_docs: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        citations = []

        quran_docs = retrieved_docs.get("quran", [])
        for item in quran_docs:
            m = item["metadata"]
            citations.append(f"Quran: Surah {m.get('surah_name_en')} {m.get('surah_no')}:{m.get('ayah_no')}")

        hadith_docs = retrieved_docs.get("hadith", [])
        for item in hadith_docs:
            m = item["metadata"]
            citations.append(f"Hadith: {m.get('collection_name')} (Hadith #{m.get('hadith_no')})")

        return citations

    def answer_question(
        self,
        question: str,
        quran_k: int = 3,
        hadith_k: int = 3,
        top_k: int = None,
    ) -> Dict[str, Any]:
        # `top_k`, if given, overrides both quran_k and hadith_k (used by the UI's single slider)
        if top_k is not None:
            quran_k = top_k
            hadith_k = top_k

        retrieved = self.retrieval_service.retrieve(question, quran_k=quran_k, hadith_k=hadith_k)
        context = self._build_context(retrieved)

        system_prompt = """You are an Islamic Assistant providing verified, authentic answers based strictly on sacred Islamic texts.

STRICT RULES:
1. Base your answer strictly and exclusively on the provided Context below.
2. Never invent, extrapolate, or modify Quranic verses or Hadiths.
3. Always maintain a respectful, objective, and scholarly tone.
4. If the provided context does not contain sufficient information to answer the question accurately, clearly state: "I could not find an authentic answer based on the available sources."
"""

        user_prompt = f"""Question: {question}

Context:
{context}

Answer:"""

        llm_response = self.llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        citations = self._format_citations(retrieved)

        return {
            "question": question,
            "answer": llm_response,
            "citations": citations,
            "raw_context": retrieved
        }