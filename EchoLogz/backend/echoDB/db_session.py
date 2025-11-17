"""
----------------------------------------------------
MODULE: Database Control Center (dp_sessions.py)
----------------------------------------------------


Handles all low-level database setup:
- Defines the connection URL (SQLite for local dev)
- Creates the SQLAlchemy engine (bridge between app <-> DB)
- Configures the session factory for request-scoped sessions
- Declares the base class for ORM model definitions

NOTE: This file should remain framework-agnostic. 
Should NOT depend on FastAPI / web-specific logic (hence removal of get_db()).

────────────────────────────────────────────
Modules using db_sessions.py:
- dependencies.py
────────────────────────────────────────────
"""

# INTERNAL IMPORTS:
from backend.core.config import settings # ... For DATABASE_URL

# EXTERNAL IMPORTS:
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ------------------------------------------------------------------------------------
# Database URL Configuration
# ------------------------------------------------------------------------------------
# ... [SQLite] used for local development (simple file-based DB).
# ... For deploy/production, switch to [PostgreSQL].
DATABASE_URL = settings.DATABASE_URL

# ------------------------------------------------------------------------------------
# SQAlchemy Database Engine (connection bridge)
# ------------------------------------------------------------------------------------
# ... Responsible for: Open the SQLite file - Create DB connections - Run SQL commands - Read/Write to DB
# ...    - Manage the Connection Pool <-- importent when hundreds of users (Postgres switch)
# ...    - Talk to SQLite under the hood
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {} # <-- easy Postgres replace
    )
# ... `check_same_thread=False`: Disables SQLite's default = database connection limited to same thread that created it
# ... ... --> Allows FastAPI's multi-threads to process HTTP requests.


# ------------------------------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------------------------------
# ... sessionmaker() - returns a callable session factory (SessionLocal)
# ... The session factory generates Session instances used for DB operations.
# ...   - autocommit=False -> Explicit control of commit transactions - auto commits are dangerous
# ...   - autoflush=False  -> Prevents premature DB flushes before commits
# ...   - bind=engine      -> Connects this factory to defined engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ------------------------------------------------------------------------------------
# Declarative Base for SQAlchemy ORM Models
# ------------------------------------------------------------------------------------
# ... This base class is inherited by all ORM model classes.
# ... It allows SQLAlchemy to map Python classes to database tables.
Base = declarative_base()

# =====================================================================================
# (Optional) Utility Function: Get Engine Metadata
# =====================================================================================
# ... This can be handy during debugging or migrations to inspect 
# ... engine configuration and metadata if needed.
def get_engine_info():
    """Return a summary of current engine configuration."""
    return {
        "database_url": DATABASE_URL,
        "driver": str(engine.url.drivername),
        "dialect": str(engine.dialect.name),
        "pool_class": engine.pool.__class__.__name__,
    }

