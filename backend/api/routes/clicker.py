from fastapi import APIRouter, Depends

from backend.api.deps import get_db, get_current_user
from backend.repositories.user_repository import UserRepository
from backend.services.click_service import ClickService

router = APIRouter(prefix="/click", tags=["clicker"])


@router.post("")
def click(
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    service = ClickService(UserRepository(db))
    new_count = service.click(user.id)
    return {"click_count": new_count}
