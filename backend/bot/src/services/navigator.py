import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class NavigatorService:
    def __init__(self) -> None:
        self.user_positions: Dict[int, str] = {}
        self.navigation_stack: Dict[int, List[str]] = {}

    def get_current_position(self, user_id: int) -> Optional[str]:
        """Получить текущую позицию пользователя."""
        return self.user_positions.get(user_id)

    def set_position(self, user_id: int, menu_id: str) -> None:
        """Установить текущую позицию пользователя."""
        self.user_positions[user_id] = menu_id

        if user_id not in self.navigation_stack:
            self.navigation_stack[user_id] = []

        # Проверяем, чтобы не было дублирования в стеке:
        # - если стек пустой или последний элемент не равен текущему menu_id
        if not self.navigation_stack[user_id] or \
           self.navigation_stack[user_id][-1] != menu_id:
            self.navigation_stack[user_id].append(menu_id)

            # Ограничиваем размер стека до 50 элементов
            if len(self.navigation_stack[user_id]) > 50:
                self.navigation_stack[user_id] \
                    = self.navigation_stack[user_id][-50:]

    def go_back(self, user_id: int) -> Optional[str]:
        """Вернуться на предыдущую позицию."""
        if (user_id in self.navigation_stack and
                len(self.navigation_stack[user_id]) > 1):
            self.navigation_stack[user_id].pop()

            # Устанавливаем текущую позицию на предыдущую
            previous = self.navigation_stack[user_id][-1] \
                if self.navigation_stack[user_id] else None
            if previous:
                self.user_positions[user_id] = previous
            return previous
        return None

    def reset(self, user_id: int) -> None:
        """Сбросить навигацию пользователя."""
        self.user_positions.pop(user_id, None)
        self.navigation_stack.pop(user_id, None)

    def get_navigation_stack(self, user_id: int) -> List[str]:
        """Получить навигационный стек пользователя."""
        return self.navigation_stack.get(user_id, [])
