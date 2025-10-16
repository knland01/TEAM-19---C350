"""
Main Application Entry Point

This module initializes and runs the EchoLogz FastAPI backend.
It handles the following core responsibilities:

- Creates the FastAPI app instance with the project title.
- Imports and initializes the database and ORM models.
- Automatically creates database tables (if they don't already exist).
- Defines basic API routes (starting with a simple root health check).

Files Connected:
- models.py     → Defines SQLAlchemy models (database structure)
- database.py   → Sets up database engine, session, and Base class

Run with:
    uvicorn main:app --reload

Access the running server at:
    http://127.0.0.1:8000/
"""


from fastapi import FastAPI
from .echoDB import models, crud, database, schemas



# Create the FastAPI app instance
app = FastAPI(title="EchoLogz API")

models.Base.metadata.create_all(bind=database.engine)


# Define a test route
@app.get("/")
def read_root():
    return {"message": "EchoLogz backend is running!"}