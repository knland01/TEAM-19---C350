"""
Match Router
============

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



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from core.dependencies import get_db
from services.score import compare_users


router = APIRouter(prefix="/match", tags=["match"])

class CompareReq(BaseModel):
    user_a_id: int = Field(ge=1)
    user_b_id: int = Field(ge=1)
    sample: int | None = Field(default=100, ge=1, le=100)

class CompareResp(BaseModel):
    score: float
    pair_id: int | None = None   # db row id if you upsert

@router.post("/compare", response_model=CompareResp)
def post_compare(req: CompareReq, db: Session = Depends(get_db)):
    try:
        res = compare_users(
            db=db,
            user_a_id=req.user_a_id,
            user_b_id=req.user_b_id,
            sample=req.sample,
        )
        return CompareResp(**res)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )