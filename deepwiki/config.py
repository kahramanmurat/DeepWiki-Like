"""Configuration management for DeepWiki-Like."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Chunking Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Database Configuration
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "./data"))
    CHROMA_DB_DIR: Path = DATA_DIR / "chroma_db"

    # Retrieval Configuration
    TOP_K: int = int(os.getenv("TOP_K", "5"))

    @classmethod
    def validate(cls) -> None:
        """Validate configuration."""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")
        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER is 'anthropic'")

        # Create data directories
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)


config = Config()
