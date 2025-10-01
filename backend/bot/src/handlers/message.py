import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from menu_api import API
from utils.menu_update import update_menu_state
from utils.texts import TEXTS
from utils.states import UserStates

logger = logging.getLogger(__name__)

router = Router(name='command')


# Инициализируем API и хранилище для навигации (стек меню)
menu_api = API()
navigation_stack: dict[int, list[str]] = {}


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""

    try:
        user = await menu_api.get_user(user_id=message.from_user.id)
        if not user:
            # Регистрируем пользователя
            await menu_api.register_user(user_id=message.from_user.id)

        # Загружаем корневое меню с API и инициализируем навигацию
        root_menu = await menu_api.get_root_menu()
        user_id = message.from_user.id
        navigation_stack[user_id] = []  # Пустой стек для корневого меню
        await state.set_state(UserStates.navigating)

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


@router.message(StateFilter(UserStates.waiting_for_question), F.text)
async def process_question(message: Message, state: FSMContext):
    """Обработка введенного вопроса."""

    # Получаем ID сохраненного сообщения
    state_data = await state.get_data()
    question_prompt_message_id = state_data.get('question_prompt_message_id')

    # Отправляем вопрос на API
    success = await menu_api.send_question(
        user_id=message.from_user.id,
        text=message.text
    )

    if success:
        # Через 5 секунд удаляем сообщение бота
        bot_message = await message.answer(
            TEXTS['send_question_done'], parse_mode='HTML')
        await asyncio.sleep(5)
        await bot_message.delete()
    else:
        bot_message = await message.answer(
            TEXTS['send_question_error'], parse_mode='HTML')
        await asyncio.sleep(5)
        await bot_message.delete()

    # Удаляем сообщение пользователя
    await message.delete()

    # Удаляем сообщение с запросом вопроса
    if question_prompt_message_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=question_prompt_message_id
            )
        except Exception as e:
            logger.error(f'Ошибка при удалении сообщения: {e}')

    await state.set_state(UserStates.navigating)


@router.message()
async def unsupported_message(message: Message) -> None:
    """Обработчик для неподдерживаемых типов сообщений."""
    await message.answer(TEXTS['unsupported'])
