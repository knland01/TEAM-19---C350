""" MODULE: Spotify Feature Vector Pipeline

Purpose:
    Generates a numeric "taste vector" for a linked Spotify user. This vector is
    the standardized representation of the user's music preferences used for
    compatibility scoring.

What this function must do:
    1. Lookup EchoLogz user:
        - Receive an EchoLogz user_id.
        - Confirm the user exists.

    2. Lookup Spotify link:
        - Fetch the SpotifyAccount row tied to this EchoLogz user.
        - If none exists → cannot build a vector → return error/None. <-- user probably needs to "Connect to Spotify"

    3. Handle token lifecycle:
        - Check if the access token is expired.
        - If expired, use the refresh token to obtain a new access token.
        - Update the SpotifyAccount row with the new token + new expiration.

    4. Get a set of Spotify tracks linked to that user (function in spot_calls.py)
        Examples:
            Top N tracks from Spotify (short/medium/long term, based on sample)
            Or: tracks they've saved/liked and EchoLogz has stored as track IDs
        NOTE: you're storing track IDs/URIs, not raw audio or giant
        metadata blobs.

    5. Fetch audio features for those tracks (function in spot_calls.py)
        - Use Spotify's /audio-features endpoint for the batch of track IDs to get
          things like: danceability, energy, valence, tempo, loudness, acousticness, 
                       instrumentalness, liveness, speechiness
        - maybe genre / artist-level embeddings if you add those later
        This gives you a matrix: num_tracks x num_features.

    6. Reduce all track features to a single user vector
        - Aggregate across tracks to get a fixed-length “taste vector”
          - EXAMPLE: mean of each feature across all tracks
          - optionally also std-dev, median, or quantiles
          - optionally normalize/scaled features

    7. Return the taste vector:
        - Return the vector to the caller (match engine, compatibility scorer, etc.).
        - Do NOT store unnecessary raw Spotify metadata.
        - 
    8. Store the derived vector (this is Spotify-compliant):
        - DESIGN CHOICE: Always recompute? or store vectors... (?) hmmmmmm....

IMPORTANT NOTE:
    - Never log tokens or Spotify user IDs in plain text.
    - Never store large Spotify metadata snapshots.
    - This function must only return derived numeric features, never raw Spotify content.
"""

# INTERNAL IMPORTS:
from . import spot_calls
from backend.echoDB import db_crud

# EXTERNAL IMPORTS:
from sqlalchemy.orm import Session
import numpy as np
from datetime import datetime, timezone
from backend.services.utils import normalize_vector


def build_feature_vector(db: Session, user_id: int, sample: str = "medium_term") -> list[float] | None:
    # DB + Spotify + high-level orchestration

    # Step 1: Lookup EchoLogz user (assumes valid user_id given)
    user = db_crud.get_user_by_id(db, user_id)
    if not user:
        return None

    # Step 2: Lookup Spotify link
    spotify_account = db_crud.get_spotify_account(db, user_id)
    if not spotify_account or not spotify_account.access_token:
        return None

    # Step 3: Token lifecycle management
    if _token_is_expired(spotify_account):
        new_token, new_expiry = spot_calls.refresh_access_token(spotify_account.refresh_token)
        if not new_token:
            return None
        spotify_account.access_token = new_token
        spotify_account.token_expires_at = new_expiry
        db.commit()

    access_token = spotify_account.access_token

    # Step 4: Get Spotify tracks for the user
    track_ids = spot_calls.get_user_top_tracks(access_token, time_range=sample)
    if not track_ids:
        return None

    # Step 5: Get audio features
    raw_features = spot_calls.get_audio_features(access_token, track_ids)
    if not raw_features:
        return None

    # Step 6–7: Reduce to taste vector and return
    return _matrix_features_to_vector(raw_features)


def _matrix_features_to_vector(raw_features: dict[str, dict[str, float]]) -> list[float]:
    # math only

    if not raw_features:
        return []

    matrix = np.array([list(track.values()) for track in raw_features.values()])
    mean_vector = matrix.mean(axis=0)
    return normalize_vector(mean_vector).tolist()


def _token_is_expired(spotify_account) -> bool:
    return spotify_account.token_expires_at < datetime.now(timezone.utc)