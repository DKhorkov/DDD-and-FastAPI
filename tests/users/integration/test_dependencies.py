import pytest
from datetime import datetime, timezone
from typing import List

from src.users.exceptions import (
    UserAlreadyExistsError,
    InvalidPasswordError,
    UserNotFoundError,
)
from src.security.exceptions import InvalidTokenError
from src.users.models import UserModel
from src.security.models import JWTDataModel
from src.users.schemas import RegisterUserScheme, LoginUserScheme
from src.security.utils import create_jwt_token
from tests.config import FakeUserConfig
from src.users.dependencies import (
    register_user,
    authenticate_user,
    verify_user_credentials,
    get_my_account,
    get_all_users
)


@pytest.mark.anyio
async def test_register_user_success(create_test_db: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    user: UserModel = await register_user(user_data=user_data)

    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL
    


@pytest.mark.anyio
async def test_register_user_fail(create_test_user: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserAlreadyExistsError):
        await register_user(user_data=user_data)


@pytest.mark.anyio
async def test_verify_user_credentials_by_username_success(create_test_user: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(username=FakeUserConfig.USERNAME, password=FakeUserConfig.PASSWORD)
    user: UserModel = await verify_user_credentials(user_data=user_data)

    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL


@pytest.mark.anyio
async def test_verify_user_credentials_by_email_success(create_test_user: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(username=FakeUserConfig.EMAIL, password=FakeUserConfig.PASSWORD)
    user: UserModel = await verify_user_credentials(user_data=user_data)

    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL


@pytest.mark.anyio
async def test_verify_user_credentials_fail_user_does_not_exist(create_test_db: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserNotFoundError):
        await verify_user_credentials(user_data=user_data)


@pytest.mark.anyio
async def test_verify_user_credentials_fail_incorrect_password(create_test_user: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    user_data.password = 'some_incorrect_password'
    with pytest.raises(InvalidPasswordError):
        await verify_user_credentials(user_data=user_data)


@pytest.mark.anyio
async def test_authenticate_user_success(create_test_db: None, access_token: str) -> None:
    user: UserModel = await authenticate_user(token=access_token)
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME
    

@pytest.mark.anyio
async def test_authenticate_user_fail_invalid_token(create_test_db: None) -> None:
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token='someInvalidToken')


@pytest.mark.anyio
async def test_authenticate_user_fail_token_expired(create_test_db: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1, exp=datetime.now(timezone.utc))
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token=token)


@pytest.mark.anyio
async def test_authenticate_user_fail_user_does_not_exist(create_test_db: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(UserNotFoundError):
        await authenticate_user(token=token)


@pytest.mark.anyio
async def test_get_all_users_with_existing_user(create_test_user: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 1
    user: UserModel = users[0]
    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL
    

@pytest.mark.anyio
async def test_get_all_users_without_existing_users(create_test_db: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 0


@pytest.mark.anyio
async def test_get_my_account_success(create_test_db: None, access_token: str) -> None:
    user: UserModel = await get_my_account(token=access_token)
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_aget_my_account_fail_user_does_not_exist(create_test_db: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(UserNotFoundError):
        await get_my_account(token=token)
