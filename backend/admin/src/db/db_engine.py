# db_engine.py
from uuid import UUID
from typing import Sequence
from sqlalchemy import select, update, delete, and_, func, text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException, status

from src.db.postgres import get_async_session
from src.models.users import User
from src.models.questions import Question
from src.models.history import History
from src.models.ratings import UserMenuNode
from src.models.nodes import MenuNode
from src.models.contents import Content
from src.schemas.entity import (
    UserCreate,
    QuestionCreate,
    HistoryCreate,
    RatingCreate,
    RatingDetailOut,
    RatingListOut,
    MenuNodeCreate,
    MenuNodeUpdate,
    ContentCreate,
)
from src.utils.pagination import PaginatedParams


class DBEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_content_with_file(
            self, menu_id: UUID, content_data: ContentCreate, file_info: dict
    ) -> Content:
        """Добавляет контент с информацией о файле"""
        content = Content(
            menu_id=menu_id,
            type=content_data.type,
            # Используем реальный путь к файлу
            server_path=file_info["server_path"],
        )
        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)
        return content

    async def update_content_with_file(
        self, content_id: UUID, content_data: ContentCreate, file_info: dict
    ) -> Content:
        """Обновляет контент с новым файлом"""
        # Сначала получаем старый контент чтобы удалить старый файл
        old_content = await self.get_content_by_id(content_id)

        stmt = (
            update(Content)
            .where(Content.id == content_id)
            .values(
                type=content_data.type,
                server_path=file_info["server_path"],
                updated_at=func.now()
            )
            .returning(Content)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        content = result.scalar_one_or_none()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
            )

        # Удаляем старый файл если он существует
        if old_content and old_content.server_path != file_info["server_path"]:
            # Здесь можно добавить удаление старого файла
            pass

        return content

    async def get_content_by_id(self, content_id: UUID) -> Content | None:
        """Получает контент по ID"""
        stmt = select(Content).where(Content.id == content_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    # User methods

    async def get_users(self, pagination: PaginatedParams) -> Sequence[User]:
        stmt = (
            select(User)
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(User.phone_number)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: str) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        # Проверяем, существует ли пользователь
        existing_user = await self.get_user_by_id(user_data.id)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        user = User(id=user_data.id, phone_number=user_data.phone_number)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_long_time_lost_users(
            self, days_count: int, pagination: PaginatedParams
    ) -> Sequence[User]:
        # Для PostgreSQL (рекомендуемый)
        cutoff_date = func.now() - text(f"INTERVAL '{days_count} days'")

        subquery = (
            select(History.user_id)
            .group_by(History.user_id)
            .having(func.max(History.action_date) < cutoff_date)
        ).alias("lost_users")

        stmt = (
            select(User)
            .join(subquery, User.id == subquery.c.user_id)
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(User.phone_number)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Question methods
    async def get_user_questions(self, user_id: str) -> Sequence[Question]:
        stmt = (
            select(Question)
            .where(Question.user_id == user_id)
            .order_by(Question.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_questions(
        self, pagination: PaginatedParams
    ) -> Sequence[Question]:
        stmt = (
            select(Question)
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(Question.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_question(self, question_data: QuestionCreate) -> Question:
        question = Question(user_id=question_data.user_id,
                            text=question_data.text)
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def delete_question(self, question_id: UUID) -> bool:
        stmt = delete(Question).where(Question.id == question_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def answer_question(self, question_id: UUID, answer: str) -> Question:
        stmt = (
            update(Question)
            .where(Question.id == question_id)
            .values(admin_answer=answer, updated_at=func.now())
            .returning(Question)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        question = result.scalar_one_or_none()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        return question

    # History methods
    async def create_history_record(
        self, user_id: str, history_data: HistoryCreate
    ) -> History:
        history = History(
            user_id=user_id,
            menu_id=history_data.menu_id,
            action_date=history_data.action_date,
        )
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history

    async def get_user_history(
        self, user_id: str, pagination: PaginatedParams
    ) -> Sequence[History]:
        stmt = (
            select(History)
            .where(History.user_id == user_id)
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(History.action_date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Menu methods
    async def get_full_menu(self) -> Sequence[MenuNode]:
        stmt = (
            select(MenuNode)
            .options(selectinload(MenuNode.content))
            .order_by(MenuNode.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_menu_node_by_id(self, menu_id: UUID) -> MenuNode | None:
        stmt = (
            select(MenuNode)
            .where(MenuNode.id == menu_id)
            .options(selectinload(MenuNode.content))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_menu_node_by_name(self, name: str) -> MenuNode | None:
        stmt = (
            select(MenuNode)
            .where(MenuNode.name == name)
            .options(selectinload(MenuNode.content))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_menu_root(self) -> MenuNode | None:
        stmt = (
            select(MenuNode)
            .where(MenuNode.parent_id.is_(None))
            .options(selectinload(MenuNode.content))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def search_menu_nodes(self, keywords: str) -> Sequence[MenuNode]:
        """Поиск узлов меню по ключевым словам с использованием ILIKE."""
        terms = keywords.split()  # Разделяем на отдельные слова
        conditions = []
        for term in terms:
            conditions.append(MenuNode.name.ilike(f"%{term}%"))
            if MenuNode.text is not None:  # Проверяем, чтобы избежать ошибок если text NULL
                conditions.append(MenuNode.text.ilike(f"%{term}%"))

        if not conditions:
            return []

        stmt = (
            select(MenuNode)
            .options(selectinload(MenuNode.content))
            .where(or_(*conditions))
            .order_by(MenuNode.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_menu_node(self, node_data: MenuNodeCreate) -> MenuNode:
        menu_node = MenuNode(
            parent_id=node_data.parent_id,
            name=node_data.name,
            text=node_data.text,
            subscription_type=node_data.subscription_type,
        )
        self.session.add(menu_node)
        await self.session.commit()
        await self.session.refresh(menu_node)
        return menu_node

    async def update_menu_node(
        self, menu_id: UUID, node_data: MenuNodeUpdate
    ) -> MenuNode:
        stmt = (
            update(MenuNode)
            .where(MenuNode.id == menu_id)
            .values(**node_data.model_dump(exclude_unset=True))
            .returning(MenuNode)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        node = result.scalar_one_or_none()
        if not node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu node not found"
            )
        return node

    async def delete_menu_node(self, menu_id: UUID) -> bool:
        stmt = delete(MenuNode).where(MenuNode.id == menu_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # Content methods
    async def add_content_to_menu(
        self, menu_id: UUID, content_data: ContentCreate
    ) -> Content:
        content = Content(
            menu_id=menu_id,
            type=content_data.type,
            server_path=content_data.server_path,
        )
        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)
        return content

    async def update_content(
        self, content_id: UUID, content_data: ContentCreate
    ) -> Content:
        stmt = (
            update(Content)
            .where(Content.id == content_id)
            .values(**content_data.model_dump(exclude_unset=True))
            .returning(Content)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        content = result.scalar_one_or_none()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
            )
        return content

    async def delete_content(self, content_id: UUID) -> bool:
        stmt = delete(Content).where(Content.id == content_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_menu_rating_summary(self, menu_id: UUID) -> dict:
        useful_stmt = select(func.count(UserMenuNode.id)).where(
            and_(
                UserMenuNode.menu_id == menu_id,
                UserMenuNode.post_rating == True
            )
        )
        useful_result = await self.session.execute(useful_stmt)
        useful_count = useful_result.scalar() or 0
        not_useful_stmt = select(func.count(UserMenuNode.id)).where(
            and_(
                UserMenuNode.menu_id == menu_id,
                UserMenuNode.post_rating == False
            )
        )
        not_useful_result = await self.session.execute(not_useful_stmt)
        not_useful_count = not_useful_result.scalar() or 0
        return {
            "useful_count": useful_count,
            "not_useful_count": not_useful_count
        }

    async def rate_menu_node(
        self, rating_data: RatingCreate, menu_id: UUID
    ) -> UserMenuNode:
        user = await self.get_user_by_id(rating_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {rating_data.user_id} not found"
            )
        menu_node = await self.get_menu_node_by_id(menu_id)
        if not menu_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu node with id {menu_id} not found"
            )
        existing_stmt = select(UserMenuNode).where(
            and_(
                UserMenuNode.user_id == rating_data.user_id,
                UserMenuNode.menu_id == menu_id,
            )
        )
        existing_result = await self.session.execute(existing_stmt)
        existing_rating = existing_result.scalar_one_or_none()
        if existing_rating:
            existing_rating.post_rating = rating_data.is_useful
            existing_rating.updated_at = func.now()
            await self.session.commit()
            await self.session.refresh(existing_rating)
            return existing_rating
        else:
            rating = UserMenuNode(
                user_id=rating_data.user_id,
                menu_id=menu_id,
                post_rating=rating_data.is_useful,
            )
            self.session.add(rating)
            await self.session.commit()
            await self.session.refresh(rating)
            return rating

    async def get_menu_ratings_all(self, menu_id: UUID) -> RatingListOut:
        menu_node = await self.get_menu_node_by_id(menu_id)
        if not menu_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu node with id {menu_id} not found"
            )
        stmt = select(UserMenuNode).where(UserMenuNode.menu_id == menu_id)
        result = await self.session.execute(stmt)
        ratings = result.scalars().all()
        rating_out_list = []
        for rating in ratings:
            rating_out = RatingDetailOut(
                user_id=rating.user_id,
                is_useful=rating.post_rating,
                created_at=rating.created_at,
                updated_at=rating.updated_at
                )
            rating_out_list.append(rating_out)
        return RatingListOut(menu_id=menu_id, ratings=rating_out_list)


def get_db_engine(session: AsyncSession = Depends(get_async_session)):
    return DBEngine(session)


def create_db_engine(session: AsyncSession) -> DBEngine:
    return DBEngine(session)
