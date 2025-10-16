"""
Configuration Center (config.py)
--------------------------------
This module manages all environment variables and application-wide settings
for the EchoLogz backend.

Core Responsibilities:
- Load environment variables from the .env file using Pydantic's BaseSettings
- Store configuration values for database URLs, API credentials, and debug modes
- Provide a single, reliable access point for global settings across the backend

Purpose:
Acts as the centralized "control panel" for the backend — keeping sensitive
information (like keys and connection strings) organized and out of code.

Typical Usage Example:
    from backend.core.config import settings

    print(settings.app_name)
    print(settings.database_url)

"""