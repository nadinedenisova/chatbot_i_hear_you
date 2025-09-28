from typing import Dict, List, Optional

from .content import MenuContent


class Menu:
    """Класс модели Menu."""
    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.parent_id = data.get('parent_id')
        self.name = data.get('name')
        self.text: Optional[str] = data.get('text')
        self.subscription_type = data.get('subscription_type')
        self.content: List[MenuContent] = [
            MenuContent(content) for content in data.get('content', [])
        ]
        self.children_names: List[str] = data.get('children_names', [])
        self.children: List['Menu'] = [
            Menu(child) for child in data.get('children', [])
        ]

    def to_dict(self) -> Dict:
        """Преобразует объект в словарь."""
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'text': self.text,
            'subscription_type': self.subscription_type,
        }

    def has_children(self) -> bool:
        """Проверяет, есть ли у меню дочерние элементы."""
        return len(self.children) > 0

    def has_content(self) -> bool:
        """Проверяет, есть ли у меню контент."""
        return len(self.content) > 0
