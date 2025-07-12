from google import genai

from app.share.config import GeminiConfig


class GeminiClient:
    def __init__(self, config: GeminiConfig):
        self.config = config

    def get_client(self):
        client = genai.Client(
            api_key=self.config.api_key,
        )

        return client
