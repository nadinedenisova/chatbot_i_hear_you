import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from menu_api import API
from utils.menu_update import update_menu_state
from utils.texts import TEXTS

logger = logging.getLogger(__name__)

router = Router(name='command')


class States(StatesGroup):
    """Состояния для навигации по меню"""
    navigating = State()


# Инициализируем API и хранилище для навигации (стек меню)
menu_api = API()
navigation_stack: dict[int, list[str]] = {}


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    try:
        # Загружаем корневое меню с API и инициализируем навигацию
        root_menu = await menu_api.get_root_menu()
        user_id = message.from_user.id
        navigation_stack[user_id] = []  # Пустой стек для корневого меню
        await state.set_state(States.navigating)

        # Отправляем сообщение с главным меню
        await update_menu_state(
            state,
            root_menu,
            message=message,
            is_root=True
        )

    except Exception as e:
        logger.error(f'Ошибка в cmd_start: {e}')
        await message.answer(TEXTS['error_start'])


@router.message(Command('help'))
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    await message.answer(TEXTS['help_text'])


@router.message(F.text)
async def echo_message(message: Message) -> None:
    """Эхо-обработчик для текстовых сообщений."""
    await message.answer(TEXTS['echo'])


@router.message()
async def unsupported_message(message: Message) -> None:
    """Обработчик для неподдерживаемых типов сообщений."""
    await message.answer(TEXTS['unsupported'])
