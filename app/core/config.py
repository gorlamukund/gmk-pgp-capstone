# app/core/config.py
# Central configuration file - reads all settings from .env file

import os

from dotenv import load_dotenv

# Load all variables from .env file into memory
load_dotenv()


class Settings:
    # Anthropic API
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Application
    APP_NAME: str = os.getenv("APP_NAME", "SAP BTP Document Assistant")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # ChromaDB
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "chroma_db")
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "documents")

    # LLM
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-haiku-4-5-20251001")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))

    # Embeddings & Chunking
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))


# Single instance used across entire app
settings = Settings()
