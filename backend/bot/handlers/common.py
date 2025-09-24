from aiogram import Router, F, types
from aiogram.filters import Command

from utils.texts import TEXTS

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """Обработчик команды /help."""
    await message.answer(TEXTS['help_text'])


@router.message(Command("about"))
async def cmd_about(message: types.Message) -> None:
    """Обработчик команды /about."""
    await message.answer(TEXTS['about_text'])


@router.message(F.text)
async def echo_message(message: types.Message) -> None:
    """Эхо-обработчик для текстовых сообщений."""
    await message.answer(TEXTS['echo'])


@router.message()
async def unsupported_message(message: types.Message) -> None:
    """Обработчик для неподдерживаемых типов сообщений."""
    await message.answer(TEXTS['unsupported'])
