
"""
----------------------------------------------------
MODULE: FastAPI Dependencies (core.dependencies.py)
----------------------------------------------------

This module contains FastAPI *dependency functions*—functions intended to be
used with -- Depends(...) -- inside route handlers. FastAPI automatically calls
these functions during the request/response lifecycle and manages any cleanup after 
the route completes (ex: code after a 'yield'). 

NOTE: Shared, reusable dependency functions belong here. Dependency functions that
are specific to a single router (such as auth-related dependencies) should
live in that router’s own module instead.

NOTE: These are not “dependencies” in the normal Python import sense. 
Instead, they are DI providers that FastAPI injects into routes. 
EXAMPLE: get_db() - creates a per-request database session and closes it once the route finishes.

NOTE: Only functions meant to be passed to 'Depends(...)' should live here.

Modules using dependency.py
- r_auth.py
- r_match.py
- r_users.py

"""

from backend.echoDB.db_session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db   # <-- FastAPI pauses here and runs your route
    finally:
        db.close() # <-- FastAPI runs this after the route returns/ends

