from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from models import Menu
from keyboards import create_menu_keyboard


async def update_menu_state(
    state: FSMContext,
    menu: Menu,
    message: Message = None,
    callback: CallbackQuery = None,
    is_root: bool = False
):
    """Универсальная функция для обновления меню."""

    # Обновляем состояние
    await state.update_data(
        current_menu_id=menu.id,
        current_children=menu.children_names,
        current_content=[content.to_dict() for content in menu.content]
    )

    # Создаем клавиатуру и текст
    keyboard = create_menu_keyboard(menu, is_root=is_root)
    text = f'<b>{menu.name}</b>\n\n{menu.text}'

    # Если стартуем, то отправлем сообщением,
    # если двигаемся по навигации, то редактируем.
    if message:
        await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
    elif callback:
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode='HTML')
        await callback.answer()
