import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from api.menu_api import MenuAPI
from keyboards.menu_keyboards import MenuKeyboard
from services.navigator import NavigatorService
from states.menu_states import MenuStates
from utils.texts import TEXTS

logger = logging.getLogger(__name__)
router = Router(name='commands')

menu_api = MenuAPI()
navigator = NavigatorService()
keyboard_builder = MenuKeyboard()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start."""
    try:
        root_menu = await menu_api.get_menu()

        #
        await state.set_state(MenuStates.navigating)
        await state.update_data(
            current_menu_id=root_menu.id,
            menu_data=root_menu.to_dict()
        )

        navigator.set_position(message.from_user.id, root_menu.id)

        keyboard = keyboard_builder.create_menu_keyboard(
            root_menu,
            message.from_user.id,
            is_root=True
        )

        await message.answer(
            f'{root_menu.name}\n\n{root_menu.text}',  # ПОСМОТРЕТЬ ЧТО В ИТОГЕ БУДЕТ отдавать в ответе!!!
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f'Ошибка загрузки главного меню: {e}')
        await message.answer(TEXTS['error'])


@router.message(Command('menu'))
async def cmd_menu(message: Message, state: FSMContext):
    """Обработчик команды /menu (перенаправляет к /start)."""
    await cmd_start(message, state)


@router.message(Command('help'))
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    await message.answer(TEXTS['help'])
