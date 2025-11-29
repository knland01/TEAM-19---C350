"""
Main Application Entry Point

This module initializes and runs the EchoLogz FastAPI backend.
It handles the following core responsibilities:

- Creates the FastAPI app instance with the project title.
- Imports and initializes the database and ORM models.
- Automatically creates database tables (if they don't already exist).
- Defines basic API routes (starting with a simple root health check).

NOTE: CORSMiddleware 
# ... CORS: Allows communication btwn diff ports (frontend -> backend) - which is only issue during dev
# ... FRONT-END (DEV): 127.0.0.1:5500 --> BACK-END (DEV): 127.0.0.1:8000
# ... FRONT-END (DEPLOY): https://echologz(or whatever).com --> BACK-END (DEPLOY): https://echologz(or whatever)/api.com



 >>>> ACCESS HELP
-----------------------------------------------------------------------------------------------------------------------
BACKEND:
    Run with Terminal Command:
                (Navigate to: EchoLogz/)
                uvicorn backend.main:app --reload

    Access the running server at: 
                http://127.0.0.1:8000/
                http://127.0.0.1:8000/docs <-- Swagger UI (FastAPI Interactive - API Documentation)
-----------------------------------------------------------------------------------------------------------------------
FRONTEND: 
    Run with Terminal Command:
                pnpm run dev
    Access the running server at: 
                http://localhost:5173
-----------------------------------------------------------------------------------------------------------------------
"""

# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../.."))

# INTERNAL IMPORTS:
from backend.echoDB import db_session, db_tables
from backend.echoDB.db_health import assert_schema_matches
from backend.routers import r_auth, r_spot_auth, r_match, r_users
# from backend.core.config import settings # Load (.env) variables via config.py

# EXTERNAL IMPORTS
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from starlette.staticfiles import StaticFiles
#----------------------------------------------------------------------------------------------

# CREATE ALL DB TABLES IF THEY DON'T ALREADY EXIST IN: backend/data/echologz.db
@asynccontextmanager
async def lifespan(app: FastAPI): # Runs when the app starts
    print("LIFESPAN START: creating tables")
    print("Tables in metadata:", db_tables.Base.metadata.tables.keys())
    db_tables.Base.metadata.create_all(bind=db_session.engine)
    assert_schema_matches() # Run schema check
    yield # Runs when the app stops (if you need cleanup)


app = FastAPI(title="EchoLogz API", lifespan=lifespan)
# app.mount("/static", StaticFiles(directory="static"), name="static") 
# Static file serving disabled (KL): No static assets needed—React frontend runs separately.

# CORS CONFIG:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ # ALLOW FRONT-END ---> HTTP REQUESTS ---> BACK-END: 127.0.0.1:8000
        "http://127.0.0.1:5500", "http://localhost:5500",
        "http://127.0.0.1:3000", "http://localhost:3000",
        "http://127.0.0.1:5173", "http://localhost:5173", # Vite assumes 5173
        "https://echoquest.app"  # production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],  # or ["GET", "POST"] if you want to limit
    allow_headers=["*"],  # or ["Authorization", "Content-Type"]
)

# ROUTERS:
app.include_router(r_auth.router)
app.include_router(r_spot_auth.router)
app.include_router(r_users.router)
app.include_router(r_match.router)
# app.include_router(r_status.router)

# TEST ROUTE:
@app.get("/")
def read_root():
    return {"message": "EchoLogz backend is running!"}


# ----------- CODE GRAVEYARD -----------
# Ensure tables exist when the app starts
# @app.on_event("startup") # deprecated ---> lifespan syntax (see below)
# def on_startup():
#     models.Base.metadata.create_all(bind=database.engine)
    