"""
MODULE: Data Validation - API-facing layer for DB (db_validation.py)

This module defines Pydantic models (schemas) used by FastAPI to validate, 
serialize, and deserialize data flowing between the API and the database.

Responsibilities:
- Validates input from client is correct shape/type (ex: JSON from client = expected types/constraints).
- Shapes data that leaves API (response objects).
- Ensure type safety and structure consistency across API endpoints.
- Keep a clear separation between internal database models/schemas (in db_schemas.py) 
  and external API-facing representations. Prevent raw ORM objects from being exposed to the outside world.

Modules Using db_validation:
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
"""

from pydantic import BaseModel, EmailStr, ConfigDict

# ---------- Inputs ----------
class UserCreate(BaseModel):
    """Validates incoming JSON when the user is being created."""
    username: str
    password: str
    email: EmailStr | None = None # optional value; default=None

class UserUpdate(BaseModel):
    """Validates schema for updating user accounts."""
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None 

# ---------- Outputs ----------
class UserOut(BaseModel):
    """Validates / shapes user DB data API sends back to the client."""
    id: int
    username: str
    email: EmailStr | None = None
    model_config = ConfigDict(from_attributes=True) # ORM objects don't use dicts.
    # pydantic v2 syntax
    # Pydantic model can receive objects with attributes (like SQLAlchemy ORM models) -> read their data 
    # ... using dot-notation instead of expecting a dictionary.

class TokenOut(BaseModel):
    """Validates standard OAuth2 token response format."""
    access_token: str
    token_type: str = "bearer"


