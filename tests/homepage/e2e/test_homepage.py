import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.config import URLPathsConfig


@pytest.mark.anyio
async def test_homepage(async_client: AsyncClient) -> None:
    response: Response = await async_client.get(url=URLPathsConfig.HOMEPAGE)
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.has_redirect_location
