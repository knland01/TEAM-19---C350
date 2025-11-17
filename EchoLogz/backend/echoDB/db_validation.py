"""
Data Validation Module (API-facing layer for DB)

This module defines Pydantic models (schemas) used by FastAPI to validate, 
serialize, and deserialize data flowing between the API and the database.

Responsibilities:
- Validates input from client is correct shape/type (ex: JSON from client = expected types/constraints).
- Shapes data that leaves API (response objects).
- Ensure type safety and structure consistency across API endpoints.
- Keep a clear separation between internal database models/schemas (in db_schemas.py) 
  and external API-facing representations. Prevent raw ORM objects from being exposed to the outside world.

Files Connected:
- db_schemas.py → Database table definitions (internal structure).
- db_crud.py   → Uses schemas to validate input/output during DB operations.
- main.py   → References schemas for API request and response models.

"""

from pydantic import BaseModel, EmailStr, ConfigDict
# BaseModel: Every Pydantic model must extend BaseModel to become a “validator class".
# ...  ... Type Val, Auto-converts types 
# ...  ... Blocks invalid data, creates .dict(), .json(), .model_validate() methods
# ...  ... Drives FastAPI's request/response validation layer

# EmailStr: Pydantic type for validating email address formats - throws FastAPI 422 error.



# ---------- Inputs ----------
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None # optional value; default=None

# ---------- Outputs ----------
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    model_config = ConfigDict(from_attributes=True) # <-- pydantic v2 syntax
    # Pydantic model can receive objects with attributes (like SQLAlchemy ORM models) -> read their data 
    # ... using dot-notation instead of expecting a dictionary.

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None 
