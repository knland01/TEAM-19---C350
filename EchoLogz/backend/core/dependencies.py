


# FastAPI wrapper for python functions that turns them into HTTP endpoints callable from the front-end
from fastapi import Depends,  HTTPException, status
# FastAPI - Depends: Before running endpoint run this other function first and give result.
from backend.echoDB.db_session import SessionLocal
#from routers.r_auth import decode_jwt  # or wherever = auth utils
# from typing import Generator

# FastAPI always runs this function (conventional name) = FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db   # <-- route executes while the session is ‘open’
    finally:
        db.close() # <-- FastAPI runs this after the route returns/raises

def get_current_user(token: str = Depends(...)):
    pass
    # user = decode_jwt(token)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials",
    #     )
    # return user