from aiogram import Router, types
from aiogram.filters import CommandStart

from keyboards.reply import get_main_keyboard
from utils.texts import TEXTS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """Обработчик команды /start."""
    await message.answer(
        TEXTS['start'],
        reply_markup=get_main_keyboard()
    )
