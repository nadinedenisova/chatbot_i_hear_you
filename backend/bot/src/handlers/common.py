from aiogram import Router, F
from aiogram.types import Message

from utils.texts import TEXTS

router = Router(name="common")


@router.message(F.text)
async def echo_message(message: Message) -> None:
    """Эхо-обработчик для текстовых сообщений."""
    await message.answer(TEXTS["echo"])


@router.message()
async def unsupported_message(message: Message) -> None:
    """Обработчик для неподдерживаемых типов сообщений."""
    await message.answer(TEXTS["unsupported"])
