"""
CRUD Operations Module

This module defines the Create, Read, Update, and Delete (CRUD) operations 
for interacting with the EchoLogz database via SQLAlchemy ORM. 

Responsibilities:
- Acts as the interface between API routes and the database.
- Contains reusable functions that handle data logic (insert, query, update, delete).
- Keeps the main API routes clean and focused on HTTP logic.

Files Connected:
- models.py     → Defines database tables and relationships.
- schemas.py    → Defines Pydantic models for request/response validation.
- database.py   → Provides the database session (SessionLocal) for queries.

Typical Usage Example (from another module):
    from . import crud, models, database
    db_user = crud.get_user_by_id(db, user_id=1)
"""

from . import models, schemas, database