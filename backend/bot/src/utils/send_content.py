import logging
from pathlib import Path

from aiogram.types import FSInputFile

from keyboards import create_navigation_buttons
from utils.texts import TEXTS

logger = logging.getLogger(__name__)


async def send_content_to_user(message, content: dict):
    """
    Отправляет контент пользователю в зависимости от типа и источника.

    Параметры:
        content: Словарь с информацией о контенте
    """
    content_path = content.get('server_path', '')

    if _is_url(content_path):
        await _send_url_content(message, content_path)
    elif _is_local_file(content_path):
        await _send_local_content(message, content)
    else:
        await _send_error_message(message, content_path)


def _is_url(path: str) -> bool:
    """Проверяет, является ли путь URL-адресом."""
    return path.startswith(('http://', 'https://'))


def _is_local_file(path: str) -> bool:
    """Проверяет, является ли путь локальным файлом."""
    return path.startswith('uploaded_content/')


async def _send_url_content(message, url: str):
    """Отправляет контент по URL."""
    await message.answer(
        f'{TEXTS["get_content"]}{url}\n\n'
    )
    await _send_navigation_buttons(message)


async def _send_local_content(message, content: dict):
    """Отправляет локальный контент."""
    await send_local_file(
        message,
        content.get('server_path', ''),
        content.get('type', 0),
        content.get('name', 'Файл')
    )
    await _send_navigation_buttons(message)


async def _send_error_message(message, content_path: str):
    """Отправляет сообщение об ошибке."""
    logger.error(f'Некорректный путь к контенту: {content_path}')
    await message.answer(TEXTS['content_not_found'])


async def _send_navigation_buttons(message):
    """Отправляет навигационные кнопки после показа контента."""
    await message.answer(
        TEXTS['navigation_hint'],
        reply_markup=create_navigation_buttons(restore_menu=True)
    )


async def send_local_file(
        message, file_path: str, content_type: int, name: str):
    """
    Отправляет локальный файл пользователю.

    Параметры:
        file_path: Путь к файлу на сервере
        content_type: Тип контента (1 - изображение, 2 - видео, 3 - документ)
        name: Имя файла для подписи
    """
    path = Path(file_path)

    if not path.exists():
        logger.error(f'Файл не найден: {path}')
        await message.answer(TEXTS['content_not_found'])
        return

    file_input = FSInputFile(path)

    # Соответствие контента и методов отправки
    content_handlers = {
        1: _send_photo,
        2: _send_video,
        3: _send_document,
    }

    handler = content_handlers.get(content_type, _send_document)
    await handler(message, file_input, name)


async def _send_photo(message, file_input, name: str):
    """Отправляет фото."""
    await message.answer_photo(
        photo=file_input,
        caption=TEXTS['photo_type']
    )


async def _send_video(message, file_input, name: str):
    """Отправляет видео."""
    await message.answer_video(
        video=file_input,
        caption=TEXTS['video_type']
    )


async def _send_document(message, file_input, name: str):
    """Отправляет документ."""
    await message.answer_document(
        document=file_input,
        caption=TEXTS['doc_type']
    )
