import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from menu_api import API
from models import Menu
from keyboards import create_menu_keyboard, create_rating_keyboard
from utils.constants import SHOW_RATING_MES_DEL
from utils.texts import TEXTS
from utils.storage import rated_menus


async def update_menu_state(
    state: FSMContext,
    menu: Menu,
    message: Message = None,
    callback: CallbackQuery = None,
    is_root: bool = False,
    save_history: bool = True
):
    """Универсальная функция для создания/обновления меню."""

    user_id = _get_user_id(message, callback)

    # Сохраняем историю навигации при необходимости
    if save_history:
        await _save_navigation_history(state, menu, user_id)

    # Обновляем состояние пользователя
    await _update_user_state(state, menu)

    # Отправляем или обновляем сообщение меню
    target_message = await _send_or_update_menu_message(
        menu, message, callback, is_root
    )

    # Показываем запрос оценки при необходимости
    await _show_rating_if_needed(
        state, menu, user_id, target_message
    )


def _get_user_id(
        message: Message = None, callback: CallbackQuery = None) -> int:
    """Получает ID пользователя из message или callback."""
    if message:
        return message.from_user.id
    if callback:
        return callback.from_user.id
    return 0


async def _save_navigation_history(
    state: FSMContext,
    menu: Menu,
    user_id: int
):
    """Сохраняет историю навигации пользователя."""
    state_data = await state.get_data()
    last_menu_id = state_data.get('last_history_menu_id')

    # Сохраняем только при переходе в другое меню
    if last_menu_id != menu.id:
        menu_api = API()
        await menu_api.add_to_history(user_id, menu.id)


async def _update_user_state(state: FSMContext, menu: Menu):
    """Обновляет состояние FSM с данными текущего меню."""
    await state.update_data(
        current_menu_id=menu.id,
        current_children=menu.children_names,
        current_content=[content.to_dict() for content in menu.content],
        rating_shown=False,
        last_history_menu_id=menu.id
    )


async def _send_or_update_menu_message(
    menu: Menu,
    message: Message = None,
    callback: CallbackQuery = None,
    is_root: bool = False
) -> Message:
    """Отправляет новое сообщение или редактирует существующее."""
    keyboard = create_menu_keyboard(menu, is_root=is_root)
    text = f'<b>{menu.name}</b>\n\n{menu.text}'

    if message:
        await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
        return message
    elif callback:
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        await callback.answer()
        return callback.message

    return None


async def _show_rating_if_needed(
    state: FSMContext,
    menu: Menu,
    user_id: int,
    target_message: Message
):
    """Показывает запрос на оценку контента при необходимости."""
    if not target_message:
        return

    state_data = await state.get_data()

    # Условия для показа оценки
    should_show_rating = (
        menu.content
        and not state_data.get('rating_shown', False)
        and menu.id not in rated_menus.get(user_id, set())
    )

    if should_show_rating:
        rating_keyboard = create_rating_keyboard(menu.id)
        rating_message = await target_message.answer(
            TEXTS['rate_content'],
            reply_markup=rating_keyboard,
            parse_mode='HTML'
        )
        await asyncio.sleep(SHOW_RATING_MES_DEL)
        await rating_message.delete()
