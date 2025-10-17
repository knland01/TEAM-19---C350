
from fastapi import Depends,  HTTPException, status
from echoDB.db_session import SessionLocal
from EchoLogz.backend.routers.r_auth import decode_jwt  # or wherever = auth utils
# from typing import Generator

def get_db():
    db = SessionLocal()
    try:
        yield db   # <-- route executes while the session is ‘open’
    finally:
        db.close() # <-- FastAPI runs this after the route returns/raises

def get_current_user(token: str = Depends(...)):
    user = decode_jwt(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user