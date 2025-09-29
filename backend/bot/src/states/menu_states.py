from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    """Класс состояний для меню."""

    navigating = State()
    waiting_input = State()
    viewing_content = State()
