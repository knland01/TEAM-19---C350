"""
Database ORM Models: DB Blueprint - ORM table models

SQAlchemy ORM models (Object-Relational Mapping models) are Python classes that represent tables in a relational database. Each class corresponds to one table, and each class attribute corresponds to a database column. The ORM automatically translates between Python objects and SQL queries, so you can work with database rows using normal Python code instead of writing raw SQL statements. 

ORM models are *pythonic schemas* that are also mapped directly to actual database tables — meaning they act as both the blueprint and the concrete table representation at once.

This module defines the database schema for EchoLogz using SQLAlchemy ORM. 
Each model/class represents a table in the database and maps Python objects 
to relational database records.

Responsibilities:
- Defines table structures and their columns (schemas).
- Maps Python classes to relational database tables using SQLAlchemy ORM.
- Establishes relationships (foreign keys, joins) between tables.
- Inherits from Base (provided by db_session.py) to register models with SQLAlchemy.

Connected Modules:
- db_session.py     -> Provides the SQLAlchemy Base class used for model inheritance.
- db_crud.py        -> Uses these SQAlchemy ORM models to perform database operations.
- db_validation.py  -> Defines Pydantic models (partially/fully mirrors Orm Models) used for API request/response validation.

Example of use (inside db_crud.py):
    def get_user_by_id(db, user_id: int):
        return db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()


        
NOTE: Spotify Developer Terms = “Except as otherwise set out in these Developer Terms, you may not store, aggregate or create compilations or databases of Spotify Content, other than as strictly necessary to operate your SDA.”
WORK AROUND: Store Track IDs + URIs (this is ok)
        
"""


from sqlalchemy import Column, Integer, String
from .db_session import Base
# from . import db_crud, db_session, schema


# Typical Entry Example (SQAlchemy ORM Model --> DB SCHEMA):
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# TRANSLATES TO:
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     username VARCHAR NOT NULL UNIQUE,
#     email VARCHAR NOT NULL UNIQUE,
#     hashed_password VARCHAR NOT NULL
# );