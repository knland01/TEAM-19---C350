"""
EchoLogz Auth Router

- /auth/signup
- /auth/login
- /auth/me (protected)
Uses JWT for stateless auth.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
import os


# -------------------------------------------------------------------
# AUTH.PY DEMO... 
# -------------------------------------------------------------------
# Minimal in-memory demo store — replace with real DB via echoDB.crud
_FAKE_USERS = {}  # {username: {"username":..., "hashed_password":...}}

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(plain):
    return pwd_context.hash(plain)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None or username not in _FAKE_USERS:
            raise credentials_error
    except JWTError:
        raise credentials_error
    return User(username=username)

@router.post("/signup", status_code=201)
def signup(user: UserCreate):
    if user.username in _FAKE_USERS:
        raise HTTPException(status_code=400, detail="Username already exists")
    _FAKE_USERS[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password),
    }
    return {"message": "User created"}

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    record = _FAKE_USERS.get(form.username)
    if not record or not verify_password(form.password, record["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user