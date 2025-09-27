from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from schemas.entity import (
    ContentCreate,
    MenuNodeOut,
    MenuNodeCreate,
    MenuNodeUpdate,
    Message,
    RatingCreate,
    RatingOut,
    AllMenuNodeOut,
)


router = APIRouter()


@router.get(
    "/",
    summary="Получить всё дерево меню навигации",
    response_model=AllMenuNodeOut,
    description="""Получить полное дерево меню. 
    Здесь указан список _content_ как список строк, но это не так, это список ```MenuNodeOut``` структур""",
)
async def get_full_menu(session: AsyncSession = Depends(get_async_session)):
    return {"Hello": "World"}


@router.get(
    "/search-by-name",
    summary="Получить узел меню навигации по названию",
    response_model=MenuNodeOut,
)
async def get_menu_node_by_name(
    name: str = Query(default=None, title="Название узла", max_length=100),
    session: AsyncSession = Depends(get_async_session),
):
    return {"Hello": "World"}


@router.get(
    "/root", summary="Получить корень узла меню навигации",
    response_model=MenuNodeOut
)
async def get_menu_root(session: AsyncSession = Depends(get_async_session)):
    return MenuNodeOut(
        id=uuid4(),
        parent_id=None,
        name='Начальный экран',
        text='Здравствуйте',
        subscription_type=None,
        content=[],
        children_names=[
            'Я волнуюсь о слухе ребенка',
            'Я волнуюсь о своем слухе'
        ]
    )


@router.post("/add", summary="Добавить узел меню навигации", response_model=Message)
async def add_menu_node(
    node_data: MenuNodeCreate, session: AsyncSession = Depends(get_async_session)
):
    return Message(detail="The menu node was added")


@router.get(
    "/{menu_id}", summary="Получить узел меню по id", response_model=MenuNodeOut
)
async def get_menu_node(
    menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    return {"Hello": "World"}


@router.put("/{menu_id}", summary="Обновить узел меню по id", response_model=Message)
async def update_menu_node(
    menu_id: UUID,
    node_data: MenuNodeCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return Message(detail="The menu node was updated")


@router.delete("/{menu_id}", summary="Удалить узел меню по id", response_model=Message)
async def delete_menu_node(
    menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    return Message(detail="The menu node was deleted.")


@router.post(
    "/{menu_id}/content/add",
    summary="Добавить контент к узлу меню",
    response_model=Message,
)
async def add_menu_content(
    menu_id: UUID,
    content_data: ContentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return Message(detail="The content was added")


@router.put(
    "/{menu_id}/content/change/{content_id}",
    summary="Обновить контент",
    response_model=Message,
)
async def update_menu_content(
    menu_id: UUID,
    content_id: UUID,
    content_data: ContentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return Message(detail="The content was changed")


@router.delete(
    "/{menu_id}/content/delete/{content_id}",
    summary="Удалить контент поста",
    response_model=Message,
)
async def delete_menu_content(
    menu_id: UUID, content_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    return Message(detail="The node content was deleted")


@router.get(
    "/{menu_id}/rate", summary="Получить рейтинг узла меню", response_model=RatingOut
)
async def get_menu_node_rate(
    menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    return {"Hello": "World"}


@router.post("/{menu_id}/rate", summary="Оценить узел меню", response_model=Message)
async def rate_menu_node(
    menu_id: UUID,
    rating_data: RatingCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return Message(detail="The node was successfully rated!")
