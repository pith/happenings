"""
DB model for User.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserModel(Base):
    """
    SQLAlchemy model for User.
    """

    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"<UserModel(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"  # noqa: E501
