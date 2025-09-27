# services/user_service.py
from uuid import UUID
from fastapi import Depends, HTTPException, status

from db.db_engine import DBEngine, get_db_engine
from schemas.entity import (
    UserCreate, UserOut, UsersListOut, QuestionCreate,
    HistoryCreate, HistoryOut, QuestionOut, QuestionsListOut
)
from utils.pagination import PaginatedParams


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, db_engine: DBEngine):
        self.db_engine = db_engine

    async def get_users(self, pagination: PaginatedParams) -> UsersListOut:
        """Получение списка пользователей"""
        users = await self.db_engine.get_users(pagination)
        user_out_list = [
            UserOut(
                id=str(user.id),
                phone_number=user.phone_number,
                created_at=user.created_at.date(),
                updated_at=user.updated_at.date() if user.updated_at else user.created_at.date()
            )
            for user in users
        ]
        return UsersListOut(items=user_out_list)

    async def create_user(self, user_data: UserCreate) -> dict:
        """Создание пользователя"""
        user = await self.db_engine.create_user(user_data)
        return {"detail": f"User {user.phone_number} created successfully"}

    async def get_long_time_lost_users(self, days_count: int, pagination: PaginatedParams) -> UsersListOut:
        """Получение пользователей, которые долго не появлялись"""
        users = await self.db_engine.get_long_time_lost_users(days_count, pagination)
        user_out_list = [
            UserOut(
                id=str(user.id),
                phone_number=user.phone_number,
                created_at=user.created_at.date(),
                updated_at=user.updated_at.date() if user.updated_at else user.created_at.date()
            )
            for user in users
        ]
        return UsersListOut(items=user_out_list)

    async def get_user_questions(self, user_id: str) -> UserOut:
        """Получение всех вопросов пользователя"""
        user = await self.db_engine.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        questions = await self.db_engine.get_user_questions(user_id)

        return UserOut(
            id=str(user.id),
            phone_number=user.phone_number,
            created_at=user.created_at.date(),
            updated_at=user.updated_at.date() if user.updated_at else user.created_at.date()
        )

    async def get_all_questions(self, pagination: PaginatedParams) -> QuestionsListOut:
        """Получение всех вопросов"""
        questions = await self.db_engine.get_all_questions(pagination)
        question_out_list = [
            QuestionOut(
                id=question.id,
                user_id=str(question.user_id),
                text=question.text,
                admin_answer=question.admin_answer,
                created_at=question.created_at.date(),
                updated_at=question.updated_at.date()
            )
            for question in questions
        ]
        return QuestionsListOut(items=question_out_list)

    async def create_question(self, question_data: QuestionCreate) -> dict:
        """Создание вопроса"""
        question = await self.db_engine.create_question(question_data)
        return {"detail": "Question created successfully"}

    async def answer_question(self, question_id: UUID, answer: str) -> dict:
        """Ответ на вопрос"""
        question = await self.db_engine.answer_question(question_id, answer)
        return {"detail": "Question answered successfully"}

    async def create_user_action_record(self, user_id: str, history_data: HistoryCreate) -> dict:
        """Создание записи истории пользователя"""
        history = await self.db_engine.create_history_record(history_data)
        return {"detail": "User action recorded successfully"}

    async def get_user_history(self, user_id: str, pagination: PaginatedParams) -> HistoryOut:
        """Получение истории пользователя"""
        history_records = await self.db_engine.get_user_history(user_id, pagination)

        return HistoryOut(
            user_id=user_id,
            action_id=history_records[0].id if history_records else UUID(int=0),
            menu_id=history_records[0].menu_id if history_records else None,
            action_date=history_records[0].action_date.date() if history_records else None,
            created_at=history_records[0].action_date.date() if history_records else None
        )


def get_user_service(db_engine: DBEngine = Depends(get_db_engine)) -> UserService:
    """Зависимость для получения UserService"""
    return UserService(db_engine)