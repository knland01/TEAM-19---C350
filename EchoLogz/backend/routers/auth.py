"""
Authentication Router (Spotify Gatekeeper)

This module defines all authentication-related API endpoints for the EchoLogz backend.
It manages user login, token verification, and integration with external OAuth provider: SPOTIFY - for secure access and authorization.

Core Responsibilities:
- Handle user login and logout routes
- Manage OAuth flows (Spotify authorization, callback, and token exchange)
- Issue and verify access tokens (JWT or session-based)
- Securely store and refresh tokens for authenticated users
- Enforce route protection for endpoints requiring authentication

Purpose:
Acts as the gatekeeper for the EchoLogz backend — responsible for verifying user identity, managing sessions, and enabling secure data access through token-based authentication.

Typical Usage Example:
    from fastapi import FastAPI
    from backend.routers import auth

    app = FastAPI()
    app.include_router(auth.router)
"""
# AUTH SKELETON:
from fastapi import APIRouter, Depends, HTTPException
import requests, os

router = APIRouter(prefix="/auth", tags=["auth"])

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

@router.get("/login")
def login_spotify():
    scopes = "user-read-email playlist-read-private"
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&scope={scopes}"
    )
    return {"auth_url": url}

@router.get("/callback")
def spotify_callback(code: str):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    resp = requests.post(token_url, data=payload)
    tokens = resp.json()

    if "access_token" not in tokens:
        raise HTTPException(status_code=400, detail="Failed to get token")

    # Save tokens to DB for the user here
    return {"message": "Spotify connected", "tokens": tokens}