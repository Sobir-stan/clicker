from fastapi import APIRouter
from backend.api.routes import auth, clicker

router = APIRouter()
router.include_router(auth.router)
router.include_router(clicker.router)
