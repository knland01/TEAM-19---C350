""" BACKEND (FastAPI + PyTest) UNIT TEST 
# IMPORTS:
TestClient: let's you fake HTTP requests to your FastAPI app
"""
from fastapi.testclient import TestClient
from backend.main import app
from backend.echoDB import db_schemas, db_session, db_crud
from backend.core.security import hash_password

# ----------------------------------------------------------------------------------------
client = TestClient(app) # fake API client

test_user = ''
test_password = ''
wrong_password = ''

def setup_test_user():
    db = db_session.SessionLocal()
    db.query(db_schemas.User).delete() # Clean DB first
    fake_user = {
        "username": test_user,
        "email": "test@example.com",
        "password": test_password
    }
    # Create test user w/ real CRUD function
    hashed = hash_password(fake_user["password"])
    db_crud.create_user_with_hash(
        db=db,
        username=fake_user["username"],
        email=fake_user["email"],
        hashed_pw=hashed
    )
    db.close()


def test_login_success() -> None:
    payload = {
        "username": test_user,
        "password": test_password,
    } # real clients can't send JSON - this is just feature of TestClient + Starlette
    # REAL CLIENT FORMAT: username=test_user&password=test_password
    response = client.post("/auth/login", json=payload) # Send post request to "auth/login"
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body.get("token_type", "").lower() == "bearer"

def test_login_fail_wrong_pw() -> None:
    payload = {
        "username": test_user,
        "password": wrong_password,
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Bad credentials"}
    