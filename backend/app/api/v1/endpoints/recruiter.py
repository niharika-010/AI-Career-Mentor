from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User

router = APIRouter()

ETHICAL_ALIGNMENT_DISCLAIMER = (
    "Resume-to-role alignment estimate based on skill overlap, semantic similarity, and ATS criteria. "
    "This score does not predict hiring outcomes."
)

@router.get("/candidates")
def get_recruiter_candidates(
    db: Any = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """Retrieves enterprise candidate scoreboard for recruiter screening with ethical alignment disclaimer."""
    candidates = [
        {
            "id": "cand-priya",
            "name": "Priya",
            "email": "priya@example.com",
            "match_score": 94,
            "ats_score": 91,
            "status": "Strong",
            "skills_matched": ["Python", "Machine Learning", "PyTorch", "FastAPI", "SQL"],
        },
        {
            "id": "cand-rahul",
            "name": "Rahul",
            "email": "rahul@example.com",
            "match_score": 88,
            "ats_score": 86,
            "status": "Strong",
            "skills_matched": ["Python", "TensorFlow", "PostgreSQL", "Docker"],
        },
        {
            "id": "cand-ananya",
            "name": "Ananya",
            "email": "ananya@example.com",
            "match_score": 82,
            "ats_score": 79,
            "status": "Review",
            "skills_matched": ["Python", "SQL", "Pandas", "Scikit-Learn"],
        },
        {
            "id": "cand-kiran",
            "name": "Kiran",
            "email": "kiran@example.com",
            "match_score": 64,
            "ats_score": 70,
            "status": "Reject",
            "skills_matched": ["Java", "SQL"],
        },
    ]

    return {
        "disclaimer": ETHICAL_ALIGNMENT_DISCLAIMER,
        "alignment_label": "Resume-to-role alignment estimate",
        "job_title": "Machine Learning Engineer",
        "candidates": candidates,
    }
