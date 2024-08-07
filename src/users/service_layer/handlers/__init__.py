from typing import List, Dict, Type

from src.core.interfaces.events import AbstractEvent
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.users.domain.events import (
    UserVotedEvent
)
from src.users.domain.commands import (
    RegisterUserCommand,
    VoteForUserCommand,
    VerifyUserCredentialsCommand
)
from src.users.service_layer.handlers.event_handlers import (
    SendVoteNotificationMessageEventHandler,
)
from src.users.service_layer.handlers.command_handlers import (
    RegisterUserCommandHandler,
    VerifyUserCredentialsCommandHandler,
    VoteForUserCommandHandler
)


EVENTS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
    UserVotedEvent: [SendVoteNotificationMessageEventHandler],
}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
    RegisterUserCommand: RegisterUserCommandHandler,
    VoteForUserCommand: VoteForUserCommandHandler,
    VerifyUserCredentialsCommand: VerifyUserCredentialsCommandHandler,
}
