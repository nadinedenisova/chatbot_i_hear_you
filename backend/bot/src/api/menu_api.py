import logging
from typing import Optional

import aiohttp

from config import config
from models.menu import Menu

logger = logging.getLogger(__name__)


class MenuAPI:
    """API для взаимодействия с меню."""

    def __init__(self):
        self.api_url = config.API_URL
        self.timeout = aiohttp.ClientTimeout(total=config.API_TIMEOUT)

    async def get_menu(self, menu_id: Optional[str] = None) -> Menu:
        """
        Получение меню по ID.
        Если menu_id не указан, получаем все меню, иначе получаем конкретное.
        """

        url = f'{self.api_url}/menu/root'  # ЗАМЕНИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if menu_id:
            url = f'{url}/{menu_id}'

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # проверка статуса
                    data = await response.json()
                    print(data)
                    return Menu(data)
        except Exception as e:
            logger.error(f'Ошибка загрузки меню: {e}')
            raise

    async def get_content_url(self, content_id: str) -> str:
        """Получение контента"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(
                    f'{self.api_url}/content/{content_id}/url'
                ) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
                    return result.get('url')
        except Exception as e:
            logger.error(f'Ошибка загрузки контента: {e}')
            raise
