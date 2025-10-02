from typing import Dict, List, Optional

from utils.texts import TEXTS


class Content:
    """Класс модели MenuContent."""

    CONTENT_TYPES = {
            1: TEXTS['photo_type'],
            2: TEXTS['video_type'],
            3: TEXTS['doc_type']
        }

    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.menu_id = data.get('menu_id')
        self.type = data.get('type')
        self.server_path = data.get('server_path')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def to_dict(self) -> Dict:
        """Преобразует объект в словарь."""
        return {
            'id': self.id,
            'menu_id': self.menu_id,
            'type': self.type,
            'server_path': self.server_path,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def get_content_type(self) -> str:
        """Возвращает строковое представление типа контента."""
        if self.type is None:
            return TEXTS['unknown_type_content']
        return self.CONTENT_TYPES.get(self.type, TEXTS['unknown_type_content'])


class Menu:
    """Класс модели Menu."""
    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.parent_id = data.get('parent_id')
        self.name = data.get('name')
        self.text: Optional[str] = data.get('text')
        self.subscription_type = data.get('subscription_type')
        self.content: List[Content] = [
            Content(content) for content in data.get('content', [])
        ]
        self.children_names: List[str] = data.get('children_names', [])

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
        return len(self.children_names) > 0

    def has_content(self) -> bool:
        """Проверяет, есть ли у меню контент."""
        return len(self.content) > 0
