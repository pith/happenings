class User:
    """
    Domain model for User.
    """

    def __init__(self, id: int, username: str, email: str, password_hash: str):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        }
