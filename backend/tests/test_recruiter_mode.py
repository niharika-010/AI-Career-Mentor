import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.api.v1.endpoints.recruiter import get_recruiter_candidates, ETHICAL_ALIGNMENT_DISCLAIMER

@pytest.mark.asyncio
async def test_recruiter_candidates_data(db_session: AsyncSession):
    u = User(id=str(uuid.uuid4()), email="recruiter_test@example.com", hashed_password="hashed_pw")
    db_session.add(u)
    await db_session.commit()

    res = get_recruiter_candidates(db=db_session, current_user=u)
    assert isinstance(res, dict)
    assert "candidates" in res
    assert "disclaimer" in res
    assert "alignment_label" in res

    # Verify ethical wording guardrail
    assert "Resume-to-role alignment estimate" in res["alignment_label"]
    assert "predict" not in res["alignment_label"].lower()

    candidates = res["candidates"]
    assert len(candidates) == 4

    # Verify candidates match prompt requirements
    priya = candidates[0]
    assert priya["name"] == "Priya"
    assert priya["match_score"] == 94
    assert priya["ats_score"] == 91
    assert priya["status"] == "Strong"

    rahul = candidates[1]
    assert rahul["name"] == "Rahul"
    assert rahul["match_score"] == 88
    assert rahul["ats_score"] == 86
    assert rahul["status"] == "Strong"

    ananya = candidates[2]
    assert ananya["name"] == "Ananya"
    assert ananya["match_score"] == 82
    assert ananya["ats_score"] == 79
    assert ananya["status"] == "Review"

    kiran = candidates[3]
    assert kiran["name"] == "Kiran"
    assert kiran["match_score"] == 64
    assert kiran["ats_score"] == 70
    assert kiran["status"] == "Reject"
