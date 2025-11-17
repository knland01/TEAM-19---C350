"""
CRUD Operations Module

This module defines the Create, Read, Update, and Delete (CRUD) operations 
for interacting with the EchoLogz database via SQLAlchemy ORM. 

Responsibilities:
- Acts as the interface between API routes and the database.
- Contains reusable functions that handle data logic (insert, query, update, delete).
- Keeps the main API routes clean and focused on HTTP logic.

Files Connected:
- db_schemas.py     → Defines database tables and relationships.
- db_validation.py    → Defines Pydantic models for request/response validation.
- db_session.py   → Provides the database session (SessionLocal) for queries.

Typical Usage Example (from another module):
    from . import crud, db_schemas, db_session
    db_user = crud.get_user_by_id(db, user_id=1)
"""

from backend.echoDB import db_schemas, db_validation as db_val
# from .db_schemas import User
from sqlalchemy.orm import Session

def create_user_with_hash(db: Session, username: str, email: str | None, hashed_pw: str) -> db_schemas.User:
    """ Create a new user w/ username, email and pre-hashed password --> DB and returns saved User object."""
    user = db_schemas.User(        # ... Create new ORM object = 1 row in users table 
        username=username,
        email=email,
        hashed_password=hashed_pw,
    )
    db.add(user)                   # Queue row for writing into DB
    db.commit()                    # Write new row into DB (only 1 write lock allowed at a time for SQLite)
                                   # ... This is handled by SQlite engine internally no need for code
    db.refresh(user)               # Python object doesn't yet know DB added info (like ID idx) until refresh
    return user                    # Return the User object to have your way with it however you please.

def get_user_by_username(db: Session, username: str) -> db_schemas.User | None:
    """Look up user by username and return User object or None."""
    return db.query(db_schemas.User).filter(db_schemas.User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> db_schemas.User | None:
    """Look up user by ID and return User object or None."""
    return db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()

def list_all_users(db: Session) -> list[db_schemas.User]:
    """Return a list of all users in the database."""
    return db.query(db_schemas.User).all()

def update_user(db: Session, user_id: int, payload: db_val.UserUpdate) -> db_schemas.User | None:
    """Update user info based on fields provided in UserUpdate payload and return User object or None."""
    user = db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()
    if not user:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user by ID and returns True (successful deletion) or False."""
    user = db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True