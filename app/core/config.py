import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Invest Today Configuration
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Invest_Today"
    GOOGLE_API_KEY: str = Field(...)
    
    # Tool Configs
    GNEWS_API_KEY: Optional[str] = Field(None)
    
    # Vector DB Configs
    FAISS_INDEX_PATH: str = os.path.join("data", "faiss_index")
    
    # Model Configs
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    ANALYST_MODEL: str = "gemini-1.5-flash"
    JUDGE_MODEL: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
