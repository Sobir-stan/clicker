from fastapi import APIRouter
from backend.api.routes import auth, clicker, ranking, pages

router = APIRouter()
router.include_router(auth.router)
router.include_router(clicker.router)
router.include_router(ranking.router)
router.include_router(pages.router)