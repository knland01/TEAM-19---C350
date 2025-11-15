"""
Configuration Center (config.py)
--------------------------------
This module manages all environment variables and application-wide settings
for the EchoLogz backend.

Core Responsibilities:
- Load environment variables from the .env file using Pydantic's BaseSettings
- Store configuration values for database URLs, API credentials, and debug modes
- Provide a single access point for global settings across the backend

Purpose:
Acts as the centralized "control panel" for the backend — keeping sensitive
information (like keys and connection strings) organized and out of code.

Typical Usage Example (access from anywhere):
    from backend.core.config import settings

    print(settings.app_name)
    print(settings.database_url)

"""

from pydantic import BaseSettings
from dotenv import load_dotenv

# Load the .env file first
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"  # Optional redundancy, Pydantic can use this too

settings = Settings()