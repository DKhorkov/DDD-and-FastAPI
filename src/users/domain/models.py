from dataclasses import dataclass

from src.core.interfaces import AbstractModel


@dataclass
class UserModel(AbstractModel):
    email: str
    password: str
    username: str

    # Optional args:
    id: int = 0


@dataclass
class UserStatisticsModel(AbstractModel):
    user_id: int

    # Optional args:
    id: int = 0
    likes: int = 0
    dislikes: int = 0


@dataclass
class UserVoteModel(AbstractModel):
    voting_user_id: int  # Who votes
    voted_for_user_id: int  # Votes for who

    # Optional args:
    id: int = 0
