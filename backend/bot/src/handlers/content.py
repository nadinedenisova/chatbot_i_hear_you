import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from api.menu_api import MenuAPI
from keyboards.menu_keyboards import MenuKeyboard
from states.menu_states import MenuStates
from utils.texts import TEXTS


logger = logging.getLogger(__name__)
router = Router(name='content')

menu_api = MenuAPI()
keyboard_builder = MenuKeyboard()


@router.callback_query(MenuStates.navigating, F.data.startswith('content:'))
async def view_content(callback: CallbackQuery, state: FSMContext):
    """View content handler"""
    try:
        content_id = callback.data.split(":")[1]
        content_url = await menu_api.get_content_url(content_id)
        await callback.message.answer(
            f"📎 Контент доступен по ссылке:\n{content_url}\n\n"
            f"Используйте /menu для возврата в меню."
        )
        await callback.answer("✅ Контент отправлен")
    except Exception as e:
        logger.error(f"Ошибка загрузки контента: {e}")
        await callback.answer(TEXTS['error'], show_alert=True)