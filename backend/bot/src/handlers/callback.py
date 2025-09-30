import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from menu_api import API
from utils.menu_update import update_menu_state
from utils.texts import TEXTS

logger = logging.getLogger(__name__)

router = Router(name='callback')


class States(StatesGroup):
    """Состояния для навигации по меню"""
    navigating = State()


# Инициализируем API и хранилище для навигации (стек меню)
menu_api = API()
navigation_stack: dict[int, list[str]] = {}


@router.callback_query(States.navigating, F.data.startswith('menu:'))
async def navigate_menu(callback: CallbackQuery, state: FSMContext):
    """Переход в подменю"""
    # Получаем индекс нажатой клавиши
    menu_index = callback.data.split(':', 1)[1]

    try:
        # Получаем текущее меню и дочерние клавиши (если есть) из состояния.
        state_data = await state.get_data()
        current_menu_id = state_data.get('current_menu_id')
        current_children = state_data.get('current_children', [])

        # Проверяем валидность индекса, чтобы предотвратить ошибку
        # при обращении к несуществующему элементу списка.
        menu_index = int(menu_index)
        if menu_index >= len(current_children):
            await callback.answer(TEXTS['error_start'])
            return

        # Загружаем меню по имени через API
        menu_name = current_children[menu_index]
        target_menu = await menu_api.find_menu_by_name(menu_name)

        if not target_menu:
            await callback.answer(TEXTS['error_start'])
            return

        # Добавляем текущее меню в стек навигации
        user_id = callback.from_user.id
        if user_id not in navigation_stack:
            navigation_stack[user_id] = []
        navigation_stack[user_id].append(current_menu_id)
        logger.debug(
            f'Навигация: пользователь перешел в меню {target_menu.name}')

        # Отпраляем обновленное меню
        await update_menu_state(
            state,
            target_menu,
            callback=callback
        )

    except Exception as e:
        logger.error(f'Ошибка при навигации: {e}', exc_info=True)
        await callback.answer(TEXTS['error_start'])


@router.callback_query(States.navigating, F.data.startswith('cnt:'))
async def show_content(callback: CallbackQuery, state: FSMContext):
    """Показ контента"""
    # Получаем индекс нажатой клавиши
    content_index = callback.data.split(':', 1)[1]

    try:
        # Получаем текущее меню из состояния
        state_data = await state.get_data()
        current_content = state_data.get('current_content', [])

        # Получаем контент по индексу
        content_index = int(content_index)
        if content_index >= len(current_content):
            await callback.answer(TEXTS['content_not_found'])
            return
        content = current_content[content_index]
        content_url = content.get('server_path', '')

        await callback.message.answer(
            f'{TEXTS['get_content']}'
            f'{content_url}'
        )

    except Exception as e:
        logger.error(f'Ошибка при показе контента: {e}')
        await callback.answer(TEXTS['content_not_found'])


@router.callback_query(States.navigating, F.data == 'home')
async def go_home(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    try:
        user_id = callback.from_user.id
        # Очищаем стек навигации
        navigation_stack[user_id] = []

        # Отправляем сообщение с главным меню
        root_menu = await menu_api.get_root_menu()
        await update_menu_state(
            state,
            root_menu,
            callback=callback,
            is_root=True
        )

    except Exception as e:
        logger.error(f'Ошибка при возврате в главное меню: {e}')
        await callback.answer(TEXTS['error_start'])


@router.callback_query(States.navigating, F.data == 'back')
async def go_back(callback: CallbackQuery, state: FSMContext):
    """Возврат назад"""
    user_id = callback.from_user.id

    if user_id not in navigation_stack or not navigation_stack[user_id]:
        await callback.answer('Вы в главном меню')
        return

    try:
        # Получаем ID предыдущего меню из стека
        previous_menu_id = navigation_stack[user_id].pop()
        previous_menu = await menu_api.get_menu_by_id(previous_menu_id)
        if not previous_menu:
            # Если не нашли меню, возвращаемся в корень
            previous_menu = await menu_api.get_root_menu()
            navigation_stack[user_id] = []

        # отправляем сообщение с предыдущим меню
        is_root = previous_menu.parent_id is None
        await update_menu_state(
            state,
            previous_menu,
            callback=callback,
            is_root=is_root
        )

    except Exception as e:
        logger.error(f'Ошибка при возврате назад: {e}')
        await callback.answer(TEXTS['error'])
