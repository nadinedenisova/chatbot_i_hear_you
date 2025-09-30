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

    async def get_user(self, user_id: int) -> bool:
        """Проверка существования пользователя в системе."""
        url = f'{self.api_url}/users/users'
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        users = data.get('items', [])
                        for user in users:
                            if user.get('id') == str(user_id):
                                logger.debug(f'Пользователь {user_id} найден')
                                return True
                        logger.debug(f'Пользователь {user_id} не найден')
                        return False
                    else:
                        response_text = await response.text()
                        logger.error(
                            f'Ошибка при получении списка пользователей: '
                            f'status={response.status}, body={response_text}'
                        )
                        return False
        except Exception as e:
            logger.error(f'Ошибка при получении пользователя: {e}')
            return False

    async def register_user(self, user_id: int) -> bool:
        """Регистрация пользователя в системе."""
        url = f'{self.api_url}/users/create'
        data = {
            'id': str(user_id),
            'phone_number': '+7{user_id}' # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! УБРАТЬ!?
        }

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, json=data) as response:
                    response_text = await response.text()
                    logger.debug(
                        f'Ответ сервера на регистрацию:'
                        f'status={response.status}, body={response_text}')

                    if response.status in [200, 201]:
                        logger.info(
                            f'Пользователь {user_id} успешно зарегистрирован')
                        return True
                    elif response.status == 400:
                        logger.info(
                            f'Пользователь {user_id} уже существует')
                        return True
                    else:
                        logger.error(
                            f'Не удалось зарегистрировать пользователя:'
                            f'{response_text}')
                        return False
        except Exception as e:
            logger.error(f'Ошибка при регистрации пользователя: {e}')
            return False

    async def get_root_menu(self) -> Menu:
        """Получение корневого меню."""
        url = f'{self.api_url}/menu/root'
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.debug('Корневое меню загружено')
                    return Menu(data)
        except aiohttp.ClientError as e:
            logger.error(f'Ошибка HTTP при загрузке корневого меню: {e}')
            raise
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
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.debug(f'Меню "{menu_name}" загружено')

                    logger.debug(f'Тип данных от API: {type(data)}')
                    logger.debug(f'Данные от API: {data}')

                    return Menu(data)
        except aiohttp.ClientError as e:
            logger.error(f'Ошибка HTTP при загрузке меню "{menu_name}": {e}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при загрузке меню "{menu_name}": {e}')
            raise

    async def get_menu_by_id(self, menu_id: int) -> Optional[Menu]:
        """Получение меню по ID."""
        url = f'{self.api_url}/menu/{menu_id}'
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    if response.status == 404:
                        return None
                    response.raise_for_status()
                    data = await response.json()
                    logger.debug(f'Меню с ID {menu_id} загружено')
                    return Menu(data)
        except aiohttp.ClientError as e:
            logger.error(f'Ошибка HTTP при загрузке меню с ID {menu_id}: {e}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при загрузке меню с ID {menu_id}: {e}')
            raise

    async def send_rating(
            self, menu_id: int, user_id: int, rating: int) -> bool:
        """Отправка рейтинга для меню."""
        url = f'{self.api_url}/menu/{menu_id}/rate'
        data = {
            'user_id': str(user_id),
            'node_rating': rating
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, json=data) as response:
                    response.raise_for_status()
                    logger.debug(
                        f'Рейтинг {rating} для меню {menu_id} отправлен')
                    return True
        except aiohttp.ClientError as e:
            logger.error(
                f'Ошибка HTTP при отправке рейтинга: {e}', exc_info=True)
            return False
        except Exception as e:
            logger.error(f'Ошибка при отправке рейтинга: {e}')
            return False
