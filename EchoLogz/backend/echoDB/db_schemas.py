"""
---------------------------------------------------------------------
MODULE: DB Schema Validation - API-facing layer for DB (db_schemas.py)
---------------------------------------------------------------------

This module defines PYDANTIC MODELS (schemas) used by FastAPI to validate, 
serialize, and deserialize data flowing between the API and the database.

Responsibilities:
- Validates input from client is correct shape/type (ex: JSON from client = expected types/constraints).
- Shapes data that leaves API (response objects).
- Ensure type safety and structure consistency across API endpoints.
- Keep a clear separation between internal database models/schemas (in db_tables.py) 
  and external API-facing representations. Prevent raw ORM objects from being exposed to the outside world.

────────────────────────────────────────────
Modules Using db_schemas:
- r_auth.py
- r_users.py

EXTERNAL IMPORTS (dependencies):
    -- [PYDANTIC] --
    # BaseModel: Every Pydantic model must extend BaseModel to become a “validator class".
                - Type Val, Auto-converts types 
                - Blocks invalid data, creates .dict(), .json(), .model_validate() methods
                - Drives FastAPI's request/response validation layer
    # EmailStr: Pydantic type for validating email address formats - throws FastAPI 422 error.
    # ConfigDict: 

INTERNAL IMPORTS (dependencies): 
    - None
────────────────────────────────────────────
"""

# EXTERNAL IMPORTS:
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Inputs ----------------------------------------------------------------------------------------
class UserCreate(BaseModel):
    """Validates incoming JSON when the user is being created."""
    email: EmailStr
    password: str
    # username: str | None = None

class UserUpdate(BaseModel):
    """Validates schema for updating user accounts."""
    email: EmailStr | None = None 
    password: str | None = None
    # username: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ---------- Outputs ----------------------------------------------------------------------------------------

class UserOut(BaseModel):
    """Validates / shapes user DB data API sends back to the client."""
    id: int
    email: EmailStr
    is_verified: bool
    # username: str
    model_config = ConfigDict(from_attributes=True) # ORM objects don't use dicts.
    # pydantic v2 syntax
    # Pydantic model can receive objects with attributes (like SQLAlchemy ORM models) -> read their data 
    # ... using dot-notation instead of expecting a dictionary.

class SignupOut(BaseModel):
    user: UserOut
    verify_token: str
    verify_expires_in: int

class TokenOut(BaseModel):
    """Validates standard OAuth2 token response format."""
    access_token: str
    token_type: str = "bearer"

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# --------- SPOTIFY ----------------------------------------------------------------------------------------
class SpotifyAccountBase(BaseModel):
    spotify_user_id: str
    scope: str | None = None


class SpotifyAccountCreate(SpotifyAccountBase):
    access_token: str
    refresh_token: str
    expires_at: datetime


class SpotifyAccountRead(SpotifyAccountBase):
    id: int
    user_id: int
    expires_at: datetime
    last_synced_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }

class SpotifyAccountUpdate(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    expires_at: datetime | None = None
    scope: str | None = None
    last_synced_at: datetime | None = None