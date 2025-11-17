"""
MODULE: EchoLogz Auth Router (r_auth.py)

Responsibilities:
Handles all authentication endpoints for the EchoLogz backend. 
Provides login, token generation, and user verification using a database-backed (persistent data, not temporary) user store. 
Uses JWT for stateless authentication (no server-side session storage). 
All request/response schemas come from backend.echoDB.db_validation.
All database access is handled through SQLAlchemy sessions and CRUD utilities.

NOTE: This module handles *EchoLogz user authentication only*. 
Spotify authentication (OAuth2 authorization flow, access tokens, refresh tokens)
is implemented separately in r_spot_auth.py.

INTRO FUNCTIONS: 
- POST /auth/signup
- POST /auth/login
- GET  /auth/me

Modules importing r_auth.py:
- main.py

INTERNAL IMPORTS
----------------
    # core.config.settings:     JWT_SECRET
    # core.dependencies.get_db: Supplies SQAlchemy DB Session to each endpoint
    # echoDB.db_validation:     Pydantic input / output schemas/models used by this auth router (r_auth). 
        - UserCreate 
        - UserOut 
        - TokenOut
    # echoDB.db_crud:           DB interaction functions.

EXTERNAL IMPORTS
----------------
    -- [DATETIME]:   BASIC PYTHON TIME HELPERS
    # datetime:      - stamp tokens with current time
    # timedelta:     - add expiration duration to JWT validity (ex: now + 60 mins)
    # timezone:      - attach timezone (UTC) to timestamp for consistency

    -- [FASTAPI]:    BUILDING API STRUCTURE / ROUTES (AND ALL THAT GOES WITH IT)
    # APIRouter:     - group all auth routes --> logical module for FastAPI app (doesn't know abt physical module)
    # Depends:       - FastAPI function depends on result of Depends(x_function).
    # HTTPException: - raises proper HTTP errors with status codes (for error responses)
    # status:        - readable HTTP status codes

    NOTE: FastAPI is a wrapper for python functions that turns them into HTTP endpoints callable from the front-end
    
    -- [FASTAPI.SECURITY]:       FASTAPI SECURITY HELPER UTILITIES for LOGIN / AUTH STUFF
    # OAuth2PasswordBearer:      - extracts bearer token from Authorization header of requests 
    # OAuth2PasswordRequestForm: - parses username/password form data for login

    NOTE: A "bearer token" is any token where possession alone grants access (it's not a specific format).

    -- [PYTHON-JOSE]: CRYPTO ENGINE: ENCODING / VERIFYING JWT TOKENS (imported as 'jose')
    # jwt:            - (J_SON W_eb T_oken) encodes and decodes JWT tokens (sign + verify)
    # JWTError:       - thrown when token verification invalid/malformed/expired
    # HS256:          - JWT signing algorithm (HMAC-SHA256 hashing)

    NOTE: HS256 is symmetric - sign token <--[Same SECRET_KEY]--> verify token - Never expose to frontend / github.
    NOTE: A JWT (JSON Web Token) is a specific type of "bearer token" that carries encoded JSON data inside it.
    NOTE: JWT = stateless auth, meaning the server doesn't record user session data. Client/Token holds credentials to authenticate per request = no server-side memory required.

    -- [PASSLIB.CONTEXT]: PASSWORD HASHING 
    # CryptContext:       - password hashing + verifying login attempts

    -- [SQALCHEMY.ORM]: DATABASE SESSION CONTROLLER
    # Session:          - creates the per-request DB session used for all reads/writes inside auth endpoints

"""

# EXTERNAL MODULES: 
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# INTERNAL MODULES:
from backend.core.config import settings
from backend.core.dependencies import get_db
from backend.echoDB.db_validation import UserCreate, UserOut, TokenOut
from backend.echoDB import db_crud


router = APIRouter(prefix="/auth", tags=["auth"])                 
# logically groups all auth - routers defined below w/ @router, adding '/auth' to each endpoint (ex: /auth/signup)

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"                                               # HS256 = JWT signing/verification algorithm
ACCESS_TOKEN_EXPIRE_MIN = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt = password hashing algorithm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")      # extracts Bearer JWT token from Authorization header

# ------------------------------------------------------------------
# Helpers: only used w/ r_auth FastAPI functions - so code included here
# ------------------------------------------------------------------
def _hash_password(plain: str) -> str:
    """FOR new user accounts: Hash a plaintext password using the application's password context."""
    return pwd_context.hash(plain)

def _verify_password(plain: str, hashed: str) -> bool:
    """FOR login authentication: Validate a plaintext password against its stored hashed version."""
    return pwd_context.verify(plain, hashed)

def _create_access_token(sub: str, minutes: int | None = None) -> str:
    """Create a signed JWT access token.
    Parameters:
        sub:      The subject identifier (typically user ID or username).
        minutes:  Optional custom expiration window. If omitted, uses the
                  default ACCESS_TOKEN_EXPIRE_MIN value.
    Returns: A signed JWT string containing the subject and expiration timestamp.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=minutes or ACCESS_TOKEN_EXPIRE_MIN
    )
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _decode_subject(token: str) -> str:
    """Decode a JWT access token and return the subject ("sub") field.
    Raises: 
        JWTError:  If the token is invalid, expired, or missing the subject.
    Returns: The subject identifier value as a string (typically user ID or username).
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload.get("sub")
    if not sub:
        raise JWTError("missing sub")
    return str(sub)

# ------------------------------------------------------------------
# Dependencies - FastAPI Depends Functions specific only to r_auth.py
# ------------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
    """Validates incoming request belongs to authenticated user — then provides that user’s data to the route."""
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
# .POST - HTTP endpoint that accepts POST requests: client sending data to server to create / process something.
# .GET:    "Give me data."
# .PUT:    "Replace existing thing with new thing."
# .PATCH:  "Update the part of existing thing."
# .DELETE: "Remove this thing."

@router.post("/signup", response_model=UserOut, status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    """Creates a new user account.
        - validates request body, check username exists, hashes pw, inserts user -> DB
        Returns: user info sans pw (UserOut shaped)
    """
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
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates a user and returns an access token.
    - validates username + password against DB, raises 401 for bad credentials, generates a JWT access token (sub = username)
    Returns: token shaped as TokenOut.
    """
    user = db_crud.get_user_by_username(db, form.username)
    if not user or not _verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad credentials")
    token = _create_access_token(sub=user.username)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current: UserOut = Depends(get_current_user)):
    """Returns the currently authenticated user.
    - extracts user from JWT via get_current_user() <- ensures token is valid + user exists
    Returns: user data shaped as UserOut.
    """
    return current