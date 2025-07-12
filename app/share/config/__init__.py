from abc import ABC, abstractmethod
import os

from dotenv import load_dotenv


class Config(ABC):
    def __init__(self):
        load_dotenv()

    def get_env(self, key):
        return os.getenv(key)


class GeminiConfig(Config):
    @property
    @abstractmethod
    def api_key(self):
        pass
