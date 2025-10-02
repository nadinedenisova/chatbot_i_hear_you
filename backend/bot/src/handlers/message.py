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
from utils.storage import navigation_stack

logger = logging.getLogger(__name__)

router = Router(name='command')


# Инициализируем API и хранилище для навигации (стек меню)
menu_api = API()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды "/start":

    Функционал:
        - Проверяет существование пользователя в базе данных и
          регистрирует его, если пользователь новый,
        - Загружает корневую структуру меню из API и
          устанавливает пустую навигационную цепочку для пользователя,
        - Переводит пользователя в режим навигации и выводит главное меню.
    """

    try:
        user = await menu_api.get_user(user_id=message.from_user.id)
        if not user:
            await menu_api.register_user(user_id=message.from_user.id)

        root_menu = await menu_api.get_root_menu()
        user_id = message.from_user.id
        navigation_stack[user_id] = []  # Пустой стек для корневого меню
        await state.set_state(UserStates.navigating)

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
    """Обработчик ввода вопроса пользователем:

    Функционал:
        - Проверяет текущее состояние пользователя и ожидает ввод текста,
        - Отправляет введённый вопрос на внешний API,
        - После успешной отправки вопроса отображает временное сообщение
          о завершении отправки и удаляет его через три секунды,
        - Удаляет исходное и предыдущее сообщение пользователя,
        - Возвращает пользователя обратно в режим навигации по меню.
    """

    state_data = await state.get_data()
    question_prompt_message_id = state_data.get('question_prompt_message_id')

    success = await menu_api.send_question(
        user_id=message.from_user.id,
        text=message.text
    )

    if success:
        bot_message = await message.answer(
            TEXTS['send_question_done'], parse_mode='HTML')
        await asyncio.sleep(3)
        await bot_message.delete()
    else:
        bot_message = await message.answer(
            TEXTS['send_question_error'], parse_mode='HTML')
        await asyncio.sleep(3)
        await bot_message.delete()

    await message.delete()
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
