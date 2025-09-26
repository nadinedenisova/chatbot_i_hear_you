from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.texts import TEXTS


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создает главную клавиатуру."""
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=TEXTS['main_menu']),
        KeyboardButton(text=TEXTS['help_button']),
        KeyboardButton(text=TEXTS['about_button']),
    )

    return builder.as_markup(resize_keyboard=True)
