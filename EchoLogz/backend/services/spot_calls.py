"""
Spotify Data Service (Spotify API Communicator)

Handles direct communication with the Spotify Web API once authentication 
is complete. These functions make HTTPS requests to Spotify using a valid 
access token provided by the database.

Typical responsibilities:
- Fetch the current user's Spotify profile
- Retrieve playlists and tracks
- Access audio feature data (energy, tempo, valence...)
- Handle basic error checking and response validation

This module never deals with login, redirects, or token exchange—that's 
the router's job (spotify_auth.py). It only performs authorized data 
retrieval and returns parsed JSON responses for the rest of the 
backend to use.

Future API routes that may call these functions:
    - /users/me              -> get_user_profile()
    - /playlists             -> get_user_playlists()
    - /playlists/{id}/tracks -> get_playlist_tracks()

Security notes:
- Requires a valid access_token from SpotifyAccount table in DB.
- Do not store tokens here; pass them in as function arguments
_______________________________________
Modules using spot_calls.py:
- spot_feature_vectors.py
_______________________________________
"""

# EXTERNAL IMPORTS:
import requests                     # allows back-end to perform HTTP requests
from typing import List, Dict, Any

BASE_URL = "https://api.spotify.com/v1"

def _auth_headers(access_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}

# Could restrict return type after testing response types
def _get(endpoint: str, access_token: str, 
         params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Helper function to encapsulate request method for Spotify endpoint requests.
    Args:
        endpoint (str): Spotify API endpoint to request.
        access_token (str): Spotify OAuth token for API access.
        params (Dict[str, Any]): Dict of parameters to pass as Args 
                 for endpoints that require them.
    Raises:
        RuntimeError: If raise_for_status fails.
    """
    url = BASE_URL + endpoint
    headers = _auth_headers(access_token)
    r = requests.get(url, headers=headers, params=params)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Spotify API request failed: {e}, Response: {r.text}")
    except requests.RequestException as e:  # broad catch for unexpected errors.
        raise RuntimeError(f"Spotify API request failed: {e}")
    return r.json()

def _validate_time_range(value: str) -> str:
    """
    Helper function to  validate a time range str to Spotify's ranges.
    Args:
        value (str): User input to check if string is in valid range array.
    Returns:
       str: Returns the original string passed in the function if valid. 
    Raises:
        ValueError: If `value` is not in valid_ranges.
    """
    valid_ranges = [
        "short_term",       # ~4 weeks
        "medium_term",      # ~6 months
        "long_term"         # ~1 year
    ]
    if value not in valid_ranges:
        raise ValueError(
            f"Invalid time range '{value}'. Must be one of: "
            f"{", ".join(valid_ranges)}"
        )
    return value

def get_user_profile(access_token: str) -> Dict[str, Any]:
    """
    Fetches the current user's Spotify profile information.
    Args:
        access_token (str): A valid Spotify OAuth token.
    Returns:
        Dict[str, Any]: Returns the current user's profile information.
    """
    return _get("/me", access_token)

def get_user_top_tracks(access_token: str, limit: int = 20, 
                        time_range: str = "medium_term") -> Dict[str, Any]:
    """
    Fetches the current user's top tracks.
    Args:
        access_token (str): A valid Spotify OAuth access token.
        limit (int): Integer value between 1-50 denoting the number of 
                    tracks to return. Defaults to 20.
        time_range (str): String value to adjust time range of search. 
    Returns:
        Dict[str, Any]: The user's top tracks data as returned by the Spotify API.
    Raises:
        ValueError: If `limit` is outside of range 1-50.
    """
    time_range = _validate_time_range(time_range)
    if limit < 1 or limit > 50:
        raise ValueError(f"Limit must be between 1-50.")

    return _get(
        "/me/top/tracks", 
        access_token,
        params={
            "limit": limit,
            "time_range": time_range
        })

def get_user_top_artists(
        access_token: str, 
        limit: int = 20,
        time_range: str = "medium_term"
        ) -> Dict[str, Any]:
    """
    Fetch user's top artists for a requested time range.
    Args:
        access_token (str): A valid Spotify OAuth access token.
        limit (int): Integer value between 1-50 denoting the number of 
                    tracks to return. Defaults to 20.
        time_range (str): String value to adjust time range of search. 
    Returns:
        Dict[str, Any]: The user's top artists data as returned by the Spotify API.
    Raises:
        ValueError: If `limit` is outside of range 1-50.
    """
    time_range = _validate_time_range(time_range)
    if limit < 1 or limit > 50:
        raise ValueError(f"Limit must be between 1-50.")

    return _get(
        "/me/top/artists",
        access_token,
        params={
            "limit": limit,
            "time_range": time_range
        })

# NOTE: This API endpoint is depricated according to Spotify Docs.
# https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
def get_audio_features(access_token: str, track_ids: List[str]) -> Dict[str, Any]:
    """
    Fetches audio features for a list of track IDs.
    Args:
        access_token (str): A valid Spotify OAuth access token.
        track_ids (List[str]): A list of Spotify track IDs.
    Returns:
        Dict[str, Any]: Audio features data for the specified tracks.
    Raises:
        ValueError: If `track_ids` has more than 100 items.
    """
    if len(track_ids) > 100:
        raise ValueError(
            f"Spotify API supports a maximum of 100 track IDs per request, "
            f"but {len(track_ids)} were provided."
        )
    ids = ",".join(track_ids)
    return _get(f"/audio-features?ids={ids}", access_token)
