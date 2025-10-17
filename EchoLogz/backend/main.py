"""
Main Application Entry Point

This module initializes and runs the EchoLogz FastAPI backend.
It handles the following core responsibilities:

- Creates the FastAPI app instance with the project title.
- Imports and initializes the database and ORM models.
- Automatically creates database tables (if they don't already exist).
- Defines basic API routes (starting with a simple root health check).

Files Connected:
- db_schemas.py     → Defines SQLAlchemy models (database structure)
- db_session.py   → Sets up database engine, session, and Base class

Run with:
    uvicorn main:app --reload

Access the running server at:
    http://127.0.0.1:8000/ (or) http://localhost:8000/
"""


from fastapi import FastAPI
from EchoLogz.backend.echoDB import db_schemas
from backend.core.config import settings # Load (.env) variables via config.py
from EchoLogz.backend.echoDB import db_session # SQLAlchemy Base/engine
from backend.routers import auth, spotify_auth, health, users
from contextlib import asynccontextmanager

# Create the FastAPI app instance
app = FastAPI(title="EchoLogz API")

# Routers
app.include_router(auth.router)
app.include_router(spotify_auth.router)
app.include_router(health.router)
app.include_router(users.router)

# Ensure tables exist when the app starts
# @app.on_event("startup") # deprecated ---> lifespan syntax (see below)
# def on_startup():
#     models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs when the app starts
    db_schemas.Base.metadata.create_all(bind=db_session.engine)
    yield
    # Runs when the app stops (if you need cleanup)

app = FastAPI(title="EchoLogz API", lifespan=lifespan)


# Define a test route
@app.get("/")
def read_root():
    return {"message": "EchoLogz backend is running!"}