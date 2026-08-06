from src.config.settings import settings
from src.repositories.chroma_repository import ChromaRepository
from src.services.retrieval_service import RetrievalService
from src.services.llm_service import LLMService
from src.services.qa_service import QAService


def init_qa_service() -> QAService:
    # Repositories handle their own embedding function internally
    quran_repo = ChromaRepository(
        db_path=settings.chroma_path,
        collection_name=settings.quran_collection
    )

    # hadith_repo = ChromaRepository(
    #     db_path=settings.chroma_path,
    #     collection_name=settings.hadith_collection
    # )

    retrieval_service = RetrievalService(quran_repo=quran_repo, hadith_repo=hadith_repo)
    llm_service = LLMService()

    return QAService(retrieval_service=retrieval_service, llm_service=llm_service)


def main() -> None:
    """Simple command-line chat loop, useful for testing without Streamlit."""
    print("=== Islamic Knowledge Assistant (CLI) ===")
    print("Type your question, or 'exit' to quit.\n")

    try:
        qa_service = init_qa_service()
    except Exception as e:
        print(f"[!] Failed to initialize services: {e}")
        print("    Make sure Ollama is running and the vector DB has been built (see README).")
        return

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            result = qa_service.answer_question(question)
            print(f"\nAssistant: {result['answer']}\n")
            if result.get("citations"):
                print("Sources:")
                for c in result["citations"]:
                    print(f"  - {c}")
            print()
        except Exception as e:
            print(f"[!] Error answering question: {e}\n")


if __name__ == "__main__":
    main()