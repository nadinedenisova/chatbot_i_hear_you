from typing import Dict


class MenuContent:
    """Класс модели MenuContent."""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.menu_id = data.get("menu_id")
        self.type = data.get("type")
        self.server_path = data.get("server_path")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    def to_dict(self) -> Dict:
        """Преобразует объект в словарь."""
        return {
            "id": self.id,
            "menu_id": self.menu_id,
            "type": self.type,
            "server_path": self.server_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
