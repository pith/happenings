from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from happenings.application.UserManagementService import UserManagementService

from .dependency_injection import get_user_management_service

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class AuthenticationTokens(BaseModel):
    access_token: str
    refresh_token: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/signup", response_model=AuthenticationTokens, status_code=201)
async def signup(
    request: UserCreate,
    user_management_service: UserManagementService = Depends(
        get_user_management_service
    ),
) -> AuthenticationTokens:
    try:
        access_token, refresh_token = user_management_service.signup(
            request.username, request.email, request.password
        )
        return AuthenticationTokens(
            access_token=access_token, refresh_token=refresh_token
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/login", response_model=AuthenticationTokens, status_code=200)
async def login(
    request: UserLogin,
    user_management_service: UserManagementService = Depends(
        get_user_management_service
    ),
) -> AuthenticationTokens:
    try:
        access_token, refresh_token = user_management_service.login(
            request.username, request.password
        )
        return AuthenticationTokens(
            access_token=access_token, refresh_token=refresh_token
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
