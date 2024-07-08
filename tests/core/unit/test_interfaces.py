import pytest

from src.core.interfaces import AbstractModel
from tests.core.fake_objects import FakeModel


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
