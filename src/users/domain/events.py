from dataclasses import dataclass

from src.core.interfaces.events import AbstractEvent


@dataclass(frozen=True)
class UserVotedEvent(AbstractEvent):
    voted_for_user_email: str
    voted_for_user_username: str
    voting_user_email: str
    voting_user_username: str
    liked: bool
    disliked: bool
