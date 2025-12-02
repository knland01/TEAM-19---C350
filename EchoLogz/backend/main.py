"""
Main Application Entry Point

This module initializes and runs the EchoLogz FastAPI backend.

It handles the following core responsibilities:
- Imports and initializes the database and ORM models.
- Automatically creates database tables (if they don't already exist).
- Creates the FastAPI app instance with the project title.
- Configures CORS middleware for frontend-->backend local server communication during dev.
- Defines basic API routes (starting with a simple root health check).

DEEPDIVE: CORSMiddleware 
# ... CORS: Allows communication btwn diff ports (frontend -> backend) - which is only issue during dev
# ... FRONT-END (DEV): 127.0.0.1:5500 --> BACK-END (DEV): 127.0.0.1:8000
# ... FRONT-END (DEPLOY): https://echologz(or whatever).com --> BACK-END (DEPLOY): https://echologz(or whatever)/api.com



 >>>> ACCESS HELP
-----------------------------------------------------------------------------------------------------------------------
BACKEND: Terminal 1
    Run local server with Terminal Command:
            (Navigate to --> EchoLogz/)
                    uvicorn backend.main:app --reload

    Access the running server at: 
                https://127.0.0.1:8000/
                http://127.0.0.1:8000/docs <-- Swagger UI (FastAPI Interactive - API Documentation)
                http://localhost:8000/docs <-- or this
-----------------------------------------------------------------------------------------------------------------------
FRONTEND: Terminal 2
    Run local server with Terminal Command: 
            (Navigate to --> frontend-react/)
                    pnpm install <-- (first time only)
                    pnpm run dev

    Access the running server at: 
                http://localhost:5173
-----------------------------------------------------------------------------------------------------------------------
"""

# INTERNAL IMPORTS:
from backend.echoDB import db_session, db_tables
from backend.echoDB.db_health import assert_schema_matches
from backend.routers import r_auth, r_spot_auth, r_match, r_users
# from backend.core.config import settings # Load (.env) variables via config.py

# EXTERNAL IMPORTS
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from starlette.staticfiles import StaticFiles
from fastapi import Request
import json
#----------------------------------------------------------------------------------------------





# AUTO-GENERATE: backend/data/echologz.db + TABLES (if they don't already exist)
@asynccontextmanager
async def lifespan(app: FastAPI): # Runs when the app starts
    print("LIFESPAN START: creating tables")
    data_dir = Path("backend/data")
    if not data_dir.exists():
        print("Creating data directory:", data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
    print("Tables in metadata:", db_tables.Base.metadata.tables.keys())
    db_tables.Base.metadata.create_all(bind=db_session.engine)
    assert_schema_matches() # Run schema check
    yield # Runs when the app stops (if you need cleanup)
    print("LIFESPAN END")


    
# INSTANTIATE FASTAPI CLASS:
app = FastAPI(title="EchoLogz API", lifespan=lifespan)
# app.mount("/static", StaticFiles(directory="static"), name="static") 
# ---> Static file serving disabled (KL): No static assets needed—React frontend runs separately.

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
# app.include_router(r_status.router) # <--- currently unused, placeholder if needed

# TEST ROUTE:
@app.get("/")
def read_root():
    return {"message": "EchoLogz backend is running!"}



@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    print("\n===== INCOMING REQUEST =====")
    print("Method:", request.method)
    print("URL:", request.url)
    print("Headers:", dict(request.headers))
    print("Body:", body.decode("utf-8"))
    print("============================\n")
    
    response = await call_next(request)
    return response

# ----------- CODE GRAVEYARD -----------------------------------------------------------------------
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../.."))

# Ensure tables exist when the app starts
# @app.on_event("startup") # deprecated ---> lifespan syntax (see below)
# def on_startup():
#     models.Base.metadata.create_all(bind=database.engine)
    