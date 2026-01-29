from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.repositories.user_repository import UserRepository
from backend.services.auth_service import AuthService
from backend.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(UserRepository(db))
    try:
        user = service.register(data.username, data.password)
        return {"id": user.id, "username": user.username}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(UserRepository(db))
    try:
        token = service.login(data.username, data.password)
        return {"access_token": token}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
