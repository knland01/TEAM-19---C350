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

Run with Terminal Command:
            uvicorn main:app --reload

Access the running server at: 
            http://127.0.0.1:8000/

"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
# ... CORS: Allows communication btwn diff ports (frontend -> backend) - which is only issue during dev
# ... FRONT-END (DEV): 127.0.0.1:5500 --> BACK-END (DEV): 127.0.0.1:8000
# ... FRONT-END (DEPLOY): https://echologz(or whatever).com --> BACK-END (DEPLOY): https://echologz(or whatever)/api.com
from EchoLogz.backend.routers import r_auth, r_spot_auth, r_status, r_match
from echoDB import db_schemas, db_session
from core.config import settings # Load (.env) variables via config.py
from EchoLogz.backend.routers import r_users
from contextlib import asynccontextmanager

# Create the FastAPI app instance
app = FastAPI(title="EchoLogz API")

# CORS CONFIG:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ # ALLOW FRONT-END ---> HTTP REQUESTS ---> BACK-END: 127.0.0.1:8000
        "http://127.0.0.1:5500", "http://localhost:5500",
        "http://127.0.0.1:3000", "http://localhost:3000",
        "https://echoquest.app"  # your production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],  # or ["GET", "POST"] if you want to limit
    allow_headers=["*"],  # or ["Authorization", "Content-Type"]
)


# Routers
app.include_router(r_auth.router)
app.include_router(r_spot_auth.router)
app.include_router(r_status.router)
app.include_router(r_users.router)
app.include_router(r_match.router)

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