"""
Compatibility Engine (Math-Only module)

This module is responsible only for vector math. Any raw data
(e.g., Spotify JSON) will be converted into numeric vectors in
`feature_vectors.py` before being passed here.

Core Responsibilities:
- Apply mathematical operations to vectors (ex: cosine similarity, weighted averages)
- Return compatibility scores or match rankings

Purpose:
Acts as the brain of the EchoLogz backend—responsible for interpreting data
and generating the 'connection scores' that drive recommendations.


"""

"""
Assignment Goals:
-----------------
--- Module = Math only (Feature extraction from Spotify JSON will occur in feature_vectors.py.)
1. Implement the `_score` function to compute a similarity / 
   compatibility score between two feature vectors.
2. Implement `compare_users` to rank 1 or more users by their
   compatibility with a target user.
3. Keep this module *web-agnostic*: no FastAPI, no HTTP logic.
   It should be importable and testable as pure Python.

Typical Usage Example:
    from services.scores import calc_compatibility

    score = calc_compatibility(user1_vector, user2_vector)
    print(f"User Compatibility: {score:.2f}")

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
    return #score

def calc_compatibility(vec1: Vector, vec2: Vector) -> float:

    return

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
    if not user_a_vec or not user_b_vec:
        return 0.0

    if user_a_vec == user_b_vec:
        return 1.0

    features = sorted(set(user_a_vec.keys()).union(set(user_b_vec.keys())))
    vec_a = np.array([user_a_vec.get(f, 0) for f in features]).reshape(1, -1)
    vec_b = np.array([user_b_vec.get(f, 0) for f in features]).reshape(1, -1)

    score = cosine_similarity(vec_a, vec_b)[0][0]
    return score

def compare_users(target: Vector, others: Dict[str, Vector], top_k: int | None = None) -> List[Tuple[str, float]]:
    """
    Rank other users by compatibility with a target user.

    Parameters
    ----------
    target:
        Feature vector for the "reference" user.
    others:
        A mapping of user identifiers (e.g. usernames or IDs)
        to their feature vectors.
    top_k:
        If provided, return only the top_k most compatible users.
        If None, return all users.

    Returns
    -------
    List[Tuple[str, float]]:
        A list of (user_id, score) pairs, sorted in descending
        order by score. Example:[('alice', 0.92), ('bob', 0.81), ('carol', 0.47)]

    Requirements:
    - Call `calc_compatibility(target, vec)` for each entry in `others`.
    - Collect the results into a list of (key, score) pairs.
    - Sort that list from highest score to lowest.
    - If `top_k` is not None, return only the first `top_k` entries.

    TODO:
        Implement the body and replace the NotImplementedError.
    """

    return

