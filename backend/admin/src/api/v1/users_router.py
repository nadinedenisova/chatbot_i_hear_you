from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from schemas.entity import (
    Message,
    UserOut,
    UsersListOut,
    UserCreate,
    HistoryCreate,
    HistoryOut,
    QuestionOut,
    QuestionCreate,
    QuestionsListOut,
)
from utils.pagination import PaginatedParams


router = APIRouter()


@router.get(
    "/users", summary="Получить список пользователей", response_model=UsersListOut
)
async def get_users(
    pagination: PaginatedParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}


@router.post("/create", summary="Добавить пользователя", response_model=Message)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    return {"Hello": "World"}


@router.get(
    "/long-time-lost",
    summary="Получить список пользователей, которые долго не появлялись",
    response_model=UsersListOut,
)
async def get_long_time_lost_users(
    days_count: int = Query(
        default=10, ge=1, title="Количество дней, которое человек бездействовал"
    ),
    pagination: PaginatedParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}


@router.get(
    "/questions/{user_id}",
    summary="Получить все вопросы пользователя",
    response_model=UserOut,
)
async def get_user_questions(
    user_id: str, session: AsyncSession = Depends(get_async_session)
):
    return {"Hello": "World"}


@router.get(
    "/questions", summary="Получить все вопросы", response_model=QuestionsListOut
)
async def get_all_questions(
    pagination: PaginatedParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}


@router.post(
    "/questions/create", summary="Добавить новый вопрос", response_model=Message
)
async def create_question(
    question_data: QuestionCreate, session: AsyncSession = Depends(get_async_session)
):
    return {"Hello": "World"}


@router.put(
    "/questions/{question_id}/answer",
    summary="Ответить на вопрос",
    response_model=Message,
)
async def answer_question(
    question_id: UUID,
    question_data: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}


@router.post(
    "/{user_id}/history/add",
    summary="Добавить действие пользователя",
    response_model=Message,
)
async def create_user_action_record(
    user_id: str,
    history_data: HistoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}


@router.get(
    "/{user_id}/history",
    summary="Получить историю пользователя",
    response_model=HistoryOut,
)
async def get_user_history(
    user_id: str,
    pagination: PaginatedParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}
