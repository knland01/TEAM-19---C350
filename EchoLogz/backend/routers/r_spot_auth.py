
"""
---------------------------------------------------------------
MODULE: Spotify OAuth Router - The Gatekeeper (r_spot_auth.py)
---------------------------------------------------------------

Handles the OAuth dance with Spotify:
- /auth/spotify/login              -> Redirect user to Spotify consent
- /auth/spotify/callback           -> Exchange code for tokens
- (optional) /auth/spotify/refresh -> Refresh access token

Secure storage notes:
- Never return raw Spotify tokens to the client.
- Encrypt/secure tokens at rest - store refresh_token to renew access.
- Tie Spotify tokens to the EchoLogz user (foreign key to the users table).
────────────────────────────────────────────
Modules using r_auth.py:
- main.py (only)
────────────────────────────────────────────
"""

# INTERNAL MODULES:
from backend.echoDB import db_tables
from backend.core.config import settings
from backend.core.dependencies import get_db
from backend.core.security import get_current_user
from backend.echoDB import db_crud

# EXTERNAL MODULES:
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
import base64, requests
from urllib.parse import urlencode
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth/spotify", tags=["spotify-auth"])

SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
SPOTIFY_REDIRECT_URI = settings.SPOTIFY_REDIRECT_URI  # e.g. http://localhost:8000/auth/spotify/callback
SCOPES = "user-read-email playlist-read-private"


# -------------------------------------------------------------------------
#    HELPER FUNCTIONS - specific only to r_spot_auth.py
# -------------------------------------------------------------------------
def _basic_auth_header(client_id: str, client_secret: str) -> dict:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

# -------------------------------------------------------------------------------
# Dependencies - FastAPI Depends(...) Functions specific only to r_spot_auth.py
# -------------------------------------------------------------------------------
def get_current_spotify_account(db: Session = Depends(get_db), 
                                current_user: db_tables.User = Depends(get_current_user),
                               ) -> db_tables.SpotifyAccount:
    """
    Returns the SpotifyAccount row for the logged-in EchoLogz user.
    Raises 404 or 400 if no Spotify link exists.
    """
    account = db_crud.get_spotify_account_by_user_id(db, user_id=current_user.id)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has not connected Spotify",
        )

    return account

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
    # .POST - HTTP endpoint that accepts POST requests: client sending data to server to create / process something.
    # .GET:    "Give me data."
    # .PUT:    "Replace existing thing with new thing."
    # .PATCH:  "Update the part of existing thing."
    # .DELETE: "Remove this thing."

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
    return RedirectResponse(url)


@router.get("/callback")
def spotify_callback(
    code: str,
    db: Session = Depends(get_db),
    current_user: db_tables.User = Depends(get_current_spotify_account),
):
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
        raise HTTPException(400, tokens.get("error_description", "Failed to get token"))
    access_token = tokens["access_token"]
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens["expires_in"]
    me = requests.get(                             # get spotify user id
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    spotify_user_id = me["id"]
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    db_crud.create_or_update_spotify_account(
        db=db,
        user_id=current_user.id,
        spotify_user_id=spotify_user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        scope=SCOPES,
    )
    return {"message": "Spotify connected"}



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


# ------------------------------------------------------------------
# CODE GRAVEYARD
# ------------------------------------------------------------------
# We now use HTTP Basic Auth for client_id/client_secret instead of sending them in the body.

# @router.get("/callback")
# def spotify_callback(code: str):
#     token_url = "https://accounts.spotify.com/api/token"
#     data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": SPOTIFY_REDIRECT_URI,
#         "client_id": SPOTIFY_CLIENT_ID,           <--- redundant if using Basic Auth header
#         "client_secret": SPOTIFY_CLIENT_SECRET,   <--- choose *either* body creds OR Basic Auth
#     }
#     headers = _basic_auth_header(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
#     resp = requests.post(token_url, data=data, headers=headers)
#     tokens = resp.json()

#     if "access_token" not in tokens:
#         raise HTTPException(status_code=400, detail=tokens.get("error_description", "Failed to get token"))

#     # TODO: associate tokens with the currently logged-in EchoLogz user
#     # Save access_token, refresh_token, expires_in (preferably encrypted/hashed)
#     return {"message": "Spotify connected", "tokens": tokens} <--- Front-End Spotify token return not allowed in design
