from typing import Annotated

from fastapi import Depends, Header, status
from sqlalchemy.orm import Session

from app.core import error_codes
from app.core.database import get_db_session
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository

DbSession = Annotated[Session, Depends(get_db_session)]


def get_current_user(
    db: DbSession,
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AppException(error_codes.AUTH_REQUIRED, "Authentication is required", status.HTTP_401_UNAUTHORIZED)
    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        raise AppException(error_codes.AUTH_REQUIRED, "Invalid access token", status.HTTP_401_UNAUTHORIZED)
    user = UserRepository(db).get_by_id(int(payload["sub"]))
    if not user or not user.is_active:
        raise AppException(error_codes.AUTH_REQUIRED, "User is not active", status.HTTP_401_UNAUTHORIZED)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(current_user: CurrentUser) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AppException(error_codes.AUTH_FORBIDDEN, "Admin permission is required", status.HTTP_403_FORBIDDEN)
    return current_user


AdminUser = Annotated[User, Depends(require_admin)]

