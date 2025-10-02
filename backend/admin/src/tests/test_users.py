import uuid

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from src.main import app


pytestmark = pytest.mark.asyncio


async def test_get_users(base_url: str):
    """Тест получения списка пользователей."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        response = await client.get('/users/users')
        assert response.status_code == status.HTTP_200_OK


async def test_create_users(base_url: str):
    """Тест создания пользователя."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        response = await client.post(
            '/users/create',
            json={
                'id': str(uuid.uuid4()),
                'phone_number': ''
            }
        )
        assert response.status_code == status.HTTP_200_OK


async def test_get_long_time_lost(base_url: str):
    """Тест получения пользователей, которые давно не заходили."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        response = await client.get('/users/long-time-lost')
        assert response.status_code == status.HTTP_200_OK


async def test_get_questions(base_url: str):
    """Тест получения списка вопросов."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        response = await client.get('/users/questions')
        assert response.status_code == status.HTTP_200_OK


async def test_create_user_question(base_url: str):
    """Тест создания вопроса пользователя."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        user_id = str(uuid.uuid4())
        await client.post(
            '/users/create',
            json={
                'id': user_id,
                'phone_number': ''
            }
        )
        response = await client.post(
            '/users/questions/create',
            json={
                'user_id': user_id,
                'text': ''
            }
        )
        assert response.status_code == status.HTTP_200_OK


async def test_get_user_history(base_url: str):
    """Тест получения истории пользователя."""

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url
    ) as client:
        user_id = str(uuid.uuid4())
        await client.post(
            '/users/create',
            json={
                'id': user_id,
                'phone_number': ''
            }
        )
        response = await client.get(f'/users/{user_id}/history')
        assert response.status_code == status.HTTP_200_OK
