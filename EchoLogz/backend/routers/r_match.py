"""
----------------------------------------------------
MODULE: Compatibility Match Router (r_match.py)
----------------------------------------------------

This router defines the API endpoints for user-to-user or entity-to-entity 
matching within the EchoLogz ecosystem.

It serves as the entry point for frontend clients (or other services) to request 
comparison and compatibility scoring between users based on their Spotify data 
or other stored features (in EchoLogz DB).

Core Responsibilities:
----------------------
- Accept and validate incoming match requests (user IDs, sample size, etc.)
- Pass validated data to the scoring engine (services.score)
- Return standardized match results containing overall and sub-scores
- Handle input validation and error responses for failed or invalid comparisons

Purpose:
--------
Acts as the gateway between the EchoLogz frontend and the internal scoring system.

────────────────────────────────────────────
Modules using r_auth.py:
- main.py (only)
────────────────────────────────────────────

"""

# INTERNAL MODULES:
from backend.core.dependencies import get_db, get_current_user_id
from backend.services.score import calc_compatibility
from backend.services.spot_feature_vectors import build_feature_vector
from backend.echoDB.db_schemas import IdentityResp, RandomMatchResp

# EXTERNAL MODULES:
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Dict, Any



router = APIRouter(prefix="/match", tags=["match"])
# logically groups all match - routers defined below w/ @router, adding '/match' to each endpoint (ex: /match/compare)

# --------------------------------------------------------------------
# Endpoint-specific payloads (these are not DB models)
# --------------------------------------------------------------------
class CompareReq(BaseModel):
    user_a_id: int = Field(ge=1)
    user_b_id: int = Field(ge=1)
    sample: int | None = Field(default=100, ge=1, le=100)

class CompareResp(BaseModel):
    score: float
    pair_id: int | None = None   # db row id if you upsert

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
    # .POST - HTTP endpoint that accepts POST requests: client sending data to server to create / process something.
    # .GET:    "Give me data."
    # .PUT:    "Replace existing thing with new thing."
    # .PATCH:  "Update the part of existing thing."
    # .DELETE: "Remove this thing."

@router.post("/compare", response_model=CompareResp)
def post_compare(req: CompareReq, db: Session = Depends(get_db)):
    """ Compare two users by their feature vectors and return a compatibility score.
           -> build_feature_vector(db, user_id=1)
            -> look up user 1 in EchoLogz DB
            -> find spotify_account_id (not implemented)
            -> find access_token / refresh_token (not implemented)
            -> call Spotify API to get features (not implemented)
            -> convert features to a numeric vector
       -> build_feature_vector(db, user_id=2)
       -> calc_compatibility(vec_a, vec_b)
       -> return score
    """
    try:
        user_a_vec = build_feature_vector(
            db=db,
            user_id=req.user_a_id,
            sample=req.sample,
        )
        user_b_vec = build_feature_vector(
            db=db,
            user_id=req.user_b_id,
            sample=req.sample,
        )
        score = calc_compatibility(user_a_vec, user_b_vec)
        pair_id = None
        return CompareResp(score=score, pair_id=pair_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get("/identity/{user_id}", response_model=IdentityResp)
def get_user_identity(
    user_id: int,
    sample: str = "medium_term",
    db: Session = Depends(get_db),
):
    """
    Return the user's derived musical identity profile.

    Uses Spotify audio_features for the user's top tracks and returns:
      - raw feature means (real units)
      - scaled feature vector in [0,1]
      - labels (feature names)
    """
    profile = build_feature_vector(
        db=db,
        user_id=user_id,
        sample=sample,
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unable to compute musical identity. "
                "User may not have Spotify connected or lacks "
                "sufficient listening data."
            ),
        )
    return IdentityResp(
        user_id=user_id,
        raw=profile["raw"],
        scaled=profile["scaled"],
        labels=profile["labels"],
    )

# ------------------------------------------------------------------
# NEW: Random synthetic match for the logged-in user
# ------------------------------------------------------------------
# @router.post("/random", response_model=RandomMatchResp)
# def post_random_match(
#     db: Session = Depends(get_db),
#     current_user_id: int = Depends(get_current_user_id),
# ):
#     """
#     Generate a random synthetic user, compute compatibility against
#     the logged-in user, and return the match score + fake profile.
#     """

#     # Real user profile
#     real_profile = build_feature_vector(
#         db=db,
#         user_id=current_user_id,
#         sample="medium_term",
#     )

#     if not real_profile:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Unable to compute musical identity for current user.",
#         )

#     labels = real_profile["labels"]

#     # Build a synthetic partner by sampling random [0,1] values
#     import random

#     fake_scaled = [random.random() for _ in labels]
#     fake_raw = {label: value for label, value in zip(labels, fake_scaled)}
#     fake_profile: Dict[str, Any] = {
#         "labels": labels,
#         "raw": fake_raw,
#         "scaled": fake_scaled,
#     }

#     # Use your existing scoring engine
#     score = calc_compatibility(real_profile, fake_profile)

#     return RandomMatchResp(
#         name="Random EchoLogz User",
#         score=score,
#         profile=fake_profile,
#     )


# @router.post("/random", response_model=RandomMatchResp)
# def post_random_match(
#     req: RandomReq,
#     db: Session = Depends(get_db),
# ):
#     real_profile = build_feature_vector(
#         db=db,
#         user_id=req.user_id,
#         sample="medium_term",
#     )

#     if not real_profile:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Unable to compute musical identity for this user.",
#         )

#     labels = real_profile["labels"]

#     import random
#     fake_scaled = [random.random() for _ in labels]
#     fake_raw = dict(zip(labels, fake_scaled))

#     fake_profile: Dict[str, Any] = {
#         "labels": labels,
#         "raw": fake_raw,
#         "scaled": fake_scaled,
#     }

#     # Build flat dicts (label -> scaled value) for compatibility calc
#     real_vec = {
#         label: value
#         for label, value in zip(real_profile["labels"], real_profile["scaled"])
#     }
#     fake_vec = {
#         label: value
#         for label, value in zip(fake_profile["labels"], fake_profile["scaled"])
#     }

#     # Now calc_compatibility sees simple dicts of floats
#     score = calc_compatibility(real_vec, fake_vec)

#     return RandomMatchResp(
#         name="Random EchoLogz User",
#         score=score,
#         profile=fake_profile,
#     )


@router.post("/random", response_model=RandomMatchResp)
def post_random_match(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Generate a random synthetic user, compute compatibility against
    the logged-in user (stubbed as id=1), and return score + fake profile.
    """

    # Real user profile from our builder
    real_profile = build_feature_vector(
        db=db,
        user_id=current_user_id,
        sample="medium_term",
    )

    if not real_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to compute musical identity for current user.",
        )

    labels = real_profile["labels"]

    # Fake partner: random scaled values in [0,1]
    import random

    fake_scaled = [random.random() for _ in labels]
    fake_raw = dict(zip(labels, fake_scaled))
    fake_profile: Dict[str, Any] = {
        "labels": labels,
        "raw": fake_raw,
        "scaled": fake_scaled,
    }

    # calc_compatibility expects flat dicts: {feature: value}
    real_vec = {
        label: value
        for label, value in zip(real_profile["labels"], real_profile["scaled"])
    }
    fake_vec = {
        label: value
        for label, value in zip(fake_profile["labels"], fake_profile["scaled"])
    }

    score = calc_compatibility(real_vec, fake_vec)

    return RandomMatchResp(
        name="Random EchoLogz User",
        score=score,
        profile=fake_profile,
    )