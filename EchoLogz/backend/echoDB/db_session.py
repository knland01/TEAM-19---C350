"""
Database Control Center
────────────────────────────────────────────
Handles all low-level database setup:
- Defines the connection URL (SQLite for local dev)
- Creates the SQLAlchemy engine (bridge between app <-> DB)
- Configures the session factory for request-scoped sessions
- Declares the base class for ORM model definitions

Note:
This file should remain framework-agnostic — 
it should NOT depend on FastAPI or any web-specific logic. (hence removal of get_db())
────────────────────────────────────────────
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------------
# 1. Database URL Configuration
# -------------------------------------------------------------------
# ... The connection string defines which database and driver to use.
# ... Here we use [SQLite] for local development (simple file-based DB).
# ... When deploying to production, switch to PostgreSQL or another RDBMS:
# ... ... EXAMPLE - production URL (uncomment and adjust as needed):
# ... ... DATABASE_URL = "postgresql+psycopg2://user:password@localhost/echologz"

DATABASE_URL = "sqlite:///./echoLogz.db"



# -------------------------------------------------------------------
# 2. Database Engine (connection bridge)
# -------------------------------------------------------------------
# ... The engine manages the core connection pool and executes SQL commands.
# ... 'check_same_thread=False' is required for SQLite because it restricts 
# ... connections to the same thread by default (not suitable for FastAPI’s async model).

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# -------------------------------------------------------------------
# 3. Session Factory
# -------------------------------------------------------------------
# ... The session factory generates Session instances used for DB operations.
# ... - autocommit=False → Explicit control of commit transactions
# ... - autoflush=False  → Prevents premature DB flushes before commits
# ... - bind=engine      → Connects this factory to our defined engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------------------------------------------
# 4. Declarative Base for ORM Models
# -------------------------------------------------------------------
# ... This base class is inherited by all ORM model classes.
# ... It allows SQLAlchemy to map Python classes to database tables.

Base = declarative_base()

# ==========================================================
# 5. (Optional) Utility Function: Get Engine Metadata
# ==========================================================
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