import pytest

from src.core.interfaces import AbstractModel, AbstractEvent, AbstractCommand
from tests.core.fake_objects import FakeModel, FakeEvent, FakeCommand


@pytest.mark.anyio
async def test_abstract_model_to_dict_basic() -> None:
    abstract_model: AbstractModel = FakeModel()
    assert await abstract_model.to_dict() == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_abstract_model_to_dict_with_exclude_existing_field() -> None:
    abstract_model: AbstractModel = FakeModel()
    assert await abstract_model.to_dict(exclude={'field1'}) == {'field2': 123}


@pytest.mark.anyio
async def test_abstract_model_to_dict_with_exclude_non_existing_field() -> None:
    abstract_model: AbstractModel = FakeModel()
    assert await abstract_model.to_dict(exclude={'some_non_existing_field'}) == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_abstract_model_to_dict_with_include() -> None:
    abstract_model: AbstractModel = FakeModel()
    assert await abstract_model.to_dict(include={'test': 123}) == {'field1': 'test', 'field2': 123, 'test': 123}


@pytest.mark.anyio
async def test_abstract_event_to_dict_basic() -> None:
    abstract_event: AbstractEvent = FakeEvent()
    assert await abstract_event.to_dict() == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_abstract_event_to_dict_with_exclude_existing_field() -> None:
    abstract_event: AbstractEvent = FakeEvent()
    assert await abstract_event.to_dict(exclude={'field1'}) == {'field2': 123}


@pytest.mark.anyio
async def test_abstract_event_to_dict_with_exclude_non_existing_field() -> None:
    abstract_event: AbstractEvent = FakeEvent()
    assert await abstract_event.to_dict(exclude={'some_non_existing_field'}) == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_abstract_event_to_dict_with_include() -> None:
    abstract_event: AbstractEvent = FakeEvent()
    assert await abstract_event.to_dict(include={'test': 123}) == {'field1': 'test', 'field2': 123, 'test': 123}


@pytest.mark.anyio
async def test_abstract_command_to_dict_basic() -> None:
    abstract_command: AbstractCommand = FakeCommand()
    assert await abstract_command.to_dict() == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_abstract_command_to_dict_with_exclude_existing_field() -> None:
    abstract_command: AbstractCommand = FakeCommand()
    assert await abstract_command.to_dict(exclude={'field1'}) == {'field2': 123}


@pytest.mark.anyio
async def test_abstract_command_to_dict_with_exclude_non_existing_field() -> None:
    abstract_command: AbstractCommand = FakeCommand()
    assert await abstract_command.to_dict(exclude={'some_non_existing_field'}) == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_abstract_command_to_dict_with_include() -> None:
    abstract_command: AbstractCommand = FakeCommand()
    assert await abstract_command.to_dict(include={'test': 123}) == {'field1': 'test', 'field2': 123, 'test': 123}
