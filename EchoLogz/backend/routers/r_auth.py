"""
----------------------------------------------------
MODULE: EchoLogz Auth Router (r_auth.py)
----------------------------------------------------

Responsibilities:
Handles all authentication endpoints for the EchoLogz backend. 
Provides login, token generation, and user verification using a database-backed 
(persistent data, not temporary) user store. 
Uses JWT for stateless authentication (no server-side session storage). 
All request/response schemas come from backend.echoDB.db_schemas.
All database access is handled through SQLAlchemy sessions and CRUD utilities.

NOTE: This module handles *EchoLogz user authentication only*. 
Spotify authentication (OAuth2 authorization flow, access tokens, refresh tokens)
is implemented separately in r_spot_auth.py.

INTRO FUNCTIONS: 
- POST /auth/signup
- POST /auth/login
- GET  /auth/me
────────────────────────────────────────────
Modules using r_auth.py:
- main.py (only)
────────────────────────────────────────────

INTERNAL IMPORTS
----------------
    # core.config.settings:     JWT_SECRET
    # core.dependencies.get_db: Supplies SQAlchemy DB Session to each endpoint
    # echoDB.db_schemas:     Pydantic input / output schemas/models used by this auth router (r_auth). 
        - UserCreate 
        - UserOut 
        - TokenOut
    # echoDB.db_crud:           DB interaction functions.

EXTERNAL IMPORTS (parts have been moved to security.py)
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
    # OAuth2PasswordRequestForm: - parses email/password form data for login

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
────────────────────────────────────────────
"""

# INTERNAL MODULES:
from backend.core.dependencies import get_db
from backend.echoDB.db_schemas import UserCreate, UserOut, TokenOut
from backend.echoDB import db_crud
from backend.core import security

# EXTERNAL MODULES: 
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth", tags=["auth"])                 
# logically groups all auth - routers defined below w/ @router, adding '/auth' to each endpoint (ex: /auth/signup)

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
        - validates request body, check email exists, hashes pw, inserts user -> DB
        Returns: user info sans pw (UserOut shaped)
    """
    if db_crud.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="email is taken")
    hashed = security._hash_password(payload.password)
    user = db_crud.create_user_with_hash(
        db=db,
        email=payload.email,
        hashed_pw=hashed,
    )
    return UserOut.model_validate(user)

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates a user and returns an access token.
    - validates email + password against DB, raises 401 for bad credentials, generates a JWT access token (sub = email)
    Returns: token shaped as TokenOut.
    """
    user = db_crud.get_user_by_email(db, form.email)
    # No user account found --> 404
    if not user:
        raise HTTPException(
            status_code=404,
            detail="No account found for this email. Please sign up."
        )
    # Correct email / wrong password --> 401
    if not security._verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect password.")
    # Correct Credentials, but email has not been verified --> 403
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Still need to verify your email before logging in."
        )
    # Everything is correct --> JWT granted
    token = security._create_access_token(sub=user.email)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current: UserOut = Depends(security.get_current_user)):
    """Returns the currently authenticated user.
    - extracts user from JWT via get_current_user() <- ensures token is valid + user exists
    Returns: user data shaped as UserOut.
    """
    return current