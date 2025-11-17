"""
MODULE: Compatibility Engine (Math-Only)

This module is responsible only for vector math. Any raw data
(ex: Spotify JSON) will be converted into numeric vectors in
spot_feature_vectors.py before being passed here.

Core Responsibilities:
- Apply mathematical operations to vectors (ex: cosine similarity, weighted averages)
- Return compatibility scores or match rankings

Purpose:
Acts as the brain of the EchoLogz backend—responsible for interpreting data
and generating the 'compatibility scores'.

Goals:
-----------------
--- Module = Math only (Feature extraction from Spotify JSON will occur in spot_feature_vectors.py.)
1. Implement the '_score' function to compute a similarity / 
   compatibility score between two feature vectors.
2. Implement 'compare_users' to rank 1 or more users by their
   compatibility with a target user.
3. Keep this module *web-agnostic*: no FastAPI, no HTTP logic.
   It should be importable and testable as pure Python.

"""

import numpy as np                                                # For vector math and similarity calculations
from typing import List, Dict, Tuple                              # For clean function type hints
from sklearn.metrics.pairwise import cosine_similarity            # Optional: built-in cosine sim

Vector = np.ndarray
""" Whatever data comes in must be representable as a numeric vector. """

def _score(vec1: Vector, vec2: Vector) -> float:
    """
    Low-level raw similarity score between two vectors.

    - Assumes both vectors are already validated.
    - Uses ex: cosine similarity (?) and returns a value in [-1.0, 1.0].
    - No clamping, no business rules, just the math.
    """
    score = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
    return score

def calc_compatibility(user_a_vec: Dict, user_b_vec: Dict) -> float:
    """Calculate and return the compatibility score between two users based on their feature vectors."""
    # Convert feature dicts to sorted numpy arrays for consistency
    """
    High-level compatibility score for the rest of the app.

    - Calls the low-level _score() function.
    - Normalizes the result into [0.0, 1.0].
    - Handles edge cases (NaN, inf, etc.).
    - This is the function routers / services should import.
    """
    vec_a = np.array(list(user_a_vec.values()))
    vec_b = np.array(list(user_b_vec.values()))

    if not _check_user_vector(vec_a) or not _check_user_vector(vec_b):
        return 0.0
    
    if user_a_vec == user_b_vec:
        return 1.0
    
    score = _score(vec_a, vec_b)

    # Edge case: score can be NaN or infinite
    if np.isnan(score) or np.isinf(score):
        return 0.0
    
    return _normalize_score(score)

def compare_users(target: Dict, others: Dict[str, Dict], top_k: int | None = None) -> List[Tuple[str, float]]:
    """
    Compare a user's score against multiple others and return sorted results.
    """
    res = []  # List to store (user_id, score) pairs

    for user_id, vec in others.items():
        score = calc_compatibility(target, vec)
        res.append((user_id, score))

    res.sort(key=lambda x: x[1], reverse=True)      # Sort by score descending

    if top_k is not None:                           # Limit to top_k results
        res = res[:top_k]

    return res


def _check_user_vector(vec: Vector) -> bool:
    """
    Validate that the input is a proper numeric vector.

    - Checks for correct type (list, np.ndarray).
    - Ensures no NaN or infinite values.
    - Ensures non-zero length.
    """
    if not isinstance(vec, (list, np.ndarray)):
        return False

    vec = np.array(vec)

    if vec.size == 0:
        return False

    if np.isnan(vec).any() or np.isinf(vec).any():
        return False

    return True

def _normalize_score(raw_score: float) -> float:
    """
    Normalize raw score from [-1.0, 1.0] to [0.0, 1.0].
    """
    return (raw_score + 1) / 2
