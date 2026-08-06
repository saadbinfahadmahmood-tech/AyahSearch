from ollama import Client
from src.config.settings import settings


class LLMService:

    def __init__(self, model_name: str = None, api_key: str = None):
        self.model_name = model_name or settings.llm_model
        self.client = Client(
            host=settings.ollama_cloud_host,
            headers={"Authorization": f"Bearer {api_key or settings.ollama_api_key}"}
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.client.chat(
            model=self.model_name,
            messages=messages,
            options={"temperature": 0.1}
        )
        return response["message"]["content"]