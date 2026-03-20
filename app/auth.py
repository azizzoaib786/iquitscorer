from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from typing import Optional
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Session token signing
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production-please")
serializer = URLSafeTimedSerializer(SECRET_KEY)


def hash_password(password: str) -> str:
    # Hash password with bcrypt
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify password against hash
    return pwd_context.verify(plain_password, hashed_password)


def create_session_token(user_id: str) -> str:
    # Create signed session token
    return serializer.dumps(user_id, salt="session")


def verify_session_token(token: str, max_age: int = 86400 * 7) -> Optional[str]:
    # Verify and extract user_id from token (7 days default)
    try:
        return serializer.loads(token, salt="session", max_age=max_age)
    except:
        return None
