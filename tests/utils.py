import os
from random import choice
from string import ascii_uppercase
from typing import Dict, Any, Optional
from httpx import Response
from starlette.requests import Request
from starlette.datastructures import Headers

from src.core.database.config import database_config


def get_base_url() -> str:
    host: str = os.environ.get('HOST', '0.0.0.0')
    port: str = os.environ.get('PORT', '8000')
    return f'http://{host}:{port}'


def drop_test_db() -> None:
    if os.path.exists(database_config.DATABASE_NAME):
        os.remove(database_config.DATABASE_NAME)


def get_error_message_from_response(response: Response) -> str:
    response_content: Dict[str, Any] = response.json()
    try:
        return response_content['detail'][0]['msg']
    except TypeError:
        return response_content['detail']


def generate_random_string(length: int) -> str:
    return ''.join(choice(ascii_uppercase) for _ in range(length))


def build_request(
        method: str = 'GET',
        server: str = 'www.example.com',
        path: str = '/',
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
) -> Request:

    """
    Builds a mock request object for testing.

    https://stackoverflow.com/questions/62231022/how-to-programmatically-instantiate-starlettes-request-with-a-body
    """

    if headers is None:
        headers = {}

    request = Request(
        {
            'type': 'http',
            'path': path,
            'headers': Headers(headers).raw,
            'http_version': '1.1',
            'method': method,
            'scheme': 'https',
            'client': ('127.0.0.1', 8080),
            'server': (server, 443),
        }
    )

    if body:
        async def request_body():
            return body

        request.body = request_body
    return request
