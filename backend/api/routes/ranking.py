from fastapi import APIRouter, Depends, Query

from backend.api.deps import get_db, get_current_user
from backend.repositories.user_repository import UserRepository
from backend.services.ranking_service import RankingService

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("/me")
def my_score(
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    service = RankingService(UserRepository(db))
    return {"click_count": service.get_my_score(user.id)}


@router.get("/top")
def leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db=Depends(get_db),
):
    service = RankingService(UserRepository(db))
    results = service.get_leaderboard(limit)
    return [
        {"username": username, "click_count": click_count}
        for username, click_count in results
    ]
