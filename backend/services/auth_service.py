from backend.repositories.user_repository import UserRepository
from backend.models.user import User
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, username: str, password: str) -> User:
        if self.repo.get_by_username(username):
            raise ValueError("Username already exists")

        user = User(
            username=username,
            hashed_password=hash_password(password),
        )
        return self.repo.create(user)

    def login(self, username: str, password: str) -> str:
        user = self.repo.get_by_username(username)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token(str(user.id))
