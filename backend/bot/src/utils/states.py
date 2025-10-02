from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    """Состояния для навигации по меню"""
    navigating = State()
    waiting_for_question = State()
