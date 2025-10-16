"""
Data Schemas Module

This module defines Pydantic models (schemas) used by FastAPI to validate, 
serialize, and deserialize data flowing between the API and the database.

Responsibilities:
- Validate incoming request data (e.g., JSON from the frontend).
- Shape and sanitize outgoing response data before sending it back to the client.
- Ensure type safety and structure consistency across API endpoints.
- Keep a clear separation between internal database models (in models.py) 
  and external API-facing representations.

Files Connected:
- models.py → Database table definitions (internal structure).
- crud.py   → Uses schemas to validate input/output during DB operations.
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