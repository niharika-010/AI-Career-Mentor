import pytest
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analysis import AnalysisHistory
from app.models.user import User

@pytest.mark.asyncio
async def test_analysis_history_model_persistence(db_session: AsyncSession):
    u = User(id=str(uuid.uuid4()), email="hist_user@example.com", hashed_password="hashed_pw")
    db_session.add(u)
    await db_session.commit()

    history_entry = AnalysisHistory(
        user_id=u.id,
        target_role="ML Engineer",
        overall_score=82.0,
        ats_score=91.0,
        confidence_score=94.0,
        action="Resume Match Evaluation",
    )
    db_session.add(history_entry)
    await db_session.commit()

    stmt = select(AnalysisHistory).where(AnalysisHistory.id == history_entry.id)
    saved = (await db_session.execute(stmt)).scalar_one_or_none()
    assert saved is not None
    assert saved.target_role == "ML Engineer"
    assert saved.overall_score == 82.0
    assert saved.ats_score == 91.0
    assert saved.user_id == u.id


@pytest.mark.asyncio
async def test_analysis_history_multiple_roles(db_session: AsyncSession):
    u = User(id=str(uuid.uuid4()), email="hist_user2@example.com", hashed_password="hashed_pw")
    db_session.add(u)
    await db_session.commit()

    roles = [
        ("ML Engineer", 82.0),
        ("Data Scientist", 76.0),
        ("AI Engineer", 88.0),
        ("Data Analyst", 71.0),
    ]

    for role, score in roles:
        entry = AnalysisHistory(
            user_id=u.id,
            target_role=role,
            overall_score=score,
        )
        db_session.add(entry)
    await db_session.commit()

    stmt = select(AnalysisHistory).where(AnalysisHistory.user_id == u.id).order_by(AnalysisHistory.overall_score.desc())
    user_entries = (await db_session.execute(stmt)).scalars().all()

    assert len(user_entries) == 4
    top_entry = user_entries[0]
    assert top_entry.target_role == "AI Engineer"
    assert top_entry.overall_score == 88.0
