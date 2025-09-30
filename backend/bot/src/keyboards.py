from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from models import Menu
from utils.texts import TEXTS


def create_menu_keyboard(
        menu: Menu,
        is_root: bool = False
        ) -> InlineKeyboardMarkup:
    """Создает клавиатуру для меню."""
    buttons = []

    # Кнопки для дочерних элементов меню
    if menu.children_names:
        for index, child_name in enumerate(menu.children_names):
            buttons.append([
                InlineKeyboardButton(
                    text=child_name,
                    callback_data=f'menu:{index}'
                )
            ])

    # Кнопки для контента
    if menu.content:
        for index, content in enumerate(menu.content):
            content_type = content.get_content_type()
            # Используем индекс контента и сохраняем URL отдельно
            buttons.append([
                InlineKeyboardButton(
                    text=content_type,
                    callback_data=f'cnt:{index}'
                )
            ])

    # Навигационные кнопки
    navigation = []
    if not is_root:  # Если не корневое меню, добавляем кнопки
        navigation.append(InlineKeyboardButton(
            text=TEXTS['back'], callback_data='back'))
        navigation.append(InlineKeyboardButton(
            text=TEXTS['home'], callback_data='home'))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def set_main_commands(bot):
    """Устанавливает команды бота, которые будут видны в меню Telegram."""

    main_menu_commands = [
        BotCommand(command='/start',
                   description=TEXTS['start_command']),
        BotCommand(command='/help',
                   description=TEXTS['help_command']),
    ]

    await bot.set_my_commands(main_menu_commands)
