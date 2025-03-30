import os, json
from typing import List

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_KEY: str = os.getenv("API_KEY", "")
    WHOIS_API_URL: str = os.getenv(
        "WHOIS_API_URL", "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    )
    
    # CORS settings
    # ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3001").split(",")
    ALLOWED_ORIGINS: List[str] = json.loads(os.getenv("ALLOWED_ORIGINS", '["http://localhost:3000" , "https://whoislookup-beryl.vercel.app"]'))

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    class Config:
        """Pydantic config."""
        
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

