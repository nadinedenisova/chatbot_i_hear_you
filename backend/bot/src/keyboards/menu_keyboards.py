from typing import List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.menu import Menu
from utils.texts import TEXTS


class MenuKeyboard:
    """Класс для создания inline клавиатур с меню."""

    @staticmethod
    def create_menu_keyboard(
        menu: Menu,
        user_id: int,
        show_navigation: bool = True,
        is_root: bool = False,
    ) -> InlineKeyboardMarkup:
        """Функция для создания inline клавиатуры с меню."""
        buttons = []

        # Подпункты:
        if menu.has_children():
            for i, child_name in enumerate(menu.children_names):
                child_id = (
                    menu.children[i].id if i < len(menu.children) else f"child_{i}"
                )
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=child_name, callback_data=f"menu:{child_id}"
                        )
                    ]
                )

        # Контент:
        if menu.content:
            for content in menu.content:
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=TEXTS["content"], callback_data=f"content:{content.id}"
                        )
                    ]
                )

        # Навигационные кнопки:
        if show_navigation:
            nav_buttons = []

            # Если не корневое меню, добавляем кнопку "Назад"
            if not is_root:
                nav_buttons.append(
                    InlineKeyboardButton(text=TEXTS["back"], callback_data="back")
                )
            # Кнопка "Домой"
            nav_buttons.append(
                InlineKeyboardButton(text=TEXTS["home"], callback_data="home")
            )

            if nav_buttons:
                buttons.append(nav_buttons)

        return InlineKeyboardMarkup(inline_keyboard=buttons)
