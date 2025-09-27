# db_engine.py
from uuid import UUID
from typing import Sequence, AsyncGenerator
from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException, status

from db.postgres import get_async_session
from models.users import User
from models.questions import Question
from models.history import History
from models.ratings import Rating
from models.nodes import MenuNode
from models.contents import Content
from schemas.entity import (
    UserCreate, QuestionCreate, HistoryCreate,
    RatingCreate, MenuNodeCreate, MenuNodeUpdate, ContentCreate
)
from utils.pagination import PaginatedParams


class DBEngine:
    """Движок для работы с базой данных"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # User methods
    async def get_users(self, pagination: PaginatedParams) -> Sequence[User]:
        """Получение списка пользователей с пагинацией"""
        stmt = (
            select(User)
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(User.phone_number)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Получение пользователя по ID"""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """Создание нового пользователя"""
        user = User(
            id=UUID(user_data.id),
            phone_number=user_data.phone_number
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_long_time_lost_users(self, days_count: int, pagination: PaginatedParams) -> Sequence[User]:
        """Получение пользователей, которые долго не появлялись"""
        cutoff_date = func.now() - func.make_interval(days=days_count)

        stmt = (
            select(User)
            .outerjoin(History, User.id == History.user_id)
            .group_by(User.id)
            .having(
                and_(
                    func.max(History.action_date) < cutoff_date,
                    func.count(History.id) > 0
                )
            )
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(User.phone_number)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Question methods
    async def get_user_questions(self, user_id: UUID) -> Sequence[Question]:
        """Получение всех вопросов пользователя"""
        stmt = (
            select(Question)
            .where(Question.user_id == user_id)
            .order_by(Question.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_questions(self, pagination: PaginatedParams) -> Sequence[Question]:
        """Получение всех вопросов с пагинацией"""
        stmt = (
            select(Question)
            .offset(pagination.offset)
            .limit(pagination.limit)
            .order_by(Question.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_question(self, question_data: QuestionCreate) -> Question:
        """Создание нового вопроса"""
        question = Question(
            user_id=UUID(question_data.user_id),
            text=question_data.text
        )
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def answer_question(self, question_id: UUID, answer: str) -> Question:
        """Ответ на вопрос"""
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        return question

    # History methods
    async def create_history_record(self, history_data: HistoryCreate) -> History:
        """Создание записи истории пользователя"""
        history = History(
            user_id=UUID(history_data.user_id),
            menu_id=history_data.menu_id
        )
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history

    async def get_user_history(self, user_id: UUID, pagination: PaginatedParams) -> Sequence[History]:
        """Получение истории пользователя"""
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
        """Получение полного дерева меню"""
        stmt = (
            select(MenuNode)
            .options(selectinload(MenuNode.content))
            .order_by(MenuNode.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_menu_node_by_id(self, menu_id: UUID) -> MenuNode | None:
        """Получение узла меню по ID"""
        stmt = (
            select(MenuNode)
            .where(MenuNode.id == menu_id)
            .options(selectinload(MenuNode.content))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_menu_node_by_name(self, name: str) -> MenuNode | None:
        """Получение узла меню по имени"""
        stmt = (
            select(MenuNode)
            .where(MenuNode.name == name)
            .options(selectinload(MenuNode.content))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_menu_root(self) -> MenuNode | None:
        """Получение корневого узла меню"""
        stmt = (
            select(MenuNode)
            .where(MenuNode.parent_id.is_(None))
            .options(selectinload(MenuNode.content))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_menu_node(self, node_data: MenuNodeCreate) -> MenuNode:
        """Создание нового узла меню"""
        menu_node = MenuNode(
            parent_id=node_data.parent_id,
            name=node_data.name,
            text=node_data.text,
            subscription_type=node_data.subscription_type
        )
        self.session.add(menu_node)
        await self.session.commit()
        await self.session.refresh(menu_node)
        return menu_node

    async def update_menu_node(self, menu_id: UUID, node_data: MenuNodeUpdate) -> MenuNode:
        """Обновление узла меню"""
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu node not found"
            )
        return node

    async def delete_menu_node(self, menu_id: UUID) -> bool:
        """Удаление узла меню"""
        stmt = delete(MenuNode).where(MenuNode.id == menu_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # Content methods
    async def add_content_to_menu(self, menu_id: UUID, content_data: ContentCreate) -> Content:
        """Добавление контента к узлу меню"""
        content = Content(
            menu_id=menu_id,
            type=content_data.type,
            server_path=content_data.server_path
        )
        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)
        return content

    async def update_content(self, content_id: UUID, content_data: ContentCreate) -> Content:
        """Обновление контента"""
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        return content

    async def delete_content(self, content_id: UUID) -> bool:
        """Удаление контента"""
        stmt = delete(Content).where(Content.id == content_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # Rating methods
    async def get_menu_rating(self, menu_id: UUID) -> float | None:
        """Получение среднего рейтинга узла меню"""
        stmt = (
            select(func.avg(Rating.node_rating))
            .where(Rating.menu_id == menu_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def rate_menu_node(self, rating_data: RatingCreate, menu_id: UUID) -> Rating:
        """Оценка узла меню"""
        # Проверяем, есть ли уже оценка от этого пользователя
        existing_stmt = select(Rating).where(
            and_(
                Rating.user_id == UUID(rating_data.user_id),
                Rating.menu_id == menu_id
            )
        )
        existing_result = await self.session.execute(existing_stmt)
        existing_rating = existing_result.scalar_one_or_none()

        if existing_rating:
            # Обновляем существующую оценку
            existing_rating.node_rating = rating_data.node_rating
            await self.session.commit()
            await self.session.refresh(existing_rating)
            return existing_rating
        else:
            # Создаем новую оценку
            rating = Rating(
                user_id=UUID(rating_data.user_id),
                menu_id=menu_id,
                node_rating=rating_data.node_rating
            )
            self.session.add(rating)
            await self.session.commit()
            await self.session.refresh(rating)
            return rating


def get_db_engine(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[DBEngine, None]:
    """Зависимость для получения экземпляра DBEngine"""
    yield DBEngine(session)