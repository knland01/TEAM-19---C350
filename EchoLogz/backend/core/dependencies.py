
"""
----------------------------------------------------
MODULE: FastAPI Dependencies (core.dependencies.py)
----------------------------------------------------
More suitable name (IMO): "Dependsies.py" -- but dependencies.py is FastAPI convention blah blah 

This module contains FastAPI *dependency functions*—functions intended to be
used with -- Depends(...) -- inside route handlers. FastAPI automatically calls
these functions during the request/response lifecycle and manages any cleanup after 
the route completes (ex: code after a 'yield'). 

NOTE: Shared, reusable dependency functions belong here. Dependency functions that
are specific to a single router (such as auth-related dependencies) should
live in that router's own module instead.

NOTE: These are not “dependencies” in the normal Python import sense. 
Instead, they are DI providers that FastAPI injects into routes. 
EXAMPLE: get_db() - creates a per-request database session and closes it once the route finishes.

NOTE: Only functions meant to be passed to 'Depends(...)' should live here.
__________________________________________________
Modules using dependencies.py
- r_auth.py
- r_match.py
- r_spot_auth.py
- r_users.py
__________________________________________________
"""
from backend.core.config import settings
from backend.echoDB.db_session import SessionLocal

from fastapi import Depends, HTTPException, Header, status
from jose import jwt, JWTError

JWT_ALGORITHM = "HS256"

# ----------------------------------------------
# Dependencies - FastAPI Depends(...) Functions
# ----------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db   # <-- FastAPI pauses here and runs your route
    finally:
        db.close() # <-- FastAPI runs this after the route returns/ends


# def get_current_user_id(authorization: str = Header(None)) -> int:
#     """
#     Extract the JWT from the Authorization header and return the user_id
#     stored inside the token payload.

#     Expects header:  Authorization: Bearer token
#     """
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authorization header format",
#         )
#     token = authorization.split(" ", 1)[1]
#     try:
#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET,
#             algorithms=[JWT_ALGORITHM],
#         )
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#         )
#     user_id = payload.get("user_id")
#     if user_id is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token missing user_id",
#         )
#     return int(user_id)

def get_current_user_id(authorization: str = Header(None)) -> int:
    """
    TEMP DEV VERSION:
    Do NOT validate JWT. Just return a fixed user id (1).

    This is only to keep endpoints working for the demo
    without dealing with JWT wiring. Replace with a real
    decoder later.
    """
    return 1