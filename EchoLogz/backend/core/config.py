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

Usage Example (access from anywhere):
    from backend.core.config import settings

    print(settings.JWT_SECRET)
"""

from pydantic import BaseSettings # Pydantic: Library for data validation / settings management
# from dotenv import load_dotenv # <--- redundant to pydantic

# Load the .env file first
# load_dotenv() <-- does the same thing as pydantic class Config

# Pydantic:
class Settings(BaseSettings):
    DATABASE_URL: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    JWT_SECRET: str

    # Populate Values from .env file:
    class Config:              # ... Auto loads environment variables from .env <-- everything is string text
        env_file = ".env"      # ... Pydantic v.1.10.24 syntax 

settings = Settings()