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

from backend.echoDB import db_schemas, db_validation as val
from .db_schemas import User
from backend.echoDB import db_session
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def create_user_with_hash(
    db: Session, username: str, email: str | None, hashed_pw: str
) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_pw,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()

def list_users(db: Session):
    return db.query(db_schemas.User).all()

def update_user(db: Session, user_id: int, payload: val.UserUpdate):
    user = db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()
    if not user:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True