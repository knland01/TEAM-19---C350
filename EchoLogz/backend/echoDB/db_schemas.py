"""
Database Models (Schemas): DB Blueprint - ORM table models

This module defines the database schema for EchoLogz using SQLAlchemy ORM. 
Each model/class represents a table in the database and maps Python objects 
to relational database records.

Responsibilities:
- Defines table structures and their columns.
- Maps Python classes to database tables.
- Establishes relationships (foreign keys, joins) between tables.
- Provides a base class for all models via the imported Base.

Files Connected:
- db_session.py → Supplies the Base class and engine connection.
- db_crud.py     → Uses these models to perform database operations.
- db_validation.py  → Mirrors model structure for data validation and serialization.

Example of use (inside db_crud.py):
    def get_user_by_id(db, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

"""


from sqlalchemy import Column, Integer, String
from .db_session import Base
from . import db_crud, db_session, schema


# Typical Entry Example:
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)