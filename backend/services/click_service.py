from backend.repositories.user_repository import UserRepository


class ClickService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def click(self, user_id: int) -> int:
        """
        Perform a single click for a user.
        Returns updated click count.
        """
        return self.repo.increment_click(user_id)
