"""
Data Validation Module (also called "schemas", "models", "classes") <-- ugh

This module defines Pydantic models (schemas) used by FastAPI to validate, 
serialize, and deserialize data flowing between the API and the database.

Responsibilities:
- Validate incoming request data (ex: JSON from client = expected types/constraints).
- Shape and sanitize outgoing response data before sending it back to the client.
- Ensure type safety and structure consistency across API endpoints.
- Keep a clear separation between internal database models/schemas (in db_schemas.py) 
  and external API-facing representations.

Files Connected:
- db_schemas.py → Database table definitions (internal structure).
- db_crud.py   → Uses schemas to validate input/output during DB operations.
- main.py   → References schemas for API request and response models.

Typical Entry Examples:

    class UserBase(BaseModel):
        name: str
        email: str

    class UserCreate(UserBase):
        password: str

    class UserResponse(UserBase):
        id: int
        class Config:
            orm_mode = True  # Enables reading SQLAlchemy objects directly

"""

from pydantic import BaseModel