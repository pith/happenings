from datetime import datetime, timedelta
from typing import Literal

import bcrypt
import jwt
from pydantic import BaseModel

from happenings.infrastructure.config import Settings


class InvalidTokenError(Exception):
    """
    Error raised when a JWT token is invalid.
    This can occur due to various reasons such as expiration, invalid signature, etc.
    """

    pass


class TokenPayload(BaseModel):
    """
    Data model for JWT token payload.
    """

    sub: str
    exp: datetime
    type: Literal["access", "refresh"]


class AuthenticationService:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def create_access_token(username: str):
        settings = Settings()
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token_payload = TokenPayload(sub=username, exp=expire, type="access")
        encoded_jwt = jwt.encode(
            token_payload.model_dump(),
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(username: str):
        settings = Settings()
        expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        token_payload = TokenPayload(sub=username, exp=expire, type="refresh")
        encoded_jwt = jwt.encode(
            token_payload.model_dump(),
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: Literal["access", "refresh"]) -> str:
        settings = Settings()
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_payload = TokenPayload(**payload)

            if token_payload.sub is None or token_payload.type != token_type:
                raise InvalidTokenError(
                    f"Invalid {token_type} token or missing user ID"
                )

            return token_payload.sub
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError(f"{token_type.capitalize()} token has expired")
        except jwt.InvalidSignatureError:
            raise InvalidTokenError(
                f"{token_type.capitalize()} token has invalid signature"
            )
        except jwt.DecodeError as e:
            raise InvalidTokenError(f"Failed to decode {token_type} token: {str(e)}")
        except jwt.PyJWTError as e:
            raise InvalidTokenError(f"JWT validation error: {str(e)}")
