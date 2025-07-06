from happenings.application.AuthenticationService import AuthenticationService
from happenings.domain.user.User import User
from happenings.domain.user.UserRepository import UserRepository


class UserManagementService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def signup(self, username: str, email: str, password: str) -> tuple[str, str]:
        """
        Create a new user and return the user along with access and refresh tokens.
        Raises ValueError if the username or email already exists.
        """
        password_hash = AuthenticationService.hash_password(password)

        user = self.user_repository.create(
            username=username, email=email, password_hash=password_hash
        )
        access_token = AuthenticationService.create_access_token(username=user.username)
        refresh_token = AuthenticationService.create_refresh_token(
            username=user.username
        )
        return access_token, refresh_token

    def login(self, username: str, password: str) -> tuple[str, str]:
        """
        Authenticate a user with username and password.
        """
        user = self.user_repository.find_by_username(username)

        if user and AuthenticationService.verify_password(password, user.password_hash):
            access_token = AuthenticationService.create_access_token(
                username=user.username
            )
            refresh_token = AuthenticationService.create_refresh_token(
                username=user.username
            )
            return access_token, refresh_token

        raise ValueError("Invalid username or password")

    def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        """
        Refresh the access and refresh tokens for a user.
        """
        user_name = AuthenticationService.verify_token(refresh_token, "refresh")
        if user_name is None:
            raise ValueError("Invalid token")

        user = self.user_repository.find_by_username(user_name)
        if user is None:
            raise ValueError("User not found")
        access_token = AuthenticationService.create_access_token(username=user.username)
        refresh_token = AuthenticationService.create_refresh_token(
            username=user.username
        )
        return access_token, refresh_token

    def get_user(self, user_id) -> User | None:
        return self.user_repository.find_by_id(user_id)
