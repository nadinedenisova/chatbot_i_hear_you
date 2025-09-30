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
