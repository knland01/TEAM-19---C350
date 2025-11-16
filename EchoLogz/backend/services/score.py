"""
Compatibility Engine

This module handles the logic for calculating similarity
and compatibility scores between users, playlists, or track features.

Core Responsibilities:
- Retrieve or receive feature vectors (ex: from Spotify API or database)
- Normalize and preprocess input data for comparison
- Apply mathematical operations (ex: cosine similarity, weighted averages)
- Return compatibility scores or match rankings

Purpose:
Acts as the brain of the EchoLogz backend—responsible for interpreting data
and generating the 'connection scores' that drive recommendations.

Typical Usage Example:
    from services.scores import calculate_compatibility

    score = calculate_compatibility(user1_vector, user2_vector)
    print(f"User Compatibility: {score:.2f}")
"""
import numpy as np                   # For vector math and similarity calculations
from typing import List, Dict        # For clean function type hints
from sklearn.metrics.pairwise import cosine_similarity  # Optional: built-in cosine sim
from ..echoDB import db_crud as crud, db_schemas as models          # To fetch data from the database if needed

def compare_users(user_a_vec: Dict, user_b_vec: Dict) -> float:
    """Calculate and return the compatibility score between two users based on their feature vectors."""
    # Convert feature dicts to sorted numpy arrays for consistency
    if not user_a_vec or not user_b_vec:
        return 0.0

    if user_a_vec == user_b_vec:
        return 1.0
    
    features = sorted(set(user_a_vec.keys()).union(set(user_b_vec.keys())))
    vec_a = np.array([user_a_vec.get(f, 0) for f in features]).reshape(1, -1)
    vec_b = np.array([user_b_vec.get(f, 0) for f in features]).reshape(1, -1)

    score = cosine_similarity(vec_a, vec_b)[0][0]
    return score
