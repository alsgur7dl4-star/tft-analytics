from fastapi import status
from sqlalchemy.orm import Session

from app.core import error_codes
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_token_expires_at,
    verify_password,
)
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.refresh_tokens = RefreshTokenRepository(db)

    def register(self, data: UserCreate) -> tuple[User, str, str]:
        if self.users.get_by_email(data.email):
            raise AppException(error_codes.AUTH_EMAIL_EXISTS, "Email is already registered", status.HTTP_409_CONFLICT)
        user = self.users.create(data.email, data.nickname, hash_password(data.password))
        access_token, refresh_token = self._issue_tokens(user)
        self.db.commit()
        return user, access_token, refresh_token

    def login(self, data: LoginRequest) -> tuple[User, str, str]:
        user = self.users.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise AppException(error_codes.AUTH_INVALID_CREDENTIALS, "Invalid email or password", status.HTTP_401_UNAUTHORIZED)
        access_token, refresh_token = self._issue_tokens(user)
        self.db.commit()
        return user, access_token, refresh_token

    def refresh(self, refresh_token: str | None) -> tuple[User, str, str]:
        if not refresh_token:
            raise AppException(error_codes.AUTH_REFRESH_INVALID, "Refresh token is missing", status.HTTP_401_UNAUTHORIZED)
        token_hash = hash_refresh_token(refresh_token)
        stored_token = self.refresh_tokens.get_valid_by_hash(token_hash)
        if not stored_token:
            raise AppException(error_codes.AUTH_REFRESH_INVALID, "Refresh token is invalid", status.HTTP_401_UNAUTHORIZED)
        self.refresh_tokens.revoke(stored_token)
        user = stored_token.user
        access_token, new_refresh_token = self._issue_tokens(user)
        self.db.commit()
        return user, access_token, new_refresh_token

    def logout(self, refresh_token: str | None) -> None:
        if refresh_token:
            stored_token = self.refresh_tokens.get_valid_by_hash(hash_refresh_token(refresh_token))
            if stored_token:
                self.refresh_tokens.revoke(stored_token)
                self.db.commit()

    def _issue_tokens(self, user: User) -> tuple[str, str]:
        access_token = create_access_token(str(user.id), {"role": user.role.value})
        refresh_token = generate_refresh_token()
        self.refresh_tokens.create(user.id, hash_refresh_token(refresh_token), refresh_token_expires_at())
        return access_token, refresh_token

