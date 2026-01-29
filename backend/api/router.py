from fastapi import APIRouter
from backend.api.routes import auth

router = APIRouter()
router.include_router(auth.router)
