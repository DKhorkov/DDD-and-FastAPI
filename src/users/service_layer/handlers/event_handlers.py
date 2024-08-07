from src.users.interfaces.handlers import UsersEventHandler
from src.users.domain.events import (
    UserVotedEvent
)
from src.celery.tasks.users_tasks import send_vote_notification_message


class SendVoteNotificationMessageEventHandler(UsersEventHandler):

    async def __call__(self, event: UserVotedEvent) -> None:
        send_vote_notification_message.delay(**await event.to_dict())
