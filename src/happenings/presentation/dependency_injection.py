from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from happenings.application import (
    AuthenticationService,
    InvalidTokenError,
    UserManagementService,
)
from happenings.domain.user import User, UserRepository
from happenings.infrastructure.persistence import get_db

security = HTTPBearer()


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_user_management_service(
    user_repository: UserRepository = Depends(get_user_repository),
):
    return UserManagementService(user_repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    try:
        username = AuthenticationService.verify_token(credentials.credentials, "access")
        user = user_repository.find_by_username(username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
