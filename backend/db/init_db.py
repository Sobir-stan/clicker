from backend.db.base import Base
from backend.db.session import engine

from backend.models.user import User  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)
