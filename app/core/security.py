from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import uuid

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    password = password[:72]
    return pwd_context.verify(password, hashed)


def _create_token(subject: Any, token_type: str, expires_delta: timedelta, extra: dict = {}) -> str:
    """Hàm nội bộ tạo JWT với type và thời hạn tùy chỉnh."""
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": str(subject),
        "exp": expire,
        "type": token_type,
        **extra,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: int, email: str, role: str) -> str:
    """
    Tạo Access Token (ngắn hạn).
    Chứa user_id, email, role để tránh truy vấn DB mỗi request.
    """
    return _create_token(
        subject=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        extra={"email": email, "role": role},
    )


def create_refresh_token(user_id: int) -> str:
    """
    Tạo Refresh Token (dài hạn).
    Chỉ chứa user_id — dùng để cấp access token mới.
    """
    return _create_token(
        subject=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def create_reset_token(email: str) -> str:
    """
    Tạo Reset Token (ngắn hạn).
    Subject là email thay vì user_id để dễ tìm user khi reset.
    """
    return _create_token(
        subject=email,
        token_type="reset",
        expires_delta=timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES),
    )


def decode_token(token: str, expected_type: Optional[str] = None) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if expected_type and payload.get("type") != expected_type:
            return None

        return payload

    except JWTError:
        return None