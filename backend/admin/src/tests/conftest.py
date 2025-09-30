import pytest_asyncio


@pytest_asyncio.fixture
async def base_url():
    """Возвращает базовый url для запросов."""

    return 'http://admin-tests/api/v1'
