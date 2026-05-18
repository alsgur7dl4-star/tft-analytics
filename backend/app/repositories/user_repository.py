from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email.lower()))

    def create(self, email: str, nickname: str, password_hash: str, role: UserRole = UserRole.USER) -> User:
        user = User(email=email.lower(), nickname=nickname, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.flush()
        return user

