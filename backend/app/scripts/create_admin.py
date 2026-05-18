from getpass import getpass

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository


def main() -> None:
    email = input("Admin email: ").strip().lower()
    nickname = input("Admin nickname: ").strip()
    password = getpass("Admin password: ")
    with SessionLocal() as db:
        users = UserRepository(db)
        existing = users.get_by_email(email)
        if existing:
            existing.role = UserRole.ADMIN
            existing.password_hash = hash_password(password)
            existing.nickname = nickname or existing.nickname
            db.add(existing)
        else:
            users.create(email=email, nickname=nickname, password_hash=hash_password(password), role=UserRole.ADMIN)
        db.commit()
    print("Admin account is ready.")


if __name__ == "__main__":
    main()

