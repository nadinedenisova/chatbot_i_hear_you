import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.menu_api import MenuAPI
from keyboards.menu_keyboards import MenuKeyboard
from services.navigator import NavigatorService
from states.menu_states import MenuStates
from utils.texts import TEXTS

logger = logging.getLogger(__name__)
router = Router(name="navigation")

menu_api = MenuAPI()
navigator = NavigatorService()
keyboard_builder = MenuKeyboard()


@router.callback_query(MenuStates.navigating, F.data.startswith("menu:"))
async def navigate(callback: CallbackQuery, state: FSMContext):
    """Навигация по меню."""
    try:
        menu_id = callback.data.split(":")[1]
        menu = await menu_api.get_menu(menu_id)
        navigator.set_position(callback.from_user.id, menu_id)
        await state.update_data(current_menu_id=menu_id, menu_data=menu.to_dict())
        if menu.has_children() and not menu.children:
            menu.children = await menu_api.get_menu_item_children(menu_id)
        keyboard = keyboard_builder.create_menu_keyboard(
            menu,
            callback.from_user.id,
        )
        text = f"📁 {menu.name}*\n\n{menu.text}"
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
        )
        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка навигации: {e}")
        await callback.answer(TEXTS["error"], show_alert=True)


@router.callback_query(MenuStates.navigating, F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    """Вернуться в предыдущее меню."""
    try:
        user_id = callback.from_user.id
        previous_id = navigator.go_back(user_id)

        if previous_id:
            menu = await menu_api.get_menu(previous_id)

            await state.update_data(
                current_menu_id=previous_id, menu_data=menu.to_dict()
            )

            keyboard = keyboard_builder.create_menu_keyboard(
                menu, user_id, is_root=(previous_id == "root" or menu.parent_id is None)
            )

            await callback.message.edit_text(
                f"📁 {menu.name}\n\n{menu.text}",
                reply_markup=keyboard,
            )
        else:
            await callback.answer("Вы в главном меню", show_alert=True)

        await callback.answer()

    except Exception as e:
        logger.error(f'Ошибка возврата "назад": {e}')
        await callback.answer(TEXTS["error"], show_alert=True)


@router.callback_query(MenuStates.navigating, F.data == "home")
async def go_home(callback: CallbackQuery, state: FSMContext):
    """Вернуться в главное меню."""
    try:
        navigator.reset(callback.from_user.id)

        root_menu = await menu_api.get_menu()
        navigator.set_position(callback.from_user.id, root_menu.id)

        await state.update_data(
            current_menu_id=root_menu.id, menu_data=root_menu.to_dict()
        )

        keyboard = keyboard_builder.create_menu_keyboard(
            root_menu, callback.from_user.id, is_root=True
        )

        await callback.message.edit_text(
            f"{root_menu.name}\n\n{root_menu.text}",
            reply_markup=keyboard,
        )
        await callback.answer(TEXTS["home"])

    except Exception as e:
        logger.error(f"Ошибка возврата в главное меню: {e}")
        await callback.answer(TEXTS["error"], show_alert=True)
