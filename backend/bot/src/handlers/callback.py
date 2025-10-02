import asyncio
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards import create_menu_keyboard
from menu_api import API
from utils.menu_update import update_menu_state
from utils.texts import TEXTS
from utils.send_content import send_content_to_user
from utils.states import UserStates
from utils.storage import navigation_stack, rated_menus

logger = logging.getLogger(__name__)

router = Router(name='callback')
menu_api = API()


@router.callback_query(UserStates.navigating, F.data.startswith('menu:'))
async def navigate_menu(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает переход пользователя в подменю.

    Выполняет навигацию по иерархии меню при нажатии на кнопку подменю.
    Сохраняет текущее положение в стек для возможности возврата назад.

    Формат Callback data:
        'menu:{index}' - где index это порядковый номер подменю.

    Функционал:
        - Обновляет стек навигации пользователя,
        - Сбрасывает флаг показа рейтинга,
        - Обновляет состояние меню в FSM,
        - Редактирует сообщение с новым меню.
    """
    try:
        menu_index = _extract_menu_index(callback.data)
        target_menu = await _load_target_menu(state, menu_index)

        if not target_menu:
            await callback.answer(TEXTS['error_start'])
            return

        await _update_navigation_stack(callback.from_user.id, state)
        await _reset_rating_flag(state)

        await update_menu_state(
            state,
            target_menu,
            callback=callback
        )

        logger.debug(
            f'Навигация: пользователь перешел в меню {target_menu.name}')

    except Exception as e:
        logger.error(f'Ошибка при навигации: {e}', exc_info=True)
        await callback.answer(TEXTS['error_start'])


@router.callback_query(UserStates.navigating, F.data == 'home')
async def go_home(callback: CallbackQuery, state: FSMContext):
    """
    Возвращает пользователя в главное меню.

    Полностью очищает стек навигации и загружает корневое меню.
    Используется для быстрого перехода из любого уровня вложенности.

    Функционал:
        - Очищает весь стек навигации пользователя,
        - Сбрасывает флаг показа рейтинга,
        - Загружает и отображает корневое меню,
        - Помечает меню как корневое (is_root=True).
    """
    try:
        user_id = callback.from_user.id
        navigation_stack[user_id] = []

        await _reset_rating_flag(state)

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


@router.callback_query(UserStates.navigating, F.data == 'back')
async def go_back(callback: CallbackQuery, state: FSMContext):
    """
    Возвращает пользователя на предыдущий уровень меню.

    Использует стек навигации для определения предыдущего меню.
    Если стек пуст, уведомляет что пользователь в главном меню.

    Функционал:
        - Извлекает ID предыдущего меню из стека,
        - Загружает меню по ID или корневое при ошибке,
        - Определяет является ли меню корневым,
        - Обновляет отображение меню.
    """
    user_id = callback.from_user.id

    if not _has_navigation_history(user_id):
        await callback.answer('Вы в главном меню')
        return

    try:
        previous_menu = await _get_previous_menu(user_id)

        await _reset_rating_flag(state)

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


@router.callback_query(UserStates.navigating, F.data.startswith('cnt:'))
async def show_content(callback: CallbackQuery, state: FSMContext):
    """
    Отображает выбранный контент пользователю.

    Обрабатывает нажатие на кнопку контента и отправляет
    соответствующий файл или ссылку.

    Формат Callback data:
        'cnt:{index}' - где index это порядковый номер контента.

    Функционал:
        - Извлекает контент по индексу из состояния,
        - Определяет тип контента (файл/URL),
        - Удаляет сообщение с меню перед показом контента,
        - Отправляет контент соответствующим методом,
        - Добавляет навигационные кнопки.
    """
    try:
        content_index = _extract_content_index(callback.data)
        content = await _get_content_by_index(state, content_index)

        if not content:
            await callback.answer(TEXTS['content_not_found'])
            return

        await callback.message.delete()

        await send_content_to_user(callback.message, content)
        await callback.answer()

    except Exception as e:
        logger.error(f'Ошибка при показе контента: {e}')
        await callback.answer(TEXTS['content_not_found'])


@router.callback_query(F.data.startswith('rate:'))
async def rate_content(callback: CallbackQuery):
    """
    Обрабатывает оценку контента пользователем.

    Сохраняет оценку на сервере и отмечает меню как оцененное,
    чтобы не показывать запрос повторно.

    Формат Callback data:
        'rate:{menu_id}:{rating}' - menu_id и булево значение оценки.

    Функционал:
        - Отправляет оценку на API сервер,
        - Сохраняет меню в локальный список оцененных,
        - Показывает обратную связь пользователю,
        - Удаляет сообщение с кнопками оценки.
    """
    try:
        menu_id, rating = _parse_rating_data(callback.data)
        user_id = callback.from_user.id

        success = await menu_api.send_rating(menu_id, user_id, rating)

        if success:
            await _save_user_rating(user_id, menu_id)
            await _show_rating_feedback(callback, rating)
        else:
            await callback.answer(TEXTS['rating_error'])

    except Exception as e:
        logger.error(f'Ошибка при оценке контента: {e}')
        await callback.answer(TEXTS['rating_error'])


@router.callback_query(F.data == 'ask_question')
async def ask_question(callback: CallbackQuery, state: FSMContext):
    """
    Активирует режим ввода вопроса от пользователя.

    Переводит бота в состояние ожидания текста вопроса,
    сохраняя текущий контекст для возможного возврата.

    Функционал:
        - Переключает состояние на waiting_for_question,
        - Сохраняет текущее состояние меню,
        - Отправляет приглашение ввести вопрос,
        - Сохраняет ID сообщения для последующего удаления.
    """
    await state.set_state(UserStates.waiting_for_question)

    await _save_current_menu_state(state)

    bot_message = await callback.message.answer(
        TEXTS['enter_question'],
        parse_mode='HTML'
    )

    await state.update_data(question_prompt_message_id=bot_message.message_id)
    await callback.answer()


@router.callback_query(UserStates.navigating, F.data == 'restore_menu')
async def restore_menu(callback: CallbackQuery, state: FSMContext):
    """
    Восстанавливает меню после просмотра контента.

    Возвращает пользователя к последнему активному меню,
    из которого был запрошен просмотр контента.

    Функционал:
        - Удаляет сообщение с навигационными кнопками,
        - Извлекает ID текущего меню из состояния,
        - Загружает структуру меню по сохраненному ID,
        - Отправляет восстановленное меню с соответствующей клавиатурой.
    """
    try:
        await callback.message.delete()

        state_data = await state.get_data()
        current_menu_id = state_data.get('current_menu_id')

        if current_menu_id:
            current_menu = await menu_api.get_menu_by_id(current_menu_id)
            if current_menu:
                is_root = current_menu.parent_id is None
                keyboard = create_menu_keyboard(current_menu, is_root=is_root)
                text = f'<b>{current_menu.name}</b>\n\n{current_menu.text}'

                await callback.message.answer(
                    text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )

        await callback.answer()

    except Exception as e:
        logger.error(f'Ошибка при восстановлении меню: {e}')
        await callback.answer(TEXTS['error'])


# ============= Вспомогательные функции =============

def _extract_menu_index(data: str) -> int:
    """Извлекает индекс меню из callback data."""
    return int(data.split(':', 1)[1])


def _extract_content_index(data: str) -> int:
    """Извлекает индекс контента из callback data."""
    return int(data.split(':', 1)[1])


async def _load_target_menu(state: FSMContext, menu_index: int):
    """Загружает целевое меню по индексу."""
    state_data = await state.get_data()
    current_children = state_data.get('current_children', [])

    if menu_index >= len(current_children):
        return None

    menu_name = current_children[menu_index]
    return await menu_api.find_menu_by_name(menu_name)


async def _update_navigation_stack(user_id: int, state: FSMContext):
    """Обновляет стек навигации пользователя."""
    if user_id not in navigation_stack:
        navigation_stack[user_id] = []

    state_data = await state.get_data()
    current_menu_id = state_data.get('current_menu_id')
    navigation_stack[user_id].append(current_menu_id)


async def _reset_rating_flag(state: FSMContext):
    """Сбрасывает флаг показа рейтинга."""
    await state.update_data(rating_shown=False)


def _has_navigation_history(user_id: int) -> bool:
    """Проверяет наличие истории навигации."""
    return user_id in navigation_stack and bool(navigation_stack[user_id])


async def _get_previous_menu(user_id: int):
    """Получает предыдущее меню из стека навигации."""
    previous_menu_id = navigation_stack[user_id].pop()
    previous_menu = await menu_api.get_menu_by_id(previous_menu_id)

    if not previous_menu:
        previous_menu = await menu_api.get_root_menu()
        navigation_stack[user_id] = []

    return previous_menu


async def _get_content_by_index(state: FSMContext, content_index: int):
    """Получает контент по индексу из состояния."""
    state_data = await state.get_data()
    current_content = state_data.get('current_content', [])

    if content_index >= len(current_content):
        return None

    return current_content[content_index]


def _parse_rating_data(data: str):
    """Парсит данные рейтинга из callback data."""
    _, menu_id, rating = data.split(':')
    return menu_id, bool(int(rating))


async def _save_user_rating(user_id: int, menu_id: str):
    """Сохраняет оценку пользователя."""
    if user_id not in rated_menus:
        rated_menus[user_id] = set()
    rated_menus[user_id].add(menu_id)


async def _show_rating_feedback(callback: CallbackQuery, rating: bool):
    """Показывает обратную связь после оценки."""
    rating_text = (
        TEXTS['rating_positive_feedback'] if rating is True
        else TEXTS['rating_negative_feedback']
    )

    await callback.answer(text=rating_text)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()


async def _save_current_menu_state(state: FSMContext):
    """Сохраняет текущее состояние меню перед переходом."""
    current_data = await state.get_data()
    await state.update_data(
        previous_menu_id=current_data.get('current_menu_id'),
        previous_children=current_data.get('current_children'),
        previous_content=current_data.get('current_content')
    )
