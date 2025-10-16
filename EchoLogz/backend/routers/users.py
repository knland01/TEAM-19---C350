"""
User Router

This module defines the API endpoints (routes) for all user-related operations
within the EchoLogz backend. It handles user registration, authentication,
profile retrieval, and other user data management tasks.

Core Responsibilities:
- Define and organize HTTP routes under the "/users" prefix
- Connect incoming requests to CRUD operations from echoDB.crud
- Handle input/output validation using echoDB.schemas
- Interface with authentication logic (auth.py) for secure endpoints
- Return JSON responses for all user actions

Purpose:
Serves as the communication bridge between frontend requests and the
database logic related to users — encapsulating how the app manages
user data and interactions through FastAPI routing.

Typical Usage Example:
    from fastapi import APIRouter, Depends
    from echoDB import crud, schemas
    from backend.routers.users import router

    @router.get("/users/{user_id}", response_model=schemas.User)
    def get_user(user_id: int, db: Session = Depends(get_db)):
        return crud.get_user_by_id(db, user_id)

"""