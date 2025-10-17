
"""
Spotify OAuth Router (Spotify Gatekeeper)

Handles the OAuth dance with Spotify:
- /auth/spotify/login      -> Redirect user to Spotify consent
- /auth/spotify/callback   -> Exchange code for tokens
- (optional) /auth/spotify/refresh -> Refresh access token

Secure storage notes
- Never return raw Spotify tokens to the client in production.
- Encrypt/secure tokens at rest; store refresh_token to renew access.
- Tie Spotify tokens to the EchoLogz user (foreign key to your users table).
"""

# AUTH SKELETON:
from fastapi import APIRouter, HTTPException
import os, base64, requests
from urllib.parse import urlencode

router = APIRouter(prefix="/auth/spotify", tags=["spotify-auth"])

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")  # e.g. http://localhost:8000/auth/spotify/callback
SCOPES = "user-read-email playlist-read-private"

def _basic_auth_header(client_id: str, client_secret: str) -> dict:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

@router.get("/login")
def login_spotify():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": SCOPES,
        # "state": "...",  # Optional: add CSRF protection
        # "show_dialog": "true",
    }
    url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return {"auth_url": url}

@router.get("/callback")
def spotify_callback(code: str):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }
    headers = _basic_auth_header(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    resp = requests.post(token_url, data=data, headers=headers)
    tokens = resp.json()

    if "access_token" not in tokens:
        raise HTTPException(status_code=400, detail=tokens.get("error_description", "Failed to get token"))

    # TODO: associate tokens with the currently logged-in EchoLogz user
    # Save access_token, refresh_token, expires_in (preferably encrypted/hashed)
    return {"message": "Spotify connected", "tokens": tokens}

@router.post("/refresh")
def refresh_token(refresh_token: str):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = _basic_auth_header(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    resp = requests.post(token_url, data=data, headers=headers)
    payload = resp.json()
    if "access_token" not in payload:
        raise HTTPException(status_code=400, detail=payload.get("error_description", "Failed to refresh token"))
    return payload