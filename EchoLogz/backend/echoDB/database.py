"""
Database Control Center

This module handles database connection and session management.

Responsibilities:
- Define the database URL.
- Create the SQLAlchemy engine (connects Python to the DB).
- Provide a SessionLocal factory (for creating database sessions).
- Define the Base class for declaring ORM models.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker