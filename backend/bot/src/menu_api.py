from datetime import datetime, timezone
import logging
from typing import Optional

import aiohttp

from config import config
from models import Menu

logger = logging.getLogger(__name__)


class API:
    """API для взаимодействия с меню."""

    def __init__(self):
        self.api_url = config.API_URL
        self.timeout = aiohttp.ClientTimeout(total=config.API_TIMEOUT)
        self.last_saved_menu = {}

    # ========== Методы для работы с пользователями ==========

    async def get_user(self, user_id: int) -> bool:
        """Проверка существования пользователя в системе."""
        url = f'{self.api_url}/users/users'

        try:
            users = await self._fetch_json(url)
            if users:
                users_list = users.get('items', [])
                user_exists = self._check_user_exists(users_list, user_id)

                log_message = (
                    f'Пользователь {user_id}'
                    f'{"найден" if user_exists else "не найден"}')
                logger.debug(log_message)
                return user_exists
            return False

        except Exception as e:
            logger.error(f'Ошибка при получении пользователя: {e}')
            return False

    async def register_user(self, user_id: int) -> bool:
        """Регистрация пользователя в системе."""
        url = f'{self.api_url}/users/create'
        data = {
            'id': str(user_id),
            'phone_number': f'+7{user_id}'
        }

        try:
            response_data = await self._post_request(url, data)

            if response_data.get('status') in [200, 201, 400]:
                log_message = 'уже существует' if response_data.get(
                    'status') == 400 else 'успешно зарегистрирован'
                logger.info(f'Пользователь {user_id} {log_message}')
                return True

            logger.error(
                f'Не удалось зарегистрировать пользователя: {response_data}')
            return False

        except Exception as e:
            logger.error(f'Ошибка при регистрации пользователя: {e}')
            return False

    # ========== Методы для работы с меню ==========

    async def get_root_menu(self) -> Menu:
        """Получение корневого меню."""
        url = f'{self.api_url}/menu/root'

        try:
            data = await self._fetch_json(url, raise_for_status=True)
            logger.debug('Корневое меню загружено')
            return Menu(data)
        except Exception as e:
            logger.error(f'Ошибка при загрузке корневого меню: {e}')
            raise

    async def find_menu_by_name(self, menu_name: str) -> Optional[Menu]:
        """Получение подменю по имени."""
        if not menu_name:
            return None

        url = f'{self.api_url}/menu/search-by-name'
        params = {'name': menu_name}

        try:
            data = await self._fetch_json(
                url, params=params, raise_for_status=True)
            logger.debug(f'Меню "{menu_name}" загружено')
            return Menu(data)
        except Exception as e:
            logger.error(f'Ошибка при загрузке меню "{menu_name}": {e}')
            raise

    async def get_menu_by_id(self, menu_id: int) -> Optional[Menu]:
        """Получение меню по ID."""
        url = f'{self.api_url}/menu/{menu_id}'

        try:
            data = await self._fetch_json(url)
            if data:
                logger.debug(f'Меню с ID {menu_id} загружено')
                return Menu(data)
            return None
        except Exception as e:
            logger.error(f'Ошибка при загрузке меню с ID {menu_id}: {e}')
            raise

    # ========== Методы для работы с рейтингами и историей ==========

    async def send_rating(
            self, menu_id: int, user_id: int, rating: bool) -> bool:
        """Отправка рейтинга для меню."""
        url = f'{self.api_url}/menu/{menu_id}/rate'
        data = {
            'user_id': str(user_id),
            'is_useful': bool(rating)
        }

        try:
            await self._post_request(url, data, raise_for_status=True)
            logger.debug(f'Рейтинг для меню {menu_id} отправлен')
            return True
        except Exception as e:
            logger.error(f'Ошибка при отправке рейтинга: {e}')
            return False

    async def add_to_history(self, user_id: int, menu_id: str) -> bool:
        """Добавление записи в историю пользователя."""
        # Проверка на дублирование
        if self.last_saved_menu.get(user_id) == menu_id:
            logger.debug(f'Пропускаем дублирование истории для меню {menu_id}')
            return True

        url = f'{self.api_url}/users/{user_id}/history/add'
        data = self._prepare_history_data(menu_id)

        try:
            response_data = await self._post_request(url, data)

            if response_data.get('status') in [200, 201]:
                log_message = (
                    f'История сохранена для пользователя {user_id}, '
                    f'меню {menu_id}')
                logger.debug(log_message)
                self.last_saved_menu[user_id] = menu_id
                return True

            logger.error(f'Ошибка сохранения истории: {response_data}')
            return False

        except Exception as e:
            logger.error(f'Ошибка при добавлении в историю: {e}')
            return False

    async def send_question(self, user_id: int, text: str) -> bool:
        """Отправка вопроса пользователя."""
        url = f'{self.api_url}/users/questions/create'
        data = {
            'user_id': str(user_id),
            'text': text
        }

        try:
            response_data = await self._post_request(url, data)
            if response_data.get('status') in [200, 201]:
                logger.debug(f'Вопрос от пользователя {user_id} отправлен')
                return True

            logger.error(f'Ошибка при отправке вопроса: {response_data}')
            return False

        except Exception as e:
            logger.error(f'Ошибка при отправке вопроса: {e}')
            return False

    # ========== Приватные вспомогательные методы ==========

    def _check_user_exists(self, users_list: list, user_id: int) -> bool:
        """Проверяет наличие пользователя в списке."""
        for user in users_list:
            if user.get('id') == str(user_id):
                return True
        return False

    def _prepare_history_data(self, menu_id: str) -> dict:
        """Подготавливает данные для сохранения истории."""
        current_time = datetime.now(timezone.utc)
        formatted_date = current_time.strftime('%Y-%m-%d %H:%M:%S')
        return {
            'menu_id': str(menu_id),
            'action_date': formatted_date
        }

    async def _fetch_json(
        self,
        url: str,
        params: dict = {},
        raise_for_status: bool = False
    ) -> Optional[dict]:
        """Выполняет GET запрос и возвращает JSON."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 404:
                        return None
                    if raise_for_status:
                        response.raise_for_status()
                    if response.status == 200:
                        return await response.json()

                    response_text = await response.text()
                    log_message = (
                        f'Ошибка запроса: status={response.status}, '
                        f'body={response_text}')
                    logger.error(log_message)
                    return None
        except aiohttp.ClientError as e:
            if raise_for_status:
                raise
            logger.error(f'Ошибка HTTP при запросе {url}: {e}')
            return None

    async def _post_request(
        self,
        url: str,
        data: dict,
        raise_for_status: bool = False
    ) -> dict:
        """Выполняет POST запрос и возвращает результат."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, json=data) as response:
                    response_text = await response.text()

                    if raise_for_status:
                        response.raise_for_status()

                    log_message = (
                        f'Ответ сервера: status={response.status}, '
                        f'body={response_text}'
                    )
                    logger.debug(log_message)

                    return {
                        'status': response.status,
                        'text': response_text
                    }
        except aiohttp.ClientError as e:
            if raise_for_status:
                raise
            logger.error(f'Ошибка HTTP при POST запросе {url}: {e}')
            raise
