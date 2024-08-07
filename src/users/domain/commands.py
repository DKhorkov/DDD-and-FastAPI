from dataclasses import dataclass

from src.core.interfaces.commands import AbstractCommand


@dataclass(frozen=True)
class RegisterUserCommand(AbstractCommand):
    username: str
    password: str
    email: str


@dataclass(frozen=True)
class VerifyUserCredentialsCommand(AbstractCommand):
    username: str
    password: str


@dataclass(frozen=True)
class VoteForUserCommand(AbstractCommand):
    voted_for_user_id: int
    voting_user_id: int
    liked: bool
    disliked: bool
