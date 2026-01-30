from sqlalchemy import update, select
from sqlalchemy.orm import Session

from backend.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalar(stmt)

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.db.scalar(stmt)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


    def increment_click(self, user_id: int) -> int:
        # 1. Atomic increment
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(click_count=User.click_count + 1)
        )
        self.db.execute(stmt)
        self.db.commit()

        # 2. Fetch updated value
        stmt = select(User.click_count).where(User.id == user_id)
        return self.db.scalar(stmt)

