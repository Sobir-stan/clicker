from backend.repositories.user_repository import UserRepository


class RankingService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_my_score(self, user_id: int) -> int:
        return self.repo.get_click_count(user_id)

    def get_leaderboard(self, limit: int = 10):
        return self.repo.get_top_users(limit)
