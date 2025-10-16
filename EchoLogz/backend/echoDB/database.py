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


# -------------------------------------------------------------------
# 1. Database URL
# -------------------------------------------------------------------
# Using SQLite for local development:
DATABASE_URL = "sqlite:///./echoLogz.db"

# Switch to this when ready to Deploy(?):
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost/echologz"

# -------------------------------------------------------------------
# 2. Database Engine (connection bridge)
# -------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
) #check_same_thread = SQLite only

# -------------------------------------------------------------------
# 3. Session Factory
# -------------------------------------------------------------------
# autocommit=False: Explicit commit control
# autoflush=False: Prevents premature flushes during transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------------------------------------------
# 4. Declarative Base for ORM Models
# -------------------------------------------------------------------
Base = declarative_base()

# -------------------------------------------------------------------
# 5. Database Session Dependency
# -------------------------------------------------------------------
def get_db():
    """
    Creates a new database session for a request and ensures it's closed after use.
    Useful for dependency injection (ex: in FastAPI routes).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()