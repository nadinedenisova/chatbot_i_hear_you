# services/menu_service.py

from uuid import UUID
from typing import Sequence
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from src.db.db_engine import DBEngine, get_db_engine
from src.models.nodes import MenuNode
from src.schemas.entity import (
    MenuNodeCreate,
    MenuNodeUpdate,
    MenuNodeOut,
    AllMenuNodeOut,
    ContentCreate,
    RatingCreate,
    RatingOut,
    Message,
    ContentOut,
)
from src.services.file_service import file_service
from fastapi import UploadFile


class MenuService:
    """Сервис для работы с меню."""

    def __init__(self, db_engine: DBEngine):
        self.db_engine = db_engine

    async def _get_children_names(self, parent_id: UUID) -> list[str]:
        stmt = select(MenuNode.name).where(MenuNode.parent_id == parent_id)
        result = await self.db_engine.session.execute(stmt)
        return result.scalars().all()

    async def _build_menu_tree(
        self, nodes: Sequence[MenuNodeOut]
    ) -> list[AllMenuNodeOut]:
        """Построение дерева меню из плоского списка."""
        node_map = {
            node.id: AllMenuNodeOut(**node.model_dump(), children=[]) for node in nodes
        }
        root_nodes = []

        for node in nodes:
            if node.parent_id and node.parent_id in node_map:
                node_map[node.parent_id].children.append(node_map[node.id])
            else:
                root_nodes.append(node_map[node.id])

        return root_nodes

    def _get_content_list(self, node: MenuNode) -> list[ContentOut]:
        """Получение списка контента для узла меню."""
        return [
            ContentOut(
                id=c.id,
                menu_id=c.menu_id,
                type=c.type,
                server_path=c.server_path,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in node.content
        ] if node.content else []
    async def _get_node_by_id(self, node_id: UUID) -> MenuNode:
        node = await self.db_engine.get_menu_node_by_id(node_id)
        if not node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu node not found"
            )
        return node

    async def get_full_menu(self) -> AllMenuNodeOut:
        """Получение полного дерева меню."""
        menu_nodes = await self.db_engine.get_full_menu()

        if not menu_nodes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No menu nodes found"
            )

        node_out_list = [
            MenuNodeOut(
                id=node.id,
                parent_id=node.parent_id,
                name=node.name,
                text=node.text,
                subscription_type=node.subscription_type,
                content=self._get_content_list(node),
                children_names=[
                    child.name for child in menu_nodes if child.parent_id == node.id
                ],
            )
            for node in menu_nodes
        ]

        tree = await self._build_menu_tree(node_out_list)
        return (
            tree[0]
            if tree
            else AllMenuNodeOut(
                id=UUID(int=0),
                name="Empty Menu",
                text="No menu items available",
                content=[],
                children_names=[],
                children=[],
            )
        )

    async def get_menu_node_by_name(self, name: str) -> MenuNodeOut:
        """Получение узла меню по имени."""
        node = await self.db_engine.get_menu_node_by_name(name)
        if not node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu node not found"
            )

        children_names = await self._get_children_names(node.id)

        return MenuNodeOut(
            id=node.id,
            parent_id=node.parent_id,
            name=node.name,
            text=node.text,
            subscription_type=node.subscription_type,
            content=self._get_content_list(node),
            children_names=children_names,
        )

    async def get_menu_root(self) -> MenuNodeOut:
        """Получение корневого узла меню."""
        node = await self.db_engine.get_menu_root()
        if not node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Root menu node not found"
            )

        children_names = await self._get_children_names(node.id)

        return MenuNodeOut(
            id=node.id,
            parent_id=node.parent_id,
            name=node.name,
            text=node.text,
            subscription_type=node.subscription_type,
            content=self._get_content_list(node),
            children_names=children_names,
        )

    async def get_menu_node_by_id(self, menu_id: UUID) -> MenuNodeOut:
        """Получение узла меню по ID."""
        node = await self._get_node_by_id(menu_id)

        children_names = await self._get_children_names(node.id)

        return MenuNodeOut(
            id=node.id,
            parent_id=node.parent_id,
            name=node.name,
            text=node.text,
            subscription_type=node.subscription_type,
            content=self._get_content_list(node),
            children_names=children_names,
        )

    async def add_menu_node(self, node_data: MenuNodeCreate) -> Message:
        """Добавление узла меню."""

        if node_data.parent_id:
            parent = await self.db_engine.get_menu_node_by_id(node_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent menu node not found",
                )

        if await self.db_engine.get_menu_node_by_name(node_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Node with the same name already exists",
            )
        await self.db_engine.create_menu_node(node_data)
        return Message(detail="The menu node was added")

    async def update_menu_node(
        self, menu_id: UUID, node_data: MenuNodeUpdate
    ) -> Message:
        """Обновление узла меню."""
        await self._get_node_by_id(menu_id)  # проверка есть ли menu_node с таким id

        if node_data.parent_id:
            parent = await self.db_engine.get_menu_node_by_id(node_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent menu node not found",
                )

        if await self.db_engine.get_menu_node_by_name(node_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Node with the same name already exists",
            )

        await self.db_engine.update_menu_node(menu_id, node_data)
        return Message(detail="The menu node was updated")

    async def delete_menu_node(self, menu_id: UUID) -> Message:
        """Удаление узла меню."""
        success = await self.db_engine.delete_menu_node(menu_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu node not found"
            )
        return Message(detail="The menu node was deleted.")

    async def add_menu_content(
        self, menu_id: UUID, content_data: ContentCreate
    ) -> Message:
        """Добавление контента к узлу меню."""
        await self._get_node_by_id(menu_id)  # проверка есть ли menu_node с таким id
        await self.db_engine.add_content_to_menu(menu_id, content_data)
        return Message(detail="The content was added")

    async def update_menu_content(
        self, content_id: UUID, content_data: ContentCreate
    ) -> Message:
        """Обновление контента."""
        await self._get_node_by_id(content_data.menu_id)  # проверка есть ли menu_node с таким id
        await self.db_engine.update_content(content_id, content_data)
        return Message(detail="The content was changed")

    async def delete_menu_content(self, content_id: UUID) -> Message:
        """Удаление контента."""
        success = await self.db_engine.delete_content(content_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
            )
        return Message(detail="The node content was deleted")

    async def add_menu_content_with_file(
            self, menu_id: UUID, content_data: ContentCreate, file: UploadFile
    ) -> Message:
        """Добавляет контент с загрузкой файла"""
        await self._get_node_by_id(menu_id)  # проверка есть ли menu_node с таким id
        # Сохраняем файл
        file_info = await file_service.save_upload_file(file)

        # Добавляем контент в БД
        await self.db_engine.add_content_with_file(menu_id, content_data, file_info)
        return Message(detail="The content was added with file")

    async def update_menu_content_with_file(
            self, content_id: UUID, content_data: ContentCreate, file: UploadFile
    ) -> Message:
        """Обновляет контент с новым файлом"""
        await self._get_node_by_id(content_data.menu_id)  # проверка есть ли menu_node с таким id

        # Сохраняем новый файл
        file_info = await file_service.save_upload_file(file)

        # Обновляем контент в БД
        await self.db_engine.update_content_with_file(content_id, content_data, file_info)
        return Message(detail="The content was changed with new file")

    # TODO рейтинг это количество оценок "Полезно" и "Не очень" а не цифра
    async def get_menu_node_rate(self, menu_id: UUID) -> RatingOut:
        """Получение рейтинга узла меню."""
        avg_rating = await self.db_engine.get_menu_rating(menu_id)

        return RatingOut(
            user_id="system",
            menu_id=menu_id,
            node_rating=int(avg_rating) if avg_rating else 0,
            created_at=None,
            updated_at=None,
        )

    async def rate_menu_node(self, menu_id: UUID, rating_data: RatingCreate) -> Message:
        """Оценка узла меню."""
        await self._get_node_by_id(menu_id) #проверка есть ли menu_node с таким id

        user= await self.db_engine.get_user_by_id(rating_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await self.db_engine.rate_menu_node(rating_data, menu_id)
        return Message(detail="The node was successfully rated!")


def get_menu_service(db_engine: DBEngine = Depends(get_db_engine)) -> MenuService:
    """Зависимость для получения MenuService."""
    return MenuService(db_engine)
