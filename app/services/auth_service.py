# Authentication service
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth import verify_password
from app.services.user_service import get_user_by_username
from typing import Optional


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
