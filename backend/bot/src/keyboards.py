from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from models import Menu
from utils.texts import TEXTS


def create_menu_keyboard(
        menu: Menu,
        is_root: bool = False,
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
        # Кнопка с вопросом от пользователя. Создаем в дочернем меню.
        if not is_root and not menu.content:
            buttons.append([
                InlineKeyboardButton(
                    text=TEXTS['ask_question_btn'],
                    callback_data='ask_question'
                )
            ])

    # Кнопки для контента
    if menu.content:
        for index, content in enumerate(menu.content):
            content_type = content.get_content_type()
            buttons.append([
                InlineKeyboardButton(
                    text=content_type,
                    callback_data=f'cnt:{index}'
                )
            ])

    # Навигационные кнопки
    if not is_root:
        nav_markup = create_navigation_buttons()
        buttons.extend(nav_markup.inline_keyboard)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_navigation_buttons() -> InlineKeyboardMarkup:
    """Создает клавиатуру только с навигационными кнопками (Назад/Домой)."""
    buttons = [
        [
            InlineKeyboardButton(text=TEXTS['back'], callback_data='back'),
            InlineKeyboardButton(text=TEXTS['home'], callback_data='home')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_rating_keyboard(menu_id: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для оценки контента."""
    buttons = []
    buttons.append([
        InlineKeyboardButton(
            text=TEXTS['useful_btn'],
            callback_data=f'rate:{menu_id}:5'
        ),
        InlineKeyboardButton(
            text=TEXTS['not_useful_btn'],
            callback_data=f'rate:{menu_id}:1'
        )
    ])

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
