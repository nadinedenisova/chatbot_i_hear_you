from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_async_session
from src.schemas.entity import (
    Message,
    UserOut,
    UsersListOut,
    UserCreate,
    HistoryCreate,
    HistoryOut,
    QuestionOut,
    QuestionCreate,
    QuestionsListOut,
    QuestionAnswer, HistoryListOut
)
from src.services.user_service import UserService, get_user_service
from src.utils.pagination import PaginatedParams

router = APIRouter()


@router.get(
    "/users", summary="Получить список пользователей", response_model=UsersListOut
)
async def get_users(
    pagination: PaginatedParams = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users(pagination)


@router.post("/create", summary="Добавить пользователя", response_model=Message)
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user_data)


@router.get(
    "/long-time-lost",
    summary="Пользователи, которые давно не заходили",
    response_model=UsersListOut,
)
async def get_long_time_lost_users(
    days_count: int = Query(10, ge=1),
    pagination: PaginatedParams = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_long_time_lost_users(days_count, pagination)


@router.get(
    "/questions/{user_id}", summary="Вопросы пользователя", response_model=QuestionsListOut
)
async def get_user_questions(
    user_id: str, user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_questions(user_id)


@router.get("/questions", summary="Все вопросы", response_model=QuestionsListOut)
async def get_all_questions(
    pagination: PaginatedParams = Depends(),
    start_date: datetime|None = Query(None, description="Начальные дата и время фильтрации (ГГГГ-ММ-ДД ЧЧ:мм:сс)"),
    end_date: datetime|None = Query(None, description="Конечные дата и время фильтрации (ГГГГ-ММ-ДД ЧЧ:мм:сс)"),
    sort_by: str = Query("created_at", description="Поле для сортировки (created_at, updated_at)"),
    sort_order: str = Query("desc", description="Порядок сортировки (asc, desc)"),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_all_questions(
        pagination,
        start_date,
        end_date,
        sort_by,
        sort_order
    )


@router.post("/questions/create", summary="Добавить вопрос", response_model=Message)
async def create_question(
    question_data: QuestionCreate, user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_question(question_data)


@router.put(
    "/questions/{question_id}/answer",
    summary="Ответить на вопрос",
    response_model=Message,
)
async def answer_question(
    question_id: UUID,
    question_data: QuestionAnswer,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.answer_question(question_id, question_data.admin_answer)

@router.delete(
    "/questions/{question_id}",
    summary="Удалить вопрос",
    response_model=Message
)
async def delete_question(
        question_id: UUID,
        user_service: UserService = Depends(get_user_service),
):
    return await user_service.delete_question(question_id)


@router.post(
    "/{user_id}/history/add",
    summary="Добавить действие пользователя",
    response_model=Message,
)
async def create_user_action_record(
    user_id: str,
    history_data: HistoryCreate,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user_action_record(user_id, history_data)


@router.get(
    "/{user_id}/history",
    summary="Получить историю пользователя",
    response_model=HistoryListOut,
)
async def get_user_history(
    user_id: str,
    pagination: PaginatedParams = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user_history(user_id, pagination)
