"""
----------------------------------------------------
MODULE: Database Control Center (dp_sessions.py)
----------------------------------------------------

────────────────────────────────────────────
Handles all low-level database setup:
- Defines the connection URL (SQLite for local dev)
- Creates the SQLAlchemy engine (bridge between app <-> DB)
- Configures the session factory for request-scoped sessions
- Declares the base class for ORM model definitions

Note:
This file should remain framework-agnostic — 
it should NOT depend on FastAPI or any web-specific logic (hence removal of get_db()).
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
# ... The connection string defines which database and driver to use.
# ... Here we use [SQLite] for local development (simple file-based DB).
# ... When deploying to production, switch to PostgreSQL or another RDBMS:
# ... ... EXAMPLE - production URL (uncomment and adjust as needed):
# ... ... DATABASE_URL = "postgresql+psycopg2://user:password@localhost/echologz"

DATABASE_URL = settings.DATABASE_URL

# ------------------------------------------------------------------------------------
# SQAlchemy Database Engine (connection bridge)
# ------------------------------------------------------------------------------------
# ... Responsible for:
# ...    - Opening the SQLite file
# ...    - Creating DB connections
# ...    - Running SQL commands
# ...    - Reading/Writing to the echologz.gb file
# ...    - Managing the Connection Pool <-- importent when hundreds of users (Postgres switch)
# ...    - Talking to SQLite under the hood
#

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {} # <-- easy Postgres replace
    )
# ... `check_same_thread=False`
# ... ... SQLite's default behavior restricts a database connection to the same thread
# ... ... that created it. FastAPI uses multiple worker threads to process HTTP requests,
# ... ... so the same connection might be accessed from different threads. 
# ... ... Setting `check_same_thread=False` disables this restriction and allows
# ... ... SQLite to work correctly in a multithreaded FastAPI environment.

# ------------------------------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------------------------------
# ... sessionmaker - returns a callable session factory (aka SessionLocal)
# ... The session factory generates Session instances used for DB operations.
# ...   - autocommit=False → Explicit control of commit transactions - auto commits are dangerous
# ...   - autoflush=False  → Prevents premature DB flushes before commits
# ...   - bind=engine      → Connects this factory to our defined engine

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

"""
FUNCTION MOVED TO: core/dependencies.py 
    # # -------------------------------------------------------------------
    # # 5. Database Session Dependency
    # # -------------------------------------------------------------------
    # def get_db():
    #     
    ##     Creates a new database session for a request and ensures it's closed after use.
    ##     Useful for dependency injection (ex: in FastAPI routes).
    #     
    #     db = SessionLocal()
    #     try:
    #         yield db
    #     finally:
    #         db.close()

"""