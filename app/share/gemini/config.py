
from app.share.config import GeminiConfig
from google.genai import types


class GeminiConfigImpl(GeminiConfig):
    @property
    def api_key(self):
        return self.get_env("GEMINI_API_KEY")
