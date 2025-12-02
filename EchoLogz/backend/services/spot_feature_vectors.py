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
import random
from typing import Any, Dict, List
from sqlalchemy.orm import Session
import numpy as np
from datetime import datetime, timezone
from backend.services.utils import normalize_vector
from datetime import timedelta

# Ordered list of keys that define our feature vector
AUDIO_FEATURE_KEYS = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo",
    "valence",
    "duration_ms",
    "key",
    "mode",
    "time_signature",
]

SPOTIFY_FEATURE_RANGES = {
    "acousticness":     (0.0, 1.0),
    "danceability":     (0.0, 1.0),
    "energy":           (0.0, 1.0),
    "instrumentalness": (0.0, 1.0),
    "liveness":         (0.0, 1.0),
    "speechiness":      (0.0, 1.0),
    "valence":          (0.0, 1.0),
    "mode":             (0.0, 1.0),      # 0 or 1
    "key":              (0.0, 11.0),     # 12 musical keys (0–11)
    
    # Spotify gives "typical working ranges"
    "loudness":         (-60.0, 0.0),     # from API docs
    "tempo":            (0.0, 250.0),     # Spotify docs say tempo rarely > 250 BPM
    "duration_ms":      (0.0, 600000.0),  # rare to exceed 10 minutes, doc references
    "time_signature":   (1.0, 7.0),       # Spotify says 3–7 are common, but 1–7 possible
}


# features that should be integers (inclusive ranges)
_INT_FEATURES = {"mode", "key", "time_signature", "duration_ms"}

def build_feature_vector(db: Session, user_id: int, sample: str = "medium_term") -> dict[str, object] | None:
    # DB + Spotify + high-level orchestration
    """
    Return FULL music profile containing:
      - raw feature means (real units)
      - scaled feature vector in [0,1]
      - labels aligned to the vector
    """
    # Step 1: Lookup EchoLogz user (assumes valid user_id given)
    user = db_crud.get_user_by_id(db, user_id)
    if not user:
        return None

    # Step 2: Lookup Spotify link
    spotify_account = db_crud.get_spotify_account_by_user_id(db, user_id)
    if not spotify_account or not spotify_account.access_token:
        return None

    # Step 3: Token lifecycle management
    if _token_is_expired(spotify_account):
        new_token, new_expiry = spot_calls.refresh_access_token(
            spotify_account.refresh_token
        )

        if not new_token or not new_expiry:
            # refresh failed
            return None

        spotify_account.access_token = new_token
        spotify_account.expires_at   = new_expiry
        db.commit()


    access_token = spotify_account.access_token

    # Step 4: Get Spotify tracks for the user (top tracks JSON → IDs)
    top_resp = spot_calls.get_user_top_tracks(
        access_token,
        time_range=sample,
        limit=50
    )
    items = top_resp.get("items", [])
    track_ids = [
        t["id"] for t in items
        if isinstance(t, dict) and t.get("id")
    ]
    if not track_ids:
        return None

    # Step 5: Get audio features
    raw_features = spot_calls.get_audio_features(access_token, track_ids)
    audio_features = raw_features.get("audio_features") or []
    if not audio_features:
        return None

    # Step 6–7: Build profile and return raw and scaled vector
    music_profile = build_music_profile(audio_features)


    return music_profile

def build_feature_vector(db: Session, user_id: int, sample: str = "medium_term"):
    print(f"[IDENTITY] start: user_id={user_id}")

    user = db_crud.get_user_by_id(db, user_id)
    print(f"[IDENTITY] user found? {bool(user)}")
    if not user:
        print("[IDENTITY] FAIL: user not found")
        return None

    spotify_account = db_crud.get_spotify_account_by_user_id(db, user_id)
    print(f"[IDENTITY] spotify account? {bool(spotify_account)}")
    if not spotify_account:
        print("[IDENTITY] FAIL: no spotify account in DB")
        return None

    print(f"[IDENTITY] access_token exists? {bool(spotify_account.access_token)}")
    print(f"[IDENTITY] expires_at={spotify_account.expires_at}")

    if _token_is_expired(spotify_account):
        print("[IDENTITY] token expired → attempting refresh")
        new_token, new_expiry = spot_calls.refresh_access_token(
            spotify_account.refresh_token
        )
        if not new_token or not new_expiry:
            # refresh failed
            return None
        spotify_account.access_token = new_token
        spotify_account.expires_at   = new_expiry
        db.commit()
    else:
        print("[IDENTITY] token OK")

    top_resp = spot_calls.get_user_top_tracks(spotify_account.access_token, 
        time_range=sample,
        limit=50
    )
    print(f"[IDENTITY] top tracks keys: {top_resp.keys() if top_resp else None}")
    print(top_resp)

    items = top_resp.get("items", [])
    print(f"[IDENTITY] num top tracks returned: {len(items)}")

    track_ids = [t["id"] for t in items if isinstance(t, dict) and t.get("id")]
    print(f"[IDENTITY] num track_ids extracted: {len(track_ids)}")

    if not track_ids:
        print("[IDENTITY] FAIL: no track IDs returned")
        return None

    raw_features = spot_calls.get_audio_features(spotify_account.access_token, track_ids)
    print(f"[IDENTITY] audio_features top-level keys: {raw_features.keys() if raw_features else None}")

    audio_features = raw_features.get("audio_features") or []
    print(f"[IDENTITY] num audio_features returned: {len(audio_features)}")

    if not audio_features:
        print("[IDENTITY] FAIL: Spotify returned NO audio features")
        return None

    print("[IDENTITY] SUCCESS: building music profile")
    return build_music_profile(audio_features)



def _token_is_expired(spotify_account) -> bool:
    expires_at = spotify_account.expires_at
    if not expires_at:
        return False

    # If the datetime is naive, treat it as UTC (because saved as UTC)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc) 
        # ... SQLite strips the timezone on retrieval --- here it is added back in for comparison

    now = datetime.now(timezone.utc)
    return expires_at < now




# ================================================================================
#         MATH ONLY HELPERS
# ================================================================================


def _rand_value(name: str, low: float, high: float) -> Any:
    """Generate a random value for a single Spotify audio feature."""
    if name == "mode":
        # explicit: 0 or 1
        return random.randint(0, 1)

    if name in {"key", "time_signature", "duration_ms"}:
        return random.randint(int(low), int(high))

    # all others are floats
    return random.uniform(low, high)

def generate_fake_audio_features(
    track_ids: List[str],
) -> List[Dict[str, Any]]:
    """
    Mimic Spotify's /audio-features response for a list of track IDs,
    using random values within documented ranges.
    """
    results: List[Dict[str, Any]] = []

    for tid in track_ids:
        feat: Dict[str, Any] = {"id": tid}

        for name, (low, high) in SPOTIFY_FEATURE_RANGES.items():
            feat[name] = _rand_value(name, low, high)

        # optional extra fields if your code expects them
        feat.setdefault("type", "audio_features")
        feat.setdefault("uri", f"spotify:track:{tid}")
        feat.setdefault("track_href", f"https://api.spotify.com/v1/tracks/{tid}")
        feat.setdefault("analysis_url",
                        f"https://api.spotify.com/v1/audio-analysis/{tid}")

        results.append(feat)

    return results


# --------------------------------------------------------
# Compute RAW MEANS (identity values shown to the user)
# --------------------------------------------------------
def _compute_raw_means(audio_features_list: list[dict]) -> dict[str, float]:
    rows = []
    for feat in audio_features_list:
        row = []
        for key in AUDIO_FEATURE_KEYS:
            v = feat.get(key)
            if v is None:
                v = 0.0
            row.append(float(v))
        rows.append(row)

    if not rows:
        return {}

    matrix = np.array(rows, dtype=float)
    means = matrix.mean(axis=0)

    return {key: float(val) for key, val in zip(AUDIO_FEATURE_KEYS, means)}


# --------------------------------------------------------
# Scale raw means to 0–1 using official Spotify ranges
# --------------------------------------------------------
def _scale_using_spotify_ranges(raw: dict[str, float]) -> list[float]:
    scaled = []
    for key in AUDIO_FEATURE_KEYS:
        v = raw.get(key, 0.0)
        fmin, fmax = SPOTIFY_FEATURE_RANGES[key]

        # clamp only to guarantee 0–1 range (mathematical requirement)
        if v < fmin:
            v = fmin
        if v > fmax:
            v = fmax

        denom = (fmax - fmin) or 1.0
        scaled.append((v - fmin) / denom)

    return scaled


# --------------------------------------------------------
# Final profile returned for identity + compatibility
# --------------------------------------------------------
def build_music_profile(audio_features_list: list[dict]) -> dict[str, object]:
    raw_means = _compute_raw_means(audio_features_list)
    if not raw_means:
        return {"raw": {}, "scaled": [], "labels": AUDIO_FEATURE_KEYS}

    scaled = _scale_using_spotify_ranges(raw_means)

    return {
        "raw": raw_means,         # original musical identity values
        "scaled": scaled,         # Spotify-normalized values in [0,1]
        "labels": AUDIO_FEATURE_KEYS,
    }



# ----------------------------- CODE GRAVEYARD -----------------------------------
# def _token_is_expired(spotify_account) -> bool:
#     return spotify_account.expires_at < datetime.now(timezone.utc)


# def _matrix_features_to_vector(
#     audio_features_list: list[dict[str, float]]
# ) -> list[float]:
#     # math only; derived data only

#     rows = []
#     for feat in audio_features_list:
#         if not isinstance(feat, dict):
#             continue

#         row = []
#         for k in AUDIO_FEATURE_KEYS:
#             v = feat.get(k)
#             if v is None:
#                 # You can choose a different fallback, but 0.0 is simple.
#                 v = 0.0
#             row.append(float(v))
#         rows.append(row)

#     if not rows:
#         return []
#     matrix = np.array(rows, dtype=float)
#     mean_vector = matrix.mean(axis=0)
#     return normalize_vector(mean_vector).tolist()

# def _compute_feature_means(audio_features_list: list[dict]) -> dict[str, float]:
#     """Return raw mean per feature in original units (derived, but not normalized)."""
#     rows = []
#     for feat in audio_features_list:
#         row = []
#         for k in AUDIO_FEATURE_KEYS:
#             v = feat.get(k)
#             if v is None:
#                 v = 0.0
#             row.append(float(v))
#         rows.append(row)

#     if not rows:
#         return {}

#     matrix = np.array(rows, dtype=float)
#     mean_vector = matrix.mean(axis=0)
#     return {
#         key: float(val) for key, val in zip(AUDIO_FEATURE_KEYS, mean_vector)
#     }


# def _scale_means_to_unit_interval(raw_means: dict[str, float]) -> list[float]:
#     """Scale each raw mean to [0,1] using FEATURE_RANGES."""
#     scaled = []
#     for key in AUDIO_FEATURE_KEYS:
#         v = raw_means.get(key, 0.0)
#         fmin, fmax = FEATURE_RANGES[key]
#         # clamp
#         if v < fmin:
#             v = fmin
#         if v > fmax:
#             v = fmax
#         denom = (fmax - fmin) or 1.0
#         scaled.append((v - fmin) / denom)
#     return scaled