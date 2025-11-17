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


def build_feature_vector(db: Session, user_id: int, sample: str) -> list[float]:
    # DB + Spotify + high-level orchestration
    ...
    return

def _matrix_features_to_vector(raw_features: dict) -> list[float]:
    # math only
    ...