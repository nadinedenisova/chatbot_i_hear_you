import logging
from pathlib import Path

from aiogram.types import FSInputFile

from keyboards import create_navigation_buttons
from utils.texts import TEXTS

logger = logging.getLogger(__name__)


async def send_content_to_user(message, content: dict):
    """
    Отправляет контент пользователю в зависимости от типа и источника.

    Парматетры:
        content: Словарь с информацией о контенте
    """
    content_path = content.get('server_path', '')
    content_type = content.get('type', 0)

    # Определяем, это URL или локальный файл
    if content_path.startswith(('http://', 'https://')):
        # Если URL - отправляем ссылку
        await message.answer(
            f'{TEXTS["get_content"]}'
            f'{content_path}\n\n'
        )
        # Отправляем навигацию с клавишами
        await message.answer(
            TEXTS['navigation_hint'],
            reply_markup=create_navigation_buttons()
        )
    elif content_path.startswith('uploaded_content/'):
        # Это локальный файл на сервере
        await send_local_file(
            message,
            content_path,
            content_type,
            content.get('name', 'Файл')
        )
        # Отправляем навигацию с клавишами
        await message.answer(
            TEXTS['navigation_hint'],
            reply_markup=create_navigation_buttons()
            )
    else:
        # Некорректный путь
        logger.error(f'Некорректный путь к контенту: {content_path}')
        await message.answer(TEXTS['content_not_found'])


async def send_local_file(
        message, file_path: str, content_type: int, name: str):
    """
    Отправляет локальный файл пользователю.

    Парматетры:
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

    # Отправляем файл в зависимости от типа
    if content_type == 1:
        await message.answer_photo(
            photo=file_input,
            caption=f"🖼 {name}"
        )
    elif content_type == 2:
        await message.answer_video(
            video=file_input,
            caption=f"🎬 {name}"
        )
    elif content_type == 3:
        await message.answer_document(
            document=file_input,
            caption=f"📄 {name}"
        )
    else:
        # Неизвестный тип - отправляем как документ
        await message.answer_document(
            document=file_input,
            caption=f"📎 {name}"
        )
