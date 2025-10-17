"""
Spotify Data Service (Spotify API Communicator)

Handles direct communication with the Spotify Web API once authentication 
is complete. These functions make HTTPS requests to Spotify using a valid 
access token provided by the OAuth flow in spotify_auth.py.

Typical responsibilities:
- Fetch the current user's Spotify profile
- Retrieve playlists and tracks
- Access audio feature data (energy, tempo, valence, etc.)
- Handle basic error checking and response validation

This module never deals with login, redirects, or token exchange—that's 
the router's job (spotify_auth.py). It only performs authorized data retrieval and returns parsed JSON responses for the rest of the backend to use.

Example routes that may call these functions:
- /users/me            -> get_user_profile()
- /playlists           -> get_user_playlists()
- /playlists/{id}/tracks -> get_playlist_tracks()

Security notes:
- Requires a valid access_token from spotify_auth.py
- Do not store tokens here; pass them in as function arguments
"""

# EXAMPLE:
import requests

BASE_URL = "https://api.spotify.com/v1"

def get_user_profile(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}