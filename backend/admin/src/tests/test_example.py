import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from src.main import app


pytestmark = pytest.mark.asyncio


async def test_example(base_url: str):
    """Пример теста."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        # совершим запрос на получение дерефа навигации
        response = await client.get('/menu/')
        assert response.status_code == status.HTTP_200_OK
