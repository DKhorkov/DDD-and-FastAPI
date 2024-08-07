import inspect
from types import MappingProxyType
from typing import Union, Type, Dict, Any, List, Optional

from src.core.interfaces import (
    AbstractCommand,
    AbstractEvent,
    AbstractUnitOfWork,
    AbstractEventHandler,
    AbstractCommandHandler
)
from src.core.messagebus import MessageBus


class Bootstrap:
    """
    Bootstrap class for Dependencies Injection purposes.
    """

    def __init__(
            self,
            uow: AbstractUnitOfWork,
            events_handlers_for_injection: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]],
            commands_handlers_for_injection: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]],
            dependencies: Optional[Dict[str, Any]] = None
    ) -> None:

        self._uow: AbstractUnitOfWork = uow
        self._dependencies: Dict[str, Any] = {'uow': self._uow}
        self._events_handlers_for_injection: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = (
            events_handlers_for_injection
        )
        self._commands_handlers_for_injection: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = (
            commands_handlers_for_injection
        )

        if dependencies:
            self._dependencies.update(dependencies)

    async def get_messagebus(self) -> MessageBus:
        """
        Makes necessary injections to commands handlers and events handlers for creating appropriate messagebus,
        after which returns messagebus instance.
        """

        injected_event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = {
            event_type: [
                await self._inject_dependencies(handler=handler)
                for handler in event_handlers
            ]
            for event_type, event_handlers in self._events_handlers_for_injection.items()
        }

        injected_command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler] = {
            command_type: await self._inject_dependencies(handler=handler)
            for command_type, handler in self._commands_handlers_for_injection.items()
        }

        return MessageBus(
            uow=self._uow,
            event_handlers=injected_event_handlers,
            command_handlers=injected_command_handlers,
        )

    async def _inject_dependencies(
            self,
            handler: Union[Type[AbstractEventHandler], Type[AbstractCommandHandler]]
    ) -> Union[AbstractEventHandler, AbstractCommandHandler]:

        """
        Inspecting handler to know its signature and init params, after which only necessary dependencies will be
        injected to the handler.
        """

        params: MappingProxyType[str, inspect.Parameter] = inspect.signature(handler).parameters
        handler_dependencies: Dict[str, Any] = {
            name: dependency
            for name, dependency in self._dependencies.items()
            if name in params
        }
        return handler(**handler_dependencies)
