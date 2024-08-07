import pytest
from typing import Dict, List, Type, no_type_check

from src.core.exceptions import MessageBusMessageError
from src.core.interfaces import (
    AbstractEvent,
    AbstractCommand,
    AbstractCommandHandler,
    AbstractEventHandler,
    AbstractUnitOfWork
)
from src.core.messagebus import MessageBus
from tests.core.fake_objects import (
    FakeEvent,
    FakeCommand,
    FakeCommandHandler,
    FakeEventHandler,
    FakeCoreUnitOfWork
)


@pytest.mark.anyio
async def test_messagebus_handle_event_with_single_handler_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    fake_event_handler: FakeEventHandler = FakeEventHandler(uow=uow, field1='test_value', field2=123)
    event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = {FakeEvent: [fake_event_handler]}
    assert not fake_event_handler.called

    messagebus: MessageBus = MessageBus(uow=uow, event_handlers=event_handlers, command_handlers={})
    await messagebus._handle_event(event=FakeEvent())
    assert fake_event_handler.called


@pytest.mark.anyio
async def test_messagebus_handle_event_with_recursion_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    fake_event_handler: FakeEventHandler = FakeEventHandler(
        uow=uow,
        field1='test_value',
        field2=123,
        create_recursion_event=True
    )

    event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = {FakeEvent: [fake_event_handler]}
    assert not fake_event_handler.called

    messagebus: MessageBus = MessageBus(uow=uow, event_handlers=event_handlers, command_handlers={})
    await messagebus._handle_event(event=FakeEvent())
    assert fake_event_handler.called


@pytest.mark.anyio
async def test_messagebus_handle_event_with_multiple_handlers_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    first_fake_event_handler: FakeEventHandler = FakeEventHandler(uow=uow, field1='test_value', field2=123)
    second_fake_event_handler: FakeEventHandler = FakeEventHandler(uow=uow, field1='test_value', field2=123)
    event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = {
        FakeEvent: [first_fake_event_handler, second_fake_event_handler],
    }

    assert not first_fake_event_handler.called
    assert not second_fake_event_handler.called

    messagebus: MessageBus = MessageBus(uow=uow, event_handlers=event_handlers, command_handlers={})
    await messagebus._handle_event(event=FakeEvent())
    assert first_fake_event_handler.called
    assert second_fake_event_handler.called


@pytest.mark.anyio
async def test_messagebus_handle_event_fail_no_event_type_in_handlers() -> None:
    with pytest.raises(KeyError):
        messagebus: MessageBus = MessageBus(uow=FakeCoreUnitOfWork(), event_handlers={}, command_handlers={})
        await messagebus._handle_event(event=FakeEvent())


@pytest.mark.anyio
async def test_messagebus_handle_command_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    fake_command_handler: FakeCommandHandler = FakeCommandHandler(uow=uow, field1='test_value', field2=123)
    command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler] = {FakeCommand: fake_command_handler}
    assert not fake_command_handler.called

    messagebus: MessageBus = MessageBus(uow=uow, event_handlers={}, command_handlers=command_handlers)
    await messagebus._handle_command(command=FakeCommand())
    assert fake_command_handler.called


@pytest.mark.anyio
async def test_messagebus_handle_command_fail_no_command_type_in_handlers() -> None:
    with pytest.raises(KeyError):
        messagebus: MessageBus = MessageBus(uow=FakeCoreUnitOfWork(), event_handlers={}, command_handlers={})
        await messagebus._handle_command(command=FakeCommand())


@pytest.mark.anyio
async def test_messagebus_handle_command_which_creates_events_success() -> None:
    uow: AbstractUnitOfWork = FakeCoreUnitOfWork()
    fake_event_handler: FakeEventHandler = FakeEventHandler(uow=uow, field1='test_value', field2=123)
    event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = {FakeEvent: [fake_event_handler]}
    fake_command_handler: FakeCommandHandler = FakeCommandHandler(uow=uow, field1='test_value', field2=123)
    command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler] = {FakeCommand: fake_command_handler}
    assert not fake_event_handler.called
    assert not fake_command_handler.called

    messagebus: MessageBus = MessageBus(uow=uow, event_handlers=event_handlers, command_handlers=command_handlers)
    await messagebus.handle(message=FakeCommand())
    assert fake_command_handler.called
    assert fake_event_handler.called


@pytest.mark.anyio
@no_type_check  # Avoiding type checks due to incorrect message type, provided to MessageBus
async def test_messagebus_handle_fail_incorrect_message_type() -> None:
    messagebus: MessageBus = MessageBus(uow=FakeCoreUnitOfWork(), event_handlers={}, command_handlers={})
    with pytest.raises(MessageBusMessageError):
        await messagebus.handle('SomeMessage')
