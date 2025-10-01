from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from models import Menu
from keyboards import create_menu_keyboard, create_rating_keyboard
from utils.texts import TEXTS


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
        current_content=[content.to_dict() for content in menu.content],
        rating_shown=False  # флаг для отслеживания показа оценки
    )

    # Создаем клавиатуру и текст
    keyboard = create_menu_keyboard(menu, is_root=is_root)
    text = f'<b>{menu.name}</b>\n\n{menu.text}'

    # Отправляем или редактируем основное сообщение
    if message:
        await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
        target_message = message  # Для отправки рейтинга
    elif callback:
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode='HTML')
        await callback.answer()
        target_message = callback.message  # Для отправки рейтинга
    else:
        return  # Если нет ни message, ни callback

    # Универсальная отправка сообщения с оценкой
    state_data = await state.get_data()
    if menu.content and not state_data.get('rating_shown', False):
        rating_keyboard = create_rating_keyboard(menu.id)
        await target_message.answer(
            TEXTS['rate_content'],
            reply_markup=rating_keyboard,
            parse_mode='HTML'
        )
        await state.update_data(rating_shown=True)
