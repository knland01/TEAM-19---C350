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
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from echoDB.db_session import get_db
from echoDB import db_crud as crud
from echoDB import db_validation as v

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=v.UserRead,
             status_code=status.HTTP_201_CREATED)
def create_user(payload: v.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)

@router.get("/{user_id}", response_model=v.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[v.UserRead])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@router.put("/{user_id}", response_model=v.UserRead)
def update_user(user_id: int, payload: v.UserUpdate,
                db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
