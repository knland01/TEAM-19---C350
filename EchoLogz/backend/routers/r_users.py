"""
User Router

Defines the API routes under "/users" for EchoLogz app users.

What this module DOES:
- Declare HTTP endpoints (list, create, read, update, delete).
- Delegate DB work to echoDB.db_crud.
- Validate I/O with echoDB.db_validation Pydantic models.
- Use dependency injection to get a DB session.

What this module DOES NOT do:
- No raw SQL or ORM session management (see echoDB.db_session).
- No table/model definitions (see echoDB.db_schemas).
- No Spotify OAuth or API calls (see routers/spotify_auth.py and
  services/spotify_calls.py).
- No business rules beyond simple request → service delegation.

Outcome:
- Thin routing layer that converts HTTP requests into db_crud calls and
  returns clean JSON responses.
"""


# EXAMPLE:
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

# from echoDB.db_session import get_db <--- removed
from core.dependencies import get_db
from echoDB import db_crud as crud
from echoDB import db_validation as val

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=val.UserOut,
             status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: val.UserCreate, db: Session = Depends(get_db)):
    """Create a new user and return the created record."""
    return crud.create_user(db, payload)

@router.get("/{user_id}", response_model=val.UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Return a single user by id, or 404 if not found."""
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=list[val.UserOut])
def list_users_endpoint(db: Session = Depends(get_db)):
    return crud.list_users(db)

@router.put("/{user_id}", response_model=val.UserOut)
def update_user_endpoint(
    user_id: int, 
    payload: val.UserUpdate,
    db: Session = Depends(get_db),
):
    """ Replace an existing user with the provided fields.
    (All fields in UserUpdate are optional; absent fields are not changed.) """
    user = crud.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Delete a user; returns 204 if successful, 404 if not found."""
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Explicitly return an empty body with 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)