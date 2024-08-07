import pytest
from typing import Dict, List, Type, Any, Union

from src.core.interfaces import (
    AbstractEvent,
    AbstractCommand,
    AbstractCommandHandler,
    AbstractEventHandler,
    AbstractUnitOfWork
)
from src.core.messagebus import MessageBus
from src.core.bootstrap import Bootstrap
from tests.core.fake_objects import (
    FakeEvent,
    FakeCommand,
    FakeCommandHandler,
    FakeEventHandler,
    FakeCoreUnitOfWork
)


@pytest.mark.anyio
async def test_bootstrap_inject_dependencies_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    dependencies: Dict[str, Any] = await FakeEvent().to_dict()
    events_handlers_for_injection: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
        FakeEvent: [FakeEventHandler]
    }

    bootstrap: Bootstrap = Bootstrap(
        uow=uow,
        events_handlers_for_injection=events_handlers_for_injection,
        commands_handlers_for_injection={},
        dependencies=dependencies
    )

    injected_handler: Union[AbstractEventHandler | AbstractCommandHandler] = await bootstrap._inject_dependencies(
        handler=FakeEventHandler
    )

    assert isinstance(injected_handler, FakeEventHandler)
    expected_handler: FakeEventHandler = FakeEventHandler(uow=uow, field1='test', field2=123)
    assert injected_handler == expected_handler


@pytest.mark.anyio
async def test_bootstrap_inject_dependencies_fail_not_all_dependencies_provided() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    events_handlers_for_injection: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
        FakeEvent: [FakeEventHandler]
    }

    bootstrap: Bootstrap = Bootstrap(
        uow=uow,
        events_handlers_for_injection=events_handlers_for_injection,
        commands_handlers_for_injection={}
    )

    with pytest.raises(TypeError):
        await bootstrap._inject_dependencies(handler=FakeEventHandler)


@pytest.mark.anyio
async def test_bootstrap_get_messagebus_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    dependencies: Dict[str, Any] = await FakeEvent().to_dict()
    events_handlers_for_injection: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
        FakeEvent: [FakeEventHandler]
    }

    command_handlers_for_injection: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
        FakeCommand: FakeCommandHandler
    }

    bootstrap: Bootstrap = Bootstrap(
        uow=uow,
        events_handlers_for_injection=events_handlers_for_injection,
        commands_handlers_for_injection=command_handlers_for_injection,
        dependencies=dependencies
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    assert messagebus._command_handlers == {
        FakeCommand: FakeCommandHandler(uow=uow, field1='test', field2=123)
    }

    assert messagebus._event_handlers == {
        FakeEvent: [FakeEventHandler(uow=uow, field1='test', field2=123)]
    }
