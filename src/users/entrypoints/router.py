from typing import MutableSequence
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, JSONResponse

from src.users.domain.models import UserModel, UserStatisticsModel
from src.users.config import RouterConfig, URLPathsConfig, URLNamesConfig, cookies_config
from src.security.models import JWTDataModel
from src.security.utils import create_jwt_token
from src.users.entrypoints.dependencies import (
    verify_user_credentials,
    register_user,
    get_my_account as get_my_account_dependency,
    get_all_users as get_all_users_dependency,
    get_my_statistics as get_my_statistics_dependency,
    like_user as like_user_dependency,
    dislike_user as dislike_user_dependency
)


router = APIRouter(
    prefix=RouterConfig.PREFIX,
    tags=RouterConfig.tags_list(),
)


@router.post(
    path=URLPathsConfig.REGISTER,
    response_class=JSONResponse,
    name=URLNamesConfig.REGISTER,
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel
)
async def register(user: UserModel = Depends(register_user)):
    return user


@router.post(
    path=URLPathsConfig.LOGIN,
    response_class=Response,
    name=URLNamesConfig.LOGIN,
    status_code=status.HTTP_204_NO_CONTENT
)
async def login(user: UserModel = Depends(verify_user_credentials)):
    jwt_data: JWTDataModel = JWTDataModel(user_id=user.id)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    response: Response = Response()
    response.set_cookie(
        key=cookies_config.COOKIES_KEY,
        value=token,
        secure=cookies_config.SECURE_COOKIES,
        httponly=cookies_config.HTTP_ONLY,
        expires=datetime.now(tz=timezone.utc) + timedelta(days=cookies_config.COOKIES_LIFESPAN_DAYS),
        samesite=cookies_config.SAME_SITE
    )
    return response


@router.get(
    path=URLPathsConfig.LOGOUT,
    response_class=Response,
    name=URLNamesConfig.LOGOUT,
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout():
    response: Response = Response()
    response.delete_cookie(
        key=cookies_config.COOKIES_KEY,
        secure=cookies_config.SECURE_COOKIES,
        httponly=cookies_config.HTTP_ONLY,
        samesite=cookies_config.SAME_SITE
    )
    return response


@router.get(
    path=URLPathsConfig.ME,
    response_class=JSONResponse,
    response_model=UserModel,
    name=URLNamesConfig.ME,
    status_code=status.HTTP_200_OK
)
async def get_my_account(user: UserModel = Depends(get_my_account_dependency)):
    return user


@router.get(
    path=URLPathsConfig.ALL,
    response_class=JSONResponse,
    response_model=MutableSequence[UserModel],
    name=URLNamesConfig.ALL,
    status_code=status.HTTP_200_OK
)
async def get_all_users(users: MutableSequence[UserModel] = Depends(get_all_users_dependency)):
    return users


@router.get(
    path=URLPathsConfig.MY_STATS,
    response_class=JSONResponse,
    response_model=UserStatisticsModel,
    name=URLNamesConfig.MY_STATS,
    status_code=status.HTTP_200_OK
)
async def get_my_statistics(statistics: UserStatisticsModel = Depends(get_my_statistics_dependency)):
    return statistics


@router.patch(
    path=URLPathsConfig.LIKE_USER,
    response_class=JSONResponse,
    response_model=UserStatisticsModel,
    name=URLNamesConfig.LIKE_USER,
    status_code=status.HTTP_200_OK
)
async def like_user(statistics: UserStatisticsModel = Depends(like_user_dependency)):
    return statistics


@router.patch(
    path=URLPathsConfig.DISLIKE_USER,
    response_class=JSONResponse,
    response_model=UserStatisticsModel,
    name=URLNamesConfig.DISLIKE_USER,
    status_code=status.HTTP_200_OK
)
async def dislike_user(statistics: UserStatisticsModel = Depends(dislike_user_dependency)):
    return statistics
