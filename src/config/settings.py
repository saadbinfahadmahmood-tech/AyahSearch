from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    chroma_path: str = "./vector_db"
    quran_collection: str = "quran"
    hadith_collection: str = "hadith"

    ollama_base_url: str = "http://localhost:11434"   # still used for embeddings
    embedding_model: str = "nomic-embed-text"

    ollama_cloud_host: str = "https://ollama.com"
    ollama_api_key: str = ""
    llm_model: str = "gpt-oss:20b-cloud"

    quran_top_k: int = 3
    hadith_top_k: int = 3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()