import streamlit as st
from src.config.settings import settings
from src.repositories.chroma_repository import ChromaRepository
from src.services.retrieval_service import RetrievalService
from src.services.llm_service import LLMService
from src.services.qa_service import QAService
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Configuration
st.set_page_config(
    page_title="Islamic Knowledge Assistant",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def init_qa_service():
    """Initialize and cache backend RAG pipeline services."""
    try:
        # Repositories now handle embeddings directly via configuration
        quran_repo = ChromaRepository(
            db_path=settings.chroma_path,
            collection_name=settings.quran_collection,
        )

        # hadith_repo = ChromaRepository(
        #     db_path=settings.chroma_path,
        #     collection_name=settings.hadith_collection,
        # )

        retrieval_service = RetrievalService(
            quran_repo=quran_repo
            # ,hadith_repo=hadith_repo
        )
        llm_service = LLMService()

        return QAService(
            retrieval_service=retrieval_service, llm_service=llm_service
        )
    except Exception as e:
        logger.exception("Failed to initialize services")
    st.error("Something went wrong starting the assistant. Please try again in a moment.")
    return None


# Sidebar Controls
with st.sidebar:
    st.title("📖 About")
    st.markdown("Ask questions and get answers grounded in the Quran, with citations.")
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Powered by ChromaDB & Ollama.")

# Main Header
st.title("📖 Islamic AI Knowledge Assistant")
st.caption("Retrieval-Augmented Generation (RAG) powered by Quran")

# Initialize Service
qa_service = init_qa_service()

if qa_service is None:
    st.warning("⚠️ Application service failed to start. Ensure vector store and local services are reachable.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("📌 Source Citations"):
                for cit in msg["citations"]:
                    if isinstance(cit, dict):
                        st.markdown(f"**[{cit.get('source', 'Source')}]** {cit.get('text', '')}")
                    else:
                        st.markdown(f"- {cit}")

# Handle User Input
if prompt := st.chat_input("Ask a question (e.g., What does Islam say about honoring parents?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching sacred collections and generating response..."):
            try:
                result = qa_service.answer_question(prompt, top_k=3)  # fixed, not user-controlled

                answer = result.get("answer", "No answer generated.")
                citations = result.get("citations", [])

                st.markdown(answer)

                if citations:
                    with st.expander("📌 Source Citations"):
                        for cit in citations:
                            if isinstance(cit, dict):
                                st.markdown(f"**[{cit.get('source', 'Source')}]** {cit.get('text', '')}")
                            else:
                                st.markdown(f"- {cit}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations,
                })
            except Exception as e:
                logger.exception("Failed to answer question")
                st.error("Sorry, I couldn't process that question. Please try rephrasing or try again shortly.")
