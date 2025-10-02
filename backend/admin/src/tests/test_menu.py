# import pytest
# import pytest_asyncio
# from fastapi import status
# from httpx import ASGITransport, AsyncClient
# from src.main import app
# from uuid import uuid4, UUID
# from datetime import datetime, timedelta
# import random
#
# pytestmark = pytest.mark.asyncio
#
#
# @pytest_asyncio.fixture
# async def client(base_url: str):
#     """Fixture for AsyncClient."""
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url=base_url
#     ) as ac:
#         yield ac
#
#
# async def test_get_full_menu(client: AsyncClient):
#     """Тест на получение полного дерева меню."""
#     response = await client.get('/menu/')
#     assert response.status_code == status.HTTP_200_OK
#     assert "id" in response.json()  # Проверяем наличие корневого id
#
#
# async def test_get_menu_node_by_name(client: AsyncClient):
#     """Тест на получение узла меню по имени."""
#     # Предполагаем, что существует узел с именем "root" или замените на реальное
#     response = await client.get('/menu/search-by-name?name=root')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#     if response.status_code == status.HTTP_200_OK:
#         assert "name" in response.json()
#
#
# async def test_get_menu_root(client: AsyncClient):
#     """Тест на получение корневого узла меню."""
#     response = await client.get('/menu/root')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["parent_id"] is None
#
#
# async def test_add_menu_node(client: AsyncClient):
#     """Тест на добавление узла меню."""
#     node_data = {
#         "parent_id": UUID("00000000-0000-0000-0000-000000000003"),
#         "name": f"Test Node",
#         "text": "Test text",
#         "subscription_type": "free"
#     }
#     response = await client.post('/menu/add', json=node_data)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["detail"] == "The menu node was added"
#
#
# async def test_get_menu_node_by_id(client: AsyncClient):
#     """Тест на получение узла меню по ID. Требует существующего ID."""
#     # Замените на реальный ID или создайте предварительно
#     menu_id = UUID("00000000-0000-0000-0000-000000000003")  # Пример ID
#     response = await client.get(f'/menu/{menu_id}')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_update_menu_node(client: AsyncClient):
#     """Тест на обновление узла меню. Требует существующего ID."""
#     menu_id = UUID("00000000-0000-0000-0000-000000001337")  # Пример ID
#     update_data = {
#         "name": f"Updated Node {uuid4()}",
#         "text": "Updated text"
#     }
#     response = await client.put(f'/menu/{menu_id}', json=update_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]
#
#
# async def test_delete_menu_node(client: AsyncClient):
#     """Тест на удаление узла меню. Требует существующего ID."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")  # Пример ID
#     response = await client.delete(f'/menu/{menu_id}')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_add_menu_content(client: AsyncClient):
#     """Тест на добавление контента к узлу меню. Требует существующего menu_id."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")  # Пример ID
#     content_data = {
#         "menu_id": str(menu_id),
#         "type": 1,
#         "server_path": "/path/to/content"
#     }
#     response = await client.post(f'/menu/{menu_id}/content/add', json=content_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_update_menu_content(client: AsyncClient):
#     """Тест на обновление контента. Требует существующих ID."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")
#     content_id = UUID("00000000-0000-0000-0000-000000000001")
#     content_data = {
#         "menu_id": str(menu_id),
#         "type": 2,
#         "server_path": "/updated/path"
#     }
#     response = await client.put(f'/menu/{menu_id}/content/change/{content_id}', json=content_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_delete_menu_content(client: AsyncClient):
#     """Тест на удаление контента. Требует существующих ID."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")
#     content_id = UUID("00000000-0000-0000-0000-000000000001")
#     response = await client.delete(f'/menu/{menu_id}/content/delete/{content_id}')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_get_menu_node_rate(client: AsyncClient):
#     """Тест на получение рейтинга узла меню."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")
#     response = await client.get(f'/menu/{menu_id}/rate')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_rate_menu_node(client: AsyncClient):
#     """Тест на оценку узла меню."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")
#     rating_data = {
#         "user_id": "user123",
#         "is_useful": True
#     }
#     response = await client.post(f'/menu/{menu_id}/rate', json=rating_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_get_menu_ratings_all(client: AsyncClient):
#     """Тест на получение всех оценок узла меню."""
#     menu_id = UUID("00000000-0000-0000-0000-000000000000")
#     response = await client.get(f'/menu/{menu_id}/rates-all')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
#
# async def test_create_user(client: AsyncClient):
#     """Тест на создание пользователя."""
#     user_data = {
#         "id": str(uuid4()),
#         "phone_number": "+1234567890"
#     }
#     response = await client.post('/users/create', json=user_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
#
#
# async def test_get_long_time_lost_users(client: AsyncClient):
#     """Тест на получение пользователей, которые давно не заходили."""
#     response = await client.get('/users/long-time-lost?days_count=10')
#     assert response.status_code == status.HTTP_200_OK
#     assert "items" in response.json()
#
#
# async def test_get_user_questions(client: AsyncClient):
#     """Тест на получение вопросов пользователя."""
#     user_id = "user_001"
#     response = await client.get(f'/users/questions/{user_id}')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_get_all_questions(client: AsyncClient):
#     """Тест на получение всех вопросов."""
#     response = await client.get('/users/questions')
#     assert response.status_code == status.HTTP_200_OK
#     assert "items" in response.json()
#
#
# async def test_create_question(client: AsyncClient):
#     """Тест на создание вопроса."""
#     question_data = {
#         "user_id": "user_001",
#         "text": "Test question?"
#     }
#     response = await client.post('/users/questions/create', json=question_data)
#     assert response.status_code == status.HTTP_200_OK
#
#
# async def test_answer_question(client: AsyncClient):
#     """Тест на ответ на вопрос."""
#     question_id = UUID("00000000-0000-0000-0000-000000000000")
#     answer_data = {
#         "admin_answer": "Test answer"
#     }
#     response = await client.put(f'/users/questions/{question_id}/answer', json=answer_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_delete_question(client: AsyncClient):
#     """Тест на удаление вопроса."""
#     question_id = UUID("00000000-0000-0000-0000-000000000000")
#     response = await client.delete(f'/users/questions/{question_id}')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_create_user_action_record(client: AsyncClient):
#     """Тест на добавление действия пользователя."""
#     user_id = "user_001"
#     history_data = {
#         "menu_id": "00000000-0000-0000-0000-000000000001",
#         "action_date": datetime.now().isoformat(),
#     }
#     response = await client.post(f'/users/{user_id}/history/add', json=history_data)
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
#
#
# async def test_get_user_history(client: AsyncClient):
#     """Тест на получение истории пользователя."""
#     user_id = "user_001"
#     response = await client.get(f'/users/{user_id}/history')
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]