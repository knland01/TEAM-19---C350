"""
CRUD Operations Module

This module defines the Create, Read, Update, and Delete (CRUD) operations 
for interacting with the EchoLogz database via SQLAlchemy ORM. 

Responsibilities:
- Data-access layer between API routers and DB.
- Contains reusable functions that handle database logic (insert, query, update, delete).
- Keeps the main API routers clean and focused only on HTTP logic + request handling.

Connected Modules/files (directly):
- db_schemas.py       -> Defines database tables and relationships.
- db_validation.py    -> Defines Pydantic models for request/response validation.
- database            -> SQLAlchemy-managed database connection (configured in db_session.py)

Connected Modules (indirectly)
- db_session.py       -> Provides SessionLocal used by routers, not directly used here.

Typical Usage (from a router or service layer):
    from backend.echoDB import db_crud
    from backend.core.dependencies import get_db

    def route_handler(db: Session = Depends(get_db)):
        user = db_crud.get_user_by_id(db, user_id=1)
        return user
"""

from backend.echoDB import db_schemas, db_validation as db_val
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