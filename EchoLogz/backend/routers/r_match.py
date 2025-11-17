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

Typical Usage Example:
----------------------
POST /match/compare

Request Body:
{
    "user_a_id": 12,
    "user_b_id": 37,
    "sample": 100
}

Response Body:
{
    "score": 0.83,
    "pair_id": 58
}
"""

# INTERNAL MODULES:
from backend.core.dependencies import get_db
from backend.services.score import calc_compatibility
from ..services.feature_vectors import build_feature_vector

# EXTERNAL MODULES:
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field



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
        score = calc_compatibility(user_a_vec, user_b_vec) # Compute compatibility using the math-only engine.
        pair_id = None # look up / store a pair_id (?)
        return CompareResp(score=score, pair_id=pair_id)
    except ValueError as e: # bad-input - features or math
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )