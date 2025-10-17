"""
EchoLogz Auth Router (DB-backed)

- POST /auth/signup
- POST /auth/login
- GET  /auth/me
Uses JWT for stateless auth. I/O models live in echoDB.db_validation.
"""

from datetime import datetime, timedelta, timezone
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, \
    OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.dependencies import get_db
from echoDB.db_validation import UserCreate, UserOut, TokenOut
from echoDB import db_crud

router = APIRouter(prefix="/auth", tags=["auth"])

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def _hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def _create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=minutes or ACCESS_TOKEN_EXPIRE_MIN
    )
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _decode_subject(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload.get("sub")
    if not sub:
        raise JWTError("missing sub")
    return str(sub)

# ------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserOut:
    try:
        username = _decode_subject(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db_crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@router.post("/signup", response_model=UserOut, status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if db_crud.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed = _hash_password(payload.password)
    user = db_crud.create_user_with_hash(
        db=db,
        username=payload.username,
        email=getattr(payload, "email", None),
        hashed_pw=hashed,
    )
    return UserOut.model_validate(user)

@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db_crud.get_user_by_username(db, form.username)
    if not user or not _verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad credentials")
    token = _create_access_token(sub=user.username)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current: UserOut = Depends(get_current_user)):
    return current