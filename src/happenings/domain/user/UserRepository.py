from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from happenings.infrastructure.persistence import UserModel

from .User import User


class UserRepository:
    def __init__(self, db: Session):
        self.session = db

    def find_by_id(self, user_id: int) -> User | None:
        user_model = (
            self.session.query(UserModel).filter(UserModel.id == user_id).first()
        )

        if user_model is None:
            return None
        return self._model_to_entity(user_model)

    def find_by_username(self, username: str) -> User | None:
        user_model = (
            self.session.query(UserModel).filter(UserModel.username == username).first()
        )

        if user_model is None:
            return None
        return self._model_to_entity(user_model)

    def create(self, username: str, email: str, password_hash: str) -> User:
        user_model = UserModel(
            username=username, email=email, password_hash=password_hash
        )
        try:
            self.session.add(user_model)
            self.session.commit()
            self.session.refresh(user_model)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("User already exists with this username or email")
        return self._model_to_entity(user_model)

    def _model_to_entity(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password_hash=user_model.password_hash,
        )
