from datetime import datetime, timezone
from jose import jwt, JWTError, ExpiredSignatureError

from src.security.config import jwt_config
from src.security.models import JWTDataModel
from src.security.exceptions import InvalidTokenError


async def create_jwt_token(jwt_data: JWTDataModel) -> str:
    jwt_token: str = jwt.encode(
        claims=jwt_data.model_dump(),
        key=jwt_config.JWT_TOKEN_SECRET_KEY,
        algorithm=jwt_config.JWT_TOKEN_ALGORITHM
    )
    return jwt_token


async def parse_jwt_token(token: str) -> JWTDataModel:
    """
    Decodes a JWT token, checks, if token is valid and hadn't expired and returns a JWTData object,
    which represents token data.
    """

    try:
        payload = jwt.decode(token, jwt_config.JWT_TOKEN_SECRET_KEY, algorithms=[jwt_config.JWT_TOKEN_ALGORITHM])
        payload['exp'] = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)  # converting to datetime format
    except (JWTError, ExpiredSignatureError):
        raise InvalidTokenError

    jwt_data: JWTDataModel = JWTDataModel(**payload)
    if jwt_data.exp < datetime.now(tz=timezone.utc):
        raise InvalidTokenError

    return jwt_data
