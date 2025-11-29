
"""
----------------------------------------------------------------
MODULE: Fast API Helpers / Depends(...) Functions (security.py)
----------------------------------------------------------------

Central security module for the EchoLogz backend.

Responsibilities:
    - Hash and verify passwords (using bcrypt)
    - Create and decode JWT access tokens (using HS256)
    - Provide FastAPI auth dependencies such as get_current_user(): verifies token and returns authenticated user
    - Configure OAuth2PasswordBearer to extract Bearer tokens

What this module does NOT do:
    - No API routes (handled in r_auth.py)
    - No database session management
    - No Spotify OAuth or token refreshing

NOTES:
    - Tokens include a subject ("sub") and expiration time
    - Invalid / expired tokens raise 401 with proper headers
__________________________________________________
Modules using security.py:
- r_auth.py
- r_spot_auth.py
__________________________________________________
"""

# INTERNAL MODULES:
from backend.core.config import settings
from backend.core.dependencies import get_db
from backend.echoDB.db_schemas import UserOut
from backend.echoDB import db_crud

# EXTERNAL MODULES: 
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session


# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"                                               # HS256 = JWT signing/verification algorithm
ACCESS_TOKEN_EXPIRE_MIN = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt = password hashing algorithm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")      # extracts Bearer JWT token from Authorization header




# ------------------------------------------------------------------
# Security Helpers: only used w/ FastAPI functions
# ------------------------------------------------------------------
def _hash_password(plain: str) -> str:
    """FOR new user accounts: Hash a plaintext password using the application's password context."""
    print("DEBUG: password received by hash_password:", repr(plain), "length:", len(plain))
    return pwd_context.hash(plain)

def _verify_password(plain: str, hashed: str) -> bool:
    """FOR login authentication: Validate a plaintext password against its stored hashed version."""
    return pwd_context.verify(plain, hashed)

def _create_access_token(sub: str, minutes: int | None = None, extra_claims: dict | None = None) -> str:
    """Create a signed JWT access token.
    Parameters:
        sub:      The subject identifier (ex: id / email).
        minutes:  Optional custom expiration window. If omitted, uses the
                  default ACCESS_TOKEN_EXPIRE_MIN value.
    Returns: A signed JWT string containing the subject and expiration timestamp.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=minutes or ACCESS_TOKEN_EXPIRE_MIN
    )
    payload = {"sub": sub, "exp": expire}
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _decode_subject(token: str) -> str:
    """Decode a JWT access token and return the subject ("sub") field.
    Raises: 
        JWTError:  If the token is invalid, expired, or missing the subject.
    Returns: The subject identifier value as a string (typically user ID or email).
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload.get("sub")
    if not sub:
        raise JWTError("missing sub")
    return str(sub)

# ------------------------------------------------------
# Security Dependencies - FastAPI Depends(...) Functions
# ------------------------------------------------------

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
    """Validates incoming request belongs to authenticated user — then provides that user's data to the route."""
    try:
        email = _decode_subject(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)

# -------------------------------------------------
# Token Builders
# -------------------------------------------------

# def create_email_verify_token(email: str) -> str:
#     return _create_access_token(
#         sub=email,
#         minutes=15,  # expires in 15 min
#         extra_claims={"purpose": "email_verify"},
#     )

def create_email_verify_token(email: str) -> tuple[str, int]:
    """
    Returns (token, expires_at_timestamp)
    """
    expires_in_minutes = 15

    # Build token using your existing helper
    token = _create_access_token(
        sub=email,
        minutes=expires_in_minutes,
        extra_claims={"purpose": "email_verify"},
    )
    return token, expires_in_minutes


def decode_email_verify_token(token: str) -> str:
    """
    Decode an email verification token.
    Returns the email (sub) if valid, otherwise raises JWTError.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    if payload.get("purpose") != "email_verify":
        raise JWTError("invalid purpose")

    sub = payload.get("sub")
    if not sub:
        raise JWTError("missing sub")

    return str(sub)

